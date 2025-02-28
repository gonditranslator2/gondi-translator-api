from fastapi import FastAPI
import pandas as pd
from typing import Dict

app = FastAPI()

# Load Gondi translation dataset
df = pd.read_csv("gondi_translations.csv")  # Ensure this file is available on the server

def translate_text(text: str, direction: str) -> str:
    """Translate text between English and Gondi based on the dataset."""
    if direction == "en_to_gondi":
        translation = df[df['English'].str.lower() == text.lower()]['Gondi']
    else:
        translation = df[df['Gondi'].str.lower() == text.lower()]['English']
    
    return translation.values[0] if not translation.empty else "Translation not found"

@app.get("/translate")
def translate(text: str, direction: str = "en_to_gondi") -> Dict[str, str]:
    translated_text = translate_text(text, direction)
    return {"input": text, "translated_text": translated_text}

@app.get("/")
def home():
    return {"message": "Gondi Translator API is running!"}
