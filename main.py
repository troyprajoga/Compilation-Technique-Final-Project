import tkinter as tk
import re
from nltk.corpus import words
import nltk
from nltk import pos_tag, word_tokenize

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
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

def check_grammar(sentence):
    tokens = word_tokenize(sentence)
    pos_tags = pos_tag(tokens)        #Get POS tags for example like ('She', 'PRP'), ('reads', 'VBZ'), ('books', 'NNS')

    # Extract POS tags only (e.g., ['PRP', 'VB', 'NN'])
    structure = [tag[1] for tag in pos_tags]

    # Define expanded grammar rules
    if structure == ['PRP', 'VB'] or structure == ['PRP', 'VBZ']:  # Subject + Verb (e.g., "He runs")
        return True, "Valid SV structure."
    elif structure == ['PRP', 'VB', 'NN'] or structure == ['PRP', 'VBZ', 'NN']:  # Subject + Verb + Object (e.g., "She reads books")
        return True, "Valid SVO structure."
    elif structure == ['PRP', 'VBZ', 'JJ'] or structure == ['PRP', 'VB', 'JJ']:  # Subject + Verb + Complement (e.g., "He is tall")
        return True, "Valid SVC structure."
    elif structure == ['DT', 'NN', 'VBZ', 'RB']:  # Article + Noun + Verb + Adverb (e.g., "The dog runs quickly")
        return True, "Valid Article + Noun + Verb + Adverb structure."
    elif structure == ['PRP', 'MD', 'VB']:  # Subject + Modal Verb + Verb (e.g., "He can run")
        return True, "Valid Subject + Modal Verb + Verb structure."
    elif structure == ['PRP', 'VBP', 'VBG']:  # Subject + Verb + Gerund (e.g., "They are running")
        return True, "Valid Subject + Verb + Gerund structure."
    else:
        return False, "Invalid sentence structure."

#Check if a token is a valid English word
def is_valid_word(token):
    return token in words.words()

#Translate English to Braille and do lexical analysis
def translate_and_analyze(event=None):  #Add event parameter to handle binding
    english_text = english_input.get("1.0", tk.END).strip().lower()
    
    if not english_text:  # Handle empty input
        braille_output.delete("1.0", tk.END)
        token_output.delete("1.0", tk.END)
        return
    
    # Check grammar first
    is_valid, grammar_message = check_grammar(english_text)
    if not is_valid:
        braille_output.delete("1.0", tk.END)
        braille_output.insert(tk.END, "Grammar Error: " + grammar_message)
        return  # Stop the function if there's a grammar error
    
    # Proceed with translation if grammar is correct
    braille_text = "".join(BRAILLE_MAP.get(char, "?") for char in english_text)
    braille_output.delete("1.0", tk.END)
    braille_output.insert(tk.END, braille_text)

    # Tokenize input and perform lexical analysis
    tokens = re.findall(r"[a-zA-Z]+|\d+|[^\w\s]", english_text)
    valid_tokens = [token for token in tokens if is_valid_word(token)]
    invalid_tokens = [token for token in tokens if not is_valid_word(token)]
    
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

english_input.bind("<KeyRelease>", lambda event: translate_and_analyze())

tk.Label(right_frame, text="Braille Translation:", font=("Arial", 14), bg="lightgreen").pack(anchor="w")
braille_output = tk.Text(right_frame, wrap="word", height=8, font=("Arial", 12), bg="lightgray")
braille_output.pack(fill="both", expand=True)

tk.Label(right_frame, text="Tokens Analysis:", font=("Arial", 14), bg="lightgreen").pack(anchor="w", pady=5)
token_output = tk.Text(right_frame, wrap="word", height=8, font=("Arial", 12), bg="lightyellow")
token_output.pack(fill="both", expand=True)

root.mainloop()
