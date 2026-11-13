#!/usr/bin/env python
"""Air-only inference using the shared batched Qwen inference engine.

Prompts are read from the SFT train Parquet, not reconstructed from labels.
"""

import sys
from pathlib import Path

import pyarrow.parquet as pq
import inference_selected_air as engine


def main():
    # Consume our additional argument, forwarding all shared CLI options.
    import argparse
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--prompt-parquet", type=Path)
    parser.add_argument("--mode", choices=["direct", "answer_only", "scheduled_cot"], default="answer_only")
    args, remaining = parser.parse_known_args()
    if args.mode != "direct":
        if args.prompt_parquet is None:
            parser.error("--prompt-parquet is required for CoT modes")
        prompts = pq.read_table(args.prompt_parquet, columns=["system_prompt", "user_prompt"])
        if not len(prompts):
            raise ValueError("Prompt Parquet is empty")
        engine.SYSTEM_PROMPT = prompts["system_prompt"][0].as_py()
        engine.USER_PROMPT = prompts["user_prompt"][0].as_py()

    original_loader = engine.items_from_data

    def air_items(data):
        # HF snapshot symlinks resolve to extensionless blob files. This
        # entrypoint supports Parquet files or image directories, so inspect
        # the filesystem type rather than relying on the filename suffix.
        rows = original_loader(data)
        selected = [row for row in rows if row["ground_truth"].startswith("Air.")]
        if not selected:
            raise ValueError("No Air-only images found")
        return selected

    engine.items_from_data = air_items
    # Scheduled CoT and answer_only use the same CoT inference path. The
    # shared engine needs only the boolean thinking behavior; the wrapper keeps
    # the public mode name for experiment bookkeeping.
    engine_mode = "direct" if args.mode == "direct" else "answer_only"
    sys.argv = [sys.argv[0]] + remaining + ["--mode", engine_mode]
    engine.main()


if __name__ == "__main__":
    main()
