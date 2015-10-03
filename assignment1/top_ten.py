import json
import operator
import re
import sys

def main():
    tweet_file = open(sys.argv[1])

    occurrences = {}

    for line in tweet_file:
        tweet_json = json.loads(line)
        if 'delete' in tweet_json:
            continue


        hashtags = [ht['text'] for ht in tweet_json['entities']['hashtags']]

        for ht in hashtags:
            if ht not in occurrences:
                occurrences[ht] = 0
            occurrences[ht] += 1

    sorted_occ = sorted(occurrences.items(), key=operator.itemgetter(1), reverse=True)
    for i in range(10):
        print '%s %s' % sorted_occ[i]

if __name__ == '__main__':
    main()
