import numpy as np
from dataclasses import dataclass
from osint.web_kw_extr import extract_text_from_url, determine_language
from osint.keyword_filter import filter_by_relevance
import private as private


@dataclass
class CombinationSettings:
    rnd_factor: float
    wordlist_factor: float
    enable_leet: bool
    fill_chars: list


def combinate(amount: int, lengths: range, keywords: list, wordlist: list, settings: CombinationSettings):
    pass

def get_keywords(url, amount=0.5, min_len=3):
    print(f'starting analysis of {url}')
    keywords = {word for word in extract_text_from_url(url).split() if len(word) >= min_len}
    lang = determine_language(url).lower()
    print(f'detected language: {lang}')
    if not keywords: return set()
    total_amount = len(keywords)
    wanted_amount = calc_amount(total_amount, amount)
    print(f'amount: {wanted_amount} / {total_amount}')
    top_keywords = filter_by_relevance(keywords, amount=wanted_amount, lang=lang)
    print(top_keywords, end='\n\n')
    return top_keywords


def calc_amount(total: int, amount=0.6):
    return scaled_function(total, amount)


def scaled_function(total: int, factor: float, curvature=0.5):
    MIN_OUT_AT_MAX_FACTOR = 8
    MAX_OUT_SCALE = 1
    factor = min(max(factor, 0), 1)
    min_value = factor * MIN_OUT_AT_MAX_FACTOR
    x = np.log(total * MAX_OUT_SCALE)
    scaled_value = np.exp(x * (factor ** curvature))
    return round(max(scaled_value, min_value))


# n = 1000
# steps = 10
# for x in range(steps + 1):
#     print(f"scaled_function({n}, {x / steps}) = {calc_amount(n, x / steps)}")

all = set()

for url in private.urls:
    all.update(get_keywords(url))

print('THOSE IS THE FULL POWER OF THE KEYWORDS MUHAHAHAHA:')
print(all)