from dataclasses import dataclass
import loguru
from transformers import PreTrainedTokenizerBase, TrainerCallback

@dataclass
class CustomCollator:
    tokenizer: PreTrainedTokenizerBase
    padding = True
    return_tensors: str = "pt"

    def __call__(self, batch):
        tokenized_batch = self.tokenizer(
            [f"FEN: {exp['fen']}\nMOVE: {exp['move']}" for exp in batch],
            return_tensors=self.return_tensors,
            padding=self.padding,
        )

        labels = tokenized_batch["input_ids"].clone()
        ignore_tokens = self.tokenizer(
            [f"FEN: {exp['fen']}\nMOVE:" for exp in batch]
        )["input_ids"]
        for i, exp in enumerate(ignore_tokens):
            labels[i, : len(exp)] = -100
        tokenized_batch["labels"] = labels
        return tokenized_batch


class LogCallback(TrainerCallback):
    """
    A bare [`TrainerCallback`] that just prints the logs.
    """

    def on_log(self, args, state, control, logs=None, **kwargs):
        _ = logs.pop("total_flos", None)
        if state.is_local_process_zero:
            loguru.logger.info(logs)