import MapReduce
import sys

mr = MapReduce.MapReduce()
size = 5

def mapper(record):
	matrix = record[0]
	i = record[1]
	j = record[2]
	v = record[3]
	if matrix == "a":
		for n in xrange(0,size):
			key = (i,n)
			value = (matrix, j, v)
			mr.emit_intermediate(key, value)
	else:
		for n in xrange(0,size):
			key = (n,j)
			value = (matrix, i, v)			
			mr.emit_intermediate(key, value)

    

def reducer(key, list_of_values):
    matrix_a_values = filter(lambda s: s[0] == 'a', list_of_values)
    matrix_b_values = filter(lambda s: s[0] == 'b', list_of_values)
    total = 0
    for n in xrange(0,size):
    	a_value = filter(lambda s: s[1] == n, matrix_a_values) or [(0,0,0)]
    	b_value = filter(lambda s: s[1] == n, matrix_b_values) or [(0,0,0)]
    	total += a_value[0][2] * b_value[0][2]

    mr.emit((key[0],key[1],total))

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)

# C = A x B 
# C_i_j = sum( A_i_k * B_k_j ) 