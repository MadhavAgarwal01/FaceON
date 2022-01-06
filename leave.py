import os 
from csv import DictWriter,DictReader
from datetime import date
from datetime import datetime
import calendar

global ROOT_LOCATION

def set_leaves(present,sd,ed):

    #==============================================================================================
    
    with open('root.csv','r') as rf:
        csv_reader_root = DictReader(rf,fieldnames = ['ROOT LOCATION'])
        for row in csv_reader_root:
            ROOT_LOCATION = row['ROOT LOCATION']
            os.chdir(ROOT_LOCATION) 

    #==============================================================================================

    # date time object
    date_time_obj1 = datetime.strptime(sd,'%d/%m/%Y')

    month = date_time_obj1.strftime('%B')
    year = date_time_obj1.strftime('%Y')

    # file names
    fname = present + f"_{month}_{year}" + "_LEAVE.csv"
    fname2 = present + f"_{month}_{year}" + "_FINAL.csv"
    fname3 = present + f"_{month}_{year}" + "_UNIQUE.csv"

    # Addresses
    dir_path = f"ATTENDANCE\{present}"
    LEAVE_ADD = os.path.join(dir_path,fname)
    FINAL_ADD = os.path.join(dir_path,fname2)
    UNI_ADD = os.path.join(dir_path,fname3)

    # variables
    s=int(sd[:2])
    e=int(ed[:2])
    last = sd[2:]

    try:
        with open(LEAVE_ADD,'a',newline='') as f:
            csv_writer = DictWriter(f,fieldnames = ['DATE']) # ==> specify headers i.e. KEY
            ld=''
            for i in range(s,e+1):
                
                ld=str(i)+last
                date_time_obj3 = datetime.strptime(ld,'%d/%m/%Y')
                csv_writer.writerow({'DATE':date_time_obj3.strftime('%d/%m/%Y')})
                ld=''
    except FileNotFoundError:
        os.chdir(ROOT_LOCATION)
        return "FILE NOT PRESENT OR WRONG DATA ENTERED !"
        
    os.chdir(ROOT_LOCATION)
    return "LEAVES ADDED !"