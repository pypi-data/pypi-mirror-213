import sys

from .src.factory import Factory

INVALID_ARGS_AMOUNT = 'Invalid amount of args %s'


def main():
    args = sys.argv

    if len(args) != 5:
        print(INVALID_ARGS_AMOUNT.format(len(args)))
        exit()

    _, from_filepath, to_filepath, format_from, format_to = args

    try:
        source_serializer = Factory.create_serializer(format_to)
        result_serializer = Factory.create_serializer(format_from)
    except Exception as e:
        print(e)
        exit()

    try:
        with open(from_filepath) as from_file, open(to_filepath, 'w') as to_file:
            deserialized_obj = source_serializer.load(from_file)
            result_serializer.dump(deserialized_obj, to_file)
    except Exception as e:
        print(e)
        exit()
