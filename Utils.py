import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from transformers import AutoTokenizer
from nltk.stem import PorterStemmer
from transformers import pipeline


def preprocessing(reviews):
    for text in reviews:
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('punkt_tab')

        # Tokenization
        # tokens = sent_tokenize(text)
        tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        tokens = tokenizer.tokenize(text)

        # Removing stopwords and stemming
        stop_words = set(stopwords.words('english'))
        stemmer = PorterStemmer()
        cleaned_tokens = [stemmer.stem(
            word.lower()) for word in tokens if word.lower() not in stop_words]
        cleaned_text = " ".join(cleaned_tokens)
        text = cleaned_text
    return reviews
