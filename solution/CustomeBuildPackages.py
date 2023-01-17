import string
import re
import collections
import difflib

# this function will remove punctuation from sentance.
def remove_punctuation(your_string):
    for i in your_string:
        if i in string.punctuation:
            your_string = your_string.replace(i,'')
    return your_string

# this function will remove uncessory spaces from sentance.
def remove_multiple_spaces(your_string):
    your_string = re.sub(' \s+', ' ', your_string)
    return your_string

# this function will remove numbers from sentance.
def remove_number(your_string):
    result = ''.join(i for i in your_string if(not i.isdigit()))
    return result

# this function will remove repeating character from sentance.
def remove_repeating_charcter(your_string):
    res = ''.join(dict.fromkeys(your_string))
    return res

# this function will print repeating words from sentance.
def repeating_words(your_string):
    words = your_string.split()
    word_counts = collections.Counter(words)
    for word, count in sorted(word_counts.items()):
        print('"%s" is repeated %d time%s.' % (word, count, "s" if count > 1 else ""))

# this function will print difference character from sentance.
def compare_string_result(str1, str2):
    output_list = [li for li in difflib.ndiff(str1, str2) if li[0] != ' ']
    res = ''.join(remove_punctuation(str(output_list)))
    return 'the comparing elements are: '+ res

# this function will check date format from string.
def check_date_format(your_string):
    import re
    r = re.compile('.*/.*/.*')
    if r.match(your_string) is not None:
        return your_string
    else: return  'please enter proper format'

# this function will count number of words from sentance.
def number_of_words(your_string):
    return len(your_string.split())

# this function will swap two character of two different strings.
def swap_first_two_character_inString(a, b):
  str1 = a[0:2]
  str2 = b[0:2]
  a = a.replace(str1,str2)
  b = b.replace(str2,str1)
  return a + " " + b

# this function will replace sentance with other word from sentance.
def replace_sentance(sentance, start, end, word_to_replace):
    start_word = sentance.find(start)
    end_word = sentance.find(end)
    if (sentance[start_word:end_word + 3]):
        sentance = sentance.replace(sentance[start_word:end_word + 3], word_to_replace)
        return sentance
    else:
        return sentance
