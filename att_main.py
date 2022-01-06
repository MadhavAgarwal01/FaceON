import os
import time
from statistics import mode, StatisticsError
from datetime import date
from datetime import datetime
from csv import DictReader,DictWriter
import skip_dups
import live_face

global ROOT_LOCATION
name =''

def att_live_face():

    #==============================================================================================
    
    with open('root.csv','r') as rf:
        csv_reader_root = DictReader(rf,fieldnames = ['ROOT LOCATION'])
        for row in csv_reader_root:
            ROOT_LOCATION = row['ROOT LOCATION']
            os.chdir(ROOT_LOCATION) 
            # print(row['ROOT LOCATION'])

    #==============================================================================================

    name,msg = live_face.is_present()
    if msg == 'OK':
        present = name
        # dd/mm/YY
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        current_month = datetime.now().strftime('%B')
        current_year = datetime.now().strftime('%Y')

        # ATTENDANCE folder
        if os.path.exists('ATTENDANCE'):
            pass
        else:
            os.mkdir('ATTENDANCE')

        p = os.getcwd()
        pi = os.path.join(p,'ATTENDANCE')
        os.chdir(pi)

        # att_name folder exists or not
        if os.path.exists(name):
            pass
        else:
            os.mkdir(name)

        p_name = os.path.join(pi,name)
        os.chdir(p_name)

        # EMPLOYEE FILE
        fname=present+f"_{current_month}_{current_year}"+".csv"

        with open(fname,'a',newline='') as f:
            csv_writer = DictWriter(f,fieldnames = ['DATE','ATTENDANCE','LEAVE']) # ==> specify headers i.e. KEY

            csv_writer.writerow({
            'DATE':d1,
            'ATTENDANCE':'P',
            'LEAVE':0,
        })


        skip_dups.skip(name,current_month,current_year)

        fname_l = present + f"_{current_month}_{current_year}" + "_LEAVE.csv"

        # MAKE A LEAVES FILE
        if os.path.isfile(os.path.join(os.getcwd(),fname_l)):
            pass
        else:
            with open(fname_l,'a',newline='') as lf:
                csv_writer = DictWriter(lf,fieldnames = ['DATE']) # ==> specify headers i.e. KEY
                csv_writer.writeheader()

        os.chdir(ROOT_LOCATION)
        return name,'ATTENDANCE MARKED SUCCESSFULLY !'

    else : 
        os.chdir(ROOT_LOCATION)
        return name,msg
