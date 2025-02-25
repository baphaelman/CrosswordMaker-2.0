common_words = {}

with open('30k.txt', 'r') as file:
    for line in file:
        word = line.strip()
        word_length = len(word)
        common_words.setdefault(word_length, []).append(word)