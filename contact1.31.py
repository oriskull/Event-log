#!/usr/bin/env python
# -*- coding: utf-8 -*
from calendar import Calendar
from numbers import Number



try:
    # Python 2.x
    from Tkinter import *
    import tkFont
    import ScrolledText
    
except:
    # Python 3.x
    from tkinter import *
    import tkinter.font as tkFont
    import tkinter.scrolledtext as ScrolledText
    
import sqlite3
'''
import flask as Flask
app=Flask(__name__)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        do_the_login()
    else:
        show_the_login_form()
'''

global DICT

DICT=[
      ("יומן ארועים","Diary"),#0
      ("ארוע","Event"),#1
      ("הוספה","Add"),#2
      ("מחיקה","Delete"),#3
      ("חיפוש","Search"),#4
      ("ראה כולם","See all"),#5
      ("שפה","Language"),#6
      ("זכויות","License"),#7
      ("He<->En","En<->He"),#8
      ("כותרת","Title"),#9
      ("תיאור","Description"),#10
      ("יום","Date"),#11
      ("חודש","Email address"),#12
      ("שנה","Role"),#13
      ("פרטים","Adding data"),#14
      ("מחיקה","Deletion"),#15
      ("מחפש","Search"),#16
      ("לא נמצא אירוע","Contact not found"),#17
      ("נמצאו  {0} ארועים","Contact(s) found {0}"),#18
      ("חסרים נתונים","Incomplete capture"),#19
      ("נוסף אירוע חדש בהצלחה","That's all right !!! Contact added."),#20
      ("רשומות {0}  נמחקו","Record {0} deleted"),#21
      ("תו לא חוקי % התקבל","Generic character % accepted"),#22
      ("סוף הרשימה","End list"),#23
      ("עריכה","Changing data"),#24
      ("הנתונים נשמרו","That's all right !!! Changing data made")#25
      
      ]

LICENCE=[(
"""
Author : Orit Dan Maor ""","""

"""
)]

import sys

class App(Tk):
    
    def __init__(self):
        
        Tk.__init__(self)
        self.lang=1 # 0 Fr 1 En in index of DICT
        
        # Do it after call Tk() !
        # All StringVar are used with DICT[] to customize the messages and the labels
       
        self.var_delete=StringVar() 
        self.var_find,self.var_find2=StringVar(),StringVar() 
        self.var_add,self.var_add2,self.var_add3=StringVar(),StringVar(),StringVar()
        self.subtitle=StringVar()
        self.function_add=StringVar()
        self.function_del=StringVar()
        self.function_search=StringVar()
        self.name=StringVar()
        self.firstname=StringVar()
        # The Date
        
        self.day=StringVar()
        self.month=StringVar()
        self.year=StringVar()
        
        self.tiptxt=StringVar()
        self.end=StringVar()
        self.var1,self.var2,self.var3,self.var4,self.var5=StringVar(),StringVar(),StringVar(),StringVar(),StringVar()
        self.width,self.height=300,320
        self.geometry_string=str(self.width)+"x"+str(self.height)
        self.geometry(self.geometry_string)
        self.title("תרגיל בית")

        self.iconbitmap(default='dia_de_los_muertos256.ico')
       
       
       
        
        # The fonts
        
        self.font8=tkFont.Font(size=8)
        self.font12=tkFont.Font(size=12,weight="bold")
        self.font14=tkFont.Font(size=14,weight="bold")
        
        # The images
        self.img1=PhotoImage(file="add.ppm")
        self.img2=PhotoImage(file="delete.ppm")
        self.img3=PhotoImage(file="checkbox.ppm")
        self.img4=PhotoImage(file="remove.ppm")
        self.img5=PhotoImage(file="modify.ppm")
        self.img6=PhotoImage(file="next.ppm")
        
        # Zone Titre & bouton
        
        self.frame=Frame(self,bg="black")
        self.frame.pack(fill=BOTH,expand=True)
        
        self.title=Label(self.frame,textvariable=self.subtitle,fg="green",bg="black",pady=10,font=self.font14)
        self.title.pack(fill=X)
    
        self.menubar = Menu(self,tearoff=0)

        self.menu1=Menu(self.menubar,tearoff=0)
        self.menu1.add_command(label="Ajouter",command=lambda choice=1:self.add(choice))
        self.menu1.add_separator()
        self.menu1.add_command(label="Supprimer",command=lambda choice=1:self.operation(choice))
        self.menu1.add_separator()
        self.menu1.add_command(label="Chercher",command=lambda choice=2:self.operation(choice))
        self.menu1.add_separator()
        self.menu1.add_command(label="Afficher tout",command=self.print_all)
        
        self.menubar.add_cascade(label="Contact",menu=self.menu1)

        self.menu2=Menu(self.menubar,tearoff=0)
        
        self.menu2.add_command(label="Fr<->En",command=self.langage)
        
        self.menubar.add_cascade(label="A propos",menu=self.menu2)
        self.config(menu=self.menubar)
        
        # Zone Graphique

        self.zone=Canvas(self.frame,width=self.width,height=100,bg="#003E3E",bd=-1,highlightthickness=0)
        self.zone.pack()
        #self.zone.create_oval(0,0,self.width,80,fill="#006C6C",disableddash=15)
        self.text=self.zone.create_text(self.width/2,50,fill="green",text="")
        
        self.langage()
        self.mainloop()
    
    def langage(self,switch=None):
        '''
            Initialize variable for changing langage Hebrew<->English
        '''
        if switch==None: 
            if self.lang==0:
                self.lang=1
            else:
                self.lang=0
        
        self.subtitle.set(DICT[0][self.lang])       # Title
        
        # Sub Title for adding or changind data
        try:
            if self.choice==1:
                self.function_add.set(DICT[14][self.lang])
            else:
                 self.function_add.set(DICT[24][self.lang])
        except:
             self.function_add.set(DICT[14][self.lang])
             
        self.function_del.set(DICT[15][self.lang])
        self.function_search.set(DICT[16][self.lang])
        
        self.menubar.entryconfigure(0,label=DICT[1][self.lang])
        
        self.menu1.entryconfigure(0,label=DICT[2][self.lang])
        self.menu1.entryconfigure(2,label=DICT[3][self.lang])
        self.menu1.entryconfigure(4,label=DICT[4][self.lang])
        self.menu1.entryconfigure(6,label=DICT[5][self.lang])
        
        self.menubar.entryconfigure(1,label=DICT[6][self.lang])
        self.menu2.entryconfigure(1,label=DICT[7][self.lang])
        self.menu2.entryconfigure(2,label=DICT[8][self.lang])
        
        self.name.set(DICT[9][self.lang])
        self.firstname.set(DICT[10][self.lang])
        self.day.set(DICT[11][self.lang])
        self.month.set(DICT[12][self.lang])
        self.year.set(DICT[13][self.lang])
      
        try:
            self.var_find.set(DICT[18][self.lang].format(len(self.r)))
        except:
            self.var_find.set(DICT[18][self.lang])
            
        self.var_find2.set(DICT[17][self.lang])
        
        self.var_add.set(DICT[19][self.lang])
        self.var_add2.set(DICT[20][self.lang])
        self.var_add3.set(DICT[25][self.lang])
        
        try:
            self.var_delete.set(DICT[21][self.lang].format(self.id))
        except:
            self.var_delete.set(DICT[21][self.lang])
               
        self.tiptxt.set(DICT[22][self.lang])
        self.end.set(DICT[23][self.lang])
        
    def print_all(self):
        
        self.zone.destroy()
       
        try:
            self.canvas.destroy()
            self.canvas2.destroy()
        except:
            pass
        
        self.canvas=Canvas(self.frame,width=self.width,height=1,bg="black",highlightthickness=0)
        self.canvas.pack(pady=10)
        self.st=ScrolledText.ScrolledText(self.canvas,bg="black",fg="green")
        bdd.mycursor.execute("select * from mycontacts")
        self.r=bdd.mycursor.fetchall()
        self.st.tag_config("line1", background="#2A6FC9",foreground="#A1F6F7",justify=CENTER)
        self.st.tag_config("line2", foreground="white",justify=CENTER)
        for e in self.r:
            self.st.insert(END,e[1]+"\n", ("line1"))
            self.st.insert(END,e[2]+"\n",("line2"))
            self.st.insert(END,e[3]+"\n",("line2"))
         
            #self.st.insert(END,"="*39+"\n")
        self.st.pack()
       

    def operation(self,choice=None):
        
        self.zone.destroy()
       
        try:
            self.canvas.destroy()
            self.canvas2.destroy()
        except:
            pass
        
        self.canvas=Canvas(self.frame,width=self.width,height=1,bg="black",highlightthickness=0)
        self.canvas.pack(pady=10)
        # 1 for Delete
        if choice==1:
            self.title=Label(self.canvas,textvariable=self.function_del,bg="black",fg="#8beddc",font=self.font12)
        # 2 for search
        elif choice==2:
            self.title=Label(self.canvas,textvariable=self.function_search,bg="black",fg="#8beddc",font=self.font12)
            
        self.title.grid(columnspan=5,sticky=E+W)
        self.lbl1=Label(self.canvas,text=" תאריך",bg="#000000",fg="white")
        self.lbl1.grid(row=1,sticky=NW)
        self.e1=Entry(self.canvas,bg="white",fg="blue")
        self.e1.grid(row=1,column=1,columnspan=2,sticky=NW)
        
         ### BINDING ###
        
        self.e1.bind("<KeyRelease>",self.dynamic_search)
        self.e1.bind("<Motion>",self.tipin)
        self.e1.bind("<Leave>",self.tipout)
         ### BINDING ###
         
        self.e1.focus()
        self.b1=Button(self.canvas,image=self.img3,command=lambda choice=choice:self.find(choice))
        self.b1.image=self.img3
        self.b1.grid(row=1,column=3,sticky=W)
     
    def dynamic_search(self,event):
        self.find()
    
    def tipin(self,event):
        self.tip=Label(self.canvas,textvariable=self.tiptxt,bg="black",fg="green")
        self.tip.grid(row=2,columnspan=4,sticky=E+W)
    
    def tipout(self,event):
        self.tip=Label(self.canvas,text=" "*30,bg="black",fg="green")
        self.tip.grid(row=2,columnspan=4,sticky=E+W)
        try:
            if len(self.r)!=0:
                self.lblx=Label(self.canvas,textvariable=self.var_find,bg="black",fg="green")
                self.lblx.grid(row=2,columnspan=4,sticky=E+W)
        except:
            pass
        
    def find(self,choice=None):
        
        res=0
    
        query_title="select * from mycontacts where title like '"+str(self.e1.get())+"%'"
        bdd.mycursor.execute(query_title)
        res=len(bdd.mycursor.fetchall())
        
        if res !=0:
            self.r=bdd.mycursor.fetchall()
        else:
            query_details="select * from mycontacts where details like '"+str(self.e1.get())+"%'"
            bdd.mycursor.execute(query_details)
            res=len(bdd.mycursor.fetchall())
            if res !=0:
                self.r=bdd.mycursor.fetchall()
           
            else:
                query_date="select * from mycontacts where date like '"+str(self.e1.get())+"%'"
                bdd.mycursor.execute(query_date)
                self.r=bdd.mycursor.fetchall()
        #self.r=bdd.mycursor.fetchall()
        
        if len(self.r)!=0:
            self.langage(1)
            self.lblx=Label(self.canvas,textvariable=self.var_find,bg="black",fg="green")
            self.lblx.grid(row=2,columnspan=4,sticky=E+W)
            self.pointer=0
            self.show(choice)
        else:
            try:
                self.canvas2.destroy()
            except:
                pass
            self.lbl5=Label(self.canvas,textvariable=self.var_find2,bg="green",fg="black",activeforeground="green")
            self.lbl5.grid(row=2,columnspan=4,sticky=E+W)
    
    def show(self,choice): 
    # Option = 1 for delete, 2 for search
        try:
            self.canvas2.destroy()
        except:
            pass
        self.canvas2=Canvas(self.frame,width=self.width,height=1,bg="black",highlightthickness=0)
        self.canvas2.pack()
        
        i=0
        self.frame2=Frame(self.canvas2,width=self.width)
        self.frame2.grid(row=2+i,columnspan=4,sticky=E+W)
        
        self.label2=[Label(self.canvas)] *5 # ID or record
        self.label3=[Label(self.canvas)] *5 # Name of record
        self.label4=[Label(self.canvas)] *5 # First name of record
        
        while self.pointer<len(self.r) and i<5:
        #for i,e in enumerate(self.r):
            i+=1
           
            self.label2[i-1]=Label(self.canvas2,text=self.r[self.pointer][0],bg="black",fg="white",activeforeground="green")
            self.label3[i-1]=Label(self.canvas2,text=self.r[self.pointer][1],bg="black",fg="white",activeforeground="green")
            self.label4[i-1]=Label(self.canvas2,text=self.r[self.pointer][2],bg="black",fg="white",activeforeground="green")
            
            self.label2[i-1].grid(row=2+i,column=0,sticky=E+W)
            self.label3[i-1].grid(row=2+i,column=1,sticky=E+W)
            self.label4[i-1].grid(row=2+i,column=2,sticky=E+W)
           
            ### Bind on the fields displayed ##
            
            self.label2[i-1].bind("<Motion>",lambda event,pointer=self.pointer:self.tiptel(event,pointer))
            self.label3[i-1].bind("<Motion>",lambda event,pointer=self.pointer:self.tiptel(event,pointer))
            self.label4[i-1].bind("<Motion>",lambda event,pointer=self.pointer:self.tiptel(event,pointer))
            
            self.label2[i-1].bind("<Leave>",lambda event,pointer=self.pointer:self.tiptelout(event,pointer))
            self.label3[i-1].bind("<Leave>",lambda event,pointer=self.pointer:self.tiptelout(event,pointer))
            self.label4[i-1].bind("<Leave>",lambda event,pointer=self.pointer:self.tiptelout(event,pointer))
            
            if choice==1:
                self.bx=Button(self.canvas2,image=self.img4,width=16,command=lambda id=self.r[self.pointer][0]:self.delete(id))
                self.bx.image=self.img4
                self.bx.grid  (row=2+i,column=3,sticky=E)
            else:
                self.bx=Button(self.canvas2,image=self.img5,width=16,command=lambda choice=2,id=self.r[self.pointer][0]:self.add(choice,id))
                self.bx.image=self.img5
                self.bx.grid  (row=2+i,column=3,sticky=E)

            self.pointer+=1
            
            # END loop
            
        if self.pointer<len(self.r):
                 self.next=Button(self.canvas2,image=self.img6,command=lambda choice=choice:self.show(choice))
                 self.next.image=self.img6
                 self.next.grid(row=i+4,columnspan=5)
        else:
                self.msg=Label(self.canvas2,textvariable=self.end)
                self.msg.grid(row=i+4,columnspan=5)
                
    def tiptel(self,event,pointer):   
       
       self.c=Canvas(self.canvas2,width=self.width,height=48,bg="#008080",highlightthickness=0)
       self.c.grid(row=10,columnspan=5,sticky=E+W,pady=5)
       #self.i=self.canvas.create_image(50,17,image=PhotoImage (file="tel.gif"))
       self.j=self.c.create_text(150,24,text="תאריך : "+str(self.r[pointer][3])+"\n",fill="#1CE68C")
    
    def tiptelout(self,event,pointer):
       self.c.destroy()
       self.c=Canvas(self.canvas2,width=self.width,height=48,bg="black",highlightthickness=0)
       self.c.grid(row=10,columnspan=5,sticky=E+W)
    
    def delete(self,id=None):
            bdd.mycursor.execute("delete  from mycontacts where id=?",(id,))
            bdd.write()
            self.id=id
            self.langage(1)
            self.msg=Label(self.canvas2,text="None",textvariable=self.var_delete,bg="green",fg="black")
            self.msg.grid(row=12,columnspan=4,sticky=E+W)
            #self.var.set("Enregistrement %d supprimé..." %id)
            
    def add(self,choice=1,id=None):
        
        # Option = 1 for adding 2 for changing
        self.choice=choice
        
        self.langage(1)
        
        self.zone.destroy()
        try:
            self.canvas.destroy()
            self.canvas2.destroy()
        except:
            pass
        
        self.canvas=Canvas(self.frame,width=self.width,height=10,bg="black",highlightthickness=0)
        self.canvas.pack(pady=10)
        
        self.title=Label(self.canvas,textvariable=self.function_add,bg="black",fg="#8beddc",font=self.font12)
        self.title.grid(row=1,columnspan=4,sticky=E+W)
        
        self.lbl1=Label(self.canvas,textvariable=self.name,bg="#000000",fg="#FA0750")
        self.lbl1.grid(row=2,sticky=NW)
        
        self.lbl2=Label(self.canvas,textvariable=self.firstname,bg="#000000",fg="#FA0750")
        self.lbl2.grid(row=3,sticky=NW)
        
        self.lbl3=Label(self.canvas,textvariable=self.day,bg="#000000",fg="#FA0750")
        self.lbl3.grid(row=4,sticky=NW)
        
        self.lbl4=Label(self.canvas,textvariable=self.month,bg="#000000",fg="#FA0750")
        self.lbl4.grid(row=5,sticky=NW)
        
        self.lbl5=Label(self.canvas,textvariable=self.year,bg="#000000",fg="#FA0750")
        self.lbl5.grid(row=6,sticky=NW)
        
        self.e1=Entry(self.canvas,textvariable=self.var1,bg="white",fg="blue")
        self.e1.grid(row=2,column=1)
        self.e1.focus()
        self.e2=Entry(self.canvas,textvariable=self.var2,bg="white",fg="blue")
        self.e2.grid(row=3,column=1)
        self.e3=Entry(self.canvas,textvariable=self.var3,bg="white",fg="blue")
        self.e3.grid(row=4,column=1)
        self.e4=Entry(self.canvas,textvariable=self.var4,bg="white",fg="blue")
        self.e4.grid(row=5,column=1)
        self.e5=Entry(self.canvas,textvariable=self.var5,bg="white",fg="blue")
        self.e5.grid(row=6,column=1)
        self.reset()  
              
        # Retrieve values if modify
        if self.choice==2: # Changing data
            self.function_add.set(DICT[24][self.lang])
            bdd.mycursor.execute("select * from mycontacts where id=?",(id,))
            self.r=bdd.mycursor.fetchall()
            self.var1.set(self.r[0][1])
            self.var2.set(self.r[0][2])
            self.var3.set(self.r[0][3])
          #  self.var4.set(self.r[0][4])
          #  self.var5.set(self.r[0][5])
            
            # Button for changing data
            self.b1=Button(self.canvas,image=self.img5,font=self.font8,command=lambda choice=2:self.insert_change(choice,id))
            self.b1.image=self.img1
            self.b1.grid(row=7,pady=10,columnspan=2)
        
        if self.choice==1: 
            
            # Button for adding data
            
            self.b1=Button(self.canvas,image=self.img1,font=self.font8,command=lambda choice=1:self.insert_change(choice))
            self.b1.image=self.img1
            self.b1.grid(row=7,pady=10,columnspan=2)
            
        self.b2=Button(self.canvas,image=self.img2,font=self.font8,command=self.reset)
        self.b2.image=self.img2
        self.b2.grid(row=7,column=1,pady=10,columnspan=2) 
    
    def insert_change(self,choice=1,id=None):
        
        # Option = 1 for adding 2 for changing
        
        if self.e1.get()!="" and self.e2.get()!="" and self.e3.get()!="":
            # Adding Data
            date_full= self.e5.get()+"-"+self.e4.get()+"-"+self.e3.get()
            if choice==1:
                bdd.mycursor.execute("insert into mycontacts values (?,?,?,?)",
                                  (None,self.e1.get(),self.e2.get(),date_full)
                                  )
                self.reset()
                self.msg=Label(self.canvas,textvariable=self.var_add2,bg="green",fg="black")
                self.msg.grid(row=8,columnspan=4,sticky=E+W)
            else:
                # Changing data
                query="update mycontacts set title='{0}',details='{1}',date='{2}' where id={3}".format(self.e1.get(),self.e2.get(),date_full,id)
                bdd.mycursor.execute(query)
                self.msg=Label(self.canvas,textvariable=self.var_add3,bg="green",fg="black")
                self.msg.grid(row=11,columnspan=4,sticky=E+W)
            bdd.write()
            
        else:
            # Incomplete Capture
            self.msg=Label(self.canvas,textvariable=self.var_add,bg="green",fg="black")
            self.msg.grid(row=11,columnspan=4,sticky=E+W)
    
    def reset(self):
            self.e1.delete(0,END)
            self.e2.delete(0,END)
            self.e3.delete(0,END)
            self.e4.delete(0,END)
            self.e5.delete(0,END)
            self.e1.focus()
    
    def gnu(self):
        
        self.zone.destroy()
       
        try:
            self.canvas.destroy()
            self.canvas2.destroy()
        except:
            pass
        self.canvas=Canvas(self.frame,width=self.width,height=self.height,bg="black",highlightthickness=2)
        self.canvas.pack(pady=10)
        id=self.canvas.create_text(self.width/2,100,fill="white",justify=CENTER,text=LICENCE[0][self.lang])
        
class Conn:
    
    def __init__(self):
        
        self.conn = sqlite3.connect("./contacts")
        self.mycursor=self.conn.cursor()
        self.mycursor.execute("create table if not exists mycontacts (id INTEGER PRIMARY KEY,title,details,date)")
       
        self.mycursor.execute('select * from mycontacts')
        #print (self.mycursor.fetchall())
    
    def write(self):
        self.conn.commit()
        
###############################
#
# START 
###############################
if __name__=="__main__":
    bdd=Conn()
    app=App()
    bdd.mycursor.close()
