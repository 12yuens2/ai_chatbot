import random
import json
import re

class Bot(object):

    def __init__(self, name, file, ngram_length, markov_order):
        self.name = name
        self.order = markov_order
        self.last_response = ""

        #load templates for eliza rules
        # with open("templates.json") as templates:
        #     self.templates = json.load(templates)

        self.words = []
        self.db = {}

        with open(file, "r") as training_file:
            for line in training_file:
                self.words.extend(line.split())

        self.populate_db(self.words, markov_order)

    def create_ngrams(self, words, n):

        if len(words) < n:
            return

        return zip(*[words[i:] for i in range(n)])


    def populate_db(self, words, n):
        ngrams = self.create_ngrams(words, n)

        for ngram in ngrams:
            key = tuple(ngram[:-1])

            if key in self.db:
                self.db[key].append(ngram[-1])
            else:
                self.db[key] = [ngram[-1]]



    def create_markov(self, user_input, length=10):
        # self.populate_db(user_input, self.order-1)

        key = user_input.split()[:self.order-1]

        message = []
        for i in range(length):
            try:
                word = random.choice(self.db[tuple(key)])
            except KeyError:
                word = random.choice(random.choice(list(self.db.values())))

            message.append(word)
            key.pop(0)
            key.append(word)

        return ' '.join(message)






    def get_response(self, input_sentence):
        responses = []

        for template in self.templates:
            match = re.match(template["regex"], input_sentence)

            if match:
                rules = [re.sub("@TOKEN@", match.group(template["pos"]), rule) for rule in template["rules"]]
                responses.extend(rules)
                break


        if self.last_response in responses:
            responses.remove(self.last_response)

        response = random.choice(responses)
        self.last_response = response;
        return response

