# Runs training pipeline, including data loading, tokenization, optimizing

# Load data

# Tokenize data

# Optimize model

import os
import math
import logging
from typing import Optional, Dict, Any

import torch
import torch.distributed as dist
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
from torch.nn.parallel import DistributedDataParallel
from transformers import (
    PreTrainedTokenizerBase,
    DataCollatorForLanguageModeling,
    get_scheduler,
    set_seed,
)
import wandb
from datasets import load_dataset
from accelerate import Accelerator
from tqdm.auto import tqdm

from model import IndieGOConfig, IndieGOForCausalLM

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

class CodeDataset(Dataset):
    """Custom dataset for code training data"""
    
    def __init__(
        self,
        tokenizer: PreTrainedTokenizerBase,
        file_path: str,
        block_size: int,
    ):
        self.tokenizer = tokenizer
        self.block_size = block_size
        
        logger.info(f"Loading dataset from {file_path}")
        self.examples = []
        
        # Load and tokenize data
        dataset = load_dataset("text", data_files=file_path)
        
        for example in dataset["train"]:
            tokenized = tokenizer(
                example["text"],
                truncation=True,
                max_length=block_size,
                padding="max_length",
                return_tensors="pt",
            )
            self.examples.append({
                "input_ids": tokenized["input_ids"].squeeze(),
                "attention_mask": tokenized["attention_mask"].squeeze(),
            })

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, i):
        return self.examples[i]

def train(
    # Model/Tokenizer parameters
    model_name_or_path: Optional[str] = None,
    tokenizer_name_or_path: Optional[str] = None,
    config_name_or_path: Optional[str] = None,
    
    # Data parameters
    train_file: str = "data/train.txt",
    validation_file: Optional[str] = None,
    max_seq_length: int = 1024,
    preprocessing_num_workers: Optional[int] = None,
    
    # Training parameters
    per_device_train_batch_size: int = 8,
    per_device_eval_batch_size: int = 8,
    learning_rate: float = 5e-5,
    weight_decay: float = 0.0,
    num_train_epochs: float = 3.0,
    max_train_steps: Optional[int] = None,
    gradient_accumulation_steps: int = 1,
    lr_scheduler_type: str = "linear",
    warmup_ratio: float = 0.0,
    
    # Other parameters
    seed: int = 42,
    output_dir: str = "checkpoints",
    logging_steps: int = 500,
    eval_steps: Optional[int] = None,
    save_steps: Optional[int] = None,
    save_total_limit: Optional[int] = None,
):
    accelerator = Accelerator()
    
    # Set random seed
    set_seed(seed)
    
    # Initialize config, tokenizer, model
    if model_name_or_path:
        config = IndieGOConfig.from_pretrained(config_name_or_path or model_name_or_path)
        model = IndieGOForCausalLM.from_pretrained(model_name_or_path, config=config)
        tokenizer = PreTrainedTokenizerBase.from_pretrained(
            tokenizer_name_or_path or model_name_or_path
        )
    else:
        config = IndieGOConfig()
        model = IndieGOForCausalLM(config)
        tokenizer = PreTrainedTokenizerBase.from_pretrained("gpt2")
    
    # Load datasets
    train_dataset = CodeDataset(
        tokenizer=tokenizer,
        file_path=train_file,
        block_size=max_seq_length,
    )
    
    if validation_file:
        eval_dataset = CodeDataset(
            tokenizer=tokenizer,
            file_path=validation_file,
            block_size=max_seq_length,
        )
    
    # Create dataloaders
    train_dataloader = DataLoader(
        train_dataset,
        batch_size=per_device_train_batch_size,
        shuffle=True,
        num_workers=preprocessing_num_workers or 0,
    )
    
    if validation_file:
        eval_dataloader = DataLoader(
            eval_dataset,
            batch_size=per_device_eval_batch_size,
            shuffle=False,
            num_workers=preprocessing_num_workers or 0,
        )
    
    # Initialize optimizer
    no_decay = ["bias", "LayerNorm.weight"]
    optimizer_grouped_parameters = [
        {
            "params": [p for n, p in model.named_parameters() 
                      if not any(nd in n for nd in no_decay)],
            "weight_decay": weight_decay,
        },
        {
            "params": [p for n, p in model.named_parameters() 
                      if any(nd in n for nd in no_decay)],
            "weight_decay": 0.0,
        },
    ]
    optimizer = torch.optim.AdamW(optimizer_grouped_parameters, lr=learning_rate)
    
    # Prepare everything with accelerator
    model, optimizer, train_dataloader = accelerator.prepare(
        model, optimizer, train_dataloader
    )
    if validation_file:
        eval_dataloader = accelerator.prepare(eval_dataloader)
    
    # Calculate number of update steps
    num_update_steps_per_epoch = math.ceil(
        len(train_dataloader) / gradient_accumulation_steps
    )
    if max_train_steps is None:
        max_train_steps = int(num_train_epochs * num_update_steps_per_epoch)
    
    # Create learning rate scheduler
    lr_scheduler = get_scheduler(
        name=lr_scheduler_type,
        optimizer=optimizer,
        num_warmup_steps=int(warmup_ratio * max_train_steps),
        num_training_steps=max_train_steps,
    )
    
    # Initialize wandb
    if accelerator.is_main_process:
        wandb.init(
            project="indiego",
            config={
                "learning_rate": learning_rate,
                "epochs": num_train_epochs,
                "batch_size": per_device_train_batch_size,
                "max_seq_length": max_seq_length,
            }
        )
    
    # Training loop
    total_batch_size = (
        per_device_train_batch_size
        * accelerator.num_processes
        * gradient_accumulation_steps
    )
    logger.info("***** Running training *****")
    logger.info(f"  Num examples = {len(train_dataset)}")
    logger.info(f"  Num epochs = {num_train_epochs}")
    logger.info(f"  Batch size per device = {per_device_train_batch_size}")
    logger.info(f"  Total train batch size = {total_batch_size}")
    logger.info(f"  Gradient accumulation steps = {gradient_accumulation_steps}")
    logger.info(f"  Total optimization steps = {max_train_steps}")
    
    progress_bar = tqdm(
        range(max_train_steps),
        disable=not accelerator.is_local_main_process,
    )
    completed_steps = 0
    best_eval_loss = float("inf")
    
    for epoch in range(int(num_train_epochs)):
        model.train()
        for step, batch in enumerate(train_dataloader):
            with accelerator.accumulate(model):
                outputs = model(**batch)
                loss = outputs[0]
                accelerator.backward(loss)
                
                if step % gradient_accumulation_steps == 0:
                    optimizer.step()
                    lr_scheduler.step()
                    optimizer.zero_grad()
                    progress_bar.update(1)
                    completed_steps += 1
                    
                    if accelerator.is_main_process:
                        wandb.log(
                            {
                                "train_loss": loss.item(),
                                "learning_rate": optimizer.param_groups[0]["lr"],
                            },
                            step=completed_steps,
                        )
            
            if completed_steps >= max_train_steps:
                break
            
            # Evaluation
            if (
                validation_file
                and eval_steps
                and completed_steps % eval_steps == 0
            ):
                model.eval()
                eval_losses = []
                
                for eval_batch in eval_dataloader:
                    with torch.no_grad():
                        outputs = model(**eval_batch)
                        loss = outputs[0]
                        eval_losses.append(
                            accelerator.gather(loss.repeat(per_device_eval_batch_size))
                        )
                
                eval_losses = torch.cat(eval_losses)
                eval_loss = torch.mean(eval_losses)
                
                if accelerator.is_main_process:
                    wandb.log(
                        {"eval_loss": eval_loss.item()},
                        step=completed_steps,
                    )
                    
                    # Save best model
                    if eval_loss < best_eval_loss:
                        best_eval_loss = eval_loss
                        accelerator.wait_for_everyone()
                        unwrapped_model = accelerator.unwrap_model(model)
                        unwrapped_model.save_pretrained(
                            os.path.join(output_dir, "best"),
                            save_function=accelerator.save,
                        )
                
                model.train()
            
            # Save checkpoint
            if (
                save_steps
                and completed_steps % save_steps == 0
            ):
                accelerator.wait_for_everyone()
                if accelerator.is_main_process:
                    unwrapped_model = accelerator.unwrap_model(model)
                    unwrapped_model.save_pretrained(
                        os.path.join(output_dir, f"checkpoint-{completed_steps}"),
                        save_function=accelerator.save,
                    )
                    
                    if save_total_limit:
                        checkpoints = [
                            d for d in os.listdir(output_dir)
                            if d.startswith("checkpoint-")
                        ]
                        checkpoints = sorted(
                            checkpoints,
                            key=lambda x: int(x.split("-")[1])
                        )
                        
                        # Remove old checkpoints
                        if len(checkpoints) > save_total_limit:
                            num_to_remove = len(checkpoints) - save_total_limit
                            to_remove = checkpoints[:num_to_remove]
                            for checkpoint in to_remove:
                                checkpoint_path = os.path.join(
                                    output_dir, checkpoint
                                )
                                logger.info(
                                    f"Deleting checkpoint {checkpoint_path}"
                                )
                                os.system(f"rm -rf {checkpoint_path}")
    
    # Save final model
    if accelerator.is_main_process:
        unwrapped_model = accelerator.unwrap_model(model)
        unwrapped_model.save_pretrained(
            os.path.join(output_dir, "final"),
            save_function=accelerator.save,
        )

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name_or_path", type=str)
    parser.add_argument("--tokenizer_name_or_path", type=str)
    parser.add_argument("--config_name_or_path", type=str)
    parser.add_argument("--train_file", type=str, required=True)
    parser.add_argument("--validation_file", type=str)
    parser.add_argument("--max_seq_length", type=int, default=1024)
    parser.add_argument("--preprocessing_num_workers", type=int)
    parser.add_argument("--per_device_train_batch_size", type=int, default=8)
    parser.add_argument("--per_device_eval_batch_size", type=int, default=8)
    parser.add_argument("--learning_rate", type=float, default=5e-5)
    parser.add_argument("--weight_decay", type=float, default=0.0)
    parser.add_argument("--num_train_epochs", type=float, default=3.0)
    parser.add_argument("--max_train_steps", type=int)
    parser.add_argument("--gradient_accumulation_steps", type=int, default=1)
    parser.add_argument("--lr_scheduler_type", type=str, default="linear")
    parser.add_argument("--warmup_ratio", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output_dir", type=str, default="checkpoints")
    parser.add_argument("--logging_steps", type=int, default=500)
    parser.add_argument("--eval_steps", type=int)
    parser.add_argument("--save_steps", type=int)
    parser.add_argument("--save_total_limit", type=int)
    
    args = parser.parse_args()
    train(**vars(args))
