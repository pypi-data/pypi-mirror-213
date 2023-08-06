def DChat(input):
    try:
        import nltk
        #nltk.download('punkt')
        #nltk.download('wordnet')
        import json
        import random
        import requests
        import pickle
        import numpy as np
        from nltk.stem import WordNetLemmatizer
        from tensorflow.keras.models import load_model
        from NikChat.results import ctime, weather, internet
        lemmatizer = WordNetLemmatizer()
        x = requests.get('https://api.jsonbin.io/v3/b/64698dac8e4aa6225ea0fcce')
        intents = json.loads(x.text)
        words = pickle.load(open('words.pkl', 'rb'))
        classes = pickle.load(open('classes.pkl', 'rb'))
        json.dumps(intents, "training.json")
        model = load_model('Speechbot.h5')
        def clean_up_sentence(sentence):
            sentence_words = nltk.word_tokenize(sentence)
            sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
            return sentence_words
        def bag_of_words(sentence):
            sentence_words = clean_up_sentence(sentence)
            bag = [0] * len(words)
            for w in sentence_words:
                for i, word in enumerate(words):
                    if word == w:
                        bag[i] = 1
            return np.array(bag)
        def predict_class(sentence):
            bow = bag_of_words(sentence)
            res = model.predict(np.array([bow]))[0]
            ERROR_TRESHOLD = 0.25
            results = [[i, r] for i, r in enumerate(res) if r > ERROR_TRESHOLD]
            results.sort(key=lambda x: x[1], reverse=True)
            return_list = []
            for r in results:
                return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
            return return_list
        def get_response(intents_list, intents_json):
            tag = intents_list[0]['intent']
            list_of_intents = intents_json['intents']
            for i in list_of_intents:
                if i['tag'] == tag:
                    result = random.choice(i['responses'])
                    break
            return result
        print('THE BOT IS RUNNING')
        message = input
        ints = predict_class(message)
        res = get_response(ints, intents['record'])
        str1 = ''
        for elm in message.split(' '):
            str1 += elm.lower() + " "
        print(str1.split(' '))
        if "weather" in str1.split(' ') or "temperature" in str1.split(' ') or "forecast" in str1.split(' '):
            res = weather()
        elif "day" in str1.split(' ') or "time" in str1.split(' ') or "date" in str1.split(' '):
            res = ctime()
        elif res == "bob is your dad":
            res = internet(str1)
        else:
            res = res
        return res
    except Exception as e:
        from os.path import exists
        if exists('words.pkl') == False:
            return 'Remember to use nikchat.init() before you use nikchat.NChat()'
        else:
            return e, " If your OS doesn't support automated downloads, please install the following libraries: nltk, numpy, tensorflow, wikipedia, bs4, geopy, geocoder"
        
def train():
    import NikChat.training as traning
    traning.init2()

def init(filePath):
    from os.path import exists
    if exists('words.pkl') == False:
        import NikChat.training as traning
        traning.init(filePath)
        return 'done'
    else:
        return 'done'

def NChat(filePath):
    try:
        import nltk
        #nltk.download('punkt')
        #nltk.download('wordnet')
        import json
        import random
        import requests
        import pickle
        import numpy as np
        from nltk.stem import WordNetLemmatizer
        from tensorflow.keras.models import load_model
        from NikChat.results import ctime, weather, internet
        lemmatizer = WordNetLemmatizer()
        intents = json.loads(filePath)
        words = pickle.load(open('words.pkl', 'rb'))
        classes = pickle.load(open('classes.pkl', 'rb'))
        json.dumps(intents, "training.json")
        model = load_model('Speechbot.h5')
        def clean_up_sentence(sentence):
            sentence_words = nltk.word_tokenize(sentence)
            sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
            return sentence_words
        def bag_of_words(sentence):
            sentence_words = clean_up_sentence(sentence)
            bag = [0] * len(words)
            for w in sentence_words:
                for i, word in enumerate(words):
                    if word == w:
                        bag[i] = 1
            return np.array(bag)
        def predict_class(sentence):
            bow = bag_of_words(sentence)
            res = model.predict(np.array([bow]))[0]
            ERROR_TRESHOLD = 0.25
            results = [[i, r] for i, r in enumerate(res) if r > ERROR_TRESHOLD]
            results.sort(key=lambda x: x[1], reverse=True)
            return_list = []
            for r in results:
                return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
            return return_list
        def get_response(intents_list, intents_json):
            tag = intents_list[0]['intent']
            list_of_intents = intents_json['intents']
            for i in list_of_intents:
                if i['tag'] == tag:
                    result = random.choice(i['responses'])
                    break
            return result
        print('THE BOT IS RUNNING')
        message = input
        ints = predict_class(message)
        res = get_response(ints, intents['record'])
        str1 = ''
        for elm in message.split(' '):
            str1 += elm.lower() + " "
        print(str1.split(' '))
        if "weather" in str1.split(' ') or "temperature" in str1.split(' ') or "forecast" in str1.split(' '):
            res = weather()
        elif "day" in str1.split(' ') or "time" in str1.split(' ') or "date" in str1.split(' '):
            res = ctime()
        elif res == "bob is your dad":
            res = internet(str1)
        else:
            res = res
        return res
    except Exception as e:
        from os.path import exists
        if exists('words.pkl') == False:
            return 'Remember to use nikchat.init() before you use nikchat.NChat()'
        else:
            return e, " If your OS doesn't support automated downloads, please install the following libraries: nltk, numpy, tensorflow, wikipedia, bs4, geopy, geocoder"