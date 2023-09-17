from tokenizers import Tokenizer, models, trainers, pre_tokenizers, decoders

# Create a new tokenizer
tokenizer = Tokenizer(models.BPE())

# Pre-tokenizer responsible for pre-segmenting the text
tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel()

# Decoder to be able to decode the output of the tokenizer
tokenizer.decoder = decoders.ByteLevel()

# Train the tokenizer
trainer = trainers.BpeTrainer(special_tokens=["[CLS]", "[SEP]", "[PAD]", "[MASK]", "[UNK]"])
files = ["path/to/your/dataset.txt"]  # Replace with the path to your dataset
tokenizer.train(files, trainer)

# Save the tokenizer
tokenizer.save("path/to/your/tokenizer.json")
