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
    return sentences

def calculate_word_frequency(sentences):
    words_frequency = {}
    stemmer = nltk.PorterStemmer()
    for sentence in sentences:
        allTokens = word_tokenize(sentence)
        allTokens=[word.lower() for word in allTokens if word.isalpha()]
        tokens = remove_stop_words(allTokens)
        for token in tokens:
            stemmedToken = stemmer.stem(token)
            if (stemmedToken in words_frequency):
                words_frequency[stemmedToken] = words_frequency[stemmedToken] + 1
            else:
                words_frequency[stemmedToken] = 1
    return words_frequency

def convert_stemmed_sentences(sentences):
    processedSentences = []
    stemmer = nltk.PorterStemmer()
    for sentence in sentences:
        allTokens = word_tokenize(sentence)
        allTokens= [word.lower() for word in allTokens if word.isalpha()]
        tokens = remove_stop_words(allTokens)
        #tokenList = [stemmer.stem(t) for t in tokens]

        for token in tokens:
            stemmedToken = stemmer.stem(token)
            tokenList = []
            tokenList.append(stemmedToken)
        processedSentences.append(tokenList)
        print(processedSentences)
    return (processedSentences)
        
def remove_stop_words(tokens):
    stopWords = set(stopwords.words('english'))
    filteredTokens = []
    for token in tokens: 
        if token not in stopWords:
            filteredTokens.append(token)
    return filteredTokens

def count_weight_per_sentence(wordsFrequency, processedSentences):
    score = []
    for sentence in processedSentences:
        scorePerSentence = 0
        for key in wordsFrequency:
            countPerWord = sentence.count(key)
            scorePerSentence = scorePerSentence + wordsFrequency[key]*countPerWord
        score.append(scorePerSentence)
    return score

def map_sentences_to_scores(sentences, score):
    sentencesScores = {}
    sentencesScores = dict(zip(sentences, score))
    return sentencesScores

def sort_sentences(sentencesScores):
    sortSentences = {}
    for k,v in sorted(sentencesScores.items(),key=lambda p:p[1], reverse=True):
        sortSentences[k] = v
        #print(k, v)

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
    sentences = ["My name is Anna", "My dog is Oscar", "Her name is Sofia", "She makes good carbonara - making"]
    #sentences = extract_sentences(extract_text_from_URL("https://en.wikipedia.org/wiki/Java_(programming_language)"))
    score = count_weight_per_sentence(calculate_word_frequency(sentences), convert_stemmed_sentences(sentences))
    sort_sentences(map_sentences_to_scores(sentences, score))

if __name__ == "__main__":
    sys.exit(main())
