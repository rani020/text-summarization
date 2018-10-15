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

def extractTextFromURL(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    paragraphs = []
    for p in soup.find_all('p'):
        paragraphs.append(p.text)
    return paragraphs

def extractSentences(paragraphs):
    sentences = []
    for paragraph in paragraphs:
        sentences_per_paragraph = sent_tokenize(paragraph)
        for sentence_per_paragraph in sentences_per_paragraph:
            sentences.append(sentence_per_paragraph)
    return sentences

def calculateWordFrequency(sentences):
    words_frequency = {}
    stemmer = nltk.PorterStemmer()
    for sentence in sentences:
        allTokens = word_tokenize(sentence)
        allTokens=[word.lower() for word in allTokens if word.isalpha()]
        tokens = removeStopWords(allTokens)
        for token in tokens:
            stemmedToken = stemmer.stem(token)
            if (stemmedToken in words_frequency):
                words_frequency[stemmedToken] = words_frequency[stemmedToken] + 1
            else:
                words_frequency[stemmedToken] = 1
    return words_frequency

def convertStemmedSentences(sentences):
    processedSentences = []
    stemmer = nltk.PorterStemmer()
    for sentence in sentences:
        allTokens = word_tokenize(sentence)
        allTokens= [word.lower() for word in allTokens if word.isalpha()]
        tokens = removeStopWords(allTokens)
        tokenList = []
        for token in tokens:
            stemmedToken = stemmer.stem(token)
            tokenList.append(stemmedToken)
        processedSentences.append(tokenList)
    return (processedSentences)
        
def removeStopWords(tokens):
    stopWords = set(stopwords.words('english'))
    filteredTokens = []
    for token in tokens: 
        if token not in stopWords:
            filteredTokens.append(token)
    return filteredTokens

def countWeightPerSentence(wordsFrequency, processedSentences):
    score = []
    for sentence in processedSentences:
        scorePerSentence = 0
        for key in wordsFrequency:
            countPerWord = sentence.count(key)
            scorePerSentence = scorePerSentence + wordsFrequency[key]*countPerWord
        score.append(scorePerSentence)
    return score

def mapSentencestoScores(sentences, score):
    sentencesScores = {}
    sentencesScores = dict(zip(sentences, score))
    return sentencesScores

def sortSentences(sentencesScores):
    sortSentences = {}
    for k,v in sorted(sentencesScores.items(),key=lambda p:p[1], reverse=True):
        sortSentences[k] = v
        print(k, v)

def numofSentences(sentences):
    numofSentences = len(sentences) // 3
    return numofSentences

def setup():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-u", "--url", required=False, help="Add the URL to be summarized")
    return parser.parse_args()

def main():
    #args = setup()
    #input_url = args.text
    #paragraphs = extractTextFromURL(input_url)
    sentences = extractSentences(extractTextFromURL("https://en.wikipedia.org/wiki/Java_(programming_language)"))
    score = countWeightPerSentence(calculateWordFrequency(sentences), convertStemmedSentences(sentences))
    sortSentences(mapSentencestoScores(sentences, score))

if __name__ == "__main__":
    sys.exit(main())
