from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from gensim import models, corpora
from nltk.corpus import stopwords
from nltk import ne_chunk
import spacy
import nltk

class PyTextProMax:
    import os
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)

    try:
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        nltk.download('vader_lexicon', quiet=True)
    
    try:
        nltk.data.find('corpora/stopwords.zip')
    except LookupError:
        nltk.download('stopwords', quiet=True)
    
    try:
        nltk.data.find('corpora/words.zip')
    except LookupError:
        nltk.download('words', quiet=True)
    
    try:
        nltk.data.find('taggers/averaged_perceptron_tagger.zip')
    except LookupError:
        nltk.download('averaged_perceptron_tagger', quiet=True)
    
    try:
        nltk.data.find('chunkers/maxent_ne_chunker')
    except LookupError:
        nltk.download('maxent_ne_chunker', quiet=True)

    def __init__(self):
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))
        try:
            spacy.load('en_core_web_sm')
        except:
            os.system("python -m spacy download en_core_web_sm > nul")
        
        self.nlp = spacy.load('en_core_web_sm')

    def get_emotion(self, text):
        emotion_scores = self.sentiment_analyzer.polarity_scores(text)
        if emotion_scores['compound'] >= 0.5:
            return 'Positive'
        elif emotion_scores['compound'] <= -0.5:
            return 'Negative'
        else:
            return 'Neutral \\ Unrecognized'

    def extract_keywords(self, text):
        word_tokens = word_tokenize(text.lower())
        keywords = [w for w in word_tokens if w.isalpha() and w not in self.stop_words]
        if len(keywords) == 0:
            return "None were found"
        return keywords

    def get_entities(self, text):
        doc = self.nlp(text)
        entities = [ent.text for ent in doc.ents if ent.label_ != '']
        if len(entities) == 0:
            return "None were found"
        return entities


if __name__ == '__main__':
    text = "The Apple Inc. is planning on opening a new store in San Francisco. The CEO (Tim Cook) will be attending the opening ceremony along with some other executives. I find this really fascinating!"
    PyTextProMax = PyTextProMax()
    emotion = PyTextProMax.get_emotion(text)
    listofkeywords = PyTextProMax.extract_keywords(text)
    listofentities = PyTextProMax.get_entities(text)

    keywords = ''
    for index, keyword in enumerate(listofkeywords):
        if index == len(listofkeywords) - 1:
            keywords += f' and \'{keyword}\''
        elif index == len(listofkeywords) - 2:
            keywords += f'\'{keyword}\''
        else:
            keywords += f'\'{keyword}\', '
    
    entities = ''
    for index, entity in enumerate(listofentities):
        if index == len(listofentities) - 1:
            entities += f' and \'{entity}\''
        elif index == len(listofentities) - 2:
            entities += f'\'{entity}\''
        else:
            entities += f'\'{entity}\', '

    print(f'\nBase sentence: \'{text}\'')
    print(f' Emotion: {emotion}.')
    print(f'  Keywords: {keywords}.')
    print(f'   Entities: {entities}.')