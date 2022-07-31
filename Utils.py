import json
import re
from nltk.tokenize import word_tokenize
from nltk import pos_tag


def write_json(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f)


def read_json(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    if data == '':
        return {}
    else:
        return json.loads(data)


def is_alphabet_present(text):
    if re.findall(r'[a-z|A-Z]', text):
        return True
    else:
        return False


def get_word_count(text):
    words = word_tokenize(text)

    # keep token if text present
    words = [w for w in words if is_alphabet_present(w)]
    return len(words)


def get_pos_set(text):
    pos_tags = pos_tag(word_tokenize(text))
    pos_tags = set([p[1] for p in pos_tags])
    return pos_tags


def get_full_stop_counts(text):
    return len(re.findall(r'\.', text))


def get_text_paragraphs(text):
    paragraphs = re.split(r'\n+', text, maxsplit=0, flags=0)
    paragraphs = [p.strip() for p in paragraphs if p.strip() != '']
    return paragraphs
