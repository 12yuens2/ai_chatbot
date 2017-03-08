import os
import re
import codecs
from collections import Counter

categories = [x[0] for x in os.walk("categories")][1:]

stop_words = []
with open("stopwords.txt", "r") as s:
    for line in s:
        stop_words.append(line.strip())


def get_dictionary(directory):
    counter_dict = {}

    for subdir in directory:
        subdir_words = []
        for filename in os.listdir(subdir):
            with codecs.open(subdir+"/"+filename, "r", encoding="utf-8", errors="ignore") as f:

                # Strip punctuation
                words = re.sub(r'[^\w\s]', "", f.read().lower()).split()

                # Remove stop words
                words = [word for word in words if word not in stop_words]

                subdir_words.extend(words)

        counter_dict[subdir] = Counter(subdir_words)

    return counter_dict

def get_probabilities(dict, string):

    prob_dict = {}

    # Calculate probability of being in each category
    for category in dict:
        prob = 0.0
        counter = dict[category]

        for word in string.split():
            prob += ((counter[word] + 1) / (sum(counter.values()) + len(string)))

        prob_dict[category] = prob

    return prob_dict

def get_category(dict, string):
    probabilities = get_probabilities(dict, string)
    
    return max(probabilities, key=probabilities.get)
        
# print("Done parsing")


# test = "The batting team attempts to score runs by hitting a ball that is thrown by the pitcher with a bat swung by the batter, then running counter-clockwise around a series of four bases: first, second, third, and home plate. A run is scored when a player advances around the bases and returns to home plate."

# counter_dict = get_dictionary(categories)

# probabilities = get_probabilities(counter_dict, test)

# print(max(probabilities, key=probabilities.get))



# import math
# import re
# from collections import Counter

# cotton = (re.sub(r'[^\w\s]', "", cotton[0]).lower(), cotton[1])
# coffee = (re.sub(r'[^\w\s]', "", coffee[0]).lower(), coffee[1])

# cotton_bag = Counter(cotton[0].split())
# coffee_bag = Counter(coffee[0].split())


# test = "ico coffee is good for consumers"
# test_bag = Counter(test.split())


# prob_cotton_sum = 0.0
# prob_coffee_sum = 0.0

# for word in test.split():
#     prob_cotton_sum += ((cotton_bag[word] + 1) / (sum(cotton_bag.values()) + len(test)))
#     prob_coffee_sum += ((coffee_bag[word] + 1) / (sum(coffee_bag.values()) + len(test)))



# print(word + " - " + "cotton: " + str(prob_cotton_sum) + "  coffee: " + str(prob_coffee_sum))
