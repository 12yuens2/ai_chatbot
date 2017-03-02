from bot import Bot

QUIT = ":q"
RELOAD = ":r"


def main():
    print "Enter 'quit' to quit"

    eliza = Bot("Eliza")

    input_string = raw_input()

    while input_string != QUIT:
        if input_string == RELOAD:
            eliza = Bot("Eliza")
            print "Bot reloaded."
        else:
            response = eliza.get_response(input_string)
            print response

        input_string = raw_input()




if __name__ == "__main__":
    main() 