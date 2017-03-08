from bot import Bot
from chatbot import ChatBot

import metrics

QUIT = ":q"
RELOAD = ":r"


def main():

    eliza = ChatBot(["dialogue/overheard.json", "dialogue/responses.json"], "categories")
    
    print("Enter 'quit' to quit")
    input_string = input("[User input]: ")

    while input_string != QUIT:
        if input_string == RELOAD:
            eliza = ChatBot("responses.json")
            print("Bot reloaded.")
        else:
            response = eliza.get_response(input_string)
            print(response)

        input_string = input("[User input]: ")


# def main():
#     print("Enter ':q' to quit")

#     markov = Bot("markov", "ubuntu.data", 0, 3)


#     input_string = input();

#     while input_string != QUIT:
#         if input_string == RELOAD:
#             markov = Bot("markov", "test.data", 0, 3)
#             print("bot reloaded...")
#         else:
#             response = markov.create_markov(input_string)
#             print(response)

#         input_string = input()






if __name__ == "__main__":
    main() 