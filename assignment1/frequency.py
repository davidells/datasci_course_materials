import json
import re
import sys

def main():
    tweet_file = open(sys.argv[1])

    occurrences = {}
    total_terms = 0

    for line in tweet_file:
        tweet_json = json.loads(line)
        if 'delete' in tweet_json:
            continue

        words = tweet_json['text'].split()
        norm_words = []
        for word in words:
            if re.search('[.!?]$', word):
                word = word[:-1]
            norm_words.append(word.lower())

        for word in norm_words:
            if word not in occurrences:
                occurrences[word] = 0
            occurrences[word] += 1

        total_terms += len(norm_words)

    for (word, count) in occurrences.items():
        print '%s %f' % (word, 1.0 * count / total_terms)

if __name__ == '__main__':
    main()
