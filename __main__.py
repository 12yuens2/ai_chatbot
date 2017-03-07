from bot import Bot
from chatbot import ChatBot

QUIT = ":q"
RELOAD = ":r"


def main():
    print("Enter 'quit' to quit")

    eliza = ChatBot("responses.json")

    input_string = input()

    while input_string != QUIT:
        if input_string == RELOAD:
            eliza = ChatBot("responses.json")
            print("Bot reloaded.")
        else:
            response = eliza.get_response(input_string)
            print(response)

        input_string = input()

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