from transformers import AutoModelForQuestionAnswering
import torch

def magnitude_prune(tensor: torch.Tensor, sparsity: float) -> torch.Tensor:
    sparsity = min(max(0.0, sparsity), 1.0)
    if sparsity == 1.0:
        tensor.zero_()
        return torch.zeros_like(tensor)
    elif sparsity == 0.0:
        return torch.ones_like(tensor)

    num_elements = tensor.numel()

    num_zeros = round(num_elements * sparsity)
    importance = tensor.abs()
    threshold = importance.view(-1).kthvalue(num_zeros).values
    mask = torch.gt(importance, threshold)
    tensor.mul_(mask)

    return mask


class BertPruner:
    def __init__(self, model_name: str, saved_dir: str, sparsity: float):
        self.model = AutoModelForQuestionAnswering.from_pretrained(model_name)
        self.saved_dir = saved_dir
        self.sparsity = sparsity
        self.masks = self.prune_model()

    @torch.no_grad()
    def prune_model(self):
        masks = dict()
        for name, module in self.model.named_modules():
            if isinstance(module, torch.nn.Linear):
                masks[name] = magnitude_prune(module.weight, self.sparsity)
        return masks

    def apply_pruning(self):
        for name, module in self.model.named_modules():
            if isinstance(module, torch.nn.Linear):
                module.weight.data.mul_(self.masks[name])

    def prune_and_save(self):
        self.apply_pruning()

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
