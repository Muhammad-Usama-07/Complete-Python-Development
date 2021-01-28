import string
import re
import collections
def remove_punctuation(your_string):
    for i in your_string:
        if i in string.punctuation:
            your_string = your_string.replace(i,'')
    return your_string
def remove_multiple_spaces(your_string):
    your_string = re.sub(' \s+', ' ', your_string)
    return your_string
def remove_number(your_string):
    result = ''.join(i for i in your_string if(not i.isdigit()))
    return result
def remove_repeating_charcter(your_string):
    res = ''.join(dict.fromkeys(your_string))
    return res
def repeating_words(your_string):
    words = your_string.split()
    word_counts = collections.Counter(words)
    for word, count in sorted(word_counts.items()):
        print('"%s" is repeated %d time%s.' % (word, count, "s" if count > 1 else ""))


