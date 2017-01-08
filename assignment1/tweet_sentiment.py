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

def sentiment_score(message):
    tokens = message["text"].replace("\n", "").split()
#    print len(tokens)
#    for token in tokens:
#        print u"{0} {1}".format(token, sentiments.get(token, 0))
    return sum(map(lambda a: sentiments.get(a, 0), tokens))

def main(tweet_file):
    for line in tweet_file.readlines():
        try:
            message = json.loads(line)
            if is_tweet(message):
                print sentiment_score(message)
        except ValueError:
            raise Exception(u"{0}".format(line))

if __name__ == '__main__':
    sentiments = precomputed_scores(open(sys.argv[1]))
    main(open(sys.argv[2]))
