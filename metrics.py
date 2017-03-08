import math


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