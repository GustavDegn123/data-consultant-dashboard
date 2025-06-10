import pandas as pd
from deep_translator import GoogleTranslator

def translate_categories(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    unique_cats = df["product_category_name_english"].dropna().unique()

    translator = GoogleTranslator(source='en', target='da')
    translations = {}

    print("🔁 Oversætter kategorier...")

    for cat in unique_cats:
        try:
            readable = cat.replace("_", " ")
            translated = translator.translate(readable).capitalize()
            translations[cat] = translated
        except Exception as e:
            print(f"❌ Fejl ved '{cat}':", e)
            translations[cat] = readable  # fallback til engelsk

    # Gem som CSV
    pd.DataFrame.from_dict(translations, orient="index", columns=["product_category_name_danish"]) \
        .reset_index() \
        .rename(columns={"index": "product_category_name_english"}) \
        .to_csv(output_csv, index=False)

    print(f"✅ Oversættelser gemt til: {output_csv}")

# Eksempelkørsel
if __name__ == "__main__":
    translate_categories(
        input_csv="data/olist/product_category_name_translation.csv",
        output_csv="data/olist/category_translation_da.csv"
    )
