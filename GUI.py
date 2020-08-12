from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import messagebox
import Main as mp
import real_time_yolo as yv
#import yolo_video as yv
import speed_check as sp
import database as db
import imageio
import cv2
import os
import shutil
import tkinter
import sqlite3

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        '''
        self.master = master
        self.pos = []
        self.line = []
        self.rect = []
        self.master.title("GUI")
        self.pack(fill=BOTH, expand=1)

        self.counter = 0
        '''
        '''
        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)
        submenu = Menu(file)
        file.add_command(label="Load Image", command=self.open_image)
        file.add_command(label="Load Video", command=self.open_video)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)
        submenu.add_command(label="detection")
        submenu.add_command(label="speed check")
        submenu.add_cascade(label='Load Video', menu=submenu, underline=0)
        '''

        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        fileMenu = Menu(menubar)

        submenu = Menu(fileMenu)
        submenu.add_command(label="detection", command=self.open_video_detect)
        submenu.add_command(label="speed check", command=self.open_video_speed)
        fileMenu.add_cascade(label='Video', menu=submenu, underline=0)

        fileMenu.add_separator()

        fileMenu.add_command(label="Exit", underline=0, command=self.client_exit)
        fileMenu.add_command(label="Image", underline=0, command=self.open_image)
        menubar.add_cascade(label="File", underline=0, menu=fileMenu) 

        self.filename = "images/logo.jpg"
        self.imgSize = Image.open(self.filename)
        self.tkimage =  ImageTk.PhotoImage(self.imgSize)
        self.w, self.h = (1066, 768)
        
        self.canvas = Canvas(master = root, width = self.w, height = self.h)
        self.canvas.create_image(20, 20, image=self.tkimage, anchor=NW)
        self.canvas.grid(row=0,column=0,columnspan=2)
        # self.canvas.pack()



    def open_image(self):
        self.filename = filedialog.askopenfilename()
        shutil.copy(self.filename,'LicPlateImages/preview.jpg')
        global number
        number=mp.main()
        myLabel1 = Label(root, text="License Plate Number :  ")
        myLabel1.grid(row=0,column=1)
        myLabel = Label(root, text=number)
        myLabel.grid(row=0,column=2)
        #myLabel.pack()
        self.show_image('LicPlateImages/preview1.jpg')
        #messagebox.showinfo("License plate Info","license plate number:"+licPlate)


        f_name_Label = Label(root,text="FIRST NAME: ")
        f_name_Label.grid(row=1,column=1)
        l_name_Label = Label(root,text="LAST NAME: ")
        l_name_Label.grid(row=2,column=1)
        add_Label = Label(root,text="ADDRESS: ")
        add_Label.grid(row=3,column=1)
        cnt_no_Label = Label(root,text="CONTACT NUMBER: ")
        cnt_no_Label.grid(row=4,column=1)

        f_name = Label(root,text=" ")
        f_name.grid(row=1,column=2,padx=20,pady=(10,0))
        l_name = Label(root,text=" ")
        l_name.grid(row=2,column=2,padx=20,pady=(10,0))
        add = Label(root,text=" ")
        add.grid(row=3,column=2,padx=20,pady=(10,0))
        cnt_no = Label(root,text=" ")
        cnt_no.grid(row=4,column=2,padx=20,pady=(10,0))

        #add info button
        add_btn=Button(root,text="Add record",command=self.add)
        add_btn.grid(row=5,column=1,pady=10,padx=10,ipadx=100,columnspan=2)

        #edit info button
        edit_btn=Button(root,text="Edit record",command=self.edit)
        edit_btn.grid(row=6,column=1,pady=10,padx=10,ipadx=100,columnspan=2)

        self.query()

        #refresh info button
        refresh_btn=Button(root,text="Refresh",command=self.query)
        refresh_btn.grid(row=7,column=1,pady=10,padx=10,ipadx=100,columnspan=2)

    def show_image(self, frame):
        self.imgSize = Image.open(frame)
        self.tkimage =  ImageTk.PhotoImage(self.imgSize)
        self.w, self.h = (1066, 768)
        self.canvas.destroy()
        self.canvas = Canvas(master = root, width = self.w, height = self.h)
        self.canvas.create_image(0, 0, image=self.tkimage, anchor=NW)
        self.canvas.grid(row=0,column=0,rowspan=7)
        #self.canvas.pack()
        
        
    def open_video_detect(self):
        self.filename = filedialog.askopenfilename()
        shutil.copy(self.filename,'videos/preview.mp4')
        yv.main()
        #os.system("outpy.avi")
        #os.remove("videos/preview.mp4")
        
    def open_video_speed(self):
        self.filename = filedialog.askopenfilename()
        shutil.copy(self.filename,'videos/preview.mp4')
        #sp.main()
        sp.trackMultipleObjects()
        #os.system("outpy.avi")
        #os.remove("videos/preview.mp4")

    def query(self):
    
        #create db or coneect to db
        conn = sqlite3.connect('database.db')
        #create cursor
        cursor=conn.cursor()
        q="""SELECT * FROM info WHERE lic_no= ?"""
        cursor.execute(q,(number,))
        records=cursor.fetchall()
        #print(records)
        if len(records)==0:
            f_name = Label(root,text=" ")
            f_name.grid(row=1,column=2,padx=20,pady=(10,0))
            l_name = Label(root,text=" ")
            l_name.grid(row=2,column=2,padx=20,pady=(10,0))
            add = Label(root,text=" ")
            add.grid(row=3,column=2,padx=20,pady=(10,0))
            cnt_no = Label(root,text=" ")
            cnt_no.grid(row=4,column=2,padx=20,pady=(10,0))
        else:
            global fname
            global lname
            global addr
            global cnt
            #loop through records
            for record in records:
                f_name = Label(root,text=record[1])
                f_name.grid(row=1,column=2,padx=20,pady=(10,0))
                fname=record[1]
                l_name = Label(root,text=record[2])
                l_name.grid(row=2,column=2,padx=20,pady=(10,0))
                lname=record[2]
                add = Label(root,text=record[3])
                add.grid(row=3,column=2,padx=20,pady=(10,0))
                addr = record[3]
                cnt_no = Label(root,text=record[4])
                cnt_no.grid(row=4,column=2,padx=20,pady=(10,0))
                cnt = record[4]
        #save changes
        conn.commit()
        #close connection
        conn.close()

    def client_exit(self):
        exit()


    def add(self):
        db.main(number)
        self.query()
        

    def edit(self):
        db.Main(number,fname,lname,addr,cnt) 
        self.query() 

root = Tk()
app = Window(root)
root.geometry("%dx%d"%(1366, 768))
root.title("Traffic Violation")

root.mainloop()