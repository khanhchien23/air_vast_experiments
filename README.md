# Air-only Vast.ai experiments

This folder is the Air counterpart of `grd_vast_experiments`.
It uses the same Qwen3.5-9B, ordinary LoRA, dynamic image processing,
masking, checkpoint/resume behavior, and scheduled CoT loss as the Ground pipeline.
Only the dataset, Air taxonomy, and Air prompts/labels differ.

Dataset:
`KhanhChien/Data-Qwen3.5-SFT-Air-Only`

## Scheduled CoT training

```bash
torchrun --standalone --nproc_per_node=1 train_air_vast.py `
  --parquet_dir KhanhChien/Data-Qwen3.5-SFT-Air-Only `
  --output_dir ./outputs/air_scheduled_cot `
  --mode scheduled_cot --model_id Qwen/Qwen3.5-9B `
  --epochs 3 --stop_after_epoch 1 `
  --batch_size 2 --grad_accum 8 --lr 2e-4 `
  --lora_r 16 --lora_alpha 32 --max_seq_length 2048 `
  --cot_weight_start 1.0 --cot_weight_end 0.5 --answer_weight 1.0 `
  --save_steps 100 --logging_steps 10 --eval_steps 100
```

For subsequent epochs, keep every setting unchanged and change only
`--stop_after_epoch 2` or `--stop_after_epoch 3`.

## Other modes

Use `--mode direct` or `--mode answer_only` with the same train script.
Keep each mode in a separate output directory.

## Inference

```bash
python inference_air_vast.py `
  --data ./data/selected_air_only_real.parquet `
  --prompt-parquet ./.hf_dataset_files/data/train-air-only.parquet `
  --adapter ./outputs/air_scheduled_cot/final_adapter `
  --mode scheduled_cot --batch-size 1 --max-new-tokens 512 `
  --output ./results/air_scheduled_cot.csv
```

The inference engine accepts a packed Parquet or class-folder image directory.
Start with `--limit 10` before running the full set.
