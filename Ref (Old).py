############################IMPORT LIBRARIES#######################
from datetime import *
import os
from tkinter import *
import tkinter as tki
from tkinter import ttk
from os import system, name
import pathlib
from tkinter.filedialog import askdirectory
from difflib import SequenceMatcher
from tkinter import filedialog
from gtts import gTTS
import sys
import random
#from docx import Document
import glob
import os.path
from idlelib.tooltip import Hovertip
from tkinter import messagebox


os.chdir("/home")
os.system("rm -rf readoutloud.mp3")

######################### Make window ############################
rootwin=Tk() #Tk window
rootwin.title("Referencing")


bgcolor="aliceblue"
accentcolor="lightcyan1"
accentcolor2="lightcyan2"
textcolor="black"

rootwin.configure(bg=bgcolor)



############### Window dimensions ###############
width=1150
maxheight=800
minheight=135
rootwin.geometry(str(width)+"x"+str(maxheight))



####################################### Entry boxes for data ###########################
#'for' indicates whether it should be shown for that medium
#'cap' indicates whether data from that box should be auto capitalised.
boxes=[{"name":"type","labelname":"typelabel","text":"Type","value":None,"forbook":True,"forjournal":True,"forweb":True,"fored":True,"forchap":True,"cap":False},
       {"name":"title","labelname":"titlelabel","text":"Title","value":None,"forbook":True,"forjournal":True,"forweb":True,"fored":True,"forchap":True,"cap":True},
       {"name":"edition","labelname":"editionlabel","text":"Edition","value":None,"forbook":True,"forjournal":False,"forweb":False,"fored":False,"forchap":False,"cap":False},
       {"name":"surname","labelname":"surnamelabel","text":"Surname","value":None,"forbook":True,"forjournal":True,"forweb":False,"fored":False,"forchap":False,"cap":False},
       {"name":"initials","labelname":"initialslabel","text":"Initials","value":None,"forbook":True,"forjournal":True,"forweb":False,"fored":False,"forchap":False,"cap":False},
       {"name":"editorsur","labelname":"edsurlabel","text":"Editor surname","value":None,"forbook":False,"forjournal":False,"forweb":False,"fored":True,"forchap":True,"cap":True},
       {"name":"editorini","labelname":"edinilabel","text":"Editor initials","value":None,"forbook":False,"forjournal":False,"forweb":False,"fored":True,"forchap":True,"cap":True},
       {"name":"publisher","labelname":"publisherlabel","text":"Publisher","value":None,"forbook":True,"forjournal":False,"forweb":False,"fored":True,"forchap":True,"cap":True},
       {"name":"city","labelname":"citylabel","text":"City","value":None,"forbook":True,"forjournal":False,"forweb":False,"fored":True,"forchap":True,"cap":True},
       {"name":"year","labelname":"yearlabel","text":"Year","value":None,"forbook":True,"forjournal":True,"forweb":True,"fored":True,"forchap":True,"cap":False},
       {"name":"journal","labelname":"journallabel","text":"Journal","value":None,"forbook":False,"forjournal":True,"forweb":False,"fored":False,"forchap":False,"cap":True},
       {"name":"volume","labelname":"volumelabel","text":"Volume","value":None,"forbook":False,"forjournal":True,"forweb":False,"fored":False,"forchap":False,"cap":False},
       {"name":"issue","labelname":"issuelabel","text":"Issue","value":None,"forbook":False,"forjournal":True,"forweb":False,"fored":False,"forchap":False,"cap":False},
       {"name":"chapter","labelname":"chapterlabel","text":"Chapter title","value":None,"forbook":False,"forjournal":False,"forweb":False,"fored":False,"forchap":True,"cap":True},
       {"name":"pages","labelname":"pageslabel","text":"Pages","value":None,"forbook":False,"forjournal":True,"forweb":False,"fored":False,"forchap":False,"cap":False},
       {"name":"url","labelname":"urllabel","text":"URL","value":None,"forbook":True,"forjournal":True,"forweb":True,"fored":True,"forchap":True,"cap":False},
       {"name":"org","labelname":"orglabel","text":"Name/ Orgnisation","value":None,"forbook":False,"forjournal":False,"forweb":True,"fored":False,"forchap":False,"cap":True},
       {"name":"access","labelname":"accesslabel","text":"Date accessed","value":str((datetime.now()).strftime("%d/%m/%Y")),"forbook":False,"forjournal":False,"forweb":True,"fored":False,"forchap":False,"cap":True},
       {"name":"written","labelname":"writtenlabel","text":"Date written","value":None,"forbook":False,"forjournal":False,"forweb":True,"fored":False,"forchap":False,"cap":True},

       {"name":"citation","labelname":"citelabel","text":"Citation","value":None,"forbook":True,"forjournal":True,"forweb":True,"fored":True,"forchap":True,"cap":True},
       {"name":"reference","labelname":"reflabel","text":"Reference","value":None,"forbook":True,"forjournal":True,"forweb":True,"fored":True,"forchap":True,"cap":True}]

radios=[{"name":"Verbatim", "o1":"v1", "o2":"v2", "labelname":"verblabel","text":"Verbatim","row":7},
        {"name":"Access", "o1":"u1", "o2":"u2", "labelname":"accesslabel","text":"Access","row":8}]
for x in boxes:
    x["labelname"]=Label(rootwin,text=x["text"],bg="aliceblue")
    x["name"]=Entry(rootwin)

    
###############List of surnames entered #################
surnames=[]
initials=[]
def shownames():
    global surnames

  
    namesbox.delete(0,END)
    for s in surnames:
        #print(s)
        namesbox.insert(0,s)
    
def store(event=None): #save surnames to list to allow more to be added

    

    dots("Initials")
    dots("Editor initials")
    
    for x in boxes:
        if x["text"]=="Surname":
            if len([char for char in x["name"].get()]) >0:
                word=[char for char in x["name"].get()]
                word.insert(0,word[0].upper())
                word.remove(word[1])
                wordstr=''
                for w in word:
                    wordstr=wordstr+w
                surnames.append(wordstr)
                x["name"].delete(0,"end")
        else:
            pass

        if x["text"]=="Initials":
            initials.append(x["name"].get())
            x["name"].delete(0,"end")
    shownames()
    boxes[3]["name"].focus_set()
    
    namesbox.configure(bg="white")
def deletenames(event=None): #Delete last surname
    global surnames
    global initials
    surnames.remove(surnames[-1])
    initials.remove(initials[-1])
    if len(surnames)<1:
        namesbox.configure(bg=bgcolor)
    shownames()

def deleteallnames(event=None): #Clear list of surnames
    global surnames
    global initials
    surnames=[]
    initials=[]
    namesbox.configure(bg=bgcolor)
    shownames()
    
################ Clear all boxes and replace with correct ones ###################
def Refresh(med):
    #authorgroup.grid(row=0,column=0)

    for x in radios:
        x["name"]=IntVar()
        try:
            x["labelname"].destroy()
            x["o1"].destroy()
            x["o2"].destroy()
        except:
            pass
  
    

    x["labelname"]=Label(text=x["text"],bg="aliceblue",font=("Verdana",10))
    print(x)
    x["o1"]=Radiobutton(rootwin,text="Yes",variable=x["name"],value=1,bg="aliceblue")
    x["o2"]=Radiobutton(rootwin,text="No",variable=x["name"],value=0,bg="aliceblue")
    x["o1"].invoke()
    x["labelname"].grid(row=x["row"],column=0,sticky="w")
    x["o1"].grid(column=1,row=x["row"],sticky="w")
    x["o2"].grid(column=1,row=x["row"])


    ######################## Show list of surnames entered ###############
    global namesbox
    while True:
        try:
            deletenames()
        except:
            break
    for x in boxes:
        x["name"].destroy()
        x["labelname"].destroy()
        x["labelname"]=Label(text=x["text"],bg="aliceblue",font=("Verdana",10))
        x["name"]=Entry(relief="flat",bd=4,width=60,highlightcolor="aliceblue")
        if x[med]==True:
            x["labelname"].grid(row=boxes.index(x)+50,column=0,sticky="w")
            x["name"].grid(row=boxes.index(x)+50,column=1,sticky="w")
        if x["text"]=="Project":
            search()
            switch()
    surnames=[]
    initials=[]

    if locked==True:
        for x in boxes:
            if x["value"]!=None:
                x["name"].insert(0,x["value"])
    else:
        for x in boxes:
            if "Date accessed" in x["text"]:
                x["name"].insert(0,x["value"])
   
    namesbox=Listbox(rootwin,relief="flat",bg=bgcolor,bd=0,highlightthickness=0)
    #namesbox=Label(rootwin,text=str(surnames),bg="aliceblue")
    namesbox.grid(column=2,row=20,columnspan=30,rowspan=50,sticky="w")
    search()
    
    makechardrop()

def cleareverything():
    #authorgroup.destroy()
    for x in radios:
        x["name"]=IntVar()
        try:
            x["labelname"].destroy()
            x["o1"].destroy()
            x["o2"].destroy()
        except:
            pass
    for x in boxes:
        x["name"].destroy()
        x["labelname"].destroy()
    namesbox.destroy()
    
    
    


        
def book(event=None):
    restore()
    Refresh("forbook")
    boxes[0]["name"].delete(0,END)
    boxes[0]["name"].insert(0,"book")
    
    
def journal(event=None):
    restore()
    Refresh("forjournal")
    boxes[0]["name"].delete(0,END)
    boxes[0]["name"].insert(0,"journal")
    

def web(event=None):
    restore()
    Refresh("forweb")
    boxes[0]["name"].delete(0,END)
    boxes[0]["name"].insert(0,"web")
    
    try:
        namesbox.destroy()
    except:
        pass
    
    namesbox.destroy()
def ed(event=None):
    Refresh("fored")

################# Minimise ######################

def restore(event=None):
    rootwin.geometry(str(width)+"x"+str(maxheight))
    #ribbon()

    
def minimise(event=None):
    rootwin.geometry(str(width)+"x"+str(minheight))
    updateheader()
    
    #menubar.destroy()
    
  

####################### Insert citation into citation box from entered data ####################
def ins(box,text,sep):
    for x in boxes:
        if x["text"]==text:
            boxes[box]["name"].insert("end",x["value"]+str(sep))

def put(For):
    for x in boxes:
        if x[For]==True:
            x["value"]=x["name"].get()

#################### Arrange the multple authors into a single string ####################
def authors(box):
    global surnames
    global initials
    store("z")

    for x in surnames:
        if len([char for char in x])==0 or "&" in x or "-" in x:
            surnames.remove(x)
    for x in initials:
        if len([char for char in x])==0 or "&" in x or "-" in x:
            initials.remove(x)

    def arr(s):
        boxes[len(boxes)+box]["name"].insert("end",s)
    if len(surnames)==0:

        
        ins(len(boxes)+box,"Surname"," ")
        if box==-2:
            ins(len(boxes)+box,"Initials",",")
    
        
    elif len(surnames)==1:
        if box==-1:
            arr((surnames[0]+str(" ")+initials[0])+str(", "))
        elif box==-2:
            arr((surnames[0])+str(", "))
        
    elif len(surnames)==2:
        if box==-1:
            arr((surnames[0]+str(" ")+initials[0]+str(" & ")+surnames[1]+str(" ")+initials[1])+str(", "))
        elif box==-2:
            arr((surnames[0]+str(" & ")+surnames[1]+str(", ")))
    
    elif len(surnames)>2:
        if box==-2:
            arr((surnames[0]+" et al., "))
        elif box==-1:
            for x in range(len(surnames)):
                arr(surnames[x]+str(" ")+initials[x]+", ")

####################Change CWD###########################
def switch(event=None):
    os.chdir(str(projdrop.cget("text")))
    showcite() 
    showref()
    updateheader()
    #openproj()

    


    

################## Search for reference lists #########################
def search(event=None):
    global f
    global projdrop
    global activelists
    
    lists=[]
    none=True
    
    for x in os.walk("/home/jonathan/Documents"):
        if "Ref.txt" in str(x):
            lists.append(x[0])
    sel=StringVar()

    activelists=[]
    for l in lists:
        file=open(l+"/"+"Ref.txt","r")
        
        if "#FINISHED#" in str(file.readlines()):
            pass
        else:
            activelists.append(l)
            none=False
    
    if none==False:
        try:
            prev=projdrop.cget("text")
            sel.set(prev)
        except:
            sel.set(activelists[0])
        
        try:
            projdrop.destroy()
        except:
            pass
        
        if hidden==False:
            projdrop=OptionMenu(filegroup,sel,*activelists,command=switch)
        elif hidden==True:
            projdrop=OptionMenu(filegroup,sel,*lists,command=switch)
        projdrop.config(background="white")
        #projdrop.config(bg="azure")
        projdrop["borderwidth"]=0
        projdrop["highlightthickness"]=0
        projdrop.grid(row=0,column=100,sticky="w")
        #projlabel=Label(text="Project: ",bg="aliceblue",font=("Verdana",10))
        #projlabel.grid(row=5,column=0,sticky="w")
        switch()
        showcite()
        showref()
        
    else:
        newlist()


########################### Mark lists for non active projects as finished but don't delete it #########
def finished(event=None):
    if (len(activelists))>1:
        file=open(str(projdrop.cget("text")+"/"+"Ref.txt"),"a")
        file.write("\n #FINISHED#")
        file.close()
        search()
        reload()
    else:
        messagebox.showwarning(title=None, message="There must be at least one active list")
        
        


hidden=False


############################## Display all the lists that have been hidden ##################
def showhidden(event=None):
    global hidden
    if hidden==True:
        hidden=False
    elif hidden==False:
        hidden=True
    else:
        hidden=False
    reload()

######################### Mark a hidden list as not hidden #############################
def unhide(event=None):
    lines=[]
    file=open(str(projdrop.cget("text")+"/"+"Ref.txt"),"r")
    for x in file.readlines():
        if "#FINISHED#" not in str(x):
            lines.append(x)
            
    file.close()
    file=open(str(projdrop.cget("text")+"/"+"Ref.txt"),"w")
    for i in lines:
        file.write("\n"+str(i)+"\n")
    
    
    
###################### List of citations ####################
def showcite():
    global setcite
    global citedrop
    global citations
    global citelist
    '''
    try:
        file=open("Ref.txt","r")
        n=int(file.readlines()[0].split(";")[6])

        if n>0:
            order()
        else:
            alphabetise()
    except:
        pass
    '''
 
    try:
        citedrop.destroy()
    except:
        pass
    citelist=[]
    try:
        file=open("Ref.txt")
        for x in file.readlines():
            c=x.split(";")[0]
            if len(c)>2:
                citelist.append(x.split(";")[0])
            
        file.close()

        def setcite():
            global citations
            global citelist
            global citedrop
            #citelist.sort()
            citations=StringVar()
            try:
                citations.set(citelist[0])
                citedrop=ttk.Combobox(listgroup,textvariable=citations,width=50)
                citedrop.bind('<<ComboboxSelected>>', synccite)
                citedrop['values']=citelist
                citedrop.grid(row=0,column=0,sticky="w",columnspan=50)
                
                
            except:
                pass
    except:
        pass
    setcite()
    
        

#################### Search box ####################



def move(d):
    try:
        selectplace.set(places[places.index(selectplace.get())+d])
    except:
        try:
            selectplace.set(places[0])
        except:
            pass
def movedown(event=None):
    move(1)
def moveup(event=None):
    move(-1)
rootwin.bind("<Down>",movedown)
rootwin.bind("<Up>",moveup)
def find(event=None):
    global searchbox
    global selectplace
    global searchdrop

    global places
    
    
    searchbox=Entry(searchgroup,relief="flat")
    searchbox.grid(row=0,column=0)
    
    
    searchbox.config(bg=bgcolor)

    rootwin.bind("<Return>",launchsearch)
    places=["✱","👥","𝐓","⩳"] #everywhere, authors, title, full text (doesn't work yet)
    selectplace=StringVar()
    selectplace.set(places[0])
    searchdrop=OptionMenu(searchgroup,selectplace,*places)
    searchdrop.config(bg=bgcolor)
    searchdrop["borderwidth"]=0
    searchdrop["highlightthickness"]=0
    searchdrop.configure()
    searchdrop.grid(row=0,column=1)
    ribbon.select(filtertab)
    searchbox.focus_set()




def launchsearch(event=None):
    if len(searchbox.get())>0:
        searchrefs()

def searchrefs():
    file=open("Ref.txt")
    for x in file.readlines():
            try:
                if "✱" in str(selectplace.get()):
                    
                    if str(searchbox.get()).upper() in str(x).upper():
                        try:
                            references.set(x.split(";")[5])
                        except:
                            references.set(x.split(";")[1])
                        citations.set(x.split(";")[0])
                elif "👥" in str(selectplace.get()):
                    
                    if str(searchbox.get()).upper() in str(x.split(";")[0]).upper():
                        try:
                            references.set(x.split(";")[5])
                        except:
                            references.set(x.split(";")[1])
                        citations.set(x.split(";")[0])
                elif "𝐓" in str(selectplace.get()):
                    try:
                        if str(searchbox.get()).upper() in str(x.split(";")[5]).upper():
                            references.set(x.split(";")[5])
                            citations.set(x.split(";")[0])
                    except:
                        if str(searchbox.get()).upper() in str(x.split(";")[1]).upper():
                            references.set(x.split(";")[1])
                            citations.set(x.split(";")[0])
               
            except:
                pass
    searchbox.delete(0,END)
    ribbon.select(citationtab)












############################ List of references ################################
def showref():
 
    global refdrop
    global references
    global reflist
    global reflabel
    global setref

    try:
        refdrop.destroy()
    except:
        pass
    reflist=[]
    file=open("Ref.txt")
    for x in file.readlines():
        chars=[]
        for char in x:
            if char.upper() not in chars:
                chars.append(char.upper())
            
        if len(chars)>2 and "#FINISHED#" not in str(x):
            try:
                reflist.append(x.split(";")[5])
            except: 
                reflist.append(x.split(";")[1])
    file.close()

    def setref():
        global references
        global citations
        global refdrop
        #reflist.sort()
        references=StringVar()
        try:
            references.set(reflist[0])
            citations.set(citelist[0])
            refdrop=ttk.Combobox(listgroup,textvariable=references,width=50)
            refdrop.bind('<<ComboboxSelected>>', syncref)
            refdrop['values']=reflist
            refdrop.grid(row=1,column=0,sticky="w")
            
        except:
            pass
    setref()

def syncref(event=None):
    citations.set(citelist[reflist.index(references.get())])
    copyref()
def synccite(event=None):
    references.set(reflist[citelist.index(citations.get())])
    copycite()
    
########################## Copy to clipboard ##########################

def copy(n):
    rootwin.clipboard_clear()
    file=open("Ref.txt","r")
    for x in file.readlines():
        if refdrop.get().replace("...","") in x:
            rootwin.clipboard_append(str(x.split(";")[n]))

##################### Copy reference to clipboard #####################

def copyref(event=None):
    copy(1)

##################### Copy index number to clipboard #####################
def copy_index(event=None):
    copy(6)

##################### Copy citation to clipboard #####################
def copycite(event=None):
    rootwin.clipboard_clear()
    rootwin.clipboard_append("["+citedrop.get()+"]")
    

################# When reference is clicked, go to its PDF or URL
def openrefweb(event=None):
    file=open("Ref.txt","r")
    for x in file.readlines():
        if refdrop.get().replace("...","") in x:
                os.system("xdg-open "+str(x.split(";")[2]))
    file.close()



def openrefpdf(event=None):
    done=False
    file=open("Ref.txt","r")
    for x in file.readlines():
        
        stripped=str(refdrop.get()[0:len(refdrop.get())-1])
        try:
            if stripped.replace("...","") in x.split(";")[1]:
                if ".pdf" in str(x.split(";")[3]):
                    os.system("xdg-open "+str(x.split(";")[3]))
                    
                    done=True
        except:
            pass
    if done==False:
        messagebox.showwarning(title="No PDF Found", message="There is no PDF associated with this reference.")
        openrefweb()
    file.close()
        
################### Delete reference list ################
def yes():
    os.system("rm Ref.txt")
    reallywin.destroy()
    search()
def no():
    reallywin.destroy()
    
def delete():
    global reallywin
    switch()
    reallywin=Tk()
    fname=str(os.getcwd()).split("/")[-1]
    really=Label(reallywin,text="Really delete reference list for "+str(fname)+"?")
    really.pack()
    for x in range(10):
        nobtn=Button(reallywin,text="No",command=no)
        nobtn.pack()
    yesbtn=Button(reallywin,text="Yes",command=yes)
    yesbtn.pack()
    for x in range(10):
        nobtn=Button(reallywin,text="No",command=no)
        nobtn.pack()
    
    
    
    

#####################Put dots in initials ############################
def dots(text):
    chars=[]
    for x in boxes:
      
        if x["text"]==text:
            for char in (x["name"].get()):
                char=char.upper()
                char=char.replace(char,char+".")
                chars.append(char)
           
            x["name"].delete(0,"end")
            for char in chars:
                x["name"].insert("end",char)

def capitalise(text):
    words=[]
    for x in boxes:
        if x["text"]==text:
            for i in (x["name"].get().split(" ")):
                words.append(i[0].upper()+i[1:])
            words=str(words).replace(",","").replace("[","").replace("]","").replace("'","")
            x["name"].delete(0,"end")
            x["name"].insert(0,words)


######################## Check to see if information is missing ###################
def checkboxes(box,For):
    global missing
    for i in boxes:
        if box in i["text"] and i[For]==True:
            if(len(i["name"].get()))<1 and "Surname" not in i["text"] and "Initial" not in i["text"]:
                missing=True
            elif(len(i["name"].get()))<1 and "Surname" in i["text"]:
                if len(surnames)<1:
                    missing=True
                else:
                    pass
            elif(len(i["name"].get()))<1 and "Initial" in i["text"]:
                if len(surnames)<1:
                    missing=True
                else:
                    pass
def warnmissing():
    if missing==True:
            messagebox.showwarning(title=None, message="Information missing")
    

def checksame(For):
    checkboxes("Title",For)
    checkboxes("Year",For)
    checkboxes("URL",For)
    
######################## Make citation and reference out of entered data ##################
def cite(event=None):
    global missing
    missing=False
    switch()
    for x in boxes:
        try:
            if x["cap"]==True:
                capitalise(x["text"])
        except:
            pass
    boxes[len(boxes)-2]["name"].delete(0,"end")
    boxes[len(boxes)-1]["name"].delete(0,"end")

    
    if "book" in boxes[0]["name"].get():
        put("forbook")
        checksame("forbook")
        checkboxes("Edition","forbook")
        checkboxes("Surname","forbook")
        checkboxes("Initials","forbook")
        checkboxes("Publisher","forbook")
        checkboxes("City","forbook")
        
        
        warnmissing()
        if missing==False:
            authors(-2)
            ins(len(boxes)-2,"Year","")
            ins(len(boxes)-1,"Title",", ")
            ins(len(boxes)-1,"Edition",", ")
            authors(-1)
            ins(len(boxes)-1,"Publisher",", ")
            ins(len(boxes)-1,"City","")
        
    elif "journal" in boxes[0]["name"].get():
        put("forjournal")
        checksame("forjournal")
        
        checkboxes("Journal","forjournal")
        checkboxes("Volume","forjournal")
        checkboxes("Issue","forjournal")
        checkboxes("Pages","forjournal")
        checkboxes("Surname","forjournal")
        checkboxes("Initials","forjournal")
        warnmissing()
        if missing==False:
            authors(-2)
            ins(len(boxes)-2,"Year","")
            authors(-1)
            ins(len(boxes)-1,"Year",", ")
            ins(len(boxes)-1,"Title",", ")
            ins(len(boxes)-1,"Journal",", ")
            ins(len(boxes)-1,"Volume",", ")
            ins(len(boxes)-1,"Issue",", ")
            ins(len(boxes)-1,"Pages","")
            
    elif "web" in boxes[0]["name"].get():
        put("forweb")
        checksame("forweb")
        checkboxes("Name/ Orgnisation","forweb")
        checkboxes("Date accessed","forweb")
        checkboxes("Date written","forweb")
        warnmissing()
        if missing==False:
            ins(len(boxes)-2,"Name/ Orgnisation",", ")
            ins(len(boxes)-2,"Year","")
            ins(len(boxes)-1,"Title"," ")
            boxes[len(boxes)-1]["name"].insert("end", ("(online), "))
            ins(len(boxes)-1,"URL",", ")
            ins(len(boxes)-1,"Date accessed",", ")
            ins(len(boxes)-1,"Date written","")
        
    elif "ed" in boxes[0]["name"].get():
        put("fored")
        ins(len(boxes)-2,"Editor surname",",")
        ins(len(boxes)-2,"Year","")
        ins(len(boxes)-1,"Editor surname"," ")
        ins(len(boxes)-1,"Editor initials",",")
        boxes[len(boxes)-1]["name"].insert("end", ("(ed.),"))
        ins(len(boxes)-1,"Year",",")
        ins(len(boxes)-1,"Publisher",",")
        ins(len(boxes)-1,"City","")
    else:
        boxes[0]["name"].delete(0,END)
        boxes[0]["name"].insert("book")
    
    if radios[0]["name"].get()==1:
        pass
    
    elif radios[0]["name"].get()==0:
        #boxes[-2]["name"].insert(0,"After ")
        pass
        
    ############# Link pdf of paper #######################
    p=filedialog.askopenfilename(title="Link PDF")

  

    ######################### Assemble citation ###################################
    
    file=open("Ref.txt","r")
    otherlines=[]
    dates=[]
    for i in file.readlines():
        if ";" in str(i) and len(i)>8:
            
            otherlines.append(i)

            dates.append(int(i.split(";")[6]))
    print(dates)
    file.close()

    
    file=open("Ref.txt","a")
    
    ref=str(boxes[-1]["name"].get())
    cite=str(boxes[-2]["name"].get())
    adr=str(boxes[-6]["name"].get())
    sep=str(";")
    
    try:
        line=str("\n")+cite+sep+ref+sep+adr+sep+str(p)
    except:
        line=str("\n")+cite+sep+ref+sep+adr+sep+str("")

    for x in radios:
        if "Access" in x["text"]:
            if int(x["name"].get())==1:
                line=line+sep+"Yes"
            else:
                line=line+sep+"No"
    t=boxes[1]["name"].get()
    
    line=line+sep+t+sep+str(max(dates)+1)+sep

    
  

    ################## Check for duplicates #########
    '''
    sims=[]
    simwin=Tk()
    simlist=Listbox(simwin,width=150)
    simlist.pack()

    delbtn=Button(simwin,text="🗑")
    delbtn.pack()
    def similar(a,b):
        s=float(SequenceMatcher(None,a,b).ratio())
        if s>0.7:
            sims.append(str(a)+str("=")+str(s)+str(" similar to ")+str(b))
            
            simlist.insert(END,str(a)+str("=")+str(s)+str(" similar to ")+str(b))
    for i in otherlines:
        similar(i,line)
    '''
    
    ################# Write citation to file ##################

    file.write("\n"+line+"\n")
    file.close()
    rootwin.clipboard_clear()
   
    for b in boxes:
        if b["text"]=="Citation":
            rootwin.clipboard_append(b["name"].get())
    
    search()
    
    
    
    
    ######################### Check that the reference has been recorded ###############
    file=open("Ref.txt","r")
    
    r=str(boxes[-1]["name"].get())
    d=str(file.readlines())

    
            
    
    if r in d:
        messagebox.showinfo(title="Success", message="Reference was successfully recorded.")
        reload()
        ribbon.select(citationtab)
        cleareverything()
        minimise()
        order_asc()
        
        for i in citelist:
            #print(i)
            if r in i:
                citations.set(i)
                synccite()
        
        
        
    else:
        messagebox.showerror(title="Error", message="There was an error recording this reference.")
######################## Show reference list ############################################
def show(event=None):
    try:
        switch()
        os.system("gnome-text-editor "+str("Ref.txt"))
    except:
        pass

def showex(event=None):
    try:
        switch()
        os.system("libreoffice --calc  "+str("Ref.txt"))
    except:
        pass

############## Insert special characters ####################
def inschar(event=None):
    try:
        boxes[0]["name"].focus_get().insert("end",drop.cget("text"))
        clicked.set("Ω")
    except:
        print("No box selected")

chars=['á','à','ä','è','é','ê','ë','ï','í','ö','ó','ò','ù','ú','ü','ł','β']
clicked=StringVar()
clicked.set("Ω")
def makechardrop():
    global drop
    drop=OptionMenu(chargroup,clicked,*chars,command=inschar)
    drop.config(bg=bgcolor)
    drop["borderwidth"]=0
    drop["highlightthickness"]=0
    drop.grid(row=0,column=1)


####################################### Open contaning folder #################
def fold(event=None):
    path=(projdrop.cget("text"))
    os.system("nautilus "+path)

###################### Make new refernece list #####################
def newlist(event=None):
    f=askdirectory()

    try:
        os.chdir(f)
        newfile=open("Ref.txt","a")
        
        newfile.close()
        search()
    except:
        pass
   
    
##################### Refresh window ##################
def reload(event=None):
    showcite()
    showref()
    search()

################# Update window header with project title #############
def updateheader():
    try:
        rootwin.title(str(projdrop.cget("text")).split("/")[-1])
    except:
        pass


#################### Proofread document ##########################

def txtsave(f):
    messagebox.showinfo(title=None, message="Save your document as a "+f+" file and then choose it here.")
    
def proofread(event=None):
    
    lines=[]
    os.chdir(projdrop.cget("text"))
    txtsave(".txt")
    try:
        progwin=Tk()
        progtext="Reading File"
        proglabel=Label(progwin,text=progtext)
        proglabel.pack()
        
        for x in open(filedialog.askopenfilename()).readlines():
            lines.append(str(x).strip())
        
        
        lines=str(lines).replace("'","").replace("ufeff","").replace("[","").replace("]","")
        language = 'en'

        progtext=progtext+"\n"+"Generating Audio"
        proglabel.configure(text=progtext)
        
        speak = gTTS(text=str(lines), lang=language, slow=False)
        
        progtext=progtext+"\n"+"Saving Audio"
        proglabel.configure(text=progtext)
        
        speak.save("readoutloud.mp3")
        
        progtext=progtext+"\n"+"Playing Audio"
        proglabel.configure(text=progtext)
        
        os.system("xdg-open readoutloud.mp3")
        progwin.destroy()
        
    except:
        pass
    
#################### Google scholar ##############################

def google():
    os.system("vivaldi "+"https://scholar.google.com")


################### Pin Project ##########################
def pin():
    f=str(os.getcwd().split("/")[-1])
    os.chdir("..")
    
    os.system("mv "+f+" 0"+f)
    search()
    #switch()
    messagebox.showwarning(title="Restart Required", message="A restart is required for this to take effect")
    sys.exit()
    

def unpin():
    f=str(os.getcwd().split("/")[-1])
    os.chdir("..")
    
    os.system("mv "+f+" "+f.replace("0",""))

##################launch tag program ##################
def tags():
    os.system("python3 /home/jonathan/Documents/Keele/Course/Notes/Home/tags.py")


############## Keep values between refreshes ###################
locked=True
def locktext(event=None):
    global locked
    if locked==False:
        locked=True
        
    else:
        locked=False
    
locktext()

################ For testing, fill boxes with random data ######

letters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
def fill(event=None):
    for x in boxes:
        
        string=""
        for i in range(random.randint(2,30)):
            string=str(string+random.choice(letters))#

        if "Type" in x["text"] or "Citation" in x["text"] or "Reference" in x["text"]:
            pass
        else:
            x["name"].delete(0,END)
            x["name"].insert(0,string)

#################Open project document#####################################

def openproj():
    try:
        file=open("project.txt","r")
        for i in file.readlines():
            os.system('xdg-open '+'"'+str(i)+'"')
    except:
        proj=filedialog.askopenfilename(title="Choose project file")
        file=open("project.txt","w")
        file.write(proj)
        os.system('xdg-open '+'"'+str(proj)+'"')

def changeproj():
    os.system("rm project.txt")
    openproj()

####################### Check for unused citations ###############


########################## Filter citations by accessibility and used state #############################
def showall():
    reload()
    showref()
    showcite()

def loading():
    global references
    global citations
    references.set("Loading...")
    citations.set("Loading...")
    
def check_used():
    global read
    global used
    global unused
    global rused
    global runused
    global access
    global no_access
    global raccess
    global rno_access
    global used_access
    global used_no_access
    global unused_access
    global unused_no_access
    global rused_access
    global rused_no_access
    global runused_access
    global runused_no_access
    global txtread
    global rtfread
    
    try:
        print(used)
    except:
            
        txtsave(".txt")
        while True:
            f=filedialog.askopenfilename(title="Choose .txt file")
            if ".txt" in str(f):
                break
            else:
                messagebox.showwarning(title="Invalid format", message="Must be a .txt file")
                break
        txtfile=open(f,"r")
        txtread=str(txtfile.readlines()).upper()
        txtfile.close()

        txtsave(".rtf")
        
        while True:
            f=filedialog.askopenfilename(title="Choose .rtf file")
            if ".rtf" in str(f):
                break
            else:
                messagebox.showwarning(title="Invalid format", message="Must be a .rtf file")
                break
        
        
        
        rtffile=open(f,"r")
        rtfread=str(rtffile.readlines()).upper()
        rtffile.close()

   
    
    try:
        refdrop.destroy()
        citedrop.destroy()
    except:
        pass
    refdrop=ttk.Combobox(rootwin,textvariable=references,width=70)
    refdrop.bind('<<ComboboxSelected>>', syncref)
    citedrop=ttk.Combobox(rootwin,textvariable=citations,width=70)
    citedrop.bind('<<ComboboxSelected>>', syncref)
    
    used=[]
    unused=[]
    rused=[]
    runused=[]
    access=[]
    no_access=[]
    raccess=[]
    rno_access=[]
    used_access=[]
    used_no_access=[]
    unused_access=[]
    unused_no_access=[]
    rused_access=[]
    rused_no_access=[]
    runused_access=[]
    runused_no_access=[]
  
    file=open("Ref.txt")
    for z in file.readlines():
        l=len(z)
        if l>1:
            c=str(z.split(";")[0])
            r=str(z.split(";")[5])
            cu=str(z.split(";")[0]).upper()
            
            if cu in txtread or cu in rtfread:
                #print("✔ "+c+"    "+z.split(";")[4])
                used.append(c)
                rused.append(r)

                if "Yes" in str(z.split(";")[4]):
                    access.append(c)
                    raccess.append(r)
                    used_access.append(c)
                    rused_access.append(r)
                    
                elif "No" in str(z.split(";")[4]):
                    no_access.append(c)
                    rno_access.append(r)
                    used_no_access.append(c)
                    rused_no_access.append(r)
                
                
            elif cu not in rtfread and cu not in txtread:
                #print("    ❌ "+c+"    "+z.split(";")[4])
                unused.append(c)
                runused.append(r)
                
                if "Yes" in str(z.split(";")[4]):
                    access.append(c)
                    raccess.append(r)
                    unused_access.append(c)
                    runused_access.append(r)
                elif "No" in str(z.split(";")[4]):
                    no_access.append(c)
                    rno_access.append(r)
                    unused_no_access.append(c)
                    runused_no_access.append(r)
  
    
def u(r,c):
    global loadwin
    citelist=[]
    reflist=[]
    for i in c:
        citelist.append(i)
    for i in r:
        reflist.append(i)
    citations.set(citelist[0])
    references.set(reflist[0])
    refdrop['values']=reflist
    citedrop['values']=citelist

def export_view():
    e=open("export.txt","w")
    for i in citelist:
        e.write(i+"\n")

    for i in reflist:
        e.write(i+"\n")
    e.close()
    os.system("xdg-open export.txt")
    
    


    
def show_unused():
    loading()
    check_used()
    u(runused,unused)
    
def show_used():
    loading()
    check_used()
    u(rused,used)
            
def show_access():
    loading()
    check_used()
    u(raccess,access)
    

def show_no_access():
    loading()
    check_used()
    u(rno_access,no_access)

def show_used_access():
    loading()
    check_used()
    u(rused_access,used_access)

def show_used_no_access():
    loading()
    check_used()
    u(rused_no_access,used_no_access)

def show_unused_access():
    loading()
    check_used()
    u(runused_access,unused_access)

def show_unused_no_access():
    loading()
    check_used()
    u(runused_no_access,unused_no_access)


        
    
    

######################## Delete specific reference ###############
def yesdel():
    delref()
    reallydelwin.destroy()
    search()
def nodel():
    reallydelwin.destroy()
    
def areyousure():
    global reallydelwin
    reallydelwin=Tk()
    really=Label(reallydelwin,text="Really delete "+str(refdrop.get())+"?")
    really.pack()
    
    for x in range(5):
        nobtn=Button(reallydelwin,text="No",command=nodel)
        nobtn.pack()
    yesbtn=Button(reallydelwin,text="Yes",command=yesdel)
    yesbtn.pack()
    for x in range(5):
        nobtn=Button(reallydelwin,text="No",command=nodel)
        nobtn.pack()
 
    
def delref():
    lines=[]
    file=open("Ref.txt","r")
    for x in file.readlines():
        lines.append(x)
    for x in lines:
        if refdrop.get() in x:
            
            lines.remove(x)
    file.close()
    file=open("Ref.txt","w")
    for x in lines:
        file.write("\n"+x+"\n")
    file.close()



############################ Edit reference ##################
def edit():
    pass

############### Dark mode #################

def makedark():
    rootwin.configure(bg="Black")
    for i in boxes:
        i["name"].configure(bg="Black")
#makedark()

######################## Sort list in alphabetical order ###############
def alphabetise():
    lines=[]
    file=open("Ref.txt","r")
    for x in file.readlines():
        if len(str(x))>7:
            lines.append(x)
    file.close()
    lines.sort()
    
    
    file=open("Ref.txt","w")
    for x in lines:
        file.write(x)
    file.close()
    reload()

def alpha_by_citation():
    lines=[]
    file=open("Ref.txt","r")
    for x in file.readlines():
        lines.append(x)
    def name(line):
            return str(line.split(";")[0])
    lines.sort(key=name)
    file.close()
    
    file=open("Ref.txt","w")
    for x in lines:
        file.write(x)
        #print(x)
    file.close()
    reload()

def alpha_by_title():
    lines=[]
    file=open("Ref.txt","r")
    for x in file.readlines():
        lines.append(x)
    def title(line):
      return str(line.split(";")[5])
    lines.sort(key=title)
    file.close()
    
    file=open("Ref.txt","w")
    for x in lines:
        file.write(x)
        #print(x)
    file.close()
    reload()

###################### Sort list by date #######################
def order(d):
    lines=[]
    file=open("Ref.txt","r")
    for x in file.readlines():
        if len(x)>5:
            lines.append(x)
    def num(line):
 
        return int(line.split(";")[6])
   
    lines.sort(reverse=d, key=num)
    file.close()
    
    file=open("Ref.txt","w")
    for x in lines:
        file.write(x)
        #print(x)
    file.close()

    reload()


def order_asc():
    order(True)
def order_desc():
    order(False)

##################### Notepad #####################
def shrink():
        
    notepad.configure(width=int(notepad.winfo_width()/10)-10)

def grow():
       
    notepad.configure(width=int(notepad.winfo_width()/10)+10)
def shownotes(event=None):
    global notepad
    global closenotesbtn
    global shrinkbtn
    global growbtn
    global openbtn
    try:
        notepad.destroy()
    except:
        pass
    notepad=Text(rootwin,bg="lightyellow",width=50)
    notepad.grid(row=1,column=100,rowspan=100)

    try:
        file=open("refnotes.txt","r")
        
    except:
        file=open("refnotes.txt","w")
        file.close()
        file=open("refnotes.txt","r")
    for x in file.readlines():
        notepad.insert(END,str(x))
    file.close()
    rootwin.geometry(str(int(width*1.6))+"x"+str(maxheight))
    letters=['<BackSpace>','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0']
    for i in letters:
        rootwin.bind(i,savenotes)

    closenotesbtn=Button(text="🞭",command=hidenotes,bg="lightyellow",relief="flat")
    closenotesbtn.grid(row=50,column=101)

    
    shrinkbtn=Button(text="〈",command=shrink,bg="lightyellow",relief="flat")
    shrinkbtn.grid(row=51,column=101)
    growbtn=Button(text="〉",command=grow,bg="lightyellow",relief="flat")
    growbtn.grid(row=52,column=101)
    openbtn=Button(text="🗔",command=opennotes,bg="lightyellow",relief="flat")
    openbtn.grid(row=53,column=101)
    rootwin.bind("<Control-Left>",hidenotes)
    

def savenotes(event=None):
    try:
        if len(str(notepad.get("1.0",END)))>1:
            file=open("refnotes.txt","w")
            file.write(notepad.get("1.0",END))
            file.close()
    except:
        pass

def hidenotes(event=None):
    savenotes()
    notepad.destroy()
    closenotesbtn.destroy()
    shrinkbtn.destroy()
    growbtn.destroy()
    openbtn.destroy()
    rootwin.geometry(str(width)+"x"+str(maxheight))

def opennotes():
    os.system("xdg-open refnotes.txt")
    hidenotes()

################## Settings window #################################
def settings():
    setwin=Tk()
    brackets=StringVar()
    bracketlist=["[]","()","{}","<>","None"]
    action=StringVar()
    actionlist=["Copy","Open PDF","Open URL","Edit","None"]
    drops=[{"labelname":"Bracket_label","Text":"Brackets","name":"bracketdrop","var":brackets,"command":None,"list":bracketlist, "row":0, "col":1},
           {"labelname":"Action_label","Text":"Action on clicking citation","name":"actiondrop","var":action,"command":None,"list":actionlist, "row":1, "col":1}]

    for i in drops:
        i["name"]=ttk.Combobox(setwin,textvariable=i["var"],width=70)
        i["name"].bind('<<ComboboxSelected>>', i["command"])
        i["name"]['values']=i["list"]
        i["name"].grid(row=i["row"],column=i["col"],columnspan=50)
        i["name"].set(i["list"][0])
        i["labelname"]=Label(setwin,text=i["Text"])
        i["labelname"].grid(row=i["row"],column=i["col"]-1)

############## Testing Mode ########################################
# Show buttons for functions which aren't finished yet
betamode=False
def beta():
    global betamode
    if betamode==True:
        betamode=False
    elif betamode==False:
        betamode=True
    ribbon()


################## Check for unused files #########################

def check_unused_files():
    chars=[" ","[","]","'",")",")"]
    files=[]
    notfound=[]
    for x in os.walk(os.getcwd()):
        x=str(x)
        for i in x.split(","):
            
            if ".pdf" in i:
                for char in chars:
                    i=i.replace(char,"")
                    i=i.upper()
                #print(i)
                files.append(i)
    file=open("Ref.txt","r")
    text=file.readlines()
    filenames=[]
    for t in text:
        try:
            filenames.append(str(t.split(";")[3]).upper())
        except:
            pass
    file.close()
    ufile=open("unused_files.txt","w")
    message=""
    
    for file in files:
        
        if file.upper() in str(filenames) or "19004395" in str(file):
            #print("✔ "+file)
            pass
        else:
            print(file)
            message=message+(str("\n"+file+"\n"))
    ufile.write(message)
    ufile.close()
    os.system("xdg-open unused_files.txt")
    #tk.messagebox.showwarning(title=None, message="These files were found in the project folder but haven't been used: "+message)
            
    
            
####################### Menu bar #################################

def ribbon():
    
    global filegroup
    global listgroup
    global searchgroup
    global buttons
    global filtertab
    global ribbon
    global citationtab
    global chargroup
    global authorgroup

    
    
    ribbon=ttk.Notebook(rootwin)
    style = ttk.Style()
    style.configure('TNotebook.Tab', font=('Verdana', 10),background=bgcolor, foreground=textcolor, padding=[10,5])
    style.map("TNotebook.Tab",background=[("active", accentcolor)],font=[("active",("Verdana",10,"bold underline"))])
    style.map("TNotebook.Tab",background=[("selected", accentcolor)],font=[("selected",("Verdana",10,"bold underline"))])
    style.configure('TNotebook',borderwidth=0)
    
    filetab=Frame(ribbon,bg=accentcolor,relief="flat")
  

    viewtab=Frame(ribbon,bg=accentcolor,relief="flat")
    citationtab=Frame(ribbon,bg=accentcolor,relief="flat")
    filtertab=Frame(ribbon,bg=accentcolor,relief="flat")
    citetab=Frame(ribbon,bg=accentcolor,relief="flat")
    toolstab=Frame(ribbon,bg=accentcolor,relief="flat")
   
    ribbon.add(filetab,text="File")
    ribbon.add(viewtab,text="View")
    ribbon.add(citationtab,text="Citation")
    ribbon.add(filtertab,text="Filter")
    ribbon.add(citetab,text="Cite")
    ribbon.add(toolstab,text="Tools")
 
    ribbon.grid(row=0,column=0,columnspan=5)

    anchor="s"
    w=0
    f=("Verdana",6)
    border=3
    r="flat"

    filegroup=LabelFrame(filetab,text="Project",bg=accentcolor2,font=f,labelanchor=anchor,bd=border,relief=r)
    opengroup=LabelFrame(filetab,text="Open",bg=accentcolor2,font=f,labelanchor=anchor,bd=border,relief=r)
    showgroup=LabelFrame(filetab,text="Show/ Hide",bg=accentcolor2,font=f,labelanchor=anchor,bd=border,relief=r)
    findgroup=LabelFrame(filtertab,text="")
    windowgroup=LabelFrame(viewtab,text="Window",bg=accentcolor2,font=f,labelanchor=anchor,bd=border,relief=r)
    copygroup=LabelFrame(citationtab,text="Copy",bg=accentcolor2,font=f,labelanchor=anchor,bd=border,relief=r)
    papergroup=LabelFrame(citationtab,text="Paper",bg=accentcolor2,font=f,labelanchor=anchor,bd=border,relief=r)
    
    listgroup=LabelFrame(citationtab,text=" ",bg=accentcolor,font=f,labelanchor=anchor,bd=border,relief=r)
    accessgroup=LabelFrame(filtertab,text="Used/ Access",bg=accentcolor2,font=f,labelanchor=anchor,bd=border,relief=r)
    sortgroup=LabelFrame(filtertab,text="Sort",bg=accentcolor2,font=f,labelanchor=anchor,bd=border,relief=r)
    exportgroup=LabelFrame(filtertab,text="",bg=accentcolor2,font=f,labelanchor=anchor,bd=border,relief=r)
    searchgroup=LabelFrame(filtertab,text="Search",bg=accentcolor2,font=f,labelanchor=anchor,bd=border,relief=r)
    citegroup=LabelFrame(citetab,text="Cite New",bg=accentcolor2,font=f,labelanchor=anchor,bd=border,relief=r)
    authorgroup=LabelFrame(citetab,text="Authors",bg=accentcolor2,font=f,labelanchor=anchor,bd=border,relief=r)
    citegroup=LabelFrame(citetab,text="Cite New",bg=accentcolor2,font=f,labelanchor=anchor,bd=border,relief=r)
    writegroup=LabelFrame(citetab,text="Cite",bg=accentcolor2,font=f,labelanchor=anchor,bd=border,relief=r)
    chargroup=LabelFrame(citetab,text="Chars",bg=accentcolor2,font=f,labelanchor=anchor,bd=border,relief=r)

    x=10
    y=10
    filegroup.grid(row=0,column=1,padx=x,pady=y),
    opengroup.grid(row=0,column=2,padx=x,pady=y),
    
    windowgroup.grid(row=0,column=0,padx=x,pady=y)
    showgroup.grid(row=0,column=3,padx=x,pady=y)
    findgroup.grid(row=0,column=100,padx=x,pady=y)
    copygroup.grid(row=0,column=0,padx=x,pady=y)
    listgroup.grid(row=0,column=100,padx=x,pady=y)
    papergroup.grid(row=0,column=1,padx=x,pady=y)
    
    accessgroup.grid(row=0,column=0,padx=x,pady=y)
    sortgroup.grid(row=0,column=1,padx=x,pady=y)
    exportgroup.grid(row=0,column=2,padx=x,pady=y)
    searchgroup.grid(row=0,column=100,padx=x,pady=y,sticky="w")
    authorgroup.grid(row=0,column=0,padx=x,pady=y)
    citegroup.grid(row=0,column=1,padx=x,pady=y)
    writegroup.grid(row=0,column=2,padx=x,pady=y)
    chargroup.grid(row=0,column=10,padx=x,pady=y)

    #load icons
    global addauthoricon
    global bookicon
    global copyciteicon
    global copyicon
    global copyindexicon
    global copyreficon
    global csvicon
    global delicon
    global delicon
    global delpersonicon
    global exporticon
    global googleicon
    global hideicon
    global journalicon
    global lockicon
    global maximiseicon
    global maximiseicon
    global minimiseicon
    global minimiseicon
    global newicon
    global newicon
    global notepadicon
    global pdficon
    global reloadicon
    global reloadicon
    global removeallauthors
    global showallicon
    global showicon
    global showicon
    global sortauthoricon
    global sortdatedescicon
    global sortdownicon
    global sorttitleicon
    global sortupicon
    global soundicon
    global switchicon
    global switchicon
    global txticon
    global urlicon
    global wordicon
    global writeicon

    addauthoricon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/addauthoricon.png').subsample(1,1)
    bookicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/bookicon.png').subsample(1,1)
    copyciteicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/copyciteicon.png').subsample(1,1)
    copyicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/copyicon.png').subsample(1,1)
    copyindexicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/copyindexicon.png').subsample(1,1)
    copyreficon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/copyreficon.png').subsample(1,1)
    csvicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/csvicon.png').subsample(1,1)
    delicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/delicon.png').subsample(1,1)
    delicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/delicon.png').subsample(1,1)
    delpersonicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/delpersonicon.png').subsample(1,1)
    exporticon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/exporticon.png').subsample(1,1)
    googleicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/googleicon.png').subsample(1,1)
    hideicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/hideicon.png').subsample(1,1)
    journalicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/journalicon.png').subsample(1,1)
    lockicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/lockicon.png').subsample(1,1)
    maximiseicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/maximiseicon.png').subsample(1,1)
    maximiseicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/maximiseicon.png').subsample(1,1)
    minimiseicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/minimiseicon.png').subsample(1,1)
    minimiseicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/minimiseicon.png').subsample(1,1)
    newicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/newicon.png').subsample(1,1)
    newicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/newicon.png').subsample(1,1)
    notepadicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/notepadicon.png').subsample(1,1)
    pdficon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/pdficon.png').subsample(1,1)
    reloadicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/reloadicon.png').subsample(1,1)
    reloadicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/reloadicon.png').subsample(1,1)
    removeallauthors=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/removeallauthors.png').subsample(1,1)
    showallicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/showallicon.png').subsample(1,1)
    showicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/showicon.png').subsample(1,1)
    showicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/showicon.png').subsample(1,1)
    sortauthoricon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/sortauthoricon.png').subsample(1,1)
    sortdatedescicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/sortdatedescicon.png').subsample(1,1)
    sortdownicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/sortdownicon.png').subsample(1,1)
    sorttitleicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/sorttitleicon.png').subsample(1,1)
    sortupicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/sortupicon.png').subsample(1,1)
    soundicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/soundicon.png').subsample(1,1)
    switchicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/switchicon.png').subsample(1,1)
    switchicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/switchicon.png').subsample(1,1)
    txticon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/txticon.png').subsample(1,1)
    urlicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/urlicon.png').subsample(1,1)
    wordicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/wordicon.png').subsample(1,1)
    writeicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/writeicon.png').subsample(1,1)
    accessicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/accessicon.png').subsample(1,1)
    noaccessicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/noaccessicon.png').subsample(1,1)
    usedicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/usedicon.png').subsample(1,1)
    unusedicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/unusedicon.png').subsample(1,1)
    redaicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/redaicon.png').subsample(1,1)
    greenaicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/greenaicon.png').subsample(1,1)






    buttons=[{"image":newicon,"img":"✱","name":"New project","short":"<Control-n>","short2":"<Control-N>","command":newlist,"menu":filegroup},
             #{"img":"📌","name":"Pin project","short":None,"command":pin,"menu":filegroup},
             #{"img":"📌","name":"Unpin project","short":None,"command":unpin,"menu":filegroup},
             {"image":delicon,"img":"🗑","name":"Delete project","short":None,"command":delete,"menu":filegroup},
             {"image":txticon,"img":"🖉","name":"Open list as .txt","short":"<Control-o>","command":show,"menu":opengroup},
             {"image":csvicon,"img":"𝓧","name":"Open list as .csv","short":"<Control-O>","command":showex,"menu":opengroup},
             {"image":wordicon,"img":"Ｗ","name":"Open Project","short":None,"short2":None,"command":openproj,"menu":filegroup},
             {"image":switchicon,"img":"⥂","name":"Change Project File","short":None,"short2":None,"command":changeproj,"menu":filegroup},
             {"image":hideicon,"img":"Ｈ","name":"Hide list","short":"<Control-h>","short2":"<Control-H>","command":finished,"menu":showgroup},
             {"image":showicon,"img":"Ｓ","name":"Unhide list","short":"<Control-u>","short2":"<Control-U>","command":unhide,"menu":showgroup},
             {"image":showallicon,"img":"👁","name":"Show/ Hide hidden lists","short":"<Control-s>","short2":"<Control-S>","command":showhidden,"menu":showgroup},
             {"image":reloadicon,"img":"↺","name":"Reload","short":"<F5>","command":search,"menu":windowgroup},
             {"image":minimiseicon,"img":"⇲","name":"Minimise","short":"<Control-minus>","command":minimise,"menu":windowgroup},
             {"image":maximiseicon,"img":"⇱","name":"Restore","short":"<Control-equal>","command":restore,"menu":windowgroup},
             {"image":lockicon,"img":"🔒","name":"Keep entries between refreshes","short":"<Control-l>","command":locktext,"menu":windowgroup},
             
             {"img":"🔎","name":"Find","short":"<Control-f>","short2":"<Control-F>","command":find,"menu":searchgroup},
             
             
             {"image":copyreficon,"img":"🗇Ｒ","name":"Copy full reference","short":None,"command":copyref,"menu":copygroup},
             {"image":copyciteicon,"img":"🗇Ｃ","name":"Copy citation","short":None,"command":copycite,"menu":copygroup},
             {"image":copyindexicon,"img":"🗇ｉ","name":"Copy index number","short":None,"command":copy_index,"menu":copygroup},
            {"image":delicon,"img":"🗑","name":"Delete citation","short":None,"command":areyousure,"menu":copygroup},
             {"image":urlicon,"img":"🌐","name":"Open paper URL","short":"<Control-u>","short2":"<Control-U>","command":openrefweb,"menu":papergroup},
             {"image":pdficon,"img":"🗎","name":"Open paper PDF","short":"<Control-p>","short2":"<Control-P>","command":openrefpdf,"menu":papergroup},
             {"image":unusedicon,"img":"Ꞹ","name":"Show only unused","short":None,"command":show_unused,"menu":accessgroup},
            {"image":usedicon,"img":"U","name":"Show only used","short":None,"command":show_used,"menu":accessgroup},
            {"image":accessicon,"img":"A","name":"Show only sources with access","short":None,"command":show_access,"menu":accessgroup},
            {"image":noaccessicon,"img":"Ⱥ","name":"Show only sources without access","short":None,"command":show_no_access,"menu":accessgroup},
            {"img":"ꞸA","name":"Show unused sources with access","short":None,"command":show_unused_access,"menu":accessgroup},
            {"img":"UȺ","name":"Show used sources with no access","short":None,"command":show_used_no_access,"menu":accessgroup},
            {"img":"UA","name":"Show used sources with access","short":None,"command":show_used_access,"menu":accessgroup},
            {"img":"ꞸȺ","name":"Show unused sources with no access","short":None,"command":show_unused_no_access,"menu":accessgroup},
            
            {"image":showallicon,"img":"✱","name":"Show all","short":None,"command":showall,"menu":accessgroup},
            {"image":exporticon,"img":"⇨","name":"Export view","short":None,"command":export_view,"menu":exportgroup},
            {"image":sortupicon,"img":"⇧","name":"Newest First","short":None,"command":order_asc,"menu":sortgroup},
            {"image":sortdownicon,"img":"⇩","name":"Oldest First","short":None,"command":order_desc,"menu":sortgroup},
            {"image":sortauthoricon,"img":"👥","name":"By Author","short":None,"command":alpha_by_citation,"menu":sortgroup},
            {"image":sorttitleicon,"img":"Ｔ","name":"By Title","short":None,"command":alpha_by_title,"menu":sortgroup},

             {"image":bookicon,"img":"📖","name":"Cite new book","short":"<Control-b>","short2":"<Control-B>","command":book,"menu":citegroup},
             {"image":journalicon,"img":"📰","name":"Cite new journal","short":"<Control-j>","short2":"<Control-J>","command":journal,"menu":citegroup},
             {"image":urlicon,"img":"🌍","name":"Cite new webpage","short":"<Control-w>","short2":"<Control-W>","command":web,"menu":citegroup},
             {"image":addauthoricon,"img":"🞥👥","name":"Add author","short":"<Insert>","command":store,"menu":authorgroup},
             {"image":removeallauthors,"img":"⛔👥","name":"Delete all authors in citation","short":None,"command":deleteallnames,"menu":authorgroup},
             {"image":delpersonicon,"img":"⛔👥¹","name":"Delete last author","short":"<Delete>","command":deletenames,"menu":authorgroup},

             {"image":writeicon,"img":"✔","name":"Write to file","short":"<Control-Return>","command":cite,"menu":writegroup},
             {"image":soundicon,"img":"📢","name":"Read out loud","short":"<Control-r>","command":proofread,"menu":toolstab},
             {"image":googleicon,"img":"Ｇ","name":"Search Google Scholar","short":"<Control-g>","command":google,"menu":toolstab},
             
             
             
             {"image":notepadicon,"img":"🗒","name":"Notepad","short":"<Control-Right>","short2":None,"command":shownotes,"menu":toolstab},
             {"img":"Ꞹ","name":"Check for unused files","short":None,"command":check_unused_files,"menu":toolstab},
             {"img":"𝝱","name":"Testing mode","short":"<Control-t>","command":beta,"menu":toolstab}]
    c=0

    from PIL import ImageTk, Image

    global photo
    #photo = PhotoImage(file="/home/jonathan/Documents/Tech/Scripts/Icons/newicon.png") 
    #photoimage = photo.subsample(3, 3) 

    for i in buttons:

    
        try:
            b=Button(i["menu"],text=i["img"],command=i["command"],image=i["image"],bg=bgcolor,relief="flat",bd=0,highlightthickness=0)
        except:
            b=Button(i["menu"],text=i["img"],command=i["command"],bg=bgcolor,relief="flat",highlightthickness=0)
    
        b.grid(row=0,column=c,padx=5)
        tip = Hovertip(b,str(i["name"])+" ("+str(i["short"])+")")
        c=c+1

        rootwin.bind(i["short"],i["command"])
        try:
            rootwin.bind(i["short2"],i["command"])
        except:
            pass
    find()
    ribbon.select(filetab)



    
ribbon()

journal()
cleareverything()
updateheader()
minimise()


###########################SQL##################
import sqlite3
citationslist=[]
referencelist=[]
def makedb():
    global cur
    global con
    os.chdir("/home/jonathan/Documents/Tech/Scripts/Ref")
    os.system("rm -rf ref.db")
    con=sqlite3.connect("ref.db")
    cur=con.cursor()

def makeprojtable():
    cur.execute("""CREATE TABLE projects (
       id integer PRIMARY KEY,
       name TEXT,
       status TEXT);""")

def insert(table,fields,values):
    d=(str(datetime.now()).replace("-","").split(" ")[0])
    command=str('INSERT INTO '+ table +' (dateaccessed, '+fields+') '+'VALUES ('+d+','+values+');')

    cur.execute(command)
    
    con.commit()
    

def makebookstable():
    cur.execute("""CREATE TABLE books (
   id integer PRIMARY KEY,
   access BOOL,
   dateaccessed DATE,
   title TEXT,
   edition INT,
   authors TEXT,
   publisher TEXT,
   city TEXT,
   year INT,
   url TEXT);""")

    insert('books','access,title,edition,authors,publisher,city,year,url','1,"The Gruffalo",1,"Donaldson","Penguin","Flitwick",2024,"Gruffalo.com"')

def makejournalstable():
    cur.execute("""CREATE TABLE journals (
   id integer PRIMARY KEY,
   access BOOL,
   dateaccessed DATE,
   title TEXT,
   authors TEXT,
   year INT,
   journal TEXT,
   volume INT,
   issue INT,
   pages TEXT,
   url TEXT);""")
    insert('journals','access,title,authors,year,journal,volume,issue,pages,url','1,"Analysis of Marmite","J.J.McFarlane",2024,"Applied Comdinents",100,200,"5-6","Elsevier.com"')
    con.commit()

def makewebtable():
    cur.execute("""CREATE TABLE websites (
   id integer PRIMARY KEY,
   dateaccessed DATE,
   access BOOL,
   title TEXT,
    url TEXT,
   authors TEXT,
   year TEXT);""")
    insert('websites','access,title,url,authors,year','1,"Banana","Wikipedia.com/banana","Wikipedia","7/9/24"')
    con.commit()
    

def sqlcite(table):
    cur.execute('Select authors,+","+year from '+table)
    printcite()
    
 
def viewcitations():
    

    sqlcite("books")
    #printcite()
    sqlcite("journals")
    #printcite()
    sqlcite("websites")
    #printcite()
    print("\n\n")


    cur.execute('Select title, edition, authors, publisher, city from books;')
    printref()
    cur.execute('Select authors, year, title, journal, volume, issue, pages from journals;')
    printref()
    cur.execute('Select title,"online", url, dateaccessed, year from websites;')
    printref()
    
    

def printcite():
    for i in cur.fetchall():
        print(i)
        citationslist.append(str(i).replace("(","").replace(")","").replace("'","").replace(", online"," (online)"))
        #print(i)
        

def printref():
    for i in cur.fetchall():
        referencelist.append(str(i).replace("(","").replace(")","").replace("'","").replace(", online"," (online)"))
def printall():
    for i in citationslist:
        print(i)
    for i in referencelist:
        print(i)
makedb()
makeprojtable()
makebookstable()
makejournalstable()
makewebtable()
viewcitations()
printall()


    
    
    


rootwin.mainloop()
