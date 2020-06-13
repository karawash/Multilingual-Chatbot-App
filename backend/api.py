
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import pandas as pd
import json
import random
from keras.models import load_model
from flask import Flask, request
from flask_restful import Resource, Api
from flask.json import jsonify
from flask_cors import CORS
from flasgger import Swagger


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)

Swagger(app)

@app.route('/api/chatbot', methods=['POST'])
def index(demand='مرحبا'):
    """
    Arabic Chatbot API Natural Processing Understanding (NLU)
    ---
    tags:
      - Chat in Arabic
    parameters:
      - name: body
        in: body
        schema:
          id: demand
          required:
            - demand
          properties:
             demand:
                type: string
                description: try an arabic string as demand to chatbot like ما الذي يمكنك فعله ؟ مرحبا, كيف حالك, ما المساعدة التي تقدمها ؟, ...
                default: 'مرحبا'
    responses:
      200:
        description: The required result is available
      500:
        description: Error!
    """
    jsonObj = request.get_json()
    demand = jsonObj.get('demand')
    resp= chatbot_response(demand)
    x='{ "response":"'+resp+'"}'
    print(x)
    return x

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_word(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    p = bag_of_word(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    print(msg)
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


if __name__ == '__main__':
    model = load_model('chatbot_model_ar.h5')
    intents = pd.read_json('intents_ar.json')
    words = pickle.load(open('words_ar.pkl','rb'))
    classes = pickle.load(open('classes_ar.pkl','rb'))
    app.run(threaded=False, port=5002, host='0.0.0.0')
