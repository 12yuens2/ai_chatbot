import random
import re
import math
import json
import string

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
                cosim = get_cosim(input_string, key)
                lev = get_lev(input_string, key)

                if cosim > self.MIN_COS_SIMILARITY:
                    possible_reponses.append((cosim, self.response_db[key], key))
                if lev < self.MAX_LEV_DISTANCE:
                    possible_reponses.append((cosim, self.response_db[key], key))

            if possible_reponses != []:
                response = self.best_response(possible_reponses)
            else:
                response = self.get_markov()

        return response

    def get_markov(self):
        return "I don't know..."

    def best_response(self, responses):
        response = max(responses)
        del self.response_db[response[2]]
        
        return response[1][0]


def get_jaccard(string1, string2):
    s1 = set(string1.split())
    s2 = set(string2.split())

    n = len(s1.intersection(s2))
    return n / float(len(s1) + len(s2) - n)


# Algorithm for calculating the Levenshtein distance between two strings.
# Written following the algorithm from "Iterative with two matrix rows" from https://en.wikipedia.org/wiki/Levenshtein_distance
def get_lev(s, t):
    if s == t: return 0
    if len(s) == 0: return len(t)
    if len(t) == 0: return len(s)

    v0 = [0] * (len(t)+1)
    v1 = [0] * (len(t)+1)

    for i in range(len(v0)):
        v0[i] = i    

    for i in range(len(s)):
        v1[0] = i + 1

        for j in range(len(t)):
            cost = 0 if (s[i] == t[j]) else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)

        for j in range(len(v0)):
            v0[j] = v1[j]

    return v1[len(t)]


# Returns the cosine similarity of two strings
def get_cosim(string1, string2):
    v1, v2 = create_vectors(string1, string2)

    dot_product = sum([v1[x] * v2[x] for x in range(len(v1))])

    mv1 = get_magnitude(v1)
    mv2 = get_magnitude(v2)

    try:
        cosim = float(dot_product) / (mv1 * mv2)
    except ZeroDivisionError:
        cosim =  0
    return cosim


def get_magnitude(vector):
    return math.sqrt(sum([vector[x] ** 2 for x in range(len(vector))]))

def create_vectors(string1, string2):
    ws1 = string1.split()
    ws2 = string2.split()

    words = list(set(ws1))
    words.extend(w for w in ws2 if w not in words)

    w1_freq = []
    w2_freq = []
    for word in words:
        w1_freq.append(string1.count(word))
        w2_freq.append(string2.count(word))

    return (w1_freq, w2_freq)