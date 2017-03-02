import random
import json
import re

class Bot(object):


    def __init__(self, name):
        self.name = name
        self.last_response = ""

        #load templates for eliza rules
        with open("templates.json") as templates:
            self.templates = json.load(templates)


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

