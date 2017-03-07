import re

path = 'data/chernobyl.txt'

word_text = {}
text_words = {}

with open(path, encoding='utf8') as inp:
    text = re.sub(r'\W+', ' ', inp.read().lower().strip()).split()
with open(path.replace('.txt', '.py'), 'w', encoding='utf8') as out:
    out.write("text = [\n")
    for word in text:
        if word not in word_text:
            text_words[len(word_text)] = word
            word_text[word] = len(word_text)
        out.write("    %r, \n" % word_text[word])
    out.write("]\n\nwords = [\n" + ',\n'.join('    %r' % s for s in text_words.values()) + '\n]')
