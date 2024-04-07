with open('invalid-words.txt') as word_file:
    invalid_words = sorted(set(word_file.read().split()))

with open('words_alpha.txt') as word_file:
    valid_words = sorted(set(word_file.read().split()))
    
for word in invalid_words:
    if word in valid_words:
        valid_words.remove(word)

for word in sorted(valid_words):
    if len(word) <= 2:
        valid_words.remove(word)

with open('curated_words.txt', 'w') as f:
    words = 0
    for line in sorted(valid_words):
        f.write(f"{line}\n")
        words += 1
print(f"curated_words_alpha: {words}")