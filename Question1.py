from flask import Flask, render_template

app = Flask(__name__)

#===Name Processing Functions===
'''
Takes in a string name and returns a version of name where the only characters that exist are in alphabet.
'''
def remove_nonalpha_chars(name: str) -> str:
    alphaonly_name = ''
    for c in name:
        if c.isalpha():
            alphaonly_name = alphaonly_name + c
    return alphaonly_name

'''
Takes in a string name, and processes the cases of each character.
Prior to processing, strip both sides of name to remove whitespaces.
If name is fully lowercase, make name fully uppercase.
If name is fully uppercase, make name fully lowercase.
If name is neither fully uppercase or lowercase, make it properly capitalized.
'''
def process_name_case_and_keep_alpha_chars(name: str) -> str:
    stripped_name = name.strip()
    name_is_lower = stripped_name == stripped_name.lower()
    name_is_upper = stripped_name == stripped_name.upper()

    if name_is_lower:
        stripped_name = stripped_name.upper()
    elif name_is_upper:
        stripped_name = stripped_name.lower()
    else:
        stripped_name = stripped_name.capitalize()
    
    return stripped_name

'''
Takes in a string name, and processes the cases of each character.
Prior to processing, strip both sides of name to remove whitespaces.
Replaces vowels in name with the corresponding emoji according to the vowel_emojies dictionary.
'''
def process_vowels_to_emoji(name: str) -> str:
    vowel_emojis = {
        "a":"🔺",
        "e":"🎗",
        "i":"👁",
        "o":"🔵",
        "u":"🆙",
    }

    stripped_name = name.strip()
    lowered_name = stripped_name.lower()
    for i in range(len(stripped_name)):
        if vowel_emojis.__contains__(lowered_name[i]):
            vowel_replacement = vowel_emojis[lowered_name[i]]
            stripped_name = stripped_name[:i] + vowel_replacement + stripped_name[i + 1:]
    
    return stripped_name

'''
Takes in a string case_processed_name which is a string that has been processed through process_name_case(name: str)
and returns a welcome message depending on the name being a palindrome and if the name is to be emoji processed.
The welcome message is structured as:

"Welcome, <case_processed_name|process_name_emoji(case_processed_name)>. <Your name is a palindrome!|empty>
'''
def generate_welcome_message(case_processed_name: str, emoji_mode: bool) -> str:
    name_is_palindrome = is_palindrome(case_processed_name.casefold())
    final_name = process_vowels_to_emoji(case_processed_name) if emoji_mode else case_processed_name
    final_message = f"Welcome, {final_name}"

    if name_is_palindrome:
        return final_message + ". Your name is a palindrome!"
    else:
        return final_message + ", to my CSCB20 website!"

def is_palindrome(word: str) -> bool:
    left = 0
    right = len(word) - 1
    while left < right:
        if word[left] != word[right]:
            return False
        left += 1
        right -= 1
    
    return True

#===Flask Routing Functions===

#Load the website by default
@app.route("/") 
def load_main():
    return render_template("index.html")


@app.route("/<name>")
def process_name(name: str):
    if name == '':
        return "Enter a name after the first slash in the url or emoji/(your name) in the url."
    
    alphaonly_name = remove_nonalpha_chars(name)
    stripped_name = process_name_case_and_keep_alpha_chars(alphaonly_name)
    return f"<h1>{generate_welcome_message(stripped_name, False)}</h1>"


@app.route("/emoji/<name>")
def process_name_emoji(name: str):
    alphaonly_name = remove_nonalpha_chars(name)
    stripped_name = process_name_case_and_keep_alpha_chars(alphaonly_name)
    return f"<h1>{generate_welcome_message(stripped_name, True)}</h1>"


if __name__ == "__main__":
    app.run(debug=True)