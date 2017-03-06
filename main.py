import re

path = 'data/chernobyl.txt'

stats = {}

with open(path, encoding='utf8') as f:
    s = f.read()
s = s.lower()

s = re.sub(r'(\s|\n)+', ' ', s).lstrip()
list_of_sentences = [l for l in re.split(r'\. ', s) if l]

with open(path.replace('.txt', '-tuples.py'), 'w', encoding='utf8') as tuples_file:
    tuples_file.write("tuples = (\n")
    with open(path.replace('.txt', '-sentences.txt'), 'w', encoding='utf8') as sentences_file:
        for sentence in list_of_sentences:
            sentences_file.write(sentence + '\n')
            words_in_sentence = [re.sub(r'[,():"?!]', "", w) for w in sentence.split() if w != '-']

            for idx_word in range(1, len(words_in_sentence) - 1):
                tuples_file.write(
                    '    ((%r, %r), %r),\n' % (words_in_sentence[idx_word - 1], words_in_sentence[idx_word + 1], words_in_sentence[idx_word])
                )
            for word in words_in_sentence:
                stats[word] = stats.get(word, 0) + 1
    tuples_file.write(")\n")

with open(path.replace('.txt', '-stats.txt'), 'w', encoding='utf8') as stats_file:
    stats_file.write('<unique words>: %d\n<total words>: %d\n\n' % (len(stats), sum(stats.values())))
    stats_file.write('\n'.join('%s: %s' % t for t in sorted(stats.items(), key=lambda t: (-t[1], t[0]))))
