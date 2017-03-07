import random
import re
import json
import string
import metrics

class ChatBot(object):

    MAX_LEV_DISTANCE = 5
    MIN_COS_SIMILARITY = 0.6
    MARKOV_LENGTH = 3

    def __init__(self, file):
        self.response_db = {}
        self.markov_db = {}

        with open(file, "r") as f:
            self.load_dbs(json.load(f))

        print(self.response_db)
        print("\n\n")
        print(self.markov_db)

        # with open(file, "r") as f:
        #     line1 = f.readline().rstrip("\n")
        #     line2 = f.readline().rstrip("\n")

        #     while line1 and line2:
        #         self.add_to_db(line1, line2)

        #         line1 = line2
        #         line2 = f.readline().rstrip("\n")


    def load_dbs(self, corpus):
         for conversation in corpus:
            for i in range(1, len(conversation)):
                self.add_to_responses(conversation[i-1], conversation[i])
                self.add_to_markov(conversation[i])


    def add_to_markov(self, line):
        words = line.split()
        if len(words) < self.MARKOV_LENGTH:
            return

        #create tri-grams from line


        ngrams = []
        ngrams.extend(zip(*[words[i:] for i in range(self.MARKOV_LENGTH)]))

        print(ngrams)
        print("\n\n")

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
        response = ""

        try:
            response = random.choice(self.response_db[input_string])
            del self.response_db[input_string]

        except KeyError:
            possible_reponses = []

            for key in self.response_db.keys():
                cosim = metrics.get_cosim(input_string, key)
                lev = metrics.get_lev(input_string, key)

                if cosim > self.MIN_COS_SIMILARITY:
                    possible_reponses.append((cosim, self.response_db[key], key))
                if lev < self.MAX_LEV_DISTANCE:
                    possible_reponses.append((cosim, self.response_db[key], key))

            if possible_reponses != []:
                response = self.best_response(possible_reponses)
            else:
                response = self.get_markov(input_string)

        return response

    def get_markov(self, input_string):
        return "I don't know..."

    def best_response(self, responses):
        response = max(responses)
        del self.response_db[response[2]]
        
        return response[1][0]