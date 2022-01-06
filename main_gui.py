from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import os
from shutil import copyfile,copy
from PIL import ImageTk,Image
import datetime
import tkcalendar
# scripts
import att_main
import live_face
import leave
import gen_final
import payroll
import gen_pay_pdf
import capture_face_data
from csv import DictReader,DictWriter

#==============================================================================================
# program root location
with open('root.csv','w',newline='') as wf:
    csv_writer = DictWriter(wf,fieldnames = ['ROOT LOCATION'])
    # csv_writer.writeheader()
    r_loc = os.getcwd()
    csv_writer.writerow({
                        'ROOT LOCATION': r_loc
                    })

#==============================================================================================

root = tk.Tk()

wi = 800 # width for the Tk root
hi = 500 # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

# calculate x and y coordinates for the Tk root window
xi = (ws/2) - (wi/2)
yi = (hs/2) - (hi/2)

# set the dimensions of the screen 
# and where it is placed
root.geometry('%dx%d+%d+%d' % (wi, hi, xi, yi))
root.title('ATTENDANCE BASED PAYROLL SYSTEM')
root.resizable(False,False)

#Tabs
tabControl = ttk.Notebook(root)

att_mode = ttk.Frame(tabControl)
pay_mode = ttk.Frame(tabControl)
leave_mode = ttk.Frame(tabControl)
capture_mode = ttk.Frame(tabControl)

tabControl.add(att_mode, text=' Attendance Mode '.upper())
tabControl.add(pay_mode, text=' Payroll Generation '.upper())
tabControl.add(leave_mode, text=' Leave Management '.upper())
tabControl.add(capture_mode, text=' Capture Face Data '.upper())
tabControl.pack(expand=1, fill="both")

# =================Attendance Mode==================== 
# other widgets
canvas = Canvas(att_mode,width = 180, height = 210,relief='ridge',highlightthickness = 2 ,borderwidth = 2,bg='white')
canvas.grid(row = 0, columnspan=3,padx=(200,30),pady=30)

ttk.Label(att_mode, text="EMPLOYEE NAME : ").grid(row=4,column=0,padx=(30,10),pady=30,sticky=W)

name_l=ttk.Label(att_mode,text= "")
name_l.grid(row=4,column=1,pady=(2,2),sticky=W)

ttk.Label(att_mode, text="STATUS : ").grid(row=4,column=2,padx=(180,0),pady=30,sticky=W)

stat_l=ttk.Label(att_mode,text= "")
stat_l.grid(row=4,column=3,padx=(0,30),pady=30,sticky=W)

progress = ttk.Progressbar(att_mode, orient = HORIZONTAL, length = 250, mode = 'indeterminate') 
progress.grid(row=7,column=3,padx=(0,30),pady=30,sticky=W)
progress.start(10)

class chk_gui:
    def ex_att_main(self):
        na,MS=att_main.att_live_face()
        if na != "":
            ex_reset()
            name_l.config(text=na.title())
            stat_l.config(text=MS)
            # image
            # os.chdir(os.path.dirname(os.getcwd()))  # name dir
            # os.chdir(os.path.dirname(os.getcwd()))  # Attendance dir
            img = Image.open(os.path.join(os.getcwd(),f"images\{na.title()}\{na}.jpg"))
            image1 = ImageTk.PhotoImage(img.resize((180, 210), Image.ANTIALIAS))
            canvas.create_image(4,4, anchor=NW, image=image1) 

        else:
            name_l.config(text="No legit face detected !")
            if MS != 'OK':
                stat_l.config(text=MS)

            canvas.delete("all")

        # os.chdir(os.path.dirname(os.getcwd())) # jump up 
        # os.chdir(os.path.dirname(os.getcwd())) # jump up to root
        
        root.mainloop()
    
def ex_reset():
    name_l.config(text="")
    stat_l.config(text="")
    canvas.delete("all")

# class instantiate
g=chk_gui()

#buttons
check_button = ttk.Button(att_mode,text='CHECK',command=g.ex_att_main)
check_button.grid(row=7,columnspan=2,padx=(0,150),pady=(2,2))

reset_button = ttk.Button(att_mode,text='RESET',command=ex_reset)
reset_button.grid(row=7,columnspan=2,padx=(180,30),pady=(2,2))

# =====================Payroll Generation==================== 

Pprogress = ttk.Progressbar(pay_mode, orient = HORIZONTAL, length = 300, mode = 'indeterminate') 
Pprogress.grid(row=5,columnspan=5,padx=(375,80),pady=(20,0),sticky=W)
Pprogress.start(10)

# dd/mm/YY
current_time = datetime.datetime.now() 

# other widgets
Pcanvas = Canvas(pay_mode,width = 180, height = 210,relief='ridge',highlightthickness = 2 ,borderwidth = 2,bg='white')
Pcanvas.grid(row = 0,rowspan = 3, column=0,padx=(265,10),pady=(30,0),sticky=NW)

ttk.Label(pay_mode, text="EMPLOYEE NAME  : ").grid(row=4,column=0,padx=(30,10),pady=(30,0),sticky=W)

Pname_l=ttk.Label(pay_mode,text= "")
Pname_l.grid(row=4,columnspan=1,padx=(150,10),pady=(30,0),sticky=W)

ttk.Label(pay_mode, text="STATUS                    : ").grid(row=5,column=0,padx=(30,10),pady=(20,0),sticky=W)

Pstat_l=ttk.Label(pay_mode,text= "")
Pstat_l.grid(row=5,columnspan=1,padx=(150,10),pady=(30,10),sticky=W)

ttk.Label(pay_mode, text="MONTH :").grid(row=7,column=0,padx=(250,30),pady=(30,10),sticky=W)
ttk.Label(pay_mode, text="YEAR :").grid(row=7,column=0,padx=(410,10),pady=(30,10),sticky=W)

# ENTRY
MONTH=tk.StringVar()
MONTH = ttk.Entry(pay_mode,width = 10,textvariable = MONTH)
MONTH.grid(row=7,column=0,padx=(310,30),pady=(30,10),sticky=W)
MONTH.focus() # to set cursor position

YEAR=tk.StringVar()
YEAR = ttk.Entry(pay_mode,width = 10,textvariable = YEAR)
YEAR.grid(row=7,column=0,padx=(470,0),pady=(30,10),sticky=W)

# SAVE LOCATION
entry_save=tk.StringVar()
entry_save = ttk.Entry(pay_mode,width = 60,textvariable = entry_save)
entry_save.grid(row=8,columnspan=1,padx=(30,10),pady=(10,20),sticky=W)

class Pchk_gui:

    def ex_leave(self):
        Pna,P_MS=live_face.is_present()
        if Pna != "":
            Pex_reset()
            Pname_l.config(text=Pna.title())
            Pstat_l.config(text="LOGGED IN SUCCESSFULLY !")
            # image
            Pimg = Image.open(os.path.join(os.getcwd(),f"images\{Pna.title()}\{Pna}.jpg"))
            Pimage1 = ImageTk.PhotoImage(Pimg.resize((180, 210), Image.ANTIALIAS))
            Pcanvas.create_image(4,4, anchor=NW, image=Pimage1) 

        else:
            Pname_l.config(text="No legit face detected !")
            if P_MS=='OK':
                Pstat_l.config(text="TRY AGAIN!")
            else:
                Pstat_l.config(text=P_MS)
            Pcanvas.delete("all")

        # os.chdir(os.path.dirname(os.getcwd())) # jump up 
        # os.chdir(os.path.dirname(os.getcwd())) # jump up to root
        
        root.mainloop()


# class instantiate
Pg=Pchk_gui()

def Pex_reset():
    Pname_l.config(text="")
    Pstat_l.config(text="")
    Pcanvas.delete("all")
    MONTH.delete(0,tk.END)
    YEAR.delete(0,tk.END)
    entry_save.delete(0,tk.END)


def fun_pay():
    Pm=MONTH.get().lower()
    Py=YEAR.get()
    P_s = payroll.gen_payroll(Pname_l.cget('text'),Pm,Py)
    Pstat_l.config(text=P_s)

def browse():  # method to browse save location
    global folder_path
    entry_save.delete(0,tk.END)
    dst = filedialog.askdirectory()
    # os.chdir(dst)
    entry_save.insert(0,dst)
    
def Pgen_pdf():
    Pm=MONTH.get().lower()
    Py=YEAR.get()
    P_s = gen_pay_pdf.gen_report(Pname_l.cget('text'),Pm,Py,entry_save.get())
    Pstat_l.config(text=P_s)

#buttons
Pcheck_button = ttk.Button(pay_mode,text='LOG IN',command=Pg.ex_leave)
Pcheck_button.grid(row=7,column=0,padx=(30,150),pady=(30,10),sticky=W)

Preset_button = ttk.Button(pay_mode,text='RESET',command=Pex_reset)
Preset_button.grid(row=7,column=0,padx=(150,30),pady=(30,10),sticky=W)

Pconfirm_button = ttk.Button(pay_mode,text='CONFIRM',command=fun_pay)
Pconfirm_button.grid(row=7,column=0,padx=(600,0),pady=(30,10),sticky=W)

Pbrowse_button = ttk.Button(pay_mode,text='BROWSE', command=browse)
Pbrowse_button.grid(row=8,column=0,padx=(410,10),pady=(10,20),sticky=W)

P_gen_pdf_button = ttk.Button(pay_mode,text='GENERATE PDF', command=Pgen_pdf,width=26)
P_gen_pdf_button.grid(row=8,column=0,padx=(510,10),pady=(10,20),sticky=W)

# =====================Leave Management======================= 

lprogress = ttk.Progressbar(leave_mode, orient = HORIZONTAL, length = 300, mode = 'indeterminate') 
lprogress.grid(row=5,column=2,pady=(30,0),sticky=W)
lprogress.start(10)

# dd/mm/YY
current_time = datetime.datetime.now() 

#start date and cal 1
ttk.Label(leave_mode, text="START DATE  : ").grid(row=0,column=0,padx=(245,0),pady=(10,20),sticky=NW)
cal1 = tkcalendar.Calendar(leave_mode,selectmode='day',year = current_time.year,month = current_time.month, day = current_time.day,date_pattern = 'DD/MM/Y')
cal1.grid(row =0,rowspan = 3, columnspan=5,padx=(250,80),pady=(30,10),sticky=W)
cal1.selection_clear()

#end date and cal 2
ttk.Label(leave_mode, text="END DATE  : ").grid(row=0,column=2,padx=(110,0),pady=(10,20),sticky=NW)
cal2 = tkcalendar.Calendar(leave_mode,selectmode = "day",year = current_time.year,month = current_time.month, day = current_time.day,date_pattern = 'DD/MM/Y')
cal2.grid(row = 0,rowspan = 3, columnspan=5,padx=(530,0),pady=(30,10),sticky=W)
cal2.selection_clear()

# other widgets
lcanvas = Canvas(leave_mode,width = 180, height = 210,relief='ridge',highlightthickness = 2 ,borderwidth = 2,bg='white')
lcanvas.grid(row = 0,rowspan = 3, column=0,padx=(30,10),pady=(30,0),sticky=NW)

ttk.Label(leave_mode, text="EMPLOYEE NAME  : ").grid(row=4,column=0,padx=(30,10),pady=(30,0),sticky=W)

lname_l=ttk.Label(leave_mode,text= "")
lname_l.grid(row=4,columnspan=1,padx=(150,10),pady=(30,0),sticky=W)

ttk.Label(leave_mode, text="STATUS                    : ").grid(row=5,column=0,padx=(30,10),pady=(30,0),sticky=W)

lstat_l=ttk.Label(leave_mode,text= "")
lstat_l.grid(row=5,columnspan=1,padx=(150,10),pady=(30,0),sticky=W)


class lchk_gui:

    def ex_leave(self):
        lna,L_MS=live_face.is_present()
        if lna != "":
            lex_reset()
            lname_l.config(text=lna.title())
            lstat_l.config(text="LOGGED IN SUCCESSFULLY !")
            # image
            limg = Image.open(os.path.join(os.getcwd(),f"images\{lna.title()}\{lna}.jpg"))
            limage1 = ImageTk.PhotoImage(limg.resize((180, 210), Image.ANTIALIAS))
            lcanvas.create_image(4,4, anchor=NW, image=limage1) 

        else:
            lname_l.config(text="No legit face detected !")
            if L_MS=='OK':
                lstat_l.config(text="TRY AGAIN!")
            else:
                lstat_l.config(text=L_MS)
            lcanvas.delete("all")

        # os.chdir(os.path.dirname(os.getcwd())) # jump up 
        # os.chdir(os.path.dirname(os.getcwd())) # jump up to root
        
        root.mainloop()


# class instantiate
lg=lchk_gui()

def lex_reset():
    cal1.selection_clear()
    cal2.selection_clear()
    lname_l.config(text="")
    lstat_l.config(text="")
    lcanvas.delete("all")

def add_leaves():
    start_date = cal1.get_date()
    end_date = cal2.get_date()
    ls = leave.set_leaves(lname_l.cget('text').lower(),start_date,end_date)
    lstat_l.config(text=ls)


#buttons
lcheck_button = ttk.Button(leave_mode,text='LOG IN',command=lg.ex_leave)
lcheck_button.grid(row=7,column=0,padx=(30,150),pady=(30,10),sticky=W)

lreset_button = ttk.Button(leave_mode,text='RESET',command=lex_reset)
lreset_button.grid(row=7,column=0,padx=(150,30),pady=(30,10),sticky=W)

lconfirm_button = ttk.Button(leave_mode,text='ADD LEAVES',command=add_leaves)
lconfirm_button.grid(row=7,column=0,padx=(270,30),pady=(30,10),sticky=W)

# =====================Capture Face Data========================= 

ttk.Label(capture_mode, text="ENTER NAME : ").grid(row=2,column=0,padx=(120,30),pady=(100,0),sticky=W)

# NAME ENTRY
fc=tk.StringVar()
fc = ttk.Entry(capture_mode,width = 10,textvariable = fc)
fc.grid(row=2,column=0,padx=(250,0),pady=(100,0),sticky=W)
fc.focus() # to set cursor position

ttk.Label(capture_mode, text="STATUS : ").grid(row=3,column=0,padx=(120,30),pady=(20,0),sticky=W)

fstat_l=ttk.Label(capture_mode,text= "")
fstat_l.grid(row=3,column=0,padx=(250,0),pady=(20,0),sticky=W)

ttk.Label(capture_mode, text="PROFILE PIC : ").grid(row=4,column=0,padx=(120,30),pady=(20,0),sticky=W)

fprogress = ttk.Progressbar(capture_mode, orient = HORIZONTAL, length = 590, mode = 'indeterminate') 
fprogress.grid(row=6,column=0,padx=(120,0),pady=(30,0),sticky=W)
fprogress.start(17)


def fex_reset():
    fstat_l.config(text="")
    fc.delete(0,tk.END)
    dp_url.delete(0,tk.END)

def dp_open():  # method to browse dp location
    global filename
    dp_url.delete(0,tk.END)
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    if filename.endswith('.jpg'):
        dp_url.insert(0,filename)
    else:
        fstat_l.config(text='ONLY JPG IMAGE ALLOWED !')
        filename = ''
    
def SAVE_DP():

    if os.path.isdir(os.path.join(os.getcwd(),f'images/{fc.get()}')):
        if filename != '':
            pn = os.path.join(os.getcwd(),f'images/{fc.get()}/{fc.get()}.jpg')
            copy(filename, pn)
            fstat_l.config(text='DP COPIED SUCCESSFULLY !')
        else:
            fstat_l.config(text='CHOOSE A JPG IMAGE !')

    else:
        fstat_l.config(text='FIRST CAPTURE FACE DATA !')

def cap():
    cb = capture_face_data.capture_biometrics(fc.get())
    fstat_l.config(text=cb)
    # os.chdir(os.path.dirname(os.getcwd())) # jump up to images
    # os.chdir(os.path.dirname(os.getcwd())) # jumpup to root

def ftrain():

    #==============================================================================================
    
    with open('root.csv','r') as rf:
        csv_reader_root = DictReader(rf,fieldnames = ['ROOT LOCATION'])
        for row in csv_reader_root:
            os.chdir(row['ROOT LOCATION'])

    #==============================================================================================

    # deleting previous trainer.yml
    if os.path.isfile('trainer.yml'):
        os.remove('trainer.yml')

    if os.path.isfile('labels.pickle'):    
        os.remove('labels.pickle')

    fstat_l.config(text='TRAINING IN PROGRESS........')

    # training started
    os.system('python faces_train.py')
    
    if os.path.isfile('trainer.yml'):
        fstat_l.config(text='FACE IDs TRAINED SUCCESSFULLY !')

# DP LOCATION
dp_url=tk.StringVar()
dp_url = ttk.Entry(capture_mode,width = 60,textvariable = dp_url)
dp_url.grid(row=4,column=0,padx=(250,0),pady=(20,0),sticky=W)

fbrowse_button = ttk.Button(capture_mode,text='BROWSE', command=dp_open)
fbrowse_button.grid(row=4,column=0,padx=(630,0),pady=(20,0),sticky=W)

cap_button = ttk.Button(capture_mode,text='CAPTURE FACE DATA',command=cap,width=25)
cap_button.grid(row=5,column=0,padx=(120,0),pady=(20,10),sticky=W)

freset_button = ttk.Button(capture_mode,text='RESET',command=fex_reset,width=20)
freset_button.grid(row=5,column=0,padx=(290,0),pady=(20,10),sticky=W)

train_button = ttk.Button(capture_mode,text='TRAIN MODEL',command=ftrain,width=20)
train_button.grid(row=5,column=0,padx=(440,0),pady=(20,10),sticky=W)

train_button = ttk.Button(capture_mode,text='SAVE DP',command=SAVE_DP,width=20)
train_button.grid(row=5,column=0,padx=(580,0),pady=(20,10),sticky=W)

root.mainloop()

