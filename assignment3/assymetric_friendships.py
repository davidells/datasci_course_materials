import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # record: friend record [a, b] (b is a friend of a)
    # we emit (a, [a, b]) and also (b, [a, b]) to "join"
    # friend records to themselves
    mr.emit_intermediate(record[0], record)
    mr.emit_intermediate(record[1], record)

def reducer(key, records):
    # key: person
    # value: rows where they appear
    followers = [r[1] for r in records if r[0] == key]
    following = [r[0] for r in records if r[1] == key]

    #print key
    #print records
    #print set(followers) - set(following)
    #sys.exit(1)

    for f in following:
        if f not in followers:
            mr.emit((key, f))

    for f in followers:
        if f not in following:
            mr.emit((key, f))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
