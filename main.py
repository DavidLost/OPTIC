
from dataclasses import dataclass
from web_kw_extr import extract_keywords
from keyword_filter import filter_by_relevance


@dataclass
class CombinationSettings:
    rnd_factor: float
    wordlist_factor: float
    enable_leet: bool
    fill_chars: list


def combinate(amount: int, lengths: range, keywords: list, wordlist: list, settings: CombinationSettings):
    
    pass






keywords = extract_keywords('https://www.gruene-landtag-bw.de/abgeordnete/detail/markus-roesler')
top_keywords = filter_by_relevance(keywords, amount=32, lang='german')
print(top_keywords)