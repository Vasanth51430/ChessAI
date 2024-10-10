from transformers import AutoModelForCausalLM, AutoTokenizer

def next_move(model, tokenizer, fen):

    input_ids = tokenizer(f"FEN: {fen}\nMOVE:", return_tensors="pt")
    input_ids = {k: v.to(model.device) for k, v in input_ids.items()}
    out = model.generate(
        **input_ids,
        max_new_tokens=5,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        temperature=0.1,
        num_beams=4,
        num_return_sequences=4
    )
    next_moves = []
    for out_str in tokenizer.batch_decode(out):
        next_moves.append(out_str.split("MOVE:")[-1].replace("<|endoftext|>", "").strip())
    return next_moves


model = AutoModelForCausalLM.from_pretrained("Vasanth/chessdevilaifen_v2")
tokenizer = AutoTokenizer.from_pretrained("Vasanth/chessdevilaifen_v2")
tokenizer.pad_token = tokenizer.eos_token

fen = "8/6kp/3p2p1/8/8/4p3/3q4/1K6 w - - 2 48"
print(next_move(model, tokenizer, fen))





