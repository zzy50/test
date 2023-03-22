import argparse


def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--cache', type=str, nargs='?', const='ram', help='--cache images in "ram" (default) or "disk"')
    parser.add_argument('--range', default=None, nargs="+")

    opt = parser.parse_known_args()[0] if known else parser.parse_args(["--cache", "ram", "--range", "0.mp4", "1.mp4"])
    return opt

def check_range_num(_range):
    arg_num = len(_range)
    if arg_num>2 or arg_num==1:
        return None
    else:
        return _range


if __name__ == "__main__":
    a = parse_opt()
    a.range = check_range_num(a.range)
    print(a.range)
    # print(a.cache)
