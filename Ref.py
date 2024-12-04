'''
This program has been designed for it to be easy to add new media types. Places where it's necessary to modify the code are marked with #mod
#platdep indicates bits which are platform dependent
'''


############################IMPORT LIBRARIES#######################
from datetime import *
import os
os.system("pip install pipreqs --break-system-packages") #automatically install necessary packages
os.system("pipreqs")
os.system("pip install -r requirements.txt")
from tkinter import *
import tkinter as tki
from tkinter import ttk

from os import system
import pathlib
from tkinter.filedialog import askdirectory
from difflib import SequenceMatcher
from tkinter import filedialog
from gtts import gTTS
import sys
import random
import glob
import os.path
from idlelib.tooltip import Hovertip
from tkinter import messagebox
import pandas as pd
import numpy as np
from PIL import ImageTk, Image
import pypandoc
import shutil
import time
import threading


def clean():
    os.system("rm *.txt")
    os.system("rm *.mp3")
    os.system("rm reflist*")
clean()
##########################Either read in the existing database or make a new one from scratch###############

def load():
    global t
    global data
    global files
    try:
        data=pd.read_csv("ref.csv",sep=";")
        projfiles=pd.read_csv("files.csv",sep=";")

    except:
        data={"Access":[True],
        "Project":["Panspermia"],
        "Surname0":["Sample"],
        "Surname1":[""],
        "Surname2":[""],
        "Surname3":[""],
        "Initial0":["T"],
        "Initial1":[""],
        "Initial2":[""],
        "Initial3":[""],
        "Initial4":[""],
        "Ed_Surname0":["Ed_Sample"],
        "Ed_Surname1":[""],
        "Ed_Surname2":[""],
        "Ed_Surname3":[""],
        "Ed_Initial0":["T"],
        "Ed_Initial1":[""],
        "Ed_Initial2":[""],
        "Ed_Initial3":[""],
        "Ed_Initial4":[""],
        "Chap_Surname0":["Sample"],
        "Chap_Surname1":[""],
        "Chap_Surname2":[""],
        "Chap_Surname3":[""],
        "Chap_Initial0":["T"],
        "Chap_Initial1":[""],
        "Chap_Initial2":[""],
        "Chap_Initial3":[""],
        "Chap_Initial4":[""],
        "Chap_Title":["The Misty Mountains"],


        "Surnames":["Sample"],
        "Initials":["T"],
        "AuthorCount":[1],
        "ChapCount":[0],
        "EdCount":[0],
        "Media":["book"],
        "Title":["Testing"],
        "Edition":[1],
        "Publisher":["Example University Press"],
        "CityOfPub":["Samplestan"],
        "Year":["2000"],
        "URL":["example.com"],
        "Journal":["Journal of Placeholding"],
        "Volume":["1"],
        "Issue":["1"],
        "Pages":["1"],
        "Organisation":["University of Exampling"],
        "DateAccessed":["091124"],
        "DateWritten":["091124"],
        "Name_Conf":["Conference of Lots of Important Stuff"],
        "Place_Conf":["Slough Trading Estate"],
        "Date_Conf":["111124"],
        "PDF":["download.pdf"],
        "Notes":["Insert notes here"],
        "CiteOverride":[""],
        "RefOverride":[""]}

        #mod add new fields to this list
        projfiles={"Project":["Panspermia"],"File":["/home/jonathan/Documents/University/Course notes/Home/Biology/Palaeontology/Panspermia/Panspermia expanded.odt"],"Default":True}

    t=pd.DataFrame(data)
    files=pd.DataFrame(projfiles)

    t.astype(str)

    t.to_csv('ref.csv',sep=";")
    files.to_csv('files.csv',sep=";")
    unnamed()

##################################### Search facility########################
def list_results(event=None):
    results.delete(0,END)
    results.insert(0,"")
    for x in t["HReference"]:
        if str(searchbox.get()).upper() in str(x).upper():
            results.insert(END,x)
def setresult(event=None):
    for i in results.curselection():
        ref.set(str(results.get(i)))

        sync_ref()
        searchwin.destroy()
        copycite()

def gotobox(event=None):
    if "entry" in str(searchwin.focus_get()):
        results.focus_set()
    else:
        for i in results.curselection():
            ref.set(str(results.get(i)))
            sync_ref()

def gotosearch(event=None):
    for i in results.curselection():
        if (len(results.get(i)))==0:
            searchbox.focus_set()
        else:
            for i in results.curselection():
                ref.set(str(results.get(i)))
                sync_ref()

def closesearch(event=None):
    searchwin.destroy()

def search(event=None):
    global searchbox
    global results
    global var
    global searchwin
    ribbon.select(citationtab)
    var=StringVar()
    var.trace("w", lambda name, index, mode,var=var: callback(var))
    searchwin=Tk()
    searchwin.title("")
    searchbox=Entry(searchwin)

    results=Listbox(searchwin)


    searchbox.pack()
    results.pack()
    chars=['<a>', '<b>', '<c>', '<d>', '<e>', '<f>', '<g>', '<h>', '<I>', '<j>', '<k>', '<l>', '<m>', '<n>', '<o>', '<p>', '<q>', '<r>', '<s>', '<t>', '<u>', '<v>', '<w>', '<x>', '<y>', '<z>','<BackSpace>']
    for x in chars:
        searchwin.bind(x, list_results)

    results.bind("<Return>", setresult)
    searchwin.bind("<Escape>", setresult)


    searchwin.bind("<Up>",gotosearch)
    searchwin.bind("<Down>",gotobox)
    searchwin.bind("<Escape>",closesearch)
    searchbox.focus_set()


#################### Sort reference list ################
def sort_list(d):
    global t
    t['DateAccessed'] = pd.to_datetime(t['DateAccessed'],dayfirst=True)

    if d=="newest":
        t=t[t["Project"]==curproj.get()].sort_values(by=["DateAccessed"],ascending=False)
    elif d=="oldest":
        t=t[t["Project"]==curproj.get()].sort_values(by=["DateAccessed"],ascending=True)
    list_citations()
    load()

def sort_newest():
    sort_list("newest")
def sort_oldest():
    sort_list("oldest")

def sort_author():
    global t
    t=t[t["Project"]==curproj.get()].sort_values(by=["HCitation"],ascending=True)
    list_citations()
    load()
def sort_title():
    global t
    t=t[t["Project"]==curproj.get()].sort_values(by=["Title"],ascending=True)
    list_citations()
    load()


##################### Remove fields labelled 'unnamed'###################
#Currently unknown where these fields are coming from - function to remove them is a workaround.
def unnamed():
    global t
    for x in t.head(0):
        if "Unnamed" in str(x):
            t=t.drop(x,axis=1)

    t.to_csv('ref.csv',sep=";")

###################### Make new project ###########
def newproj(event=None):
    global newprojbox
    global newprojwin
    newprojwin=Tk()
    newprojwin.title("New Project")
    newprojbox=Entry(newprojwin,width=50)
    newprojbox.pack()
    newprojok=Button(newprojwin,text="✅",command=makenewproj)
    newprojok.pack()
def makenewproj():
    global t
    curproj.set(str(newprojbox.get()))
    newprojwin.destroy()


################## Delete project ###########

def askdel():
    areyousure(delproject,"project")
def delproject():

    todel = t[ t['Project'] == str(projdrop.cget("text"))].index
    t.drop(todel,inplace=True)
    t.to_csv('ref.csv',sep=";")
    load()
    list_projects()



########################## List of projects ###################
def change_proj(event=None):
    global projdrop

    curproj.set(projdrop.cget("text"))
    list_citations()

def confdrop(x):
    x.config(bg=btncolor,fg="black")
    x["highlightthickness"]=0
    x["borderwidth"]=0

def list_projects():
    global curproj
    global projdrop
    global projects
    curproj=StringVar(rootwin)
    projects=[]

    for x in t["Project"]:
        if x not in projects:
            projects.append(x)
    try:
        projdrop.destroy()
    except:
        pass

    projframe=Frame(filegroup)
    projframe.grid(row=0,column=0,columnspan=3,padx=10,pady=10)

    projdrop=OptionMenu(projframe,curproj,*projects,command=change_proj)
    projdrop.grid(row=0,column=0,columnspan=30)
    confdrop(projdrop)



    curproj.set(projects[0])

################# Open project document ########################

def loadfile():
    global files
    global filelist

    filelist=files[files["Project"]==str(projdrop.cget("text"))]["File"]
    if len(filelist)<1:
        p=filedialog.askopenfilename(title="Link Project File")

        files=files._append({"Project":projdrop.cget("text"),"File":p},ignore_index=True)
        files.to_csv('files.csv',sep=";")
    display_proj()

def openfile():
    loadfile()
    for x in filelist:

        os.system('xdg-open "'+str(x)+'"') #platdep



def changefile(event=None):
    filelist=files[files["Project"]==str(projdrop.cget("text"))]["File"]

    p=filedialog.askopenfilename(title="Change Project File")
    files.loc[files["Project"] == projdrop.cget("text"), "File"] = p

    files.to_csv('files.csv',sep=";")
    loadfile()

def display_proj():
    dispframe=Frame(projgroup)
    dispframe.grid(row=0,column=0,columnspan=100,padx=10,pady=10)
    for x in filelist:
        plabel=Label(dispframe,bg=btncolor,text=(x.split("/")[-1]))
        plabel.grid(row=0,column=0,columnspan=2)

############################## List all recorded citations ###############
def list_citations():
    global citedrop
    global refdrop
    global ref
    global citation
    try:
        citedrop.destroy()
        refdrop.destroy()
    except:
        pass
    assemble()

    citation=StringVar(rootwin)
    ref=StringVar(rootwin)
    citations=[]
    refs=[]

    for x in t[t["Project"]==curproj.get()]["HCitation"]:
        citations.append(x)
    for x in t[t["Project"]==curproj.get()]["HReference"]:
        refs.append(x)

    try:
        citedrop.destroy()
        refdrop.destroy()
    except:
        pass
    citedrop=OptionMenu(listgroup,citation,*citations,command=sync_cite)
    citedrop.grid(row=0,column=0,sticky="w")

    citation.set(citations[0])

    refdrop=OptionMenu(listgroup,ref,*refs,command=sync_ref)
    citedrop.configure(width=30)
    refdrop.configure(width=30)
    refdrop.grid(row=1,column=0,sticky="w")
    ref.set(refs[0])

    confdrop(refdrop)
    confdrop(citedrop)


################################## Keep the citation and reference boxes in sync, so that they always show text from the same citation##################
def sync_cite(event=None):
    i=int((t[t["HCitation"]==citedrop.cget("text")].index.astype(str)[0]))
    ref.set(t.iloc[i]["HReference"])

def sync_ref(event=None):
    i=int((t[t["HReference"]==refdrop.cget("text")].index.astype(str)[0]))
    citation.set(t.iloc[i]["HCitation"])


########################### Export reference list #################################
def export_as_csv(event=None):
    pd.set_option('display.max_colwidth', None)
    export_table=(t[t["Project"]==projdrop.cget("text")][["HCitation","HReference"]])
    export_table.to_csv('reflistcsv.csv',sep=";",index=False)
    os.system("libreoffice --calc reflistcsv.csv") #platdep

def export_as_txt(event=None):
    pd.set_option('display.max_colwidth', None)
    export_table=(t[t["Project"]==projdrop.cget("text")]["HReference"])
    export_table.to_csv('reflisttxt.csv',sep=";",index=False,header=None)
    os.system("gnome-text-editor reflisttxt.csv") #platdep

def copyref():
    rootwin.clipboard_clear()
    rootwin.clipboard_append(refdrop.cget("text"))
def copycite():
    rootwin.clipboard_clear()
    rootwin.clipboard_append(citedrop.cget("text"))
def copyindex():
    rootwin.clipboard_clear()
    rootwin.clipboard_append(int((t[t["HCitation"]==citedrop.cget("text")].index.astype(str)[0])))


################## Delete a reference #########################
def ask_delref():
    areyousure(delref,"reference")

def delref():
    global t
    i=int((t[t["HCitation"]==citedrop.cget("text")].index.astype(str)[0]))
    i=int(i)

    t=t.drop([i])

    t.to_csv('ref.csv',sep=";")
    list_citations()

######################### Make window ############################

bgcolor="aliceblue"
accentcolor="lightcyan1"
accentcolor2="lightcyan2"
textcolor="black"
activetabstyle=("Verdana",10,"bold underline")
bgtabstyle=("Verdana",10)
groupstyle=("Verdana",6)
labelstyle=("Verdana",10)
entrystyle=("Verdana",10)
btncolor="white"


def makewin(event=None):
    global rootwin



    splashwin.quit()
    splashwin.destroy() #this line causes an error but the program doesn't work without it. No idea why. Needs fixing
    rootwin=Tk() #Tk window
    rootwin.title("Referencing")
    rootwin.configure(bg=bgcolor)
    splashwin.destroy()

def splash(event=None):
    global splashwin
    splashwin=Tk()
    splashwin.overrideredirect(True)
    logo=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Ref/Logo.png').subsample(1)
    splashlabel=Button(splashwin,text="test",image=logo,relief="flat")
    splashlabel.pack()
    splashwin.after(0, makewin)
    splashwin.mainloop()


splash()


####################### Add an author to the list of authors so that another can be added #################

def insert_author(event=None):
    insert(surnamelist,ilist,surnamebox,initialbox)
def insert_editor(event=None):
    insert(esurnamelist,eilist,edsurnamebox,edinitialbox)
def insert_chapter_author(event=None):
    insert(csurnamelist,cilist,chapsurnamebox,chapinitialbox)

def del_author(event=None):
    surnamelist.delete(END)
    ilist.delete(END)

def del_editor(event=None):
    esurnamelist.delete(END)
    eilist.delete(END)
def del_chapter_author(event=None):
    csurnamelist.delete(END)
    cilist.delete(END)

def insert(slb,ilb, sentry,ientry):
    global surnamelist
    global esurnamelist
    global csurnamelist
    try:
        slb.insert(END,str(sentry.get())[0].upper() + str(sentry.get())[1:])

        i=""
        for n in range (len(ientry.get())):
            i=i+str(ientry.get()[n].upper()+".")
        ilb.insert(END,i)

        sentry.delete(0,END)
        ientry.delete(0,END)


    except:
        print("Nothing there")

def inscheck(event=None):

    if(len((initialbox.get()))>0 and (len((surnamebox.get()))>0)):
        insert_author()
    if(len((edinitialbox.get()))>0 and (len((edsurnamebox.get()))>0)):
        insert_editor()
    if(len((chapinitialbox.get()))>0 and (len((chapinitialbox.get()))>0)):
        insert_chapter_author()


def insclick(event):

    inscheck()
rootwin.bind("<Insert>",inscheck)


####################################### Entry boxes for data ###########################
#'for' indicates whether it should be shown for that medium
#'cap' indicates whether data from that box should be auto capitalised.

boxframe=Frame(rootwin,bg=bgcolor)
boxframe.grid(row=1,column=0)

def makebox():
    return Entry(boxframe,relief="flat",borderwidth=-1,highlightthickness=-1,background=accentcolor2,font=entrystyle,width=40)
titlebox=makebox()
editionbox=makebox()
surnamebox=makebox()
initialbox=makebox()
edsurnamebox=makebox()
edinitialbox=makebox()
chapsurnamebox=makebox()
chapinitialbox=makebox()
chaptitlebox=makebox()
pubbox=makebox()
citybox=makebox()
yearbox=makebox()
volbox=makebox()
issuebox=makebox()
pagesbox=makebox()
urlbox=makebox()
orgbox=makebox()
accessbox=makebox()
writtenbox=makebox()
journalbox=makebox()
conference_title_box=makebox()
conference_place_box=makebox()
conference_date_box=makebox()
PDFbox=makebox()
notesbox=makebox()
customcite=makebox()
customref=makebox()



#mod: insert new box here


boxes=[{'box':titlebox,"text":"Title","book":True,"journal":True,"web":True,"data":True,"ed":True,"chap":True,"conf":True,"cap":True,"unpub":True,"custom":False,"field":"Title"},
       {'box':editionbox,"text":"Edition","book":True,"journal":False,"web":False,"data":False,"ed":False,"chap":True,"conf":False,"cap":False,"unpub":True,"custom":False,"field":"Edition"},
       {'box':surnamebox,"text":"Surname","book":True,"journal":True,"web":False,"data":False,"ed":False,"chap":False,"conf":True,"cap":False,"unpub":True,"custom":False,"field":None},
       {'box':initialbox,"text":"Initials","book":True,"journal":True,"web":False,"data":False,"ed":True,"chap":False,"conf":True,"cap":False,"unpub":True,"custom":False,"field":None},
       {'box':edsurnamebox,"text":"Ed. Surname","book":False,"journal":True,"web":False,"data":False,"ed":True,"chap":True,"conf":True,"cap":False,"unpub":True,"custom":False,"field":None},
       {'box':edinitialbox,"text":"Ed. Initials","book":False,"journal":True,"web":False,"data":False,"ed":True,"chap":True,"conf":True,"cap":False,"unpub":True,"custom":False,"field":None},
        {'box':chapsurnamebox,"text":"Chap. Surname","book":False,"journal":False,"web":False,"data":False,"ed":False,"chap":True,"conf":False,"cap":True,"unpub":True,"custom":False,"field":None},
       {'box':chapinitialbox,"text":"Chap. Initials","book":False,"journal":False,"web":False,"data":False,"ed":False,"chap":True,"conf":False,"cap":True,"unpub":True,"custom":False,"field":None},
       {'box':chaptitlebox,"text":"Chap. Title","book":False,"journal":False,"web":False,"data":False,"ed":False,"chap":True,"conf":False,"cap":True,"unpub":True,"custom":False,"field":"Chap_Title"},
    {'box':pubbox,"text":"Publisher","book":True,"journal":False,"web":False,"data":False,"ed":True,"chap":True,"conf":False,"cap":True,"unpub":True,"custom":False,"field":"Publisher"},
       {'box':citybox,"text":"City","book":True,"journal":False,"web":False,"data":False,"ed":True,"chap":True,"conf":False,"cap":True,"unpub":True,"custom":False,"field":"CityOfPub"},
       {'box':yearbox,"text":"Year","book":True,"journal":True,"web":True,"data":True,"ed":True,"chap":True,"conf":True,"cap":False,"unpub":True,"custom":False,"field":"Year"},
       {'box':journalbox,"text":"Journal","book":False,"journal":True,"web":False,"data":False,"ed":False,"chap":False,"conf":False,"cap":True,"unpub":True,"custom":False,"field":"Journal"},
       {'box':volbox,"text":"Volume","book":False,"journal":True,"web":False,"data":False,"ed":False,"chap":False,"conf":False,"cap":False,"unpub":True,"custom":False,"field":"Volume"},
       {'box':issuebox,"text":"Issue","book":False,"journal":True,"web":False,"data":False,"ed":False,"chap":False,"conf":False,"cap":False,"unpub":True,"custom":False,"field":"Issue"},
       {'box':pagesbox,"text":"Pages","book":False,"journal":True,"web":False,"data":False,"ed":False,"chap":True,"conf":True,"cap":False,"unpub":True,"custom":False,"field":"Pages"},
       {'box':urlbox,"text":"URL","book":True,"journal":True,"web":True,"data":True,"ed":True,"chap":True,"conf":True,"cap":False,"unpub":True,"custom":False,"field":"URL"},
       {'box':orgbox,"text":"Org.","book":False,"journal":False,"web":True,"data":True,"ed":False,"chap":False,"conf":False,"cap":True,"unpub":True,"custom":False,"field":"Organisation"},
       {'box':accessbox,"text":"Accessed","book":True,"journal":True,"web":True,"data":True,"ed":True,"chap":True,"conf":True,"cap":True,"unpub":True,"custom":False,"field":"DateAccessed"},
       {'box':writtenbox,"text":"Written","book":False,"journal":False,"web":True,"data":True,"ed":False,"chap":False,"conf":False,"cap":True,"unpub":True,"custom":False,"field":"DateWritten"},
       {'box':conference_place_box,"text":"Conference Place","book":False,"journal":False,"web":False,"data":False,"ed":False,"chap":False,"conf":True,"cap":True,"unpub":True,"custom":False,"field":"Place_Conf"},
       {'box':conference_title_box,"text":"Conference Name","book":False,"journal":False,"web":False,"data":False,"ed":False,"chap":False,"conf":True,"cap":True,"unpub":True,"custom":False,"field":"Name_Conf"},
       {'box':conference_date_box,"text":"Conference Date","book":False,"journal":False,"web":False,"data":False,"ed":False,"chap":False,"conf":True,"cap":True,"unpub":True,"custom":False,"field":"Date_Conf"},
       {'box':PDFbox,"text":"PDF","book":True,"journal":True,"web":True,"data":True,"ed":True,"chap":True,"conf":True,"cap":True,"unpub":True,"custom":False,"field":"PDF"},
       {'box':notesbox,"text":"Notes","book":True,"journal":True,"web":True,"data":True,"ed":True,"chap":True,"conf":True,"cap":True,"unpub":True,"custom":False,"field":"Notes"},
       {'box':customcite,"text":"Custom Citation","book":False,"journal":False,"web":False,"data":False,"ed":False,"chap":False,"conf":False,"cap":False,"unpub":False,"custom":True,"field":"CiteOverride"},
       {'box':customref,"text":"Custom Reference","book":False,"journal":False,"web":False,"data":False,"ed":False,"chap":False,"conf":False,"cap":False,"unpub":False,"custom":True,"field":"RefOverride"}]
        #mod: insert new box here
        #mod book,web,data field etc indicates whether it should show up for that medium. Add a new key for any new medium.




for x in boxes:
    x["text"]=Label(boxframe,text=x["text"],bg="aliceblue",justify="right",font=labelstyle)
    x["box"].bind("<1>",insclick)





############################## Populate window with fields necessary to cite selected media ###################

def refresh(forwhat):
    for widget in boxframe.winfo_children():
        try:
            widget.delete(0,END)
        except:
            pass
        widget.grid_forget()


    global surnamelist
    global ilist
    global esurnamelist
    global eilist
    global csurnamelist
    global cilist
    r=1
    for x in boxes:
        if x[forwhat]==True:
            x["text"].grid(row=r,column=0,sticky="w")
            x["box"].grid(row=r,column=1)
            #x["box"].insert(0,x["text"])
            r=r+1

    def makesbox(c,f):
        s=Listbox(f,bg=accentcolor2,relief="flat",highlightthickness=0,width=10)
        s.grid(row=0,column=1,rowspan=10)


        return s

    def makeibox(c,f,com):
        i=Listbox(f,bg=accentcolor2,relief="flat",highlightthickness=0,width=5,justify="right")
        i.grid(row=1,column=0,rowspan=10)
        b=Button(f,image=delpersonicon,command=com,relief="flat",bg=accentcolor2,highlightthickness=0)
        b.grid(row=100,column=0,sticky="w")


        return i
    def makeframe(c,label):
        l=LabelFrame(boxframe,text=label,bg=accentcolor2,font=labelstyle)
        l.grid(row=1,column=c,rowspan=100,sticky="n")
        return l

    authorframe=makeframe(3,"Authors")
    editorframe=makeframe(4,"Editors")
    chapterframe=makeframe(5,"Chapter Authors")

    ilist=makeibox(0,authorframe,del_author)
    surnamelist=makesbox(1,authorframe)
    eilist=makeibox(0,editorframe,del_editor)
    esurnamelist=makesbox(1,editorframe)
    cilist=makeibox(0,chapterframe,del_chapter_author)
    csurnamelist=makesbox(1,chapterframe)

    accessbox.insert(0,(datetime.date(datetime.now())).strftime("%d-%m-%Y"))

    ribbon.select(citetab)


def citenew(m):
    global media
    refresh(m)
    media=m
    rootwin.title("Citing new "+media)


def book(event=None):
    citenew("book")
def journal(event=None):
    citenew("journal")
def web(event=None):
    citenew("web")
def dataset(event=None):
    citenew("data")
def confpapers(event=None):
    citenew("conf")
def edbook(event=None):
    citenew("ed")
def chap(event=None):
    citenew("chap")
def unpub(event=None):
    citenew("unpub")
def custom(event=None):
    citenew("custom")
#mod add function here

#################### Link PDF of paper to reference ################
def linkpdf(event):
    p=filedialog.askopenfilename(title="Link PDF")
    PDFbox.insert(0,p)


################# Open PDF or URL linked to reference ############
def open_pdf(event=None):
    x=""
    for x in t[t["HReference"]==refdrop.cget("text")]["PDF"]:

        if "nan" in str(x):
            p=filedialog.askopenfilename(title="Link PDF")
            t.loc[(t["HReference"]==refdrop.cget("text")), "PDF"]=p
            t.to_csv('ref.csv',sep=";")
        else:
            os.system('xdg-open "'+str(x)+'"') #platdep

def open_url(event=None):
    x=""
    for x in t[t["HReference"]==refdrop.cget("text")]["URL"]:
        os.system('xdg-open "'+str(x)+'"') #platdep

PDFbox.bind("<1>", linkpdf)

############################## Clear boxes after media has been cited ##############
def reset(event=None):
    for widget in boxframe.winfo_children():
        try:
            widget.delete(0,END)
        except:
            pass
        widget.grid_forget()

def minimise(event=None):
    rootwin.geometry("800x100")


###################### Assemble the citation into the right syntax #########################
def assemble():
    n=0
    global t
    #global year
    #global title
    def s(x):
        return t[x].astype(str).str.replace("[","").str.replace("]","").str.replace("'","")
    def j(media,thingtocount,ac,field,ref):

        t.loc[((t["Media"]==media) & (t[thingtocount]==ac)), field]=ref #needs fixing - author count only counts authors not editors or chapter authors

    year=s("Year").astype(str)
    title=s("Title")

    book=" ("+year+") "+title+". "+s("Edition")+" edn. "+s("CityOfPub")+": "+s("Publisher")+"."
    journal=" ("+year+") '"+title+"', "+s("Journal")+","+s("Volume")+"("+s("Issue")+"), pp. "+s("Pages")+". "+s("URL")
    c=""

    s0=s("Surname0")
    s1=s("Surname1")
    s2=s("Surname2")
    i0=s("Initial0")
    i1=s("Initial1")
    i2=s("Initial2")

    es0=s("Ed_Surname0")
    es1=s("Ed_Surname1")
    es2=s("Ed_Surname2")
    ei0=s("Ed_Initial0")
    ei1=s("Ed_Initial1")
    ei2=s("Ed_Initial2")

    cs0=s("Chap_Surname0")
    cs1=s("Chap_Surname1")
    cs2=s("Chap_Surname2")
    ci0=s("Chap_Initial0")
    ci1=s("Chap_Initial1")
    ci2=s("Chap_Initial2")





    def book_single_author():
        j("book","AuthorCount",1,"HCitation",s0+" ("+year+")")
        j("book","AuthorCount",1,"HReference",s0+", "+i0+book)
    def book_2_authors():
        j("book","AuthorCount",2,"HCitation",s0+", "+i0+" and "+s1+", "+i1+" ("+year+")")
        j("book","AuthorCount",2,"HReference",s0+", "+i0+" and "+s1+", "+i1+book)
    def book_3_authors():
        j("book","AuthorCount",3,"HCitation",s0+", "+i0+", "+s1+", "+i1+" and "+s2+", "+i2+" ("+year+")")
        j("book","AuthorCount",3,"HReference",s0+", "+i0+", "+s1+", "+i1+" and "+s2+", "+i2+book)
    def book_4_authors():
        for x in range(50):
            if x<4:
                pass
            else:
                j("book","AuthorCount",x,"HCitation",s0+" et al. ("+year+")")
                j("book","AuthorCount",x,"HReference",s0+", "+i0+" et al."+book)
    def journal_1_author():
        j("journal","AuthorCount",1,"HCitation",s0+" ("+year+")")
        j("journal","AuthorCount",1,"HReference",s0+", "+i0+journal)
    def journal_2_authors():
        j("journal","AuthorCount",2,"HCitation",s0+", "+i0+" and "+s1+", "+i1+" ("+year+")")
        j("journal","AuthorCount",2,"HReference",s0+", "+i0+" and "+s1+", "+i1+journal)
    def journal_3_authors():
        j("journal","AuthorCount",3,"HCitation",s0+", "+i0+", "+s1+", "+i1+" and "+s2+", "+i2+" ("+year+")")
        j("journal","AuthorCount",3,"HReference",s0+", "+i0+", "+s1+", "+i1+" and "+s2+", "+i2+journal)
    def journal_4_authors():
        for x in range(50):
            if x<4:
                pass
            else:
                j("journal","AuthorCount",x,"HCitation",s0+" et al. ("+year+")")
                j("journal","AuthorCount",x,"HReference",s0+", "+i0+" et al."+journal)
    def webpage():
        j("web","AuthorCount",0,"HCitation",s("Organisation")+" ("+year+")")
        j("web","AuthorCount",0,"HReference",s("Organisation")+" ("+year+") "+title+". Available at: "+s("URL")+" (Accessed: "+s("DateAccessed")+")")
    def assemble_dataset():
        j("data","AuthorCount",0,"HCitation",s("Organisation")+" ("+year+")")
        j("data","AuthorCount",0,"HReference",s("Organisation")+" ("+year+") "+title+". Available at: "+s("URL")+" (Accessed: "+s("DateAccessed")+")")

    def assemble_conf_papers_1_author():
        j("conf","AuthorCount",1,"HCitation",s0+" ("+year+")")
        j("conf","AuthorCount",1,"HReference",s0+", "+i0+" ("+year+") '"+title+"', "+s("Name_Conf")+". "+s("Place_Conf")+", "+s("Date_Conf")+", "+s("Pages")+". Available at: "+s("URL"))


    def ed_1_author():
        j("ed","EdCount",1,"HCitation",es0+" ("+year+")")
        j("ed","EdCount",1,"HReference",es0+", "+ei0+" (ed.)"+book)
    def ed_2_authors():
        j("ed","EdCount",2,"HCitation",es0+", "+ei0+" and "+es1+", "+ei1+" ("+year+")")
        j("ed","EdCount",2,"HReference",es0+", "+ei0+" and "+es1+", "+ei1+" (eds.)"+book)
    def ed_3_authors():
        j("ed","EdCount",3,"HCitation",es0+", "+ei0+", "+es1+", "+ei1+" and "+es2+", "+ei2+" ("+year+")")
        j("ed","EdCount",3,"HReference",es0+", "+ei0+", "+es1+", "+ei1+" and "+es2+", "+ei2+" (eds.)"+book)
    def ed_4_authors():
        for x in range(50):
            if x<4:
                pass
            else:
                j("ed","EdCount",x,"HCitation",es0+" et al. ("+year+")")
                j("ed","EdCount",x,"HReference",es0+", "+ei0+" et al. (eds.)"+book)

    one_chap=cs0+", "+ci0
    two_chap=cs0+", "+ci0+" and "+cs1+", "+ci1
    three_chap=cs0+", "+ci0+", "+cs1+", "+ci1+" and "+cs2+", "+ci2
    four_chap=cs0+", "+ci0+" et al."

    one_ed=es0+", "+ei0
    two_ed=es0+", "+ei0+" and "+es1+", "+ei1
    three_ed=es0+", "+ei0+", "+es1+", "+ei1+" and "+es2+", "+ei2
    four_ed=es0+", "+ei0+" et al."

    def ed_chaps(n,a,b):
        j("chap","EdCount",n,"HReference",a+" ("+year+") '"+s("Chap_Title")+"', in "+b+" (ed) "+title+". "+s("Edition")+". "+s("CityOfPub")+": "+s("Publisher")+", "+s("Pages")+".")
    def chap_1_author_1_ed():
        j("chap","EdCount",1,"HCitation",cs0+" ("+year+")")
        ed_chaps(1,one_chap,one_ed)
    def chap_1_author_2_ed():
        j("chap","EdCount",2,"HCitation",cs0+" ("+year+")")
        ed_chaps(2,one_chap,two_ed)

    def unpub_1_author():
        j("unpub","AuthorCount",1,"HCitation",s0+" ("+year+")")
        j("unpub","AuthorCount",1,"HReference",s0+", "+i0+" ("+year+") "+title+". "+s("CityOfPub")+": "+s("Publisher")+"."+" Unpublished.")
    def custom():
        j("custom","AuthorCount",0,"HCitation",s("CiteOverride"))
        j("custom","AuthorCount",0,"HReference",s("RefOverride"))
     #mod add function to generate the right syntax

    book_single_author()
    book_2_authors()
    book_3_authors()
    book_4_authors()
    journal_1_author()
    journal_2_authors()
    journal_3_authors()
    journal_4_authors()
    webpage()
    assemble_dataset()
    assemble_conf_papers_1_author()
    ed_1_author()
    ed_2_authors()
    ed_3_authors()
    ed_4_authors()
    chap_1_author_1_ed()
    chap_1_author_2_ed()
    unpub_1_author()
    custom()
    #mod list function here


########################## Write the information entered into the boxes to the dataframe######################
#This puts the data into fields in the table, but the citation is assembled in the assemble() function.

def cite(event=None):
    global t

    keys=[]
    values=[]
    dictionary={}

    for x in boxes:

        if x[media]==True and x["field"]!=None:

            keys.append(str(x["field"]))

            values.append(str(x["box"].get()))
    surnames=[]
    initials=[]
    ed_surnames=[]
    ed_initials=[]
    chap_surnames=[]
    chap_initials=[]

    def append(sbox,ibox,s,i):


        for x in sbox.get(0,END):
            s.append(x)
        for x in ibox.get(0,END):
            i.append(x)

    append(surnamelist,ilist,surnames,initials)
    append(esurnamelist,eilist,ed_surnames,ed_initials)
    append(csurnamelist,cilist,chap_surnames,chap_initials)

    keys.append("AuthorCount")
    values.append(int(len(surnames)))
    keys.append("EdCount")
    values.append(int(len(ed_surnames)))
    keys.append("ChapCount")
    values.append(int(len(chap_surnames)))

    def fill(s,i):
        for x in range(6-len(s)):
            s.append(None)
            i.append(None)
    fill(surnames,initials)
    fill(ed_surnames,ed_initials)
    fill(chap_surnames,chap_initials)


    def name(f,l):
        try:
            keys.append(f)
            values.append(l)
        except:
            pass

    name("Surname0",surnames[0])
    name("Surname1",surnames[1])
    name("Surname2",surnames[2])
    name("Surname3",surnames[3])
    name("Surname4",surnames[4])
    name("Surname5",surnames[5])
    name("Initial0",initials[0])
    name("Initial1",initials[1])
    name("Initial2",initials[2])
    name("Initial3",initials[3])
    name("Initial4",initials[4])
    name("Initial5",initials[5])
    name("Ed_Surname0",ed_surnames[0])
    name("Ed_Surname1",ed_surnames[1])
    name("Ed_Surname2",ed_surnames[2])
    name("Ed_Surname3",ed_surnames[3])
    name("Ed_Surname4",ed_surnames[4])
    name("Ed_Surname5",ed_surnames[5])
    name("Ed_Initial0",ed_initials[0])
    name("Ed_Initial1",ed_initials[1])
    name("Ed_Initial2",ed_initials[2])
    name("Ed_Initial3",ed_initials[3])
    name("Ed_Initial4",ed_initials[4])
    name("Ed_Initial5",ed_initials[5])
    name("Chap_Surname0",chap_surnames[0])
    name("Chap_Surname1",chap_surnames[1])
    name("Chap_Surname2",chap_surnames[2])
    name("Chap_Surname3",chap_surnames[3])
    name("Chap_Surname4",chap_surnames[4])
    name("Chap_Surname5",chap_surnames[5])
    name("Chap_Initial0",chap_initials[0])
    name("Chap_Initial1",chap_initials[1])
    name("Chap_Initial2",chap_initials[2])
    name("Chap_Initial3",chap_initials[3])
    name("Chap_Initial4",chap_initials[4])
    name("Chap_Initial5",chap_initials[5])


    keys.append("Media")
    values.append(media)
    keys.append("Project")
    values.append(projdrop.cget("text"))

    for i in range(len(keys)):
        dictionary[keys[i]]=values[i]
    t=t._append(dictionary,ignore_index=True)
    assemble()


    list_citations()

    exclude={"HReference","HCitation"}
    allcol = set(t.keys())
    t.to_csv('ref.csv',sep=";") #columns=list(exclude.symmetric_difference(allcol)),sep=";")


    reset()





########################## Check for any citations that have been cited in Ref Buddy but haven't been used in the project ###############
def check_unused():
    for x in files[files["Project"]==projdrop.cget("text")]["File"]:
        output = pypandoc.convert_file(x, 'plain', outputfile="unused.txt")
        assert output == ""


    file=open("unused.txt")
    filestring=""
    for x in file.readlines():
        filestring=filestring+str(x)


    usedwin=Tk()
    usedwin.title("Unused Citation Checker")
    for x in t["HCitation"]:

        if x in filestring:
            t.loc[((t["HCitation"]==x)), "Used"]="Used"
            l=Label(usedwin,text="🗸 "+x,bg="lightgreen",justify="left",width=50)
            l.pack()

        else:
            pass
    for x in t["HCitation"]:
        if x not in filestring:
            t.loc[((t["HCitation"]==x)), "Used"]="Not Used"
            l=Label(usedwin,text="✕ "+x,bg="red",justify="left",width=50)
            l.pack()




############## Read project out loud #############################
            #if this doesn't work try running sudo apt install pandoc


def check_prog(): #checks whether the function has finished and stops the progress bar
    if proofthread.is_alive():
        rootwin.after(1, check_prog)
    else:
        #prog.stop()
        prog.destroy()

def proofread(event=None): #puts the proofread function in a separate thread so that the progress bar can work
    global proofthread
    global prog
    #prog=ttk.Progressbar(rootwin,orient=HORIZONTAL,length=500,mode='indeterminate')
    prog=ttk.Progressbar(rootwin,orient=HORIZONTAL,length=500,mode='determinate',color="green")

    prog.grid(row=100,column=0,columnspan=100)
    proofthread=threading.Thread(target=generate_audio)

    proofthread.daemon=True
    #prog.start()
    proofthread.start()
    rootwin.after(1, check_prog)

def inc(n):
    for x in range(n):
        prog ['value']=prog ['value']+1
        time.sleep(0.001)
def generate_audio(event=None): #generates the mp3

    m="This tool may take several minutes to run, depending on the length of your document, and may look like it's not dong anything. Please be patient. A 500 word document will take approximately 45 seconds to generate."
    messagebox.showinfo(title="Slow Process", message=m)
    prog ['value']=0

    for x in files[files["Project"]==projdrop.cget("text")]["File"]:
        output = pypandoc.convert_file(x, 'plain', outputfile="readoutloud.txt")
        assert output == ""
    inc(20)
    file=open("readoutloud.txt")
    lines=""
    for x in file.readlines():
        lines=lines+" "+x
    inc(10)
    lines=lines.replace("-"," ")
    lines=lines.replace("|"," ")
    lines=lines.replace("+"," ")
    lines=lines.split("References")[0]
    inc(10)
    speak = gTTS(text=str(lines), lang='en', slow=False)
    inc(35)
    speak.save("readoutloud.mp3")
    inc(25)
    os.system("xdg-open readoutloud.mp3") #platdep



def areyousure(com,word):
    conf=messagebox.askquestion("Are you sure", "Do you really want to delete this "+word+"?")
    if conf=="yes":
        com()
    else:
        pass

####################### Make menu bar #################################

def makeribbon():
    global filegroup
    global listgroup
    global searchgroup
    global buttons
    global filtertab
    global ribbon
    global citationtab
    global chargroup
    global authorgroup
    global filetab
    global citetab
    global papergroup
    global toolstab
    global notegroup
    global projgroup
    global listgroup

    ribbon=ttk.Notebook(rootwin)
    style = ttk.Style()
    style.configure('TNotebook.Tab', font=bgtabstyle,background=bgcolor, foreground=textcolor, padding=[10,5])
    #style.map("TNotebook.Tab",background=[("active", accentcolor)],font=[("active",("Verdana",10,"bold underline"))])
    style.map("TNotebook.Tab",background=[("selected", accentcolor)],font=[("selected",activetabstyle)])
    style.configure('TNotebook',borderwidth=0)


    def maketab(label):
        f=Frame(ribbon,bg=accentcolor,relief="flat")


        ribbon.add(f,text=label)
        return f
    def makegroup(tab,label,col):
        l=LabelFrame(tab,text=label,bg=accentcolor2,font=groupstyle,labelanchor="s",bd=3,relief="flat")
        l.grid(row=0,column=col,padx=10,pady=10)
        return l

    ############### Make tabs##############
    filetab=maketab("File")
    #viewtab=maketab("View")
    citationtab=maketab("Citations")
    #filtertab=maketab("Filter")
    citetab=maketab("Cite")
    prooftab=maketab("Proofread")

    ################ Place Ribbon in window #############
    ribbon.grid(row=0,column=0,columnspan=500,sticky="w")


    ################ Make groups to organise buttons on tabs##################
    filegroup=makegroup(filetab,"File",1)
    projgroup=makegroup(filetab,"Project File",2)
    opengroup=makegroup(filetab,"Open List",3)
    showgroup=makegroup(filetab,"Show/ Hide",4)
    notegroup=makegroup(filetab,"Notepad",4)
    #findgroup=makegroup(filtertab,"Find",100)
    #windowgroup=makegroup(viewtab,"Window",0)
    copygroup=makegroup(citationtab,"Copy",0)

    #accessgroup=makegroup(filtertab,"Used/Access",0)

    exportgroup=makegroup(filetab,"Export",4)
    searchgroup=makegroup(citationtab,"Search",100)
    citegroup=makegroup(citetab,"Cite New",0)
    authorgroup=makegroup(citetab,"Authors",1)
    writegroup=makegroup(citetab,"Cite",2)
    chargroup=makegroup(citetab,"Chars",10)
    proofgroup=makegroup(prooftab,"Proofread",10)
    papergroup=makegroup(citationtab,"Paper",1)
    listgroup=makegroup(citationtab,"Citations",2)
    sortgroup=makegroup(citationtab,"Sort",3)
    listgroup=makegroup(citationtab,"",100)


    ############### Load icons for buttons ##################
    global delpersonicon
    global removeallauthors
    addauthoricon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/addauthoricon.png').subsample(1)
    bookicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/bookicon.png').subsample(1)
    copyciteicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/copyciteicon.png').subsample(1)
    copyicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/copyicon.png').subsample(1)
    copyindexicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/copyindexicon.png').subsample(1)
    copyreficon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/copyreficon.png').subsample(1)
    csvicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/csvicon.png').subsample(1)
    delicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/delicon.png').subsample(1)
    delpersonicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/delpersonicon.png').subsample(1)
    exporticon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/exporticon.png').subsample(1)
    googleicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/googleicon.png').subsample(1)
    hideicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/hideicon.png').subsample(1)
    journalicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/journalicon.png').subsample(1)
    lockicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/lockicon.png').subsample(1)
    maximiseicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/maximiseicon.png').subsample(1)
    maximiseicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/maximiseicon.png').subsample(1)
    minimiseicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/minimiseicon.png').subsample(1)
    minimiseicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/minimiseicon.png').subsample(1)
    newicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/newicon.png').subsample(1)
    newicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/newicon.png').subsample(1)
    notepadicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/notepadicon.png').subsample(1)
    pdficon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/pdficon.png').subsample(1)
    reloadicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/reloadicon.png').subsample(1)
    reloadicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/reloadicon.png').subsample(1)
    removeallauthors=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/removeallauthors.png').subsample(1)
    showallicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/showallicon.png').subsample(1)
    showicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/showicon.png').subsample(1)
    showicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/showicon.png').subsample(1)
    sortauthoricon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/sortauthoricon.png').subsample(1)
    sortdatedescicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/sortdatedescicon.png').subsample(1)
    sortdownicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/sortdownicon.png').subsample(1)
    sorttitleicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/sorttitleicon.png').subsample(1)
    sortupicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/sortupicon.png').subsample(1)
    soundicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/soundicon.png').subsample(1)
    switchicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/switchicon.png').subsample(1)
    switchicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/switchicon.png').subsample(1)
    txticon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/txticon.png').subsample(1)
    urlicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/urlicon.png').subsample(1)
    wordicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/wordicon.png').subsample(1)
    writeicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/writeicon.png').subsample(1)
    accessicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/accessicon.png').subsample(1)
    noaccessicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/noaccessicon.png').subsample(1)
    usedicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/usedicon.png').subsample(1)
    unusedicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/unusedicon.png').subsample(1)
    redaicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/redaicon.png').subsample(1)
    greenaicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/greenaicon.png').subsample(1)
    dataicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/dataset.png').subsample(1)
    conficon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/conf.png').subsample(1)
    edbookicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/edbookicon.png').subsample(1)
    chapicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/chaptericon.png').subsample(1)
    unpubicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/unpubicon.png').subsample(1)
    pinicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/pinicon.png').subsample(1)
    customicon=PhotoImage(file='/home/jonathan/Documents/Tech/Scripts/Icons/customicon.png').subsample(1)
    #mod add path to new icon here



    ################## Make buttons ###############################
    buttons=[{"image":newicon,"img":"✱","name":"New project","short":"<Control-n>","short2":"<Control-N>","command":newproj,"menu":filegroup, "row":1,"col":0},
             {"image":delicon,"img":"🗑","name":"Delete project","short":None,"command":askdel,"menu":filegroup, "row":1,"col":1},
             {"image":pinicon,"img":"","name":"Set as Default","short":None,"command":None,"menu":filegroup, "row":1,"col":3},
             {"image":txticon,"img":"🖉","name":"Open list as .txt","short":"<Control-o>","command":export_as_txt,"menu":opengroup, "row":0,"col":0},
             {"image":csvicon,"img":"𝓧","name":"Open list as .csv","short":"<Control-O>","command":export_as_csv,"menu":opengroup, "row":1,"col":0},
             {"image":wordicon,"img":"Ｗ","name":"Open Project","short":None,"short2":None,"command":openfile,"menu":projgroup, "row":1,"col":0},
             {"image":switchicon,"img":"⥂","name":"Change Project File","short":None,"short2":None,"command":changefile,"menu":projgroup, "row":1,"col":1},
             
             
             {"img":"🔎","name":"Find","short":"<Control-f>","short2":"<Control-F>","command":search,"menu":listgroup, "row":1,"col":100},

             {"image":copyreficon,"img":"🗇Ｒ","name":"Copy full reference","short":None,"command":copyref,"menu":copygroup, "row":0,"col":1},
             {"image":copyciteicon,"img":"🗇Ｃ","name":"Copy citation","short":None,"command":copycite,"menu":copygroup, "row":0,"col":2},
             {"image":copyindexicon,"img":"🗇ｉ","name":"Copy index number","short":None,"command":copyindex,"menu":copygroup, "row":1,"col":1},
            {"image":delicon,"img":"🗑","name":"Delete citation","short":None,"command":ask_delref,"menu":copygroup, "row":1,"col":2},

             {"image":urlicon,"img":"🌐","name":"Open paper URL","short":"<Control-u>","short2":"<Control-U>","command":open_url,"menu":papergroup, "row":0,"col":0},
             {"image":pdficon,"img":"🗎","name":"Open paper PDF","short":"<Control-p>","short2":"<Control-P>","command":open_pdf,"menu":papergroup, "row":1,"col":0},

            {"image":sortupicon,"img":"⇧","name":"Newest First","short":None,"command":sort_newest,"menu":sortgroup, "row":0,"col":0},
            {"image":sortdownicon,"img":"⇩","name":"Oldest First","short":None,"command":sort_oldest,"menu":sortgroup, "row":0,"col":1},
            {"image":sortauthoricon,"img":"👥","name":"By Author","short":None,"command":sort_author,"menu":sortgroup, "row":1,"col":0},
            {"image":sorttitleicon,"img":"Ｔ","name":"By Title","short":None,"command":sort_title,"menu":sortgroup, "row":1,"col":1},

             {"image":bookicon,"img":"📖","name":"Cite new book","short":"<Control-b>","short2":"<Control-B>","command":book,"menu":citegroup, "row":0,"col":0},
             {"image":journalicon,"img":"📰","name":"Cite new journal","short":"<Control-j>","short2":"<Control-J>","command":journal,"menu":citegroup, "row":0,"col":1},
             {"image":urlicon,"img":"🌍","name":"Cite new webpage","short":"<Control-w>","short2":"<Control-W>","command":web,"menu":citegroup, "row":1,"col":0},
             {"image":dataicon,"img":"🗠","name":"Cite new dataset","short":"<Control-d>","short2":"<Control-D>","command":dataset,"menu":citegroup, "row":1,"col":1},
             {"image":conficon,"img":".","name":"Cite new conference paper","short":None,"short2":None,"command":confpapers,"menu":citegroup, "row":0,"col":2},
             {"image":edbookicon,"img":".","name":"Cite new edited book","short":"<Control-e>","short2":None,"command":edbook,"menu":citegroup, "row":1,"col":2},
             {"image":chapicon,"img":".","name":"Cite new chapter in an edited book","short":"<Control-h>","short2":None,"command":chap,"menu":citegroup, "row":1,"col":3},
             {"image":unpubicon,"img":".","name":"Cite new unpublished item","short":"<Control-u>","short2":None,"command":unpub,"menu":citegroup, "row":0,"col":3},
             {"image":customicon,"img":".","name":"Manually create custom citation","short":None,"short2":None,"command":custom,"menu":citegroup, "row":0,"col":4},


             {"image":removeallauthors,"img":"⛔👥","name":"Delete all authors in citation","short":None,"command":None,"menu":authorgroup, "row":0,"col":0},

             {"image":writeicon,"img":"✔","name":"Write to file","short":"<Control-Return>","command":cite,"menu":writegroup, "row":1,"col":0},

             {"image":soundicon,"img":"📢","name":"Read out loud","short":"<Control-r>","command":proofread,"menu":proofgroup, "row":0,"col":0},

            {"image":usedicon,"img":"U","name":"Check for unused citations","short":None,"short2":None,"command":check_unused,"menu":proofgroup, "row":1,"col":0}]
    #mod add new button here
    c=0

    global photo
    def makebutton(menu,command,img,short,c,tip):
        b=Button(menu,command=command,image=img,bg=bgcolor,relief="flat",bd=0,highlightthickness=0)
        b.grid(row=0,column=c,padx=5)
        print(img)
        rootwin.bind(short,command)
        tip = Hovertip(b,tip+" ("+short+")")
        return b

    for i in buttons:
        try:
            pass
            b=Button(i["menu"],text=i["img"],command=i["command"],image=i["image"],bg=bgcolor,relief="flat",bd=0,highlightthickness=0)
        except:
            pass
            b=Button(i["menu"],text=i["img"],command=i["command"],bg=bgcolor,relief="flat",highlightthickness=0)

        b.grid(row=i["row"],column=i["col"],padx=5)
        tip = Hovertip(b,str(i["name"])+" ("+str(i["short"])+")")
        c=c+1
        rootwin.bind(i["short"],i["command"])
        try:
            rootwin.bind(i["short2"],i["command"])
        except:
            pass


load()
makeribbon()
list_projects()
list_citations()
loadfile()
rootwin.bind("<Tab>",inscheck)
book()
rootwin.mainloop()
