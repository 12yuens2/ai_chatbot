import os

i = 0
with open("corpus.data", "w") as corpus:
    for fname in os.listdir(os.getcwd()):
        with open(fname, "rw") as filename:
            for line in filename:
                writeline = ' '.join(line.split()[3:])
                corpus.write(writeline + "\n")

        i = i + 1

        if i == 50:
            break
