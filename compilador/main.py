import sys

if __name__ == "__main__":

    args = []
    for i in range(1, len(sys.argv)):
        args.append(sys.argv[i])

    print(args)
