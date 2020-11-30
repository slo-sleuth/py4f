import argparse
import re

# regex to find ASCII and big or little endian English UTF-16
endian = {
    'b': b'(?:\x00?[\t\x20-\x7e]){%d,}',
    'l': b'(?:[\t\x20-\x7e]\x00?){%d,}'
}

def get_strings(obj, regex, min=4):
    """Extract ascii and unicode strings of min_str_len from obj."""
    
    strings = []
    for match in re.finditer(regex % min, obj):
        yield (match.start(), match.group(0).decode())


def main():
    parser = argparse.ArgumentParser(description='Extract both \
        ASCII and UTF-16 strings from a file')
    parser.add_argument('FILE', help='File from which to extract \
        strings')
    parser.add_argument('-e', '--endianess', action='store', default='l',
        help='"b" big endian, "l" little endian (default)')
    parser.add_argument('-f', '--filename', action='store_true', 
        help="Print filename with each string")
    parser.add_argument('-n', '--number', action='store', default=4, type=int,
        help='Minimum string length (default=4)')
    parser.add_argument('-o', '--offset', action='store_true',
        help='Print offset of string')

    args = parser.parse_args()

    fname = args.FILE
    minimum = args.number
    regex = endian.get(args.endianess)

    with open(fname, 'rb') as f:
        for offset, string in get_strings(f.read(), regex, minimum):
            if args.filename and args.offset:
                print(f'{fname}: {offset} {string}')
            elif args.offset:
                print(f'{offset} {string}')
            else:
                print(string)


if __name__ == "__main__":
    main()
