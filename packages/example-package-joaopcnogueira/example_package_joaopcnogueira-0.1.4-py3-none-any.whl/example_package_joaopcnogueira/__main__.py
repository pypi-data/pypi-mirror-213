import argparse

def main(args):
    if args.add_one:
        print(args.add_one + 1)
    elif args.add_two:
        print(args.add_two + 2)
    elif args.add_three:
        print(args.add_three + 3)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--add-one", type=int, help="Add one to a number")
    parser.add_argument("--add-two", type=int, help="Add one to a number")
    parser.add_argument("--add-three", type=int, help="Add one to a number")
    args = parser.parse_args()
    main(args)
