import os 
from csv import DictWriter,DictReader
from datetime import date
from datetime import datetime
import calendar

global ROOT_LOCATION

def gen(present,mo,ye):

    #==============================================================================================
    
    with open('root.csv','r') as rf:
        csv_reader_root = DictReader(rf,fieldnames = ['ROOT LOCATION'])
        for row in csv_reader_root:
            ROOT_LOCATION = row['ROOT LOCATION']
            os.chdir(ROOT_LOCATION) 

    #==============================================================================================

    try:
        # date time object
        date_time_obj1 = datetime.strptime(f"01/{mo}/{ye}",'%d/%B/%Y')

        month = mo
        year = ye

        # file names
        fname = present + f"_{month}_{year}" + "_LEAVE.csv"
        fname2 = present + f"_{month}_{year}" + "_FINAL.csv"
        fname3 = present + f"_{month}_{year}" + "_UNIQUE.csv"

        # Addresses
        dir_path = f"ATTENDANCE\{present}"
        LEAVE_ADD = os.path.join(dir_path,fname)
        FINAL_ADD = os.path.join(dir_path,fname2)
        UNI_ADD = os.path.join(dir_path,fname3)

        # leaves , presents and data
        l_list = []
        p_list = []

        with open(LEAVE_ADD,'r') as rf2:
            csv_reader2 = DictReader(rf2,fieldnames = ['DATE'])

            for row_2 in csv_reader2:
                l_list.append(row_2['DATE'])

        with open(UNI_ADD,'r') as rf3:
            csv_reader3 = DictReader(rf3,fieldnames = ['DATE','ATTENDANCE','LEAVE'])

            for row_3 in csv_reader3:
                p_list.append(row_3['DATE'])

        # deleting previous data
        if os.path.isfile(FINAL_ADD):
            os.remove(FINAL_ADD)

        # final file with all data
        with open(FINAL_ADD,'a',newline='') as wf:

            monthf = int(date_time_obj1.strftime('%m'))
            yearf = int(date_time_obj1.strftime('%Y'))

            csv_writer = DictWriter(wf,fieldnames = ['DATE','ATTENDANCE','LEAVE'])
            csv_writer.writeheader()
            no_of_days = calendar.monthrange(yearf, monthf)[1]

            for i in range(1,(no_of_days + 1)):

                date_time_obj2 = datetime.strptime(f"{i}/{monthf}/{yearf}", '%d/%m/%Y')
                d = date_time_obj2.strftime('%d/%m/%Y')

                dict = {
                            'DATE':d,
                            'ATTENDANCE':'A',
                            'LEAVE':0,
                        }

                if d in l_list:
                    dict['LEAVE']='L'
                elif d in p_list:
                    dict['ATTENDANCE']='P'

                csv_writer.writerow(dict)

    except ValueError:
        os.chdir(ROOT_LOCATION)
        return "ENTER DATA CORRECTLY !"

    except FileNotFoundError:
        os.chdir(ROOT_LOCATION)
        return "DATA FILES NOT PRESENT/CORRUPTED !"