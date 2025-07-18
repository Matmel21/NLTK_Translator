import nltk
import tkinter as tk
from tkinter import ttk
from langdetect import detect
from nltk.stem import WordNetLemmatizer as wnl
from nltk.corpus import wordnet
from deep_translator import GoogleTranslator


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def translate_text():
    input_text = input_box.get("1.0", tk.END).strip()
    if not input_text:
        output_box.config(state=tk.NORMAL)
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, "Please enter some text to translate.")
        output_box.config(state=tk.DISABLED)
        return
    
    detected_language = detect(input_text)
    target_language = target_language_var.get()

    tokens = nltk.word_tokenize(input_text)
    tagged = nltk.pos_tag(tokens)

    if lemmatization_flag.get():
        lemmatizer = wnl()
        lemmatized = [lemmatizer.lemmatize(token, pos=get_wordnet_pos(pos)) for token, pos in tagged]
        cleaned_text = ' '.join(lemmatized)
    else:
        cleaned_text = input_text

    try:
        translated_text = GoogleTranslator(source=detected_language, target=target_language).translate(cleaned_text)
    except Exception as e:
        translated_text = f"Error during translation: {str(e)}"
    
    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, translated_text)
    output_box.config(state=tk.DISABLED)


# GUI setup
root = tk.Tk()
root.title("Translator")
root.geometry("600x400")

# input box
input_label = tk.Label(root, text="Enter text to translate:")
input_box = tk.Text(root, height=10, width=50)
input_box.pack()

# Language selection
tk_label = tk.Label(root, text="Select target language:")
target_language_var = tk.StringVar(value='en')  # Default to English
target_language_menu = ttk.Combobox(root, textvariable=target_language_var)

# List of supported languages
languages = ['en', 'fr', 'es', 'de', 'it', 'pt', 'ru', 'zh-CN', 'ja', 'ko']
target_language_menu['values'] = languages
target_language_menu.current(0)  # Set default selection
target_language_menu.pack()

# Translate button
translate_button = tk.Button(root, text="Translate", command=translate_text)
translate_button.pack(pady=10)

# Output box
output_label = tk.Label(root, text="Translated text:").pack(pady=5)
output_box = tk.Text(root, height=10, width=50, state=tk.DISABLED)
output_box.pack()

# lemmatization flag
lemmatization_flag = tk.BooleanVar(value=False)
lemmatization_checkbox = tk.Checkbutton(root, 
                                        text="Enable Lemmatization", 
                                        variable=lemmatization_flag
                                        )
lemmatization_checkbox.pack(pady=5)

root.mainloop()

