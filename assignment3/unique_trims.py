import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    seq_id = record[0]
    nucleotides = record[1]
    mr.emit_intermediate(0, nucleotides[:-10])

def reducer(key, values):
    for v in set(values):
        mr.emit(v)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
