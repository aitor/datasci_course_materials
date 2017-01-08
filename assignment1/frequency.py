import sys
import json
import operator
import itertools

def terms_for(message):
    return message.get("text", "").split()

def main():
    tweets = open(sys.argv[1])
    frequencies = {}
    for line in tweets.readlines():
        message = json.loads(line)
        terms = terms_for(message)
        if terms:
            for term in terms:
                frequencies[term] = frequencies.get(term, 0) + 1

    total_terms = sum(frequencies.itervalues())

    for frequency in frequencies:
        print u"{0} {1}".format(frequency, frequencies[frequency]/float(total_terms))

if __name__ == '__main__':
    main()
