from functools import cache
from collections import Counter
import argparse

parser = argparse.ArgumentParser()
group = parser.add_argument_group()
group.add_argument("-s", "--string", type=str)
group.add_argument("-f", "--file", type=str)

args = parser.parse_args()


@cache
def count_solo(string):
    if not isinstance(string, str):
        raise TypeError

    count_all = Counter(string)
    return sum(i for i in count_all.values() if i == 1)


def read_file(path):
    if path is None:
        print("Не правильно введена команда: -f, або -s")
        return
    try:
        with open(path, 'r') as file:
            for line in file.readlines():
                print(count_solo(line.strip()))
    except FileNotFoundError:
        print(f'{path} - шлях не знайдено')


def main(args):
    if args.file:
        read_file(args.file)
    elif args.string:
        print(count_solo(args.string))
    else:
        read_file(args.file)


if __name__ == '__main__':
    main(args)


