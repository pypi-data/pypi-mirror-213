from transformers import AutoModelForQuestionAnswering
from torch.nn.utils import prune
import torch
from factory import MagnitudeModelFactory, PostPrunedModelFactory, BlockPrunedModelFactory

class BertPruner:
    def __init__(self, model_name: str, saved_dir: str, method: str, value: float):
        self.model_name = model_name
        self.saved_dir = saved_dir
        self.method = method
        self.value = value
        self.model = self.get_model()

    def get_model(self):
        if self.method == "magnitude":
            factory = MagnitudeModelFactory(self.model_name, self.value)
        elif self.method == "post":
            factory = PostPrunedModelFactory(self.model_name, self.value)
        elif self.method == "block":
            factory = BlockPrunedModelFactory(self.model_name, self.value)
        else:
            raise ValueError(f"Unknown pruning method: {self.method}")

        return factory.create_model()

    def prune_and_save(self):
        # it fixed using previous code (2 potential changes: eval model/input_id)
        input_shape = (1, 512)
        input_ids = torch.zeros(input_shape, dtype=torch.long, device=self.model.device)
        attention_mask = torch.ones(input_shape, dtype=torch.long, device=self.model.device)
        token_type_ids = torch.zeros(input_shape, dtype=torch.long, device=self.model.device)

        torch.onnx.export(self.model, (input_ids, attention_mask, token_type_ids),
                          self.saved_dir,
                          opset_version=11,
                          input_names=['input_ids', 'input_mask', 'segment_ids'],
                          output_names=['output'],
                          dynamic_axes={'input_ids': {0: 'batch_size', 1: 'sequence_length'},
                                        'input_mask': {0: 'batch_size', 1: 'sequence_length'},
                                        'segment_ids': {0: 'batch_size', 1: 'sequence_length'},
                                        'output': {0: 'batch_size', 1: 'sequence_length'}})