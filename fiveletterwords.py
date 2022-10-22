import array

from multiprocessing import Pool

bitfield_lookup = {c: 1 << i for i, c in enumerate('aesiorunltycdhmpgkbwfvzjxq')}


def load_words():
    ret = {}
    with open('./words_alpha.txt') as word_file:
        for word in word_file.read().split():
            if len(word) != 5: continue
            bitfield = 0
            for c in word:
                bits = bitfield_lookup[c]
                # all bits need to be unique
                if bits & bitfield != 0:
                    break
                bitfield |= bits
            else:
                # only add word if the for loop don't break
                ret[bitfield] = word
    return ret

word_sets = load_words()
all_letters = (1 << 26) - 1
masks = [(1 << i) - 1 for i in range(1, 27)]
word_array = array.array('I', sorted(word_sets.keys(), reverse=True))
array_indexes = [0]
old_bit_length = 26
for i, word in enumerate(word_array):
    if word.bit_length() != old_bit_length:
        array_indexes.append(i)
        old_bit_length = word.bit_length()
by_char = [
    [
        word
        for word in word_sets
        if word & m == word and word & (m + 1 >> 1)
    ]
    for m in masks
]
print(len(by_char[25]))
print(len(word_array[array_indexes[0]: array_indexes[1]]))

def step(to_compute):
    for lefts, words in to_compute:
        for word in by_char[lefts.bit_length() - 1]:
            if word & lefts == word:
                yield lefts & ~word, words + (word,)
def main ():
    queue = step((all_letters ^ 1 << i, ()) for i in range(26))
    queue = step(queue)
    queue = step(queue)
    queue = step(queue)
    queue = step(queue)
    count = 0
    for _ in queue:
        count += 1
    print(count)

if __name__ == '__main__':
    main()