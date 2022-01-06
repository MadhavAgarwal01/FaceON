import os
from csv import DictWriter,DictReader
import gen_final

global ROOT_LOCATION

def gen_payroll(per,R_mon,R_year):

    #==============================================================================================

    with open('root.csv','r') as rf:
        csv_reader_root = DictReader(rf,fieldnames = ['ROOT LOCATION'])
        for row in csv_reader_root:
            ROOT_LOCATION = row['ROOT LOCATION']
            os.chdir(ROOT_LOCATION) 

    #==============================================================================================

    try:
        # function attributes
        spd=2000  
        pre=0
        ab=0
        lev=0
        pay=0
        net_pay=0
        all_lev=5
        p_lev=0
        pf=15
        person=per.lower()
        
        R_month = R_mon.title()

        gene = gen_final.gen(person,R_month,R_year)

        # os files
        if os.path.exists('PAYROLL'):
            pass
        else:
            os.mkdir('PAYROLL')

        p = os.getcwd()
        pi = os.path.join(p,'PAYROLL')
        os.chdir(pi)

        # person folder exists or not
        if os.path.exists(person):
            pass
        else:
            os.mkdir(person)
        p_name = os.path.join(pi,person)

        # filenames and addresses
        fname1 = person + f"_{R_month}_{R_year}_FINAL" + ".csv"

        ATT = os.path.join(p,f'ATTENDANCE\{person}')
        PAY_FNAME = person + f"_{R_month}_{R_year}_PAYROLL" + ".csv"
        ATT_NEW = os.path.join(ATT,fname1)

        os.chdir(p_name)

        if os.path.isfile(PAY_FNAME):
            os.remove(PAY_FNAME)

        # Generate Payroll
        with open(ATT_NEW,'r') as rf:
            with open(PAY_FNAME,'w',newline='') as wf:

                csv_reader = DictReader(rf)

                csv_writer = DictWriter(wf,fieldnames=['DAYS_PRESENT','DAYS_ABSENT','LEAVES','LEAVES_PRESENT','TOTAL_PAY','NET_PAY','PF'])
                csv_writer.writeheader()

                for row in csv_reader:
                    for k,v in row.items():
                        if v =='P':
                            pre=pre+1
                        if v =='L':
                            lev=lev+1
                        if v =='A':
                            ab=ab+1

                if all_lev>lev:
                    p_lev = all_lev-lev    

                pay = abs(pre*spd - spd*lev + spd*p_lev)

                net_pay = abs(pay-(pay*pf)/100)

                csv_writer.writerow({
                                        'DAYS_PRESENT':pre,
                                        'DAYS_ABSENT':ab,
                                        'LEAVES':lev,
                                        'LEAVES_PRESENT':p_lev,
                                        'TOTAL_PAY':pay,
                                        'NET_PAY':net_pay,
                                        'PF':(pay*pf)/100,
                                    })

        if gene == "ENTER DATA CORRECTLY !":
            os.chdir(ROOT_LOCATION)
            return gene
        else:
            os.chdir(ROOT_LOCATION)
            return "PAYROLL GENERATED SUCCESSFULLY !"

    except FileNotFoundError:
        os.chdir(ROOT_LOCATION)
        return "FILE ABSENT OR WRONG INPUT !"
