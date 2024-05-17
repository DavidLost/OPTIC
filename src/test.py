import os, nltk

print(os.environ.get('http_proxy'))
print(os.environ.get('https_proxy'))

nltk.download('punkt')