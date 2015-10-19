import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    matrix = record[0]
    i = record[1]
    j = record[2]
    val = record[3]

    if matrix == 'a':
        for r in range(5):
            mr.emit_intermediate((i,r), record)
    else:
        for r in range(5):
            mr.emit_intermediate((r,j), record)

def reducer(key, values):
    a_rec = [rec for rec in values if rec[0] == 'a']
    b_rec = [rec for rec in values if rec[0] == 'b']

    dot = 0
    for a in a_rec:
        for b in b_rec:
            if a[2] == b[1]:
                dot += (a[3] * b[3])

    mr.emit((key[0], key[1], dot))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
