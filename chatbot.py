import random
import re
import os
import json
import string
import metrics

class ChatBot(object):

    MAX_LEV_DISTANCE = 5
    MIN_COS_SIMILARITY = 0.85
    MARKOV_LENGTH = 3

    def __init__(self, training_dir):
        self.response_db = {}
        self.markov_db = {}

        for file in os.listdir(training_dir):
            with open(os.path.join(training_dir, file), "r") as f:
                print(file)
                self.load_dbs(json.load(f))

        # print(self.response_db)
        # print("\n\n")
        # print(self.markov_db)

        self.reflections = {
            "am": "are",
            "i": "you",
            "i'd": "you would",
            "i've": "you have",
            "i'll": "you will",
            "my": "your",
            "are": "am",
            "you've": "I have",
            "you'll": "I will",
            "your": "my",
            "yours": "mine",
            "you": "me",
            "me": "you"
        }

    def load_dbs(self, corpus):
         for conversation in corpus:
            for i in range(1, len(conversation)):
                self.add_to_responses(conversation[i-1], conversation[i])
                self.add_to_markov(conversation[i])


    def create_ngrams(self, words):
        words.append("\n")

        # Don't add as a markov state if not enough words in the line
        if len(words) < self.MARKOV_LENGTH:
            return []

        # Create 3-grams
        ngrams = []
        ngrams.extend(zip(*[words[i:] for i in range(self.MARKOV_LENGTH)])) 

        return ngrams

    def add_to_markov(self, line):
        ngrams = self.create_ngrams(line.split())

        # Add to markov_db in 2:1 ratio
        # i.e. 2-gram key, 1-gram value
        for ngram in ngrams:
            key = tuple(ngram[:-1])

            if key in self.markov_db:
                self.markov_db[key].append(ngram[-1])
            else:
                self.markov_db[key] = [ngram[-1]]



    def add_to_responses(self, line1, line2):
        if not line1 and not line2:
            return

        line1 = line1.lower()

        if line1 in self.response_db:
            self.response_db[line1].append(line2)
        else:
            self.response_db[line1] = [line2]


    def get_response(self, input_string):
        input_string = input_string.lower()

        response = ""

        # First try to find a response from the db
        try:
            response = random.choice(self.response_db[input_string])
            print("[Found response]: ", end="")
            # del self.response_db[input_string]

        # Next try to find inputs that are similar using metrics
        except KeyError:
            possible_reponses = []

            for key in self.response_db.keys():

                # Get cosine similarity and Levenshtein distance 
                cosim = metrics.get_cosim(input_string, key)
                lev = metrics.get_lev(input_string, key)

                # Add to possible responses if the similarity and distance are close
                if cosim > self.MIN_COS_SIMILARITY:
                    possible_reponses.append((cosim, self.response_db[key], key))
                if lev < self.MAX_LEV_DISTANCE:
                    possible_reponses.append((cosim, self.response_db[key], key))

            # Use the best response found which had similar input
            if possible_reponses != []:
                print("[Distance response]: ", end="")
                response = self.best_response(possible_reponses)
            
            # If no close reponses were found, just use markov chains.
            else:
                print("[Markov response]: ", end="")
                response = self.get_markov(input_string)

        return response

    def get_markov(self, input_string):
        key = self.find_keyword(input_string)

        word = ""
        message = []
        while len(message) < 2 or word != "\n":
            try:
                entry = self.markov_db[tuple(key)]
                word = random.choice(entry)

            except KeyError:
                word = random.choice(random.choice(list(self.markov_db.values())))

            message.append(word)
            key.pop(0)
            key.append(word)


        return re.sub("\n", "", " ".join(message))

    # Get keywords from the input string for Markov chain
    def find_keyword(self, input_string):
        words = self.reflect(input_string.split())

        ngrams = self.create_ngrams(words)

        for ngram in ngrams:
            if ngram in self.markov_db.keys():
                return tuple(ngram)
        
        return [random.choice(words)] * 2


    def reflect(self, words):
        reflected = []

        for word in words:
            if word in self.reflections.keys():
                reflected.append(self.reflections[word])
            else:
                reflected.append(word)

        return reflected


    def best_response(self, responses):
        response = random.choice(responses)
        # del self.response_db[response[2]]
        
        return response[1][0]