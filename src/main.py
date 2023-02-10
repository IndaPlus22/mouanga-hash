"""

Author: Anders Mouanga (salticecream)
Description: DB management system written in Python

"""

# constants

from sys import argv

TABLE = []


class Row:

    def __init__(self, name = "", gram_price = 0, grams = 0, description = 0):
        self.name = name
        self.gram_price = gram_price
        self.grams = grams
        self.description = description
    
    # what to print with print()
    def __str__(self):
        return f"""Name: {self.name}
Price per gram: {self.gram_price}
Grams: {self.grams}
Description: {self.description}
"""
    
    # what to save when saving this row to a file
    def as_file(self):
        return f"""{self.name}|{self.gram_price}|{self.grams}|{self.description}"""

# convert a row from readlines() to a Row
def line_to_row(line):
    name, gram_price, grams, description = line.split("|")
    
    return Row(name, gram_price, grams, description)

# add `rows` new rows to the table
def expand_table(rows: int):
    for _ in range(rows):
        TABLE.append(Row())




# convert a row name to an array index
def hash(row_name):
    sum = 0
    for i in range(len(row_name)):
        sum += (i + 1) * ord(row_name[i])
    
    return sum % len(TABLE)


""" 
insert a new row
returns True on success,
returns False if there already is a row with that name
"""
def insert(row: Row):
    index = hash(row.name)
    
    # find a suitable location in "memory" to put this data
    while True:
        if TABLE[index].name == "":
            # found suitable location, inserting
            TABLE[index] = row
            print(f"Done! Index: {index}")
            return True

        else:
            # did not find suitable location, checking the next index
            index += 1

            if TABLE[index].name == row.name:
                # entry already exists!!!
                return False

            # went out of bounds, expanding table and inserting row there
            if index > len(TABLE):
                expand_table(16)
                TABLE[len(TABLE) - 15] = row
                return True


""" 
delete the row with the name `name` 
returns True on success,
returns False if the row was not found
"""
def delete(name):
    # try to find the index asap
    index = hash(name)
    
    # iterate through possible indices for the name
    while True:
        if TABLE[index].name == "":
            TABLE[index] = Row()
            return True
        else:
            index += 1
            if index == len(TABLE):
                return False


def list_rows():
    empty_row = Row()
    for row in TABLE:
        if row != empty_row:
            print(row)

# get the row at row_id.
def get_row(row_id):
    return TABLE[row_id]

# save the database to the db.420 file
def save_db():
    file = open("db.420", "w")
    lines = []
    for row in TABLE:
        lines.append(row.as_file())
    file.writelines(lines)

try:
    # try to import existing db
    file = open("db.420", "r")
    lines = file.readlines()
    file.close()
    for line in lines:
        TABLE.append(line_to_row(line))
except:
    # if db does not exist, then create new one
    expand_table(16)


match argv[1]:
    case "insert":
        insert(Row(
            argv[2],        # name
            int(argv[3]),    # price/gram
            int(argv[4]),    # grams
            argv[5]         # description
        ))
        save_db()
    
    case "delete":
        if delete(argv[2]):
            save_db()
        else:
            print(f"Invalid name `{argv[2]}`")

    case "list":
        list_rows()

    case "getId":
        _row = TABLE[int(argv[2])]
        if _row != Row():
            print(TABLE)
        else:
            print(f"Invalid id `{argv[2]}`")






