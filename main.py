import tkinter as tk
from nltk import pos_tag, word_tokenize
from nltk.corpus import brown
from nltk.tree import Tree
import nltk
import matplotlib.pyplot as plt

# Download required resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('brown')

# Extract words from Brown Corpus and tag them
brown_words = brown.words()
tagged_words = pos_tag(brown_words)

# Create a dictionary to store words based on their POS tags
tagged_word_list = {}

for word, tag in tagged_words:
    if tag not in tagged_word_list:
        tagged_word_list[tag] = set()
    tagged_word_list[tag].add(word.lower())

# Braille map for translation
BRAILLE_MAP = {
    "a": "⠁", "b": "⠃", "c": "⠉", "d": "⠙", "e": "⠑",
    "f": "⠋", "g": "⠛", "h": "⠓", "i": "⠊", "j": "⠚",
    "k": "⠅", "l": "⠇", "m": "⠍", "n": "⠝", "o": "⠕",
    "p": "⠏", "q": "⠟", "r": "⠗", "s": "⠎", "t": "⠞",
    "u": "⠥", "v": "⠧", "w": "⠺", "x": "⠭", "y": "⠽",
    "z": "⠵", " ": "   ",
    ",": "⠂", ".": "⠲", "?": "⠦", "!": "⠖",
    "'": "⠄", "-": "⠤", ":": "⠒", ";": "⠆",
    "(": "⠶", ")": "⠶"
}

# Validate grammar dynamically
def validate_grammar(pos_tags):
    valid_structures = [
        ['PRP', 'VB'],  # Subject + Verb
        ['PRP', 'VBZ'],  # Subject + Verb (3rd person singular)
        ['PRP', 'VB', 'NN'],  # Subject + Verb + Object
        ['PRP', 'VB', 'NNS'],
        ['PRP', 'VBZ', 'NN'],  # Subject + Verb + Object (3rd person singular)
        ['PRP', 'VBZ', 'NNS'],
        ['PRP', 'VBZ', 'JJ'],  # Subject + Verb + Complement
        ['DT', 'NN', 'VBZ', 'RB'],  # Article + Noun + Verb + Adverb
        ['PRP', 'MD', 'VB'],  # Subject + Modal Verb + Verb
    ]
    structure = [tag for _, tag in pos_tags]
    return structure in valid_structures

# Create and display parse tree
def display_parse_tree(pos_tags):
    # Close previous figure if it exists
    plt.close('all')
    tree = Tree('S', [Tree(tag, [word]) for word, tag in pos_tags])
    # Plot the tree using Matplotlib
    plt.figure(figsize=(10, 6))
    tree.draw()
    plt.show()

# Update Braille and token analysis continuously
def update_continuous(event=None):
    english_text = english_input.get("1.0", tk.END).strip().lower()

    # Clear outputs for continuous sections
    braille_output.delete("1.0", tk.END)
    token_output.delete("1.0", tk.END)

    if not english_text:  # Handle empty input
        return

    # Tokenize input
    tokens = word_tokenize(english_text)
    pos_tags = pos_tag(tokens)

    # Translate to Braille
    braille_text = " ".join("".join(BRAILLE_MAP.get(char, "?") for char in word) for word in english_text.split())
    braille_output.insert(tk.END, braille_text)

    # Token analysis
    valid_tokens = []
    invalid_tokens = []
    for word, tag in pos_tags:
        if tag in tagged_word_list and word in tagged_word_list[tag]:
            valid_tokens.append(word)
        else:
            invalid_tokens.append(word)

    token_output.insert(tk.END, "Valid Tokens:\n" + "\n".join(valid_tokens) + "\n\n")
    token_output.insert(tk.END, "Invalid Tokens:\n" + "\n".join(invalid_tokens))

# Generate parse tree on Enter key
def generate_parse_tree(event=None):
    english_text = english_input.get("1.0", tk.END).strip().lower()

    if not english_text:  # Handle empty input
        return

    # Tokenize input
    tokens = word_tokenize(english_text)
    pos_tags = pos_tag(tokens)

    if not validate_grammar(pos_tags):
        braille_output.delete("1.0", tk.END)
        braille_output.insert(tk.END, "Grammar Error: Invalid sentence structure.")
        return

    # Generate and display parse tree
    display_parse_tree(pos_tags)

# GUI setup
root = tk.Tk()
root.title("English to Braille Translator with Parse Tree")

# Configure grid layout
root.rowconfigure(0, weight=0)  # Headers
root.rowconfigure(1, weight=1)  # Input and translation section
root.columnconfigure([0, 1, 2], weight=1)  # Equal columns

# Input Section
tk.Label(root, text="Enter English Text:", font=("Arial", 14), bg="lightblue").grid(row=0, column=0, sticky="nsew")
english_input = tk.Text(root, wrap="word", font=("Arial", 12), bg="lightblue")
english_input.grid(row=1, column=0, sticky="nsew")
english_input.bind("<KeyRelease>", update_continuous)  # Continuous update on key release
english_input.bind("<Return>", generate_parse_tree)  # Parse tree generation on Enter

# Braille Output Section
tk.Label(root, text="Braille Translation:", font=("Arial", 14), bg="lightgreen").grid(row=0, column=1, sticky="nsew")
braille_output = tk.Text(root, wrap="word", font=("Arial", 12), bg="lightgreen")
braille_output.grid(row=1, column=1, sticky="nsew")

# Token Analysis Section
tk.Label(root, text="Tokens Analysis:", font=("Arial", 14), bg="lightyellow").grid(row=0, column=2, sticky="nsew")
token_output = tk.Text(root, wrap="word", font=("Arial", 12), bg="lightyellow")
token_output.grid(row=1, column=2, sticky="nsew")

root.mainloop()
