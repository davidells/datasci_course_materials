import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # record: friend record [a, b] (b is a friend of a)
    # we just emit (a, 1) to count that a has a friend
    mr.emit_intermediate(record[0], 1)

def reducer(key, list_of_values):
    # key: person
    # value: list of friend counts
    mr.emit((key, sum(list_of_values)))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
