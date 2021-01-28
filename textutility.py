import string
import re
import collections
import difflib
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
def compare_string_result(str1, str2):
    output_list = [li for li in difflib.ndiff(str1, str2) if li[0] != ' ']
    res = ''.join(remove_punctuation(str(output_list)))
    return 'the comparing elements are: '+res
def check_date_format(your_string):
    import re
    r = re.compile('.*/.*/.*')
    if r.match(your_string) is not None:
        return your_string
    else: return  'please enter proper format'


