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


def load_words():
    with open('./words_alpha.txt') as word_file:
        valid_words = list(word_file.read().split())
    return valid_words


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
for scanA in range(0, number_of_words - 1):
    a_bitfield, a_word = word_sets_items[scanA]
    for scanB in range(scanA + 1, number_of_words):
        b_bitfield, b_word = word_sets_items[scanB]
        if a_bitfield & b_bitfield == 0:
            doublewords[a_bitfield | b_bitfield] = a_word, b_word

number_of_doublewords = len(doublewords)

print(f"we found {number_of_doublewords} combos")

success_found = set()

scanA = 0
print(f"starting at position {scanA}")
doublewords_items = list(doublewords.items())
for scanA in range(0, number_of_doublewords - 1):
    if scanA % 100000 == 0:
        print(f"Up to {scanA} of {number_of_doublewords} after {time.time() - start_time} seconds.")
    a_bitfield, a_words = doublewords_items[scanA]
    for scanB in range(scanA + 1, number_of_doublewords - 1):
        b_bitfield, b_words = doublewords_items[scanB]
        if a_bitfield & b_bitfield == 0:
            give_it_a_try = a_bitfield | b_bitfield
            for c_bitfield in word_sets:
                if give_it_a_try & c_bitfield == 0:
                    success = frozenset(a_words + b_words + (word_sets[c_bitfield],))
                    if success not in success_found:
                        success_found.add(success)


print(f"Damn, we had {len(success_found)} successful finds!")
print(f"That took {time.time() - start_time} seconds")

print("Here they all are:")
for i in success_found:
    print(i)

print("DONE")
