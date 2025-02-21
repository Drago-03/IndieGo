import os
import logging
from typing import List, Dict, Any
import json
from pathlib import Path
import random
from concurrent.futures import ThreadPoolExecutor
import requests
import gzip
import tarfile
from tqdm import tqdm
import pandas as pd

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

class DataPreparation:
    """Prepare training data for IndieGO model"""
    
    def __init__(
        self,
        output_dir: str = "datasets",
        num_workers: int = 4,
        random_seed: int = 42,
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.num_workers = num_workers
        random.seed(random_seed)
        
        # Create subdirectories
        (self.output_dir / "raw").mkdir(exist_ok=True)
        (self.output_dir / "processed").mkdir(exist_ok=True)
        (self.output_dir / "final").mkdir(exist_ok=True)
    
    def download_dataset(self, url: str, output_path: Path) -> None:
        """Download dataset from URL with progress bar"""
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get("content-length", 0))
        
        with open(output_path, "wb") as f, tqdm(
            desc=f"Downloading {output_path.name}",
            total=total_size,
            unit="iB",
            unit_scale=True,
        ) as pbar:
            for data in response.iter_content(chunk_size=1024):
                size = f.write(data)
                pbar.update(size)
    
    def download_code_datasets(self):
        """Download various code datasets"""
        datasets = {
            # Python
            "python-code": "https://huggingface.co/datasets/codeparrot/github-code/resolve/main/python_train.jsonl.gz",
            
            # Documentation
            "python-docs": "https://huggingface.co/datasets/codeparrot/github-code/resolve/main/python_documentation_train.jsonl.gz",
            
            # Stack Overflow
            "stackoverflow": "https://huggingface.co/datasets/codeparrot/stackoverflow-questions/resolve/main/train.jsonl.gz",
        }
        
        for name, url in datasets.items():
            output_path = self.output_dir / "raw" / f"{name}.jsonl.gz"
            if not output_path.exists():
                logger.info(f"Downloading {name} dataset...")
                self.download_dataset(url, output_path)
            else:
                logger.info(f"Dataset {name} already exists, skipping download")
    
    def process_python_code(self, file_path: Path) -> List[Dict[str, str]]:
        """Process Python code dataset"""
        examples = []
        
        with gzip.open(file_path, "rt") as f:
            for line in tqdm(f, desc=f"Processing {file_path.name}"):
                example = json.loads(line)
                
                # Clean and filter code
                code = example["code"]
                if len(code.split("\n")) > 5:  # Skip very short snippets
                    examples.append({
                        "text": code,
                        "type": "code",
                    })
        
        return examples
    
    def process_documentation(self, file_path: Path) -> List[Dict[str, str]]:
        """Process documentation dataset"""
        examples = []
        
        with gzip.open(file_path, "rt") as f:
            for line in tqdm(f, desc=f"Processing {file_path.name}"):
                example = json.loads(line)
                
                # Clean and format documentation
                doc = example["documentation"]
                if len(doc) > 100:  # Skip very short docs
                    examples.append({
                        "text": doc,
                        "type": "documentation",
                    })
        
        return examples
    
    def process_stackoverflow(self, file_path: Path) -> List[Dict[str, str]]:
        """Process Stack Overflow dataset"""
        examples = []
        
        with gzip.open(file_path, "rt") as f:
            for line in tqdm(f, desc=f"Processing {file_path.name}"):
                example = json.loads(line)
                
                # Format Q&A pairs
                question = example["question"]
                answer = example["answer"]
                
                if len(question) > 50 and len(answer) > 50:
                    examples.append({
                        "text": f"Question: {question}\n\nAnswer: {answer}",
                        "type": "qa",
                    })
        
        return examples
    
    def create_training_examples(
        self,
        code_examples: List[Dict[str, str]],
        doc_examples: List[Dict[str, str]],
        qa_examples: List[Dict[str, str]],
    ) -> List[Dict[str, str]]:
        """Create training examples with different tasks"""
        
        examples = []
        
        # Code explanation tasks
        for code in random.sample(code_examples, min(1000, len(code_examples))):
            examples.append({
                "text": f"Explain this code:\n\n{code['text']}\n\nExplanation:",
                "type": "explanation",
            })
        
        # Code generation tasks
        for doc in random.sample(doc_examples, min(1000, len(doc_examples))):
            examples.append({
                "text": f"Generate code based on this documentation:\n\n{doc['text']}\n\nCode:",
                "type": "generation",
            })
        
        # Code improvement tasks
        for code in random.sample(code_examples, min(1000, len(code_examples))):
            examples.append({
                "text": f"Suggest improvements for this code:\n\n{code['text']}\n\nImprovements:",
                "type": "improvement",
            })
        
        # Q&A tasks
        examples.extend(random.sample(qa_examples, min(1000, len(qa_examples))))
        
        return examples
    
    def prepare_data(self):
        """Prepare all training data"""
        logger.info("Starting data preparation...")
        
        # Download datasets
        self.download_code_datasets()
        
        # Process datasets
        logger.info("Processing datasets...")
        code_examples = self.process_python_code(
            self.output_dir / "raw" / "python-code.jsonl.gz"
        )
        doc_examples = self.process_documentation(
            self.output_dir / "raw" / "python-docs.jsonl.gz"
        )
        qa_examples = self.process_stackoverflow(
            self.output_dir / "raw" / "stackoverflow.jsonl.gz"
        )
        
        # Create training examples
        logger.info("Creating training examples...")
        training_examples = self.create_training_examples(
            code_examples, doc_examples, qa_examples
        )
        
        # Save processed data
        logger.info("Saving processed data...")
        output_path = self.output_dir / "final" / "train.jsonl"
        with open(output_path, "w") as f:
            for example in training_examples:
                f.write(json.dumps(example) + "\n")
        
        # Create train/val split
        df = pd.DataFrame(training_examples)
        train_df = df.sample(frac=0.9, random_state=42)
        val_df = df.drop(train_df.index)
        
        train_df.to_json(
            self.output_dir / "final" / "train.jsonl",
            orient="records",
            lines=True,
        )
        val_df.to_json(
            self.output_dir / "final" / "validation.jsonl",
            orient="records",
            lines=True,
        )
        
        logger.info(
            f"Data preparation complete. "
            f"Created {len(train_df)} training examples "
            f"and {len(val_df)} validation examples."
        )

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output_dir",
        type=str,
        default="datasets",
        help="Output directory for datasets",
    )
    parser.add_argument(
        "--num_workers",
        type=int,
        default=4,
        help="Number of worker threads",
    )
    parser.add_argument(
        "--random_seed",
        type=int,
        default=42,
        help="Random seed",
    )
    
    args = parser.parse_args()
    
    data_prep = DataPreparation(
        output_dir=args.output_dir,
        num_workers=args.num_workers,
        random_seed=args.random_seed,
    )
    data_prep.prepare_data() 