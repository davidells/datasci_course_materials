import json
import re
import sys

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

# Normalize to all lower case
us_state_abbrev = dict((k.lower(), v.lower()) for k,v in us_state_abbrev.iteritems())
us_state_abbrev_values = us_state_abbrev.values()

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
    state_scores = dict((abbrev, 0) for abbrev in us_state_abbrev_values)

    for line in tweet_file:
        tweet_json = json.loads(line)
        if 'delete' in tweet_json:
            continue

        if 'lang' not in tweet_json or tweet_json['lang'] != 'en':
            continue

        #print json.dumps(tweet_json, indent=2)

        words = tweet_json['text'].split()
        norm_words = []
        for word in words:
            if re.search('[.!?]$', word):
                word = word[:-1]
            norm_words.append(word.lower())

        tweet_score = sum([ \
            w in sentiment_scores and sentiment_scores[w] or 0 \
            for w in norm_words \
        ])

        #print tweet_score

        location = tweet_json['user']['location']
        if location is None:
            continue

        loc_words = [ re.sub('\W', '', w).lower() for w in location.split() ]
        state = None
        for lw in loc_words:
            if lw in us_state_abbrev:
                state = us_state_abbrev[lw]
                break
            elif lw in us_state_abbrev_values:
                state = lw
                break

        if state is None:
            continue

        state_scores[state] += tweet_score

    #print state_scores

    # Find happiest state by sentiment score
    happiest_state = None
    max_score = None
    for (state, score) in state_scores.items():
        if max_score is None or score > max_score:
            max_score = score
            happiest_state = state

    print happiest_state.upper()

if __name__ == '__main__':
    main()
