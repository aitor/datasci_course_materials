import sys
import json

def precomputed_scores(scores_file):
    scores = {}
    for line in scores_file:
      term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
      scores[term] = int(score)  # Convert the score to an integer.
    return scores

def is_tweet(message):
    return "created_at" in message

def tokenized_tweet(tweet):
    return tweet["text"].replace("\n", "").split()

def sentiment_score(message):
    tokens = tokenized_tweet(message)
#    print len(tokens)
#    for token in tokens:
#        print u"{0} {1}".format(token, sentiments.get(token, 0))
    return sum(map(lambda a: sentiments.get(a, 0), tokens))

def index_new_terms(message, score):
    delta = 1 if score > 0 else -1
    tokens = tokenized_tweet(message)
    for token in tokens:
        if not sentiments.get(token):
            new_terms[token] = new_terms.get(token, 0) + delta

def main(tweet_file):
    for line in tweet_file.readlines():
        message = json.loads(line)
        if is_tweet(message):
            tweet_score = sentiment_score(message)
            index_new_terms(message, tweet_score)

    for term in new_terms:
        print u"{0} {1}".format(term, new_terms[term])


if __name__ == '__main__':
    new_terms = {}
    sentiments = precomputed_scores(open(sys.argv[1]))
    main(open(sys.argv[2]))
