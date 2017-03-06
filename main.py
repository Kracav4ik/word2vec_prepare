import re

path = 'data/chernobyl.txt'

stats = {}
ctx2id = {}
id2ctx = {}
word2id = {}
id2word = {}
words_ctxs = []
ctx_words = []

ctx_idx = 2*10**9
word_idx = 10**9

with open(path, encoding='utf8') as f:
    s = f.read()
s = s.lower()

s = re.sub(r'(\s|\n)+', ' ', s).lstrip()
list_of_sentences = [l for l in re.split(r'\. ', s) if l]

for sentence in list_of_sentences:
    words_in_sentence = [re.sub(r'^[("]*(.*?)[,):"?!]*$', r'\1', w) for w in sentence.split() if w != '-']

    for idx_word in range(1, len(words_in_sentence) - 1):
        words_ctxs.append((words_in_sentence[idx_word], words_in_sentence[idx_word - 1]))
        words_ctxs.append((words_in_sentence[idx_word], words_in_sentence[idx_word + 1]))
        ctx_words.append(
            ((words_in_sentence[idx_word - 1], words_in_sentence[idx_word + 1]), words_in_sentence[idx_word]))

    for word in words_in_sentence:
        stats[word] = stats.get(word, 0) + 1


with open(path.replace('.txt', '-sentences.txt'), 'w', encoding='utf8') as sentences_file:
    for sentence in list_of_sentences:
        sentences_file.write(sentence + '\n')

with open(path.replace('.txt', '-tuples.py'), 'w', encoding='utf8') as tuples_file:
    tuples_file.write("ctx_words = (\n")
    for word in ctx_words:
        tuples_file.write("    (%r, %r),\n" % word)
        for i in range(2):
            if not ctx2id.get(word[0][i], 0):
                ctx2id[word[0][i]] = ctx_idx
                id2ctx[ctx_idx] = word[0][i]
                ctx_idx += 1
        if not word2id.get(word[1], 0):
            word2id[word[1]] = word_idx
            id2word[word_idx] = word[1]
            word_idx += 1
    tuples_file.write(")\n\n")

    tuples_file.write("words_ctxs = (\n")
    for word in words_ctxs:
        tuples_file.write("    (%r, %r),\n" % word)
    tuples_file.write(")\n\n")

    tuples_file.write("ctx2id = {\n")
    tuples_file.write(''.join('    %r: %s,\n' % t for t in sorted(ctx2id.items(), key=lambda t: t[1])))
    tuples_file.write("}\n\n")

    tuples_file.write("id2ctx = {\n")
    tuples_file.write(''.join('    %s: %r,\n' % t for t in sorted(id2ctx.items(), key=lambda t: t[0])))
    tuples_file.write("}\n\n")

    tuples_file.write("word2id = {\n")
    tuples_file.write(''.join('    %r: %s,\n' % t for t in sorted(word2id.items(), key=lambda t: t[1])))
    tuples_file.write("}\n\n")

    tuples_file.write("id2word = {\n")
    tuples_file.write(''.join('    %s: %r,\n' % t for t in sorted(id2word.items(), key=lambda t: t[0])))
    tuples_file.write("}\n")

with open(path.replace('.txt', '-stats.txt'), 'w', encoding='utf8') as stats_file:
    stats_file.write('<unique words>: %d\n<total words>: %d\n\n' % (len(stats), sum(stats.values())))
    stats_file.write('\n'.join('%s: %s' % t for t in sorted(stats.items(), key=lambda t: (-t[1], t[0]))))
