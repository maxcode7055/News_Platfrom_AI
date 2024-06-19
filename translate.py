from transformers import MBartForConditionalGeneration, MBart50Tokenizer

def download_model():
    model_name = "facebook/mbart-large-50-many-to-many-mmt"
    model = MBartForConditionalGeneration.from_pretrained(model_name)
    tokenizer = MBart50Tokenizer.from_pretrained(model_name)
    return model, tokenizer

def translate_text(text, model, tokenizer, target_lang):
    tokenizer.src_lang = "en_XX"  
    tokenizer.tgt_lang = target_lang 

    if target_lang in tokenizer.lang_code_to_id:
        encoded_text = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        generated_tokens = model.generate(
            **encoded_text,
            forced_bos_token_id=tokenizer.lang_code_to_id[target_lang]
        )

        out = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        return out
    else:
        return ["Translation not available for this language code."]

model, tokenizer = download_model()

text = input("Enter Your Text for translation...")

english_text = f"""{text}"""

languages = {
    "English": "en_XX",
    "Farsi (Persian)": "fa_IR",
    "French": "fr_XX",
    "Polish": "pl_PL",
    "Somali": "so_SO",
    "Spanish": "es_XX",
    "Turkish": "tr_TR"
}

for lang, lang_code in languages.items():
    translated_text = translate_text(english_text, model, tokenizer, lang_code)
    print(f"Translation in {lang}:\n{translated_text[0]}\n")

