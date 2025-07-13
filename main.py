import nltk
from langdetect import detect
from nltk.stem import WordNetLemmatizer as wnl
from nltk.corpus import wordnet
from deep_translator import GoogleTranslator

prompt= str(input("Enter a prompt: "))

language = detect(prompt)

tokens = nltk.word_tokenize(prompt)
print("Tokens:", tokens)

tagged = nltk.pos_tag(tokens)
print("POS Tags:", tagged)

tree = nltk.ne_chunk(tagged)
print("Named Entities:", tree)

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

lemmatizer = wnl()
lemmatized = [lemmatizer.lemmatize(token, pos=get_wordnet_pos(pos)) for token, pos in tagged]
print("Lemmatized Tokens:", lemmatized)

translated = GoogleTranslator(source=language, target='fr').translate(prompt)
print("Translated Text:", translated)