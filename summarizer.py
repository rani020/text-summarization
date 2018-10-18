import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
nltk.download('stopwords')
set(stopwords.words('english'))
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import urllib.request as urlreq
from bs4 import BeautifulSoup
import requests
import operator
import sys
import argparse
from collections import defaultdict

def extract_text_from_URL(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    paragraphs = []
    for p in soup.find_all('p'):
        paragraphs.append(p.text)
    return paragraphs

def extract_sentences(paragraphs):
    sentences = []
    for paragraph in paragraphs:
        sentences_per_paragraph = sent_tokenize(paragraph)
        for sentence_per_paragraph in sentences_per_paragraph:
            sentences.append(sentence_per_paragraph)
    print(sentences)
    return sentences

def calculate_word_frequency(sentences):
    words_frequency = defaultdict(int)
    stemmer = nltk.PorterStemmer()
    for sentence in sentences:
        all_tokens = word_tokenize(sentence)
        all_tokens =[word.lower() for word in all_tokens if word.isalpha()]
        tokens = remove_stop_words(all_tokens)
        for token in tokens:
            stemmed_token = stemmer.stem(token)
            words_frequency[stemmed_token] += 1
    return words_frequency

def convert_stemmed_sentences(sentences):
    processed_sentences = []
    tokenList = []
    stemmer = nltk.PorterStemmer()
    for sentence in sentences:
        all_tokens = word_tokenize(sentence)
        all_tokens= [word.lower() for word in all_tokens if word.isalpha()]
        tokens = remove_stop_words(all_tokens)
        tokenList = [stemmer.stem(t) for t in tokens]
        processed_sentences.append(tokenList)
    return (processed_sentences)
        
def remove_stop_words(tokens):
    stop_words = set(stopwords.words('english'))
    filteredTokens = [t for t in tokens if t not in stop_words]
    return filteredTokens

def count_weight_per_sentence(words_frequency, processedSentences):
    score = []
    for sentence in processedSentences:
        score_per_sentence = 0
        for key in words_frequency:
            count_per_word = sentence.count(key)
            score_per_sentence = score_per_sentence + words_frequency[key]*count_per_word
        score.append(score_per_sentence)
    return score

def map_sentences_to_scores(sentences, score):
    sentences_scores = {}
    sentences_scores = dict(zip(sentences, score))
    return sentences_scores

def sort_sentences(sentencesScores):
    sortSentences = {}
    for k,v in sorted(sentencesScores.items(),key=lambda p:p[1], reverse=True):
        sortSentences[k] = v
        print(k, v)

def numof_sentences(sentences):
    numofSentences = len(sentences) // 3
    return numofSentences

def setup():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-u", "--url", required=False, help="Add the URL to be summarized")
    return parser.parse_args()

def main():
    #args = setup()
    #input_url = args.text
    #paragraphs = extract_text_from_URL(input_url)
    #sentences = ["My name is Anna", "My dog is Oscar", "Her name is Sofia", "She makes good carbonara - making"]
    sentences = extract_sentences(extract_text_from_URL("https://en.wikipedia.org/wiki/Java_(programming_language)"))
    score = count_weight_per_sentence(calculate_word_frequency(sentences), convert_stemmed_sentences(sentences))
    sort_sentences(map_sentences_to_scores(sentences, score))

if __name__ == "__main__":
    sys.exit(main())
