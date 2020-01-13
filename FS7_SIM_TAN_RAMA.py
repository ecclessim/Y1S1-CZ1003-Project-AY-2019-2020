##----------------------------------------------------------------------------
##  AUTHORS
##  Sim Jia Xuen Eccles
##  Tan Teck Heng, Eugene
##  Renganathan Ramasamy
##----------------------------------------------------------------------------
import tkinter as tk
from tkinter import messagebox,ttk
import time
import datetime
import json
from tkcalendar import DateEntry
from PIL import ImageTk, Image
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer

standardFont = ('calibri',20)
default_bg = "light grey"
stall_list = []
img_def = "images/pizza_bl.jpg"
global sel_hour,sel_minute,dateClassFlag,sel_date,todaylist,today,curr_time,select,sel_time
sel_hour = None
sel_minute = None
dateClassFlag = None
sel_date = None
todaylist = None
today = None
curr_time = None
select = None
sel_time = None

# Load JSON file into code
with open('db.json','r') as f:
    dbDict = json.load(f)
# Store the stall names into a list for access later
for stall in dbDict['Canteen'].keys():
    stall_list.append(stall)

# Master class for the Foodies@NTU
class CanteenApp(tk.Tk):        
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame = None
        self.switch_frame(Home) #Go to Homepage when start the program
    
    #Destroy current frame if exists and create a new frame
    def switch_frame(self,frame): 
        newFrame = frame(self)
        if self.frame != None:
            self.frame.destroy() 
        self.frame = newFrame
        self.frame.pack()

    #Background images
    def getImage(self,imageNo):
        img = Image.open(imageNo)
        img = img.resize((900,600), Image.ANTIALIAS)
        self.tkimage = ImageTk.PhotoImage(img)
        return self.tkimage

#  Home page containing the main features of the application
#  VIEW TODAY'S STORES | CHOOSE A CUSTOM DATE 
class Home(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        # Initialise mixer for music player
        mixer.init()
        
        # initialise flags and multiclass variables on Homepage
        # reset flags to default state
        global sel_hour,sel_minute,dateClassFlag,sel_date
        sel_hour = sel_minute = dateClassFlag = sel_date = None

        #User Interface on Homepage
        #Display background image
        tk.Label(self,image = master.getImage(img_def)).grid(sticky='nsew')
        # Digital clock function
        self.label = tk.Label(self, text = "", font = ('calibri', 25, 'bold'), width=55, background = 'light blue', foreground = 'black') 
        self.label.place(x = 0,y = 0)
        self.clock()

        #Background music button
        self.musicBtn = tk.Button(self, text="Play",bg='yellow',fg='black', font=('calibri',18),borderwidth=0 ,width=5,command = self.play)
        self.musicBtn.place(x=840,y=0)

        # State detector for the play/stop button, if music is playing, the button's name should be "Stop"
        if mixer.music.get_busy() == True:
            self.musicBtn.config(text="Stop")

        # Layout code for home page
        self.label1 = tk.Label(self,text="\nWelcome to Foodies@Northspine!\n",bg = "orange", borderwidth=0,width= 30,fg='black', anchor='center',font=standardFont).place(x = 250,y=100)
        self.button1 = tk.Button(self,text="View Today's Stores",bg="green",fg='PaleTurquoise2',borderwidth=0, width= 30,font=standardFont, command=lambda: master.switch_frame(ChooseStore)).place(x = 250,y = 230)
        self.button2 = tk.Button(self,text="Choose Date",bg = "green",fg='PaleTurquoise2',borderwidth=0,width= 30, font=standardFont, command=lambda: master.switch_frame(ChooseDate)).place(x = 250,y = 300)
        self.button3 = tk.Button(self,text="Exit",bg = 'red',fg='PaleTurquoise2', borderwidth=0,width= 30,font=standardFont,command= master.destroy).place(x = 250,y = 370)

    #Homepage functions
    #Clock Function for displaying the current time. Updates every second  
    def clock(self): 
        now = time.strftime('%A, %d %B, %H:%M:%S %p') 
        self.label.config(text = now) 
        self.label.after(1000, self.clock) #call itself in every 1000 millisecond which is 1 second

    #Background music to play if no music is playing otherwise it will stop if music is playing
    def play(self):
        if mixer.music.get_busy() == False: #check if the music is playing
            mixer.music.load('Music/jazz.mp3')
            mixer.music.play(-1)# loop is -1 to let the music keep playing
            self.musicBtn.config(text="Stop")
        else:
            self.musicBtn.config(text="Play")
            mixer.music.stop()

class ChooseStore(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        # initialise variables on ChooseStore page
        # list to store current date's open stalls
        global todaylist
        todaylist = []
        self.g_time()

        space = 0 # offset for spacing between widgets

        #User Interface on ChooseStore page
        #Display background image    
        tk.Label(self,image = master.getImage(img_def)).grid(sticky='nsew')

        #Label of the open stalls
        label0 = tk.Label(self,text=f'Showing open stalls for {today}, {curr_time}',font = ('calibri', 25, 'bold'),  width= 55, background = 'light blue', foreground = 'black')
        label0.place(x = 0,y = 0)
        
        # dynamic generation of buttons based on  todaylist
        for i,val in enumerate(todaylist):
            i += 1
            stallLbl = tk.Label(self,text=val,bg = "black",fg='light blue',font=standardFont, width= 15,anchor='w')
            stallBtn = tk.Button(self,text='Menu',bg="green",fg='PaleTurquoise2',width= 15 ,borderwidth=0,font=('calibri',16),command=lambda i = val: self.getSelection(i))
            stallLbl.place(x = 280,y = 100+space)
            stallBtn.place(x = 500,y = 100+space)
            space+=45

        #Back Button
        backBtn = tk.Button(self,text="Back",bg = 'red',fg='PaleTurquoise2',borderwidth=0, width= 30,font=standardFont,command=lambda: master.switch_frame(Home))
        backBtn.place(x =250,y = 500)

    #Functions on ChooseStore page
    #function comparison | displays stalls relative to current or user-defined datetime
    def g_time(self):
        global today,curr_time
        # get current date and time
        curr = datetime.datetime.now()
        curr_d_time = curr.strftime("%A,%H:%M")
        stringcurrtime = str(curr_d_time).split(",")
        today = stringcurrtime[0]
        curr_time = stringcurrtime[1]  
        # User input date and time | If dateClassFlag set, store user input.
        if dateClassFlag == True:
            if sel_date is not None and sel_time is not None:
                today = sel_date
                curr_time = sel_time
        # Compare stall's operating hours with the date and time specified (user/current)
        for i,val in enumerate(stall_list):
                for day,hour in dbDict['Canteen'][val]['hours'].items():
                    if today == day:
                        if dbDict['Canteen'][stall_list[i]]['hours'][day]['open'] <= curr_time <= dbDict['Canteen'][stall_list[i]]['hours'][day]['close']:
                            todaylist.append(stall_list[i])
                            break
                        else:
                            pass
                    else:
                        pass
  
    # pass selected button to stall page 
    def getSelection(self,selected):
        global select
        select = selected
        self.master.switch_frame(StallPage)

class ChooseDate(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        # initialise and reset flag and multiclass variables on ChooseDate page
        global sel_hour,sel_minute,dateClassFlag
        sel_hour = sel_minute = sel_date = sel_time = dateClassFlag = None

        #User Interface of ChooseDate page
        #Display Background Image
        tk.Label(self,image = master.getImage(img_def)).grid(sticky='nsew')
        
        # Values in dropdownlist for hours and minutes
        hours = [i for i in range(25)]
        minutes = [i for i in range(60)]
        
        # Arguments for dropdownlist widget (data type declaration for userinput)
        hourVar = tk.StringVar()
        minuteVar = tk.StringVar()

        #Date Label
        self.date_prompt = tk.Label(self,text="Date", width=8, bg = "black",fg='PaleTurquoise2', font=standardFont,anchor='center')
        self.date_prompt.place(x = 250,y = 50)
        
        # Date picker widget instantiation
        self.dateEnt = DateEntry(self,state="readonly",font=standardFont)
        self.dateEnt.bind("<<DateEntrySelected>>", self.print_date)
        self.dateEnt.place(x = 350,y = 50)

        #Display the date in the format of Friday 5 Nov 
        self.sel_date_lbl = tk.Label(self,text="Today",font=standardFont,bg="black",fg='PaleTurquoise2',anchor='center')
        self.sel_date_lbl.place(x = 550,y = 50)
        
        # Dropdown list for hours
        self.hour_label = tk.Label(self,text="Hour",width=8, font=standardFont,bg = "black",fg='PaleTurquoise2')
        self.hour_cbb = ttk.Combobox(self,state="readonly",font=standardFont,textvariable=hourVar,values=hours,width = 9)
        self.hour_cbb.bind("<<ComboboxSelected>>", self.print_time)
        self.hour_label.place(x = 250,y = 150)
        self.hour_cbb.place(x = 350,y = 150)
        
        # Dropdown list for minutes
        self.minute_label = tk.Label(self,text="Min",width=8, font=standardFont,bg = "black",fg='PaleTurquoise2')
        self.minute_cbb = ttk.Combobox(self,state="readonly",font=standardFont,textvariable=minuteVar,values=minutes,width = 9)
        self.minute_cbb.bind("<<ComboboxSelected>>", self.print_time)
        self.minute_label.place(x = 250,y = 200)
        self.minute_cbb.place(x = 350,y = 200)

        #Display the hour and minutes like like 12:05 if got user input
        self.sel_time_lbl = tk.Label(self,text="00:00",font=standardFont,bg = "black",fg='PaleTurquoise2',anchor='center')
        self.sel_time_lbl.place(x = 550,y = 150)

        #Submit Button
        self.submitBtn = tk.Button(self,text="Submit",bg = "green",fg='PaleTurquoise2',borderwidth=0, width = 30, font=standardFont,command=self.submitTime)
        self.submitBtn.place(x = 250,y = 350)
        
        #Back Button
        self.backBtn = tk.Button(self,text="Back",bg='red',fg='PaleTurquoise2',borderwidth=0, width = 30,font=standardFont,command=lambda: master.switch_frame(Home))
        self.backBtn.place(x =250,y = 400)

    #Functions for ChooseDate page
    #Check the user input for time
    def submitTime(self):
        global sel_hour,sel_minute,sel_date,sel_time,dateClassFlag
        ## Validation for empty user input
        if len(self.hour_cbb.get()) == 0 or len(self.minute_cbb.get()) == 0:
            messagebox.showwarning("Uh Oh!","Please select hours and minutes")
        else:
            sel_hour = int(self.hour_cbb.get())
            sel_minute = int(self.minute_cbb.get()) 
            sel_time = "{0:0=2d}".format(sel_hour) + ":" + "{0:0=2d}".format(sel_minute)
            sel_date = self.dateEnt.get_date().strftime("%A")
            dateClassFlag = True
            self.master.switch_frame(ChooseStore)
            
    #Configure the label based on user input of the date like Tuesday 5 Nov        
    def print_date(self,e):
        selD_display = self.dateEnt.get_date().strftime("%A %d %b")
        self.sel_date_lbl.config(text=selD_display)

    #Configure the label based on user input of hour and time like 12:05
    def print_time(self,e):
        if len(self.hour_cbb.get())==0 or len(self.minute_cbb.get())==0:
            pass
        else:
            selT_display = "{0:0=2d}".format(int(self.hour_cbb.get())) + ":" + "{0:0=2d}".format(int(self.minute_cbb.get()))
            self.sel_time_lbl.config(text=str(selT_display))

class StallPage(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        space = 0 # offset for spacing between widgets

        #Functions of the StallPage
        #Validation of only enter numbers
        def paxValidate(val):
            if val in [str(i) for i in range(0,10)]:
                return True
            return False
        
        #Calculate the pax timing and show the timing
        def calcPax(self):
            wait_time = int(dbDict['Canteen'][select]["waittime"])
            if len(paxEnt.get()) == 0:
                messagebox.showerror("Uh Oh!","I need some numbers!")
            else:
                pax_val = int(paxEnt.get())
                if pax_val > 25:
                    messagebox.showerror("Limit","Please enter a number 0-25!")
                    paxEnt.delete(0,'end')
                elif pax_val == 0:
                    messagebox.showinfo("No One","Queue is empty!")
                    paxEnt.delete(0,'end')
                else:
                    total_time = pax_val * wait_time
                    messagebox.showinfo("Information","Total Waiting Time: " + str(total_time) + " minutes")
                    paxEnt.delete(0,'end')

        #Get information of operating hours
        def show_op(self):
            dates=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
            info = []
            info1 = []
            info.append(select + "'s operating hours")
            storename= "".join(info) #Convert list into string
            for i in dates:
                open_H = dbDict["Canteen"][select]["hours"][i]["open"]
                close_H = dbDict["Canteen"][select]["hours"][i]["close"]
                if "closed" in open_H.lower().strip():
                    info1.append(i + ": " + "Closed\n")
                else:
                    info1.append(i + ":  " + open_H + " - " + close_H +" \n" )
            ophours="".join(info1) #Convert list into string
            messagebox.showinfo(storename,ophours)

        #User Interface of StallPage
        #bgImage gets the image from the JSON file and displays the relative file according to the stall
        bgImage = dbDict['Canteen'][select]["image"]
        tk.Label(self,image = master.getImage(bgImage)).grid(sticky='nsew')

        # time range for special menu
        breakfast = ("07:30","09:30")
        lunch = ("12:00","13:30")
        dinner = ("18:00","20:29")
        special_list = [breakfast,lunch,dinner]
        meal_list = ["breakfast","lunch","dinner"]
        
        #Name of the Stall
        self.stall_label = tk.Label(self, text=f"{select} MENU", fg='PaleTurquoise2',bg = "black",font=standardFont)
        self.stall_label.place(x = 360,y = 10)       
        
        #Show Operating Hours
        op_hour_btn = tk.Button(self,text="Operating Hours",borderwidth=3,font=('calibri',15),bg = "black",fg='Cyan',command=lambda:show_op(self))
        op_hour_btn.place(x = 600,y = 10)
        
        #Label to Calculate Waiting time
        paxLbl = tk.Label(self,text=f"Calculate waiting time for {select}",bg = "black",fg='PaleTurquoise2',font=("calibri",16))
        paxLbl.place(x= 150,y = 60)

        #Validation to calculate the pax timing
        vcmd = (self.register(paxValidate), '%S')
        paxEnt = tk.Entry(self,validate='key',vcmd=vcmd,bg='azure',fg='blue4', font=standardFont, width=10)
        paxEnt.bind("<Return>", (lambda event: calcPax(self)))
        paxEnt.place(x = 500,y = 60)

        #Button to calculate
        paxBtn = tk.Button(self,text="Calculate",font=("calibri",15),bg = "black",fg='Cyan',borderwidth=3,command=lambda:calcPax(self))
        paxBtn.place(x = 650,y = 60)

        #The label of item and price
        item_head_lbl = tk.Label(self,text='Item',bg = "black",width=8,fg="goldenrod1",font=standardFont)
        item_head_lbl.place(x = 250,y = 120)
        price_head_lbl = tk.Label(self,text='Price',bg = "black",width=8,fg="goldenrod1",font=standardFont)
        price_head_lbl.place(x= 545,y = 120)

        # Display menu (excluding special menu)  
        for item,price in dbDict['Canteen'][select]['standardmenu'].items():
            item_lbl = tk.Label(self,text=item,font=('calibri',15),bg = "black",fg='PaleTurquoise2',width=20,anchor='w')
            price_lbl = tk.Label(self,text="${:.2f}".format(price),font=('calibri',15),bg = "black",fg='PaleTurquoise2',width=20,anchor='center')
            item_lbl.place(x = 250,y = 170+space)
            price_lbl.place(x= 500,y = 170+space)
            space += 35

        # Display special menu (if condition fulfil)
        for i,val in enumerate(special_list):
            if val[0] <= curr_time <= val[1]:
                menuPair = dbDict['Canteen'][select][meal_list[i]].items()
                if len(menuPair) != 0: #if no special menu for the stall, not displaying the breakfast/lunch/dinner label
                    special_header = tk.Label(self, text=meal_list[i].upper(),font=standardFont,bg = "black", fg="goldenrod1", width=12)
                    special_header.place(x = 360, y=170+space)
                    for item,price in menuPair:
                        sp_item_lbl = tk.Label(self,text=item,font=('calibri',15),bg = "black",fg='goldenrod1',width=20,anchor='w')
                        sp_price_lbl = tk.Label(self,text="${:.2f}".format(price),font=('calibri',15),bg = "black",fg='goldenrod1',width=20,anchor='center')
                        sp_item_lbl.place(x = 250,y = 220+space)
                        sp_price_lbl.place(x = 500,y = 220+space)
                        space += 35
                else:
                    pass
            else:
                pass

        #Back Button
        self.home_btn = tk.Button(self, text='Back',bg='red',fg='PaleTurquoise2',borderwidth=0,width= 30,font=standardFont,command=lambda: master.switch_frame(ChooseStore))
        self.home_btn.place(x =250,y = 550)

app = CanteenApp()
app.title("NTU Foodies")
screenwidth = app.winfo_screenwidth()
screenheight = app.winfo_screenheight()
width = 900
height = 600
x = int((screenwidth/2) - (width/2))
y = int((screenheight/2) - (height/2))

app.geometry(f'{width}x{height}+{x}+{y}')
app.mainloop() 

## Thats all folks :)!
