import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    table = record[0]
    order_id = record[1]
    mr.emit_intermediate(order_id, record)

def reducer(key, list_of_values):
    order = list_of_values.pop(0)
    for v in list_of_values:
      joined = order + v
      mr.emit(joined)

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)


