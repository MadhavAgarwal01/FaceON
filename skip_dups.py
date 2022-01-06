import os 
from csv import DictWriter,DictReader

def skip(person,month,year):

    # file names
    fname = person + f"_{month}_{year}" + ".csv"
    fname1 = person + f"_{month}_{year}_UNIQUE" + ".csv"

    # Addresses
    ATT = os.getcwd()
    ATT_FNAME = os.path.join(ATT,fname)
    ATT_NEW = os.path.join(ATT,fname1)

    with open(ATT_FNAME,'r') as in_file, open(ATT_NEW,'w') as out_file:
        seen = set()
        for line in in_file:
            if line in seen:
                continue 

            seen.add(line)
            out_file.write(line)

    os.remove(ATT_FNAME)