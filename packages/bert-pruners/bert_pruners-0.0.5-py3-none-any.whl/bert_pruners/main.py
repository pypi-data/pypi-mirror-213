import argparse
from .bert_pruner import BertPruner

def main():
    parser = argparse.ArgumentParser(description='BERT pruner')
    parser.add_argument('--model_name', default='xihajun/krai-mlperf-inference-v3.0-bert-pytorch-fp32-squad-v1.1', type=str, help='Path to save the pruned model')
    parser.add_argument('--saved_dir', type=str, help='Path to save the pruned model')
    parser.add_argument('--sparsity', type=float, default=0.5, help='Desired sparsity of the pruned model')
    parser.add_argument('--method', type=str, default='magnitude', help='Select different pruning methods')
    args = parser.parse_args()
    pruner = BertPruner(model_name=args.model_name, saved_dir=args.saved_dir, sparsity=args.sparsity, method=args.method)
    pruner.prune_and_save()

if __name__ == "__main__":
    main()
