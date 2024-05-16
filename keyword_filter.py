import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
import requests


# Download NLTK data files (only the first time)
nltk.download('punkt')

from nltk.tokenize import word_tokenize

DEFAULT_LANG = 'english'
DEFAULT_STOPWORD_SOURCE = 'https://countwordsfree.com/stopwords/{lang}/txt'
MIN_TOKEN_LENGTH = 2


def download_stopwords(lang) -> set[str]:
    """
    Alternative for a much smaller stopword list is already provided directly by nltk:
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    set(stopwords.words(lang))
    """
    url = DEFAULT_STOPWORD_SOURCE
    response = requests.get(url.format(lang=lang))
    stopwords = set(response.text.splitlines())
    return stopwords


def extend_stopwords(stopwords, lang):
    additional_stopwords = {
        'english': {'dot'},
        'german': {'innen', 'gerne', 'ausdrücklich', 'wofür'}
    }
    stopwords.update(additional_stopwords.get(lang, []))
    return stopwords

def get_stopwords(lang, extend_with_default_lang=True):
    stopwords = download_stopwords(lang)
    stopwords = extend_stopwords(stopwords, lang)
    
    if extend_with_default_lang and lang != DEFAULT_LANG:
        default_stopwords = download_stopwords(DEFAULT_LANG)
        stopwords.update(default_stopwords)
        stopwords = extend_stopwords(stopwords, DEFAULT_LANG)
    
    return stopwords


def filter_by_relevance(keywords, amount, lang=DEFAULT_LANG):
    """
    Filters out the n most relevant keywords from a list of keywords based on TF-IDF.

    Parameters:
    keywords_list (list): A list of strings where each string is a set of keywords.
    amount (int): The number of most relevant keywords to return.
    stopwords_lang (str): The language of the stopwords.

    Returns:
    list: A list of the n most relevant keywords.
    """
    # Get the stop words for the specified language
    stopwords = get_stopwords(lang)
    
    # Preprocess each set of keywords in the list
    filtered_corpus = []
    # print('---TOKENS---')
    for keyword in keywords:
        tokens = word_tokenize(keyword, lang)
        filtered_tokens = [token for token in tokens if len(token) >= MIN_TOKEN_LENGTH and token.lower() not in stopwords] # and word.isalpha()
        # print(f'{keyword}: {filtered_tokens}')
        filtered_corpus.append(' '.join(filtered_tokens))
    
    # Calculate TF-IDF scores and return the most relevant keywords
    vectorizer = TfidfVectorizer(max_features=amount)
    tfidf_matrix = vectorizer.fit_transform(filtered_corpus)
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray().sum(axis=0)
    
    # Create a list of tuples (word, score) and sort by score
    keyword_scores = list(zip(feature_names, tfidf_scores))
    ranked_keywords = sorted(keyword_scores, key=lambda x: x[1], reverse=True)
    
    # Extract the top keywords and return
    return [keyword for keyword, _ in ranked_keywords[:amount]]