import MapReduce
import sys
from collections import OrderedDict

mr = MapReduce.MapReduce()

def mapper(record):
    key = record[0] # book file name
    value = record[1] # book contents
    words = list(OrderedDict.fromkeys(value.split()))
    for w in words:
      mr.emit_intermediate(w, key)

def reducer(key, list_of_values):
    # key: word 
    # list_of_values: list of documents where it appears
    mr.emit((key, list_of_values))

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)


