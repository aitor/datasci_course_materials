import sys
import json
import operator
import itertools

def hashtags_for(message):
    hashtags_list = message.get("entities", {}).get("hashtags")
    if hashtags_list:
        return map(lambda tag: tag['text'], hashtags_list)
    else:
        return []

def main():
    tweets = open(sys.argv[1])
    scores = {}
    for line in tweets.readlines():
        message = json.loads(line)
        hashtags = hashtags_for(message)
        if hashtags:
            for hashtag in hashtags:
                scores[hashtag] = scores.get(hashtag, 0) + 1

    sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))

    for score in sorted_scores[-10:]:
        print u"{0} {1}".format(score[0], score[1])

if __name__ == '__main__':
    main()
