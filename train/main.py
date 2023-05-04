import torch
from transformers import GPT2Tokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling, TextDataset, GPTNeoForCausalLM
from accelerate import Accelerator
from torch.nn.parallel import DistributedDataParallel
import argparse
from dataset import prepare_data

def config():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default='EleutherAI/gpt-neo-1.3B')
    parser.add_argument('--epochs', default=10)
    parser.add_argument('--batch_size', default=8)
    parser.add_argument('--learning_rate', default=5e-5)
    parser.add_argument('--warmup_steps', default=2000)
    parser.add_argument('--weight_decay', default=0.05)
    parser.add_argument('--json_path', default="./train.json")
    parser.add_argument('--block_size', default=128)
    parser.add_argument('--checkpoint_path', default='./checkpoint')
    parser.add_argument('--init_data', default=True)

    args = parser()
    return args

def main():
    args = config()

    accelerator = Accelerator()
    # device = accelerator.device("cuda:0" if torch.cuda.is_available() else "cpu")
    device = accelerator.device
    tokenizer = GPT2Tokenizer.from_pretrained('EleutherAI/gpt-neo-1.3B')
    model = GPTNeoForCausalLM.from_pretrained('EleutherAI/gpt-neo-1.3B', low_cpu_mem_usage=True)

    if args.init_data:
        prepare_data(args.json_path, args.block_size, tokenizer, outdir=f"./train_raw_{args.block_size}.txt")

    # model = model.to(device)
    model = DistributedDataParallel(model)

    # EPOCHS = 10
    # BATCH_SIZE = 16
    # LR = 5e-5
    # WARMUP_STEPS = 2000
    # WEIGHT_DECAY = 0.05
    # TRAIN_PATH = "./raw_data.txt"
    # BLOCK_SIZE = 128

    train_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=args.train_config,
        block_size=args.block_size
    )

    training_args = TrainingArguments(
        output_dir=args.checkpoint_path,
        overwrite_output_dir=True,
        save_total_limit=1,
        num_train_epochs=args.epochs,

        save_strategy="step",
        logging_strategy="step",
        per_device_train_batch_size=args.batch_size,

        learning_rate=args.learning_rate,
        warmup_steps=args.warmup_steps,
        weight_decay=args.weight_decay,
        lr_scheduler_type='linear',
        report_to='wandb',
        save_steps=200,
        # gradient_accumulation_steps=8,
        # max_steps=4
    )

    collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    model, train_dataset = accelerator.prepare(model, train_dataset)

    trainer = Trainer(
        model=model,
        # compute_metrics=compute_metrics,              
        args=training_args,
        train_dataset=train_dataset,
        # eval_dataset=train_dataset,
        data_collator=collator,
    )

    trainer.train()

    model.save_pretrained("./GPT-Neo-1.3_model_v2")
    tokenizer.save_pretrained("./GPT-Neo-1.3_tokenizer_v2")


if __name__ == "__main__":
    main()
