import sys
import json
import math
import operator

def states_dictionary():
  return {
      'AL': ["Alabama", 32.806671, -86.791130],
      'AK': ["Alaska", 61.370716, -152.404419],
      'AZ': ["Arizona", 33.729759, -111.431221],
      'AR': ["Arkansas", 34.969704, -92.373123],
      'CA': ["California", 36.116203, -119.681564],
      'CO': ["Colorado", 39.059811, -105.311104],
      'CT': ["Connecticut", 41.597782, -72.755371],
      'DE': ["Delaware", 39.318523, -75.507141],
      'DC': ["District of Columbia", 38.897438, -77.026817],
      'FL': ["Florida", 27.766279, -81.686783],
      'GA': ["Georgia", 33.040619, -83.643074],
      'HI': ["Hawaii", 21.094318, -157.498337],
      'ID': ["Idaho", 44.240459, -114.478828],
      'IL': ["Illinois", 40.349457, -88.986137],
      'IN': ["Indiana", 39.849426, -86.258278],
      'IA': ["Iowa", 42.011539, -93.210526],
      'KS': ["Kansas", 38.526600, -96.726486],
      'KY': ["Kentucky", 37.668140, -84.670067],
      'LA': ["Louisiana", 31.169546, -91.867805],
      'ME': ["Maine", 44.693947, -69.381927],
      'MD': ["Maryland", 39.063946, -76.802101],
      'MA': ["Massachusetts", 42.230171, -71.530106],
      'MI': ["Michigan", 43.326618, -84.536095],
      'MN': ["Minnesota", 45.694454, -93.900192],
      'MS': ["Mississippi", 32.741646, -89.678696],
      'MO': ["Missouri", 38.456085, -92.288368],
      'MT': ["Montana", 46.921925, -110.454353],
      'NE': ["Nebraska", 41.125370, -98.268082],
      'NV': ["Nevada", 38.313515, -117.055374],
      'NH': ["New Hampshire", 43.452492, -71.563896],
      'NJ': ["New Jersey", 40.298904, -74.521011],
      'NM': ["New Mexico", 34.840515, -106.248482],
      'NY': ["New York", 42.165726, -74.948051],
      'NC': ["North Carolina", 35.630066, -79.806419],
      'ND': ["North Dakota", 47.528912, -99.784012],
      'OH': ["Ohio", 40.388783, -82.764915],
      'OK': ["Oklahoma", 35.565342, -96.928917],
      'OR': ["Oregon", 44.572021, -122.070938],
      'PA': ["Pennsylvania", 40.590752, -77.209755],
      'RI': ["Rhode Island", 41.680893, -71.511780],
      'SC': ["South Carolina", 33.856892, -80.945007],
      'SD': ["South Dakota", 44.299782, -99.438828],
      'TN': ["Tennessee", 35.747845, -86.692345],
      'TX': ["Texas", 31.054487, -97.563461],
      'UT': ["Utah", 40.150032, -111.862434],
      'VT': ["Vermont", 44.045876, -72.710686],
      'VA': ["Virginia", 37.769337, -78.169968],
      'WA': ["Washington", 47.400902, -121.490494],
      'WV': ["West Virginia", 38.491226, -80.954453],
      'WI': ["Wisconsin", 44.268543, -89.616508],
      'WY': ["Wyoming", 42.755966, -107.302490]
    }
def precomputed_scores(scores_file):
    scores = {}
    for line in scores_file:
      term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
      scores[term] = int(score)  # Convert the score to an integer.
    return scores

def distance(lat1, lon1, lat2, lon2):
  rlat1 = math.radians(lat1)
  rlat2 = math.radians(lat2)
  rlon1 = math.radians(lon1)
  rlon2 = math.radians(lon2)
  R = 6371 # earth
  x = (rlon2 - rlon1) * math.cos((rlat1 + rlat2) / 2);
  y = (rlat2 - rlat1);
  return math.sqrt(x * x + y * y) * R

def inside_the_usa(message):
    lat, lon = message["coordinates"]["coordinates"]
    usa = [
        -123.837890625, -67.32421875,
        24.2469645543, 48.8647147618
    ]
    return lat >= usa[0] and lat <= usa[1] and lon >= usa[2] and lon <= usa[3]

def is_geolocated(message):
  return message.get("coordinates", None)

def sentiment_score(message):
    tokens = message["text"].replace("\n", "").split()
#    print len(tokens)
#    for token in tokens:
#        print u"{0} {1}".format(token, sentiments.get(token, 0))
    return sum(map(lambda a: sentiments.get(a, 0), tokens))


def main(tweet_file):
    state_scores = {}
    for line in tweet_file.readlines():
        message = json.loads(line)
        if is_geolocated(message) and inside_the_usa(message):
            lat, lon = message["coordinates"]["coordinates"]
            #print u"coord {0} {1}".format(lat, lon)
            max_distance = 4800
            closest_state = None
            for state in states:
                state_distance = distance(lat, lon, states[state][2], states[state][1])
                #print u"   {0} {1}".format(states[state][0], state_distance)
                if state_distance < max_distance:
                    closest_state = state
                    max_distance = state_distance

            if closest_state:
                #print u"{0} {1}".format(closest_state, max_distance)
                state_scores[closest_state] =  state_scores.get(closest_state, 0) + sentiment_score(message)

    sorted_state_scores = sorted(state_scores.items(), key=operator.itemgetter(1))
    print sorted_state_scores[-1][0]

if __name__ == '__main__':
    states = states_dictionary()
    sentiments = precomputed_scores(open(sys.argv[1]))
    main(open(sys.argv[2]))
