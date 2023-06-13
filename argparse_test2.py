import argparse

def func(v):
    print(type(v))
    return v


parser = argparse.ArgumentParser()
parser.add_argument("--test", action="store_true")
parser.add_argument("--string", type=func)
args = parser.parse_args()

print(args.test)
