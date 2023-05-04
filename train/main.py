import torch
from transformers import GPT2Tokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling, TextDataset, GPTNeoForCausalLM


def main():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    tokenizer = GPT2Tokenizer.from_pretrained('EleutherAI/gpt-neo-1.3B')
    model = GPTNeoForCausalLM.from_pretrained(
        'EleutherAI/gpt-neo-1.3B', low_cpu_mem_usage=True)

    EPOCHS = 10
    BATCH_SIZE = 16
    LR = 5e-5
    WARMUP_STEPS = 2000
    WEIGHT_DECAY = 0.05
    TRAIN_PATH = "./raw_data.txt"
    BLOCK_SIZE = 128

    training_args = TrainingArguments(
        output_dir="./checkpoint",
        overwrite_output_dir=True,
        save_total_limit=1,
        num_train_epochs=EPOCHS,

        save_strategy="epoch",
        logging_strategy="epoch",
        per_device_train_batch_size=BATCH_SIZE,

        learning_rate=LR,
        warmup_steps=WARMUP_STEPS,
        weight_decay=WEIGHT_DECAY,
        lr_scheduler_type='linear',
        # gradient_accumulation_steps=8,
        # max_steps=4
    )

    train_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=TRAIN_PATH,
        block_size=BLOCK_SIZE
    )
    collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    trainer = Trainer(
        model=model.to(device),
        # compute_metrics=compute_metrics,              
        args=training_args,
        train_dataset=train_dataset,
        # eval_dataset=train_dataset,
        data_collator=collator,
    )

    trainer.train()

    model.save_pretrained("./GPT-Neo-1.3_model_v2")
    tokenizer.save_pretrained("./GPT-Neo-1.3_tokenizer_v2")

