import json
import re
import sys

def sentiment_dict(sentiment_file):
    scores = {} # initialize an empty dictionary
    for line in sentiment_file:
      term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
      scores[term] = int(score)  # Convert the score to an integer.
    return scores

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    sentiment_scores = sentiment_dict(sent_file)
    for line in tweet_file:
        tweet_json = json.loads(line)
        if 'delete' in tweet_json:
            continue

        #print json.dumps(tweet_json, indent=2)
        #break

        words = tweet_json['text'].split()
        norm_words = []
        for word in words:
            if re.search('[.!?]$', word):
                word = word[:-1]
            norm_words.append(word.lower())

        word_scores = [ \
            w in sentiment_scores and sentiment_scores[w] or 0 \
            for w in norm_words \
        ]
        tweet_score = sum(word_scores)

        print tweet_score

if __name__ == '__main__':
    main()
