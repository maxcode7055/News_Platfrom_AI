from transformers import MBartForConditionalGeneration, MBart50Tokenizer

def download_model():
    model_name = "facebook/mbart-large-50-many-to-many-mmt"
    model = MBartForConditionalGeneration.from_pretrained(model_name)
    tokenizer = MBart50Tokenizer.from_pretrained(model_name)
    return model, tokenizer

def translate_text(text, model, tokenizer, target_lang):
    tokenizer.src_lang = "en_XX"  # English
    tokenizer.tgt_lang = target_lang  # Target language
    encoded_text = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    generated_tokens = model.generate(**encoded_text, forced_bos_token_id=tokenizer.lang_code_to_id[target_lang])
    out = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    return out

model, tokenizer = download_model()

# Example text to be translated
english_text = """Learn the basics and advanced concepts of natural language processing (NLP) with our complete NLP tutorial and get ready to explore the vast and exciting field of NLP, where technology meets human language.

NLP tutorial is designed for both beginners and professionals. Whether you’re a data scientist, a developer, or someone curious about the power of language, our tutorial will provide you with the knowledge and skills you need to take your understanding of NLP to the next level."""

# Define the target languages
languages = {
    "en_XX": "English",
    "fa_IR": "Farsi (Persian)",
    "fr_XX": "French",
    "pl_PL": "Poolish",
    "so_SO": "Soomali",
    "es_XX": "Spanish",
    "tr_TR": "Turkish"
}

# Reverse mapping for language names to codes
languages_reverse = {v.lower(): k for k, v in languages.items()}

# Function to get user input for language selection
def get_target_language():
    print("Please select the target language by its code or name:")
    for code, lang in languages.items():
        print(f"{code}: {lang}")
    user_input = input("Enter the language code or name: ").strip().lower()
    
    if user_input in languages:
        return user_input
    elif user_input in languages_reverse:
        return languages_reverse[user_input]
    else:
        print("Invalid language code or name. Please try again.")
        return get_target_language()

# Get user-selected target language
target_language_code = get_target_language()

# Translate the text to the selected language
translated_text = translate_text(english_text, model, tokenizer, target_language_code)
print(f"Translation in {languages[target_language_code]}:\n{translated_text[0]}")
