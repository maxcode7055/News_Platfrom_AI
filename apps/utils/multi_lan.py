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
text = input("Enter Your Text for translation...")

english_text = f"""{text}"""

# Define the target languages
languages = {
    "English": "en_XX",
    "Farsi (Persian)": "fa_IR",
    "French": "fr_XX",
    "Polish": "pl_PL",
    "Somali": "so_SO",
    "Spanish": "es_XX",
    "Turkish": "tr_TR"
}

# Translate text to each language and print the result
for lang, lang_code in languages.items():
    translated_text = translate_text(english_text, model, tokenizer, lang_code)
    print(f"Translation in {lang}:\n{translated_text[0]}\n")

