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


word_map = load_words()
all_letters = (1 << 26) - 1
by_char = [
    [
        word
        for word in word_map
        if word & m == word and word & (m + 1 >> 1)
    ]
    for m in ((1 << i) - 1 for i in range(1, 27))
]


def step(to_compute):
    for lefts, words in to_compute:
        for word in by_char[lefts.bit_length() - 1]:
            if word & lefts == word:
                yield lefts & ~word, words + (word,)


def main():
    queue = step((all_letters ^ 1 << i, ()) for i in range(26))
    queue = step(queue)
    queue = step(queue)
    queue = step(queue)
    queue = step(queue)
    count = 0
    for _, words in queue:
        print(*(word_map[w] for w in words))
        count += 1
    print(count)


if __name__ == '__main__':
    main()
