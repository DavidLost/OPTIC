import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
import requests

# Download NLTK data files (only the first time)
# nltk.download('stopwords')
nltk.download('punkt')

# from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

DEFAULT_LANG = 'english'
DEFAULT_STOPWORD_SOURCE = 'https://countwordsfree.com/stopwords/{lang}/txt'
MIN_TOKEN_LENGTH = 4

# def get_extended_stopwords(lang=DEFAULT_LANG):
#     """
#     Returns an extended list of stopwords for the specified language.

#     Parameters:
#     lang (str): The language of the stopwords.

#     Returns:
#     set: A set of extended stopwords.
#     """
#     stop_words = set(stopwords.words(lang))

#     # Add more stopwords to the list
#     additional_stopwords = {
#         'german': {'de', 'innen', 'statt', 'stattdessen', 'seid', 'seit', 'wofür', 'warum', 'noch', 'durch'},
#         'english': {'could', 'would', 'should'}
#     }

#     for word in additional_stopwords['german']:
#         if word in stop_words:
#             print(f'{word} is already inside!')
    
#     stop_words.update(additional_stopwords.get(lang, []))
#     return stop_words

def download_stopwords(url=DEFAULT_STOPWORD_SOURCE, lang=DEFAULT_LANG):


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
    # fillwords = get_extended_stopwords(lang)

    
    # Preprocess each set of keywords in the list
    filtered_corpus = []
    print('---TOKENS---')
    for keyword in keywords:
        tokens = word_tokenize(keyword, lang)
        print(f'{keyword}: {tokens}')
        filtered_tokens = [token for token in tokens if len(token) >= MIN_TOKEN_LENGTH and token.lower() not in fillwords] # and word.isalpha()
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