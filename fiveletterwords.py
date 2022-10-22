import time

import string
from typing import Dict

bitfield_lookup = {c: 1 << i for i, c in enumerate(string.ascii_lowercase)}


def word_to_bitfield(word):
    ret = 0
    for c in word:
        ret |= bitfield_lookup[c]
    return ret

start_time = time.time()

filestub = './'


def load_words():
    words_txt = './words_alpha.txt'
    with open(words_txt) as word_file:
        valid_words = list(word_file.read().split())
    return valid_words


# number of scanA increases per progress report
stepgap = 1000

# I could be clever and write this to be dynamic
# but for now I'll hard code everything assuming five words
number_of_sets = 5

english_words = load_words()

print(f"{len(english_words)} words in total")

five_letter_words = [word for word in english_words if len(word) == 5]

print(f"{len(five_letter_words)} words have {5} letters")

word_sets: Dict[int, str] = {}

for word in five_letter_words:
    unique_letters = set(word)
    if len(unique_letters) == 5:
        bitfield = word_to_bitfield(word)
        if bitfield not in word_sets:
            word_sets[bitfield] = word

number_of_words = len(word_sets)

print(f"{number_of_words} words have a unique set of {5} letters")
doublewords = {}
scanA = 0
word_sets_items = list(word_sets.items())
while scanA < number_of_words - 1:
    scanB = scanA + 1
    a_bitfield, a_word = word_sets_items[scanA]
    while scanB < number_of_words:
        b_bitfield, b_word = word_sets_items[scanB]
        if a_bitfield & b_bitfield == 0:
            doublewords[a_bitfield | b_bitfield] = a_word, b_word
        scanB += 1
    scanA += 1

number_of_doublewords = len(doublewords)

print(f"we found {number_of_doublewords} combos")

success_found = []

scanA = 0
print(f"starting at position {scanA}")
doublewords_items = list(doublewords.items())
while scanA < number_of_doublewords - 1:
    if scanA % stepgap == 0:
        print(f"Up to {scanA} of {number_of_doublewords} after {time.time() - start_time} seconds.")

    scanB = scanA + 1
    a_bitfield, a_words = doublewords_items[scanA]
    while scanB < number_of_doublewords:
        b_bitfield, b_words = doublewords_items[scanB]
        if a_bitfield & b_bitfield == 0:
            give_it_a_try = a_bitfield | b_bitfield
            for c_bitfield, c_word in word_sets.items():
                if give_it_a_try & c_bitfield == 0:
                    success = list(a_words + b_words + (c_word,))
                    success.sort()
                    if success not in success_found:
                        success_found.append(success)
                        print(success)
        scanB += 1
    scanA += 1

print(f"Damn, we had {len(success_found)} successful finds!")
print(f"That took {time.time() - start_time} seconds")

print("Here they all are:")
for i in success_found:
    print(i)

print("DONE")
