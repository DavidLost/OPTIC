import numpy as np
from math import sqrt
from dataclasses import dataclass
from web_kw_extr import extract_text_from_url, determine_language
from keyword_filter import filter_by_relevance


@dataclass
class CombinationSettings:
    rnd_factor: float
    wordlist_factor: float
    enable_leet: bool
    fill_chars: list


def combinate(amount: int, lengths: range, keywords: list, wordlist: list, settings: CombinationSettings):
    pass

def get_keywords(url, amount=0.1, min_len=3):
    print(f'starting analysis of {url}')
    keywords = {word for word in extract_text_from_url(url).split() if len(word) >= min_len}
    lang = determine_language(url).lower()
    print(f'detected language: {lang}')
    if not keywords: return set()
    total_amount = len(keywords)
    wanted_amount = calc_amount(total_amount, amount)
    print(f'amount: {wanted_amount} / {total_amount}')
    top_keywords = filter_by_relevance(keywords, amount=wanted_amount, lang='german')
    print(top_keywords, end='\n\n')
    return top_keywords


def calc_amount(total: int, factor: float):
    MIN_OUT_FULL = 8
    MAX_OUT_FACTOR = 1
    factor = min(max(factor, 0), 1)
    min_value = factor * MIN_OUT_FULL
    b = np.log(total * MAX_OUT_FACTOR)
    scaled_value = np.exp(b * factor)
    return round(max(scaled_value, min_value))

    
urls = [
    'https://markusroesler.de/ueber-mich',
    'https://www.gruene-landtag-bw.de/abgeordnete/detail/markus-roesler',
    'https://www.landtag-bw.de/home/der-landtag/abgeordnete/abgeordnetenprofile/die-grunen/r%C3%B6sler.html'
]


# n = 1000
# steps = 10
# for x in range(steps + 1):
#     print(f"scaled_function({n}, {x / steps}) = {calc_amount(n, x / steps)}")


all = set()

for url in urls:
    all.update(get_keywords(url))

print('THOSE IS THE FULL POWER OF THE KEYWORDS MUHAHAHAHA:')
print(all)