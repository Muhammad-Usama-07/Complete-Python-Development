import string
import re
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
def bold_string(your_string):
    bolded_string = "\033[1m" + your_string + "\033[0m"
    return bolded_string
