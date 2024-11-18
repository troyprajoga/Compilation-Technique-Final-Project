import tkinter as tk
import re
from nltk.corpus import words
import nltk

nltk.download('words')

BRAILLE_MAP = {
    "a": "⠁", "b": "⠃", "c": "⠉", "d": "⠙", "e": "⠑", 
    "f": "⠋", "g": "⠛", "h": "⠓", "i": "⠊", "j": "⠚", 
    "k": "⠅", "l": "⠇", "m": "⠍", "n": "⠝", "o": "⠕", 
    "p": "⠏", "q": "⠟", "r": "⠗", "s": "⠎", "t": "⠞", 
    "u": "⠥", "v": "⠧", "w": "⠺", "x": "⠭", "y": "⠽", 
    "z": "⠵", " ": " ", 
    ",": "⠂", ".": "⠲", "?": "⠦", "!": "⠖", 
    "'": "⠄", "-": "⠤", ":": "⠒", ";": "⠆", 
    "(": "⠶", ")": "⠶"
}

# Check if a token is a valid English word
def is_valid_word(token):
    return token in words.words()

# Translate English to Braille and perform lexical analysis
def translate_and_analyze():
    english_text = english_input.get("1.0", tk.END).strip().lower()
    
    # Translate to Braille
    braille_text = "".join(BRAILLE_MAP.get(char, "?") for char in english_text)
    braille_output.delete("1.0", tk.END)
    braille_output.insert(tk.END, braille_text)
    
    # Tokenize input
    tokens = re.findall(r"[a-zA-Z]+|\d+|[^\w\s]", english_text)
    valid_tokens = [token for token in tokens if is_valid_word(token)]
    invalid_tokens = [token for token in tokens if not is_valid_word(token)]
    
    # Display tokens and lexical analysis results
    token_output.delete("1.0", tk.END)
    token_output.insert(tk.END, "Valid Tokens:\n" + "\n".join(valid_tokens) + "\n\n")
    token_output.insert(tk.END, "Invalid Tokens:\n" + "\n".join(invalid_tokens))

root = tk.Tk()
root.title("English to Braille Translator with Lexical Analysis")

left_frame = tk.Frame(root, width=300, height=400, bg="lightblue", padx=10, pady=10)
right_frame = tk.Frame(root, width=300, height=400, bg="lightgreen", padx=10, pady=10)

left_frame.pack(side="left", fill="both", expand=True)
right_frame.pack(side="right", fill="both", expand=True)

tk.Label(left_frame, text="Enter English Text:", font=("Arial", 14), bg="lightblue").pack(anchor="w")
english_input = tk.Text(left_frame, wrap="word", height=15, font=("Arial", 12))
english_input.pack(fill="both", expand=True)

translate_button = tk.Button(left_frame, text="Translate & Analyze", command=translate_and_analyze, bg="white")
translate_button.pack(pady=10)

tk.Label(right_frame, text="Braille Translation:", font=("Arial", 14), bg="lightgreen").pack(anchor="w")
braille_output = tk.Text(right_frame, wrap="word", height=8, font=("Arial", 12), bg="lightgray")
braille_output.pack(fill="both", expand=True)

tk.Label(right_frame, text="Tokens Analysis:", font=("Arial", 14), bg="lightgreen").pack(anchor="w", pady=5)
token_output = tk.Text(right_frame, wrap="word", height=8, font=("Arial", 12), bg="lightyellow")
token_output.pack(fill="both", expand=True)

root.mainloop()
