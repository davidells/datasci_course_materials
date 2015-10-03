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
    new_word_scores = {}

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

        word_scores = [ \
            w in sentiment_scores and sentiment_scores[w] or 0 \
            for w in norm_words \
        ]

        tweet_score = sum(word_scores)

        # If this tweet has some sentiment, add that to running sentiment scores
        # for unscored words
        if tweet_score != 0:
            unscored_words = [w for w in norm_words if w not in sentiment_scores]
            for word in unscored_words:
                if word not in new_word_scores:
                    new_word_scores[word] = []
                new_word_scores[word].append(tweet_score)

    # Create final unscored word sentiment scores by averaging out sentiments
    # of tweets where they appear
    for (word, scores) in new_word_scores.items():
        avg_score = sum(scores) / len(scores)
        print '%s %d' % (word, avg_score)



if __name__ == '__main__':
    main()
