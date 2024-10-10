from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from dataset import CustomCollator
from datasets import load_dataset
import os
os.environ["HF_TOKEN"] = "YOUR_API_KEY"

train_dataset = load_dataset("Vasanth/Vasanth/chessdevilai_fen_dataset", split="train")
eval_dataset = load_dataset("Vasanth/Vasanth/chessdevilai_fen_dataset", split="test")

model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token
collator = CustomCollator(tokenizer=tokenizer)

training_args = TrainingArguments(
    output_dir="chessdevilaifen_v2",
    logging_dir="chessdevilaifen_v2",
    overwrite_output_dir=True,
    logging_strategy="steps",
    logging_steps=1000,
    evaluation_strategy="steps",
    eval_steps=1000,
    save_strategy="steps",
    save_steps=1000,
    per_device_eval_batch_size=16,
    per_device_train_batch_size=16,
    num_train_epochs=1,
    gradient_accumulation_steps=1,
    learning_rate=5e-5,
    fp16=True,
    remove_unused_columns=False,
    dataloader_num_workers=30,
    resume_from_checkpoint=False,
    push_to_hub=True,
    report_to="tensorboard"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    data_collator=collator,
)

trainer.train(resume_from_checkpoint=False)
trainer.save_model("chessdevilai_fenv2")