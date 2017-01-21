import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    person = record[0]
    friend = record[1]
    #pair = sorted([person, friend])
    mr.emit_intermediate((person, friend), 1)
    mr.emit_intermediate((friend, person), 1)

def reducer(key, list_of_values):
	#print key
	#print list_of_values
    if len(list_of_values) == 1:
        mr.emit(key)

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
