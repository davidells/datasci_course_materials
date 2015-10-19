import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # record: row of order or line_item table
    order_id = record[1]
    mr.emit_intermediate(order_id, record)

def reducer(key, list_of_values):
    # key: order_id
    # value: list of matching rows
    orders = [
        row for row 
        in list_of_values 
        if row[0] == 'order' 
    ]

    line_items = [
        row for row
        in list_of_values 
        if row[0] == 'line_item' 
    ]

    for order in orders:
        for line_item in line_items:
            if order[1] == line_item[1]:
                mr.emit(order + line_item)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
