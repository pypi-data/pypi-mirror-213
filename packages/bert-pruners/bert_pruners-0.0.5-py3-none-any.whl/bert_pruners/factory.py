import glob
import os
import subprocess
from abc import ABC, abstractmethod
import torch

import datasets
from datasets import load_dataset

import numpy as np

import transformers
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, TrainingArguments
from transformers.models.bert import BertForQuestionAnswering
from transformers import Trainer, DataCollatorWithPadding, BertTokenizerFast

from nn_pruning.patch_coordinator import ModelPatchingCoordinator, SparseTrainingArguments
from nn_pruning.sparse_trainer import SparseTrainer
from nn_pruning.inference_model_patcher import optimize_model

from pruners.emmental.modules import MagnitudeBinarizer, ThresholdBinarizer, TopKBinarizer
from pruners.magnitude_pruner import magnitude_prune

from pytorch_block_sparse import BlockSparseModelPatcher
from transformers import BertModel

class CustomBertModel(BertModel):
    def set_head_mask(self, mask):
        print("Mask shape:", mask.shape)
        print("Mask contents:", mask)
        for param in self.parameters():
            param.data *= mask.to(param.device)

    def set_neuron_mask(self, mask):
        print("Mask shape:", mask.shape)
        print("Mask contents:", mask)
        # mask = torch.ones(1024, 1)  # replace this with your actual mask
        # mask = mask.expand_as(self.encoder.layer[0].attention.self.key.weight)
        # mask = mask.expand_as(self.encoder.layer[0].attention.self.key.weight)
        for layer in self.encoder.layer:
            layer.attention.self.key.weight.data *= mask.to(layer.attention.self.key.weight.device)
            layer.attention.self.query.weight.data *= mask.to(layer.attention.self.query.weight.device)
            layer.attention.self.value.weight.data *= mask.to(layer.attention.self.value.weight.device)


datasets.logging.set_verbosity_error()
transformers.logging.set_verbosity_error()

class PruningTrainer(SparseTrainer, Trainer):
    def __init__(self, sparse_args, *args, **kwargs):
        Trainer.__init__(self, *args, **kwargs)
        SparseTrainer.__init__(self, sparse_args)
        
    def compute_loss(self, model, inputs, return_outputs=False):
        """
        We override the default loss in SparseTrainer because it throws an 
        error when run without distillation
        """
        start_positions = inputs.pop("start_positions")
        end_positions = inputs.pop("end_positions")
        outputs = model(**inputs)
        start_logits, end_logits = outputs.start_logits, outputs.end_logits
        
        loss_fct = torch.nn.CrossEntropyLoss()
        start_loss = loss_fct(start_logits, start_positions)
        end_loss = loss_fct(end_logits, end_positions)
        loss = (start_loss + end_loss) / 2

        return (loss, outputs) if return_outputs else loss
        
class CustomDataCollator(DataCollatorWithPadding):
    def __call__(self, features):
        for feature in features:
            feature.pop("original_answers", None)

        batch = super().__call__(features)
        if "start_positions" in features[0].keys() and "end_positions" in features[0].keys():
            batch["start_positions"] = torch.tensor([f["start_positions"] for f in features], dtype=torch.long)
            batch["end_positions"] = torch.tensor([f["end_positions"] for f in features], dtype=torch.long)
        return batch

def compute_metrics(pred):
    logits, labels = pred
    squad_metric = load_metric("squad")
    predictions = [{"id": idx, "prediction_text": tokenizer.decode(logits[idx].argmax(-1))} for idx in range(len(logits))]
    labels = [{"id": idx, "answers": {"text": [tokenizer.decode(labels[idx])], "answer_start": [0]}} for idx in range(len(labels))]
    return squad_metric.compute(predictions=predictions, references=labels)


def prepare_squad_features(examples):
    # Tokenize the questions and contexts
    # tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer = BertTokenizerFast.from_pretrained('madlag/bert-large-uncased-whole-word-masking-finetuned-squadv2')

    tokenized_examples = tokenizer(
        examples["question"],
        examples["context"],
        truncation="only_second",
        max_length=384,
        stride=128,
        return_overflowing_tokens=True,
        return_offsets_mapping=True,
        padding="max_length",
    )

    sample_mapping = tokenized_examples.pop("overflow_to_sample_mapping")
    offset_mapping = tokenized_examples.pop("offset_mapping")

    tokenized_examples["start_positions"] = []
    tokenized_examples["end_positions"] = []
    # tokenized_examples["original_answers"] = []

    for i, offsets in enumerate(offset_mapping):
        input_ids = tokenized_examples["input_ids"][i]
        cls_index = input_ids.index(tokenizer.cls_token_id)

        sequence_ids = tokenized_examples.sequence_ids(i)

        sample_index = sample_mapping[i]
        answers = examples["answers"][sample_index]

        if len(answers["answer_start"]) == 0:
            tokenized_examples["start_positions"].append(cls_index)
            tokenized_examples["end_positions"].append(cls_index)
            # tokenized_examples["original_answers"].append({"answer_start": [], "text": []})
        else:
            start_char = answers["answer_start"][0]
            end_char = start_char + len(answers["text"][0])
            # tokenized_examples["original_answers"].append(answers)

            token_start_index = 0
            while sequence_ids[token_start_index] != 1:
                token_start_index += 1

            token_end_index = len(input_ids) - 1
            while sequence_ids[token_end_index] != 1:
                token_end_index -= 1

            if not (offsets[token_start_index][0] <= start_char and offsets[token_end_index][1] >= end_char):
                tokenized_examples["start_positions"].append(cls_index)
                tokenized_examples["end_positions"].append(cls_index)
            else:
                while token_start_index < len(offsets) and offsets[token_start_index][0] <= start_char:
                    token_start_index += 1
                tokenized_examples["start_positions"].append(token_start_index - 1)

                while offsets[token_end_index][1] >= end_char:
                    token_end_index -= 1
                tokenized_examples["end_positions"].append(token_end_index + 1)

    return tokenized_examples

def find_snapshot_folder(model_name):
    if "/" not in model_name:
        base_folder_pattern = f"/home/junfan/.cache/huggingface/hub/*{model_name}"
        base_folders = glob.glob(base_folder_pattern)
    else:
        repo, model_name = model_name.split("/")
        base_folder_pattern = f"/home/junfan/.cache/huggingface/hub/*{repo}*{model_name}"
        base_folders = glob.glob(base_folder_pattern)

    if len(base_folders) == 0:
        raise FileNotFoundError(f"Base folder not found for model: {model_name}")
    
    base_folder = base_folders[0]
    snapshot_folder = os.path.join(base_folder, "snapshots")
    snapshot_subfolders = glob.glob(os.path.join(snapshot_folder, "*"))

    if len(snapshot_subfolders) > 0:
        return snapshot_subfolders[0]
    else:
        raise FileNotFoundError(f"Snapshot folder not found for model: {model_name}")

class Pruner(ABC):
    @abstractmethod
    def apply(self, model):
        pass

class ModelFactory:
    def __init__(self, model_name):
        self.model_name = model_name

    def create_model(self):
        raise NotImplementedError("Subclasses must implement this method")

class MagnitudePruner(Pruner):
    def __init__(self, model, sparsity_dict):
        self.masks = MagnitudePruner.prune(model, sparsity_dict)

    @torch.no_grad()
    def apply(self, model):
        for name, param in model.named_parameters():
            if name in self.masks:
                param.data.mul_(self.masks[name])  # Apply the mask directly to the weights

    @staticmethod
    @torch.no_grad()
    def prune(model, sparsity_dict):
        masks = dict()
        print(f"sparsity_dict:{sparsity_dict}")
        for name, param in model.named_parameters():
            if param.dim() > 1 and "intermediate" in name and sparsity_dict:
                if sparsity_dict > 0:
                    masks[name] = magnitude_prune(param, sparsity_dict)
        return masks


class MagnitudeModelFactory(ModelFactory):
    def __init__(self, model_name, sparsity=None):
        super().__init__(model_name)
        self.sparsity = sparsity
        self.method="Magnitude Pruning"

    def create_model(self):
        model = AutoModelForQuestionAnswering.from_pretrained(self.model_name)
        pruner = MagnitudePruner(model, self.sparsity)
        pruner.apply(model)
        return model


class PostPruner(Pruner):
    def __init__(self, full_model_name, constraint=None):
        self.full_model_name = full_model_name
        self.constraint = constraint
        self.output_dir = "pruning_output"
        self.head_mask_output = "head_mask.pt"
        self.neuron_mask_output = "neuron_mask.pt"

    def apply(self):
        if self.constraint is not None:
            # Implement the apply() method for the PostPruner class
            snapshot_folder = find_snapshot_folder(self.full_model_name)
            command = [
                "postpruner",
                "--model_name", self.full_model_name,
                "--task_name", "squad",
                "--ckpt_dir", snapshot_folder,
                "--output_dir", self.output_dir,
                "--constraint", str(self.constraint)
            ]
            # Execute the pruning command and return the mask files
            subprocess.run(command, check=True)
            head_mask_path = os.path.join(self.output_dir, self.head_mask_output)
            neuron_mask_path = os.path.join(self.output_dir, self.neuron_mask_output)
            head_mask = torch.load(head_mask_path)
            neuron_mask = torch.load(neuron_mask_path)
            
            # Remove the head_mask and neuron_mask files after loading them
            # os.remove(head_mask_path)
            # os.remove(neuron_mask_path)
        else:
            head_mask, neuron_mask = None, None

        return head_mask, neuron_mask

class PostPrunedModelFactory(ModelFactory):
    def __init__(self, model_name, constraint=None):
        super().__init__(model_name)
        self.constraint = constraint
        self.method="Post Training Pruning"

    def create_model(self):

        # model = CustomBertModel.from_pretrained(self.model_name)
        model = AutoModelForQuestionAnswering.from_pretrained(self.model_name)
        if self.constraint is not None:
            pruner = PostPruner(self.model_name, 1 - self.constraint)
            head_mask, neuron_mask = pruner.apply()
        else:
            head_mask, neuron_mask = None, None
        
        if head_mask is not None:
            model.set_head_mask(head_mask)
        if neuron_mask is not None:
            model.set_neuron_mask(neuron_mask)
        head_mask = neuron_mask = None

        return model, head_mask, neuron_mask

class BlockPruner(Pruner):
    def __init__(self, model, density):
        self.model = model
        self.layer_patterns = [
            "(bert|roberta)\\.encoder\\.layer\\.[0-1]+\\.intermediate\\.dense",
            #"(bert|roberta)\\.encoder\\.layer\\.[0-9]+\\.output\\.dense",
            #"(bert|roberta)\\.encoder\\.layer\\.[0-9]+\\.attention\\.output\\.dense"
        ]
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.density = density

    def apply(self):
        # Create a model patcher
        model_patcher = BlockSparseModelPatcher()

        # Add patterns for the layers to be sparsified
        for layer_pattern in self.layer_patterns:
            model_patcher.add_pattern(layer_pattern, {"density": self.density})

        # Apply the block pruning to the model

        model_patcher.patch_model(self.model.to(self.device))


class BlockPrunedModelFactory(ModelFactory):
    def __init__(self, model_name, density=1):
        super().__init__(model_name)

        self.density = density
        self.method = "Block Pruning"

    def create_model(self):
        model = AutoModelForQuestionAnswering.from_pretrained(self.model_name)
        pruner = BlockPruner(model, self.density)
        pruner.apply()

        return model


import re
class MovementPruner(Pruner):
    def __init__(self, model, threshold=0):
        self.pruning_method = "topK"
        self.threshold = 1 - threshold
        self.masks = MovementPruner.prune(model, self.pruning_method, threshold)

    @torch.no_grad()
    def apply(self, model):
        for name, param in model.named_parameters():
            if name in self.masks:
                param *= self.masks[name]
    @staticmethod
    @torch.no_grad()
    def prune(model, pruning_method, threshold):
        masks = dict()
        model_params = model.state_dict()
        model_params = dict(model.named_parameters())
        print("Model Parameters:")
        print(model_params.keys())


        for name, tensor in model.named_parameters():
            if ("embeddings" not in name and "LayerNorm" not in name and
                "pooler" not in name and "classifier" not in name and
                "qa_output" not in name and "bias" not in name):

                prefix_ = re.sub(r'\.[^.]*$', '', name)
                print(prefix_)

                if pruning_method == "magnitude":
                    mask = MagnitudeBinarizer.apply(inputs=tensor, threshold=threshold)
                elif pruning_method == "topK":
                    if "mask_scores" in name:
                        continue
                    scores = model_params[f"{prefix_}.mask_scores"]
                    mask = TopKBinarizer.apply(scores, threshold)
                elif pruning_method == "sigmoied_threshold":
                    if "mask_scores" in name:
                        continue
                    scores = model_params[f"{prefix_}.mask_scores"]
                    mask = ThresholdBinarizer.apply(scores, threshold, True)
                elif pruning_method == "l0":
                    if "mask_scores" in name:
                        continue
                    scores = model_params[f"{prefix_}.mask_scores"]
                    l, r = -0.1, 1.1
                    s = torch.sigmoid(scores)
                    s_bar = s * (r - l) + l
                    mask = s_bar.clamp(min=0.0, max=1.0)
                else:
                    raise ValueError("Unknown pruning method")

                masks[name] = mask

        return masks


class MovementModelFactory(ModelFactory):
    def __init__(self, model_name, sparsity=0):
        super().__init__(model_name)
        self.sparsity = sparsity
        self.method = "Movement Pruning"

    def create_model(self):
        model = AutoModelForQuestionAnswering.from_pretrained(self.model_name)
        pruner = MovementPruner(model, self.sparsity)
        pruner.apply(model)
        return model