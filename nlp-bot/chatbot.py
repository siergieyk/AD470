#import  libraries
from flask import Flask, render_template, request
import string 
import warnings
import numpy as np
import io
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')
import nltk
from nltk.stem import WordNetLemmatizer

# Download packages
nltk.download('popular', quiet=True)
nltk.download('punkt') 
nltk.download('wordnet')


#Reading in the corpus
with open('nintendo.txt','r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()

#Sentence tokenization
#List of sentences
sent_tokens = nltk.sent_tokenize(raw)

#Convert snetences into list of words
word_tokens = nltk.word_tokenize(raw)


#Part where all the information is being processed
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


#Words are being matched here
GREET_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREET_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

app = Flask(__name__)

def greet(sentence):
    for word in sentence.split():
        if word.lower() in GREET_INPUTS:
            return random.choice(GREET_RESPONSES)
        
        

def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response
    

#Output
flag=True
print("I am MARIO, Nintendo Chatbot.\nI can answer some of the questions about Nintendo Switch.\nIf you want to exit, type Bye!\nHow may I serve you?")
while(flag==True):
    user_response = input()
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            print("MARIO: You are welcome..")
        else:
            if(greet(user_response)!=None):
                print("MARIO: "+greet(user_response))
            else:
                print("MARIO: ",end="")
                print(response(user_response))
                sent_tokens.remove(user_response)
    else:
        flag=False
        print("MARIO: Bye! take care..")




