import string
import re
def remove_punctuation(your_string):
    for i in your_string:
        if i in string.punctuation:
            your_string = your_string.replace(i,'')
    return your_string
def remove_multiple_spaces(your_string):
    your_string = re.sub(' \s+', ' ', your_string)
    return  your_string