'''
Citation management system, adapted to Sheffield's flavor of Harvard.
It's easy to add new media types. Places where it's necessary to modify the code are marked with #mod
#platdep indicates bits which are platform dependent
'''

import os
'''
packages=["gTTS","pandas","pypandoc","tkinter","datetime","threading","time","os","sys"]
for i in packages:
    os.system("pip install "+i+" --break-system-packages")
'''
from datetime import *

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from gtts import gTTS
import os.path
from tkinter import messagebox
import pandas as pd
import pypandoc
import time
import threading
from idlelib.tooltip import Hovertip



##Either read in the existing database or make a new one from scratch
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
        "RefOverride":[""],
        "CommMethod":[""],
        "Receiver":[""],
        "prep":[""]}
        #mod add new fields to this list
        
        
        projfiles={"Project":["Panspermia"],"File":["./SampleDocument.odt"],"Default":True}

    t=pd.DataFrame(data)
  
    files=pd.DataFrame(projfiles)
    
    t.astype(str)
    t.fillna(0,inplace=True)
    
    t.to_csv('ref.csv',sep=";")
    files.to_csv('files.csv',sep=";")
    unnamed()

## Remove old outputs 
def clean():
    os.system("rm -f *.txt")
    os.system("rm -f *.mp3")
    os.system("rm -f reflist*")
    
### Search facility##
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


## Sort reference list #
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


## Remove fields labelled 'unnamed'##
#Currently unknown where these fields are coming from - function to remove them is a workaround.
def unnamed():
    global files
    global t
    
    for x in t.head(0):
        if "Unnamed" in str(x):
            t=t.drop(x,axis=1)
    t.to_csv('ref.csv',sep=";")
    
    for x in files.head(0):
        if "Unnamed" in str(x):
            files=files.drop(x,axis=1)
    files.to_csv('files.csv',sep=";")

## Make new project #
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


## Delete project #

def askdel():
    areyousure(delproject,"project")
def delproject():

    todel = t[ t['Project'] == str(cur_proj())].index
    t.drop(todel,inplace=True)
    t.to_csv('ref.csv',sep=";")
    load()
    list_projects()



## List of projects#
def change_proj(event=None):
    global projdrop

    curproj.set(cur_proj())
    list_citations()
    loadfile()
    rootwin.title(str(curproj.get()))
    
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
   
    if 'projdrop' in globals():
        projdrop.destroy()
   

    projdrop=OptionMenu(filegroup,curproj,*projects,command=change_proj)
    projdrop.grid(row=0,column=0,columnspan=30)

    confdrop(projdrop)

    curproj.set(projects[0])
    rootwin.title("Project: "+str(curproj.get()))

## Cycle between projects with the pgup and pgdown keys

def move(n):
    try:
        curproj.set(projects[int(projects.index(str(cur_proj())))+n])
    except:
        curproj.set(projects[0])
    change_proj()
    
def nextproj(event=None):
    move(1)
def prevproj(event=None):
    move(-1)

## Open project document#

def loadfile():
    global files
    global filelist

    filelist=files[files["Project"]==str(cur_proj())]["File"]
    if len(filelist)<1:
        p=filedialog.askopenfilename(title="Link Project File")

        files=files._append({"Project":cur_proj(),"File":p},ignore_index=True)
        files.to_csv('files.csv',sep=";")
    display_proj()

def openfile():
    loadfile()
    for x in filelist:
        os.system('xdg-open "'+str(x)+'"') #platdep



def changefile(event=None):


    p=filedialog.askopenfilename(title="Change Project File")
    files.loc[files["Project"] == cur_proj(), "File"] = p
    files.to_csv('files.csv',sep=";")
    loadfile()

def display_proj():
    global plabel
    try:
        plabel.destroy()
    except:
        pass
    for x in filelist:
        plabel=Label(projgroup,bg=btncolor,text=(x.split("/")[-1]))
        plabel.grid(row=0,column=0,columnspan=20)

## List all recorded citations #
def list_citations():
    global citedrop
    global refdrop
    global ref
    global citation
    global citations
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
    for x in t[t["Project"]==curproj.get()]["Title"]:
        refs.append(x)
      

    try:
        citedrop.destroy()
        refdrop.destroy()
    except:
        pass
    citedrop=OptionMenu(listgroup,citation,*citations,command=sync_cite)
    
    citedrop.grid(row=0,column=1,sticky="w")

    citation.set(citations[0])

    refdrop=OptionMenu(listgroup,ref,*refs,command=sync_ref)
    
    refdrop.grid(row=1,column=1,sticky="w")
    ref.set(refs[0])

    confdrop(refdrop)
    confdrop(citedrop)
    

##get selected citation
def cur_cite():
    return citedrop.cget("text")
def cur_ref():
    return refdrop.cget("text")
def cur_proj():
    return projdrop.cget("text")
### Keep the citation and reference boxes in sync, so that they always show text from the same citation##

def makestring(x):
    return x.index.astype(str)[0]
def sync_cite(event=None):
    i=int(makestring(t[t["HCitation"]==cur_cite()]))
    ref.set(t.iloc[i]["Title"])

def sync_ref(event=None):
    i=int(makestring(t[t["Title"]==cur_ref()]))
    citation.set(t.iloc[i]["HCitation"])


## Export reference list##
def export_as_csv(event=None):
    pd.set_option('display.max_colwidth', None)
    export_table=(t[t["Project"]==cur_proj()][["HCitation","HReference"]])
    export_table.to_csv('reflistcsv.csv',sep=";",index=False)
    os.system("xdg-open reflistcsv.csv") #platdep

def export_as_txt(event=None):
    pd.set_option('display.max_colwidth', None)
    export_table=(t[t["Project"]==cur_proj()]["HReference"])
    export_table.to_csv('reflisttxt.csv',sep=";",index=False,header=None)
    os.system("gnome-text-editor reflisttxt.csv") #platdep

##Open master sheet
def openmaster(event=None):
    x="Opening backend database for manual editing. \nRemoving data may permanently break the database. \nThis should only be used to correct data entry mistakes. \nTo export an independent reference list, use the export tools on the file tab.\n\nRefBuddy uses semicolons as the field deliminator, but Excel will assume that it is separated by commas - be sure to change this."
    messagebox.showwarning(title="Proceed with caution", message=x)
    os.system("xdg-open ref.csv")

def copyref():
    rootwin.clipboard_clear()
    rootwin.clipboard_append(cur_ref()) #change
def copycite():
    rootwin.clipboard_clear()
    rootwin.clipboard_append(cur_cite())
def copyindex():
    rootwin.clipboard_clear()
    rootwin.clipboard_append(int(makestring(t[t["HCitation"]==cur_cite()])))


## Delete a reference#
def ask_delref():
    areyousure(delref,"reference")

def delref():
    global t
    i=int(makestring(t[t["HCitation"]==cur_cite()]))
    i=int(i)
    t=t.drop([i])
    t.to_csv('ref.csv',sep=";")
    list_citations()

## Make window#

def makestyles():
    global bgcolor
    global accentcolor
    global accentcolor2
    global textcolor
    global activetabstyle
    global bgtabstyle
    global groupstyle
    global labelstyle
    global entrystyle
    global btncolor

    bgcolor="aliceblue"
    accentcolor="lightcyan1"
    accentcolor2="lightcyan2"
    textcolor="black"
    activetabstyle=("Verdana",10,)
    bgtabstyle=("Verdana",10)
    groupstyle=("Verdana",6)
    labelstyle=("Verdana",10)
    entrystyle=("Verdana",10)
    btncolor="white"

def exit(event=None):
    pass
def makewin(event=None):
    global rootwin
    rootwin=Tk() #Tk window
    rootwin.title("Referencing")
    #rootwin.configure(bg=bgcolor)
    rootwin.attributes("-alpha", 0)
    rootwin.wm_attributes('-type', 'splash')
    

    
    rootwin.geometry('%dx%d+%d+%d' % (500, 125, rootwin.winfo_screenwidth(), rootwin.winfo_screenheight()))

    
    

    #rootwin.wm_attributes("-topmost", True)


## Add an author to the list of authors so that another can be added#

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
        sentry.focus_set()
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
    


### Entry boxes for data#
#'cap' indicates whether data from that box should be auto capitalised.

def makeboxframes():
    global boxframe
 
    boxframe=Frame(citewin,bg=bgcolor)
    boxframe.grid(row=1,column=0)



def makebox():
    global boxframe
    return Entry(boxframe,relief="flat",borderwidth=-1,highlightthickness=-1,background=accentcolor2,font=entrystyle,width=40)

def makeboxes():
    global titlebox
    global editionbox
    global surnamebox
    global initialbox
    global edsurnamebox
    global edinitialbox
    global chapsurnamebox
    global chapinitialbox
    global chaptitlebox
    global pubbox
    global citybox
    global yearbox
    global volbox
    global issuebox
    global pagesbox
    global urlbox
    global orgbox
    global accessbox
    global writtenbox
    global journalbox
    global conference_title_box
    global conference_place_box
    global conference_date_box
    global PDFbox
    global notesbox
    global customcite
    global customref
    global commbox
    global recbox
    global prepbox

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
    commbox=makebox()
    recbox=makebox()
    prepbox=makebox()

    #mod: insert new box here and make it global

def makefields():
    global boxes
    boxes=[{'box':titlebox,"text":"Title","book":1,"journal":1,"web":1,"data":1,"ed":1,"chap":1,"conf":1,"cap":1, "unpub":1,"custom":0,"pers":0,"None":0,"report":1,"All":1,"field":"Title"},
            {'box':editionbox,"text":"Edition","book":1,"journal":0,"web":0,"data":0,"ed":0,"chap":1,"conf":0,"cap":0,"unpub":0,"custom":0,"pers":0,"None":0,"report":0,"All":1,"field":"Edition"},
            {'box':surnamebox,"text":"Surname","book":1,"journal":1,"web":0,"data":0,"ed":0,"chap":0,"conf":1,"cap":0, "unpub":1,"custom":0,"pers":1,"None":0,"report":0,"All":1,"field":None},
            {'box':initialbox,"text":"Initials","book":1,"journal":1,"web":0,"data":0,"ed":1,"chap":0,"conf":1,"cap":0, "unpub":1,"custom":0,"pers":1,"None":0,"report":0,"All":1,"field":None},
            {'box':edsurnamebox,"text":"Ed. Surname","book":0,"journal":0,"web":0,"data":0,"ed":1,"chap":1,"conf":1,"cap":0,"unpub":0,"custom":0,"pers":0,"None":0,"report":0,"All":1,"field":None},
            {'box':edinitialbox,"text":"Ed. Initials","book":0,"journal":0,"web":0,"data":0,"ed":1,"chap":1,"conf":1,"cap":0,"unpub":0,"custom":0,"pers":0,"None":0,"report":0,"All":1,"field":None},
            {'box':chapsurnamebox,"text":"Chap. Surname","book":0,"journal":0,"web":0,"data":0,"ed":0,"chap":1,"conf":0,"cap":1,"unpub":0,"custom":0,"pers":0,"None":0,"report":0,"All":1,"field":None},
            {'box':chapinitialbox,"text":"Chap. Initials","book":0,"journal":0,"web":0,"data":0,"ed":0,"chap":1,"conf":0,"cap":1,"unpub":0,"custom":0,"pers":0,"None":0,"report":0,"All":1,"field":None},
            {'box':chaptitlebox,"text":"Chap. Title","book":0,"journal":0,"web":0,"data":0,"ed":0,"chap":1,"conf":0,"cap":1,"unpub":0,"custom":0,"pers":0,"None":0,"report":0,"All":1,"field":"Chap_Title"},
            {'box':pubbox,"text":"Publisher","book":1,"journal":0,"web":0,"data":0,"ed":1,"chap":1,"conf":0,"cap":1, "unpub":1,"custom":0,"pers":0,"None":0,"report":0,"All":1,"field":"Publisher"},
            {'box':citybox,"text":"City","book":1,"journal":0,"web":0,"data":0,"ed":1,"chap":1,"conf":0,"cap":1, "unpub":1,"custom":0,"pers":0,"None":0,"report":0,"All":1,"field":"CityOfPub"},
            {'box':yearbox,"text":"Year","book":1,"journal":1,"web":1,"data":1,"ed":1,"chap":1,"conf":1,"cap":0, "unpub":1,"custom":0,"pers":1,"None":0,"report":1,"All":1,"field":"Year"},
            {'box':journalbox,"text":"Journal","book":0,"journal":1,"web":0,"data":0,"ed":0,"chap":0,"conf":0,"cap":1,"unpub":0,"custom":0,"pers":0,"None":0,"report":0,"All":1,"field":"Journal"},
            {'box':volbox,"text":"Volume","book":0,"journal":1,"web":0,"data":0,"ed":0,"chap":0,"conf":0,"cap":0,"unpub":0,"custom":0,"pers":0,"None":0,"report":0,"All":1,"field":"Volume"},
            {'box':issuebox,"text":"Issue","book":0,"journal":1,"web":0,"data":0,"ed":0,"chap":0,"conf":0,"cap":0,"unpub":0,"custom":0,"pers":0,"None":0,"report":0,"All":1,"field":"Issue"},
            {'box':pagesbox,"text":"Pages","book":0,"journal":1,"web":0,"data":0,"ed":0,"chap":1,"conf":1,"cap":0, "unpub":0,"custom":0,"pers":0,"None":0,"report":1,"All":1,"field":"Pages"},
            {'box':urlbox,"text":"URL","book":1,"journal":1,"web":1,"data":1,"ed":1,"chap":1,"conf":1,"cap":0, "unpub":0,"custom":0,"pers":0,"None":0,"report":1,"All":1,"field":"URL"},
            {'box':orgbox,"text":"Org.","book":0,"journal":0,"web":1,"data":1,"ed":0,"chap":0,"conf":0,"cap":1, "unpub":0,"custom":0,"pers":0,"None":0,"report":1,"All":1,"field":"Organisation"},
            {'box':accessbox,"text":"Accessed","book":1,"journal":1,"web":1,"data":1,"ed":1,"chap":1,"conf":1,"cap":1, "unpub":0,"custom":0,"pers":1,"None":0,"report":1,"All":1,"field":"DateAccessed"},
            {'box':writtenbox,"text":"Written","book":0,"journal":0,"web":0,"data":0,"ed":0,"chap":0,"conf":0,"cap":1, "unpub":0,"custom":0,"pers":0,"None":0,"report":0,"All":1,"field":"DateWritten"},
            {'box':conference_place_box,"text":"Conference Place","book":0,"journal":0,"web":0,"data":0,"ed":0,"chap":0,"conf":1,"cap":1, "unpub":0,"custom":0,"pers":0,"None":0,"report":0,"All":1,"field":"Place_Conf"},
            {'box':conference_title_box,"text":"Conference Name","book":0,"journal":0,"web":0,"data":0,"ed":0,"chap":0,"conf":1,"cap":1, "unpub":0,"custom":0,"pers":0,"None":0,"report":0,"All":1,"field":"Name_Conf"},
            {'box':conference_date_box,"text":"Conference Date","book":0,"journal":0,"web":0,"data":0,"ed":0,"chap":0,"conf":1,"cap":1, "unpub":0,"custom":0,"pers":0,"None":0,"report":0,"All":1,"field":"Date_Conf"},
            {'box':PDFbox,"text":"PDF","book":1,"journal":1,"web":1,"data":1,"ed":1,"chap":1,"conf":1,"cap":1, "unpub":0,"custom":0,"pers":0,"None":0,"report":0,"All":1,"field":"PDF"},
            {'box':notesbox,"text":"Notes","book":1,"journal":1,"web":1,"data":1,"ed":1,"chap":1,"conf":1,"cap":1, "unpub":0,"custom":0,"pers":0,"None":0,"report":0,"All":1,"field":"Notes"},
            {'box':customcite,"text":"Custom Citation","book":0,"journal":0,"web":0,"data":0,"ed":0,"chap":0,"conf":0,"cap":0,"unpub":0,"custom":1,"pers":0,"None":0,"report":0,"All":1,"field":"CiteOverride"},
            {'box':customref,"text":"Custom Reference","book":0,"journal":0,"web":0,"data":0,"ed":0,"chap":0,"conf":0,"cap":0,"unpub":0,"custom":1,"pers":0,"None":0,"report":0,"All":1,"field":"RefOverride"},
            {'box':commbox,"text":"Communication Method","book":0,"journal":0,"web":0,"data":0,"ed":0,"chap":0,"conf":0,"cap":0,"unpub":0,"custom":0,"pers":1,"None":0,"report":0,"All":1,"field":"CommMethod"},
            {'box':recbox,"text":"Receiver","book":0,"journal":0,"web":0,"data":0,"ed":0,"chap":0,"conf":0,"cap":0,"unpub":0,"custom":0,"pers":1,"None":0,"report":0,"All":1,"field":"Receiver"},
            {'box':prepbox,"text":"Preposition","book":0,"journal":0,"web":0,"data":0,"ed":0,"chap":0,"conf":0,"cap":0,"unpub":0,"custom":0,"pers":1,"None":0,"report":0,"All":1,"field":"prep"}]
            #mod: insert new box here
            #book,web,data field etc indicates whether it should show up for that medium. 1=show 0=hide. Add a new key for any new medium.

def makecitewin():
    global citewin
    global tlabel
    try:
        citewin.withdraw()
    except:
        pass


    
    citewin=Tk()
 
    citewin.title("Cite new")
    
    tlabel=Label(citewin,text="",bg=bgcolor,font=labelstyle)
    tlabel.grid(row=0,column=0)
  

    
    citewin.configure(bg=bgcolor)
    citewin.wm_attributes("-topmost", True)
    citewin.wm_attributes('-type', 'splash')
    #citewin.focus_force()

    closebtn=Button(citewin,text="❌",command=closecitewin,relief="flat",bg=bgcolor,highlightthickness=0)
    closebtn.grid(row=0,column=1000,sticky="e")
    citewin.bind("<FocusIn>",maximise)
    #citewin.overrideredirect(1)
    
    
def closecitewin(event=None):
    citewin.withdraw()
    

def makelabels():

    for x in boxes:
        x["default"]=str(x["text"])
        x["text"]=Label(boxframe,text=x["text"],bg="aliceblue",justify="right",font=labelstyle)
        x["box"].bind("<1>",insclick)
        #x["box"].bind("<1>",maximise)



## Populate window with fields necessary to cite selected media#

def refresh(forwhat):
    
  
    citewin.deiconify()
    
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
    global authorframe
    global editorframe
    global chapterframe

    r=1
    for x in boxes:
        if x[forwhat]==1:
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
        b=Button(f,command=com,text="-",relief="flat",bg=accentcolor2,highlightthickness=0)
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


def citenew(m,title):
    global media
    refresh(m)
    media=m
    rootwin.title("Project: "+str(curproj.get()))
    tlabel.configure(text="Citing new "+str(title)+" into "+str(curproj.get()))
    citewin.title("Citing New "+str(title)+" into "+str(projdrop.cget("text")))


def book(event=None):
    citenew("book","Book")
def journal(event=None):
    citenew("journal","Journal")
def web(event=None):
    citenew("web","Webpage")
def dataset(event=None):
    citenew("data","Dataset")
def confpapers(event=None):
    citenew("conf","Conference Paper")
def edbook(event=None):
    citenew("ed","Edited Book")
def chap(event=None):
    citenew("chap","Chapter")
def unpub(event=None):
    citenew("unpub","Unpublished Material")
def custom(event=None):
    citenew("custom","Custom Citation")
def pers(event=None):
    citenew("pers","Personal Communication")
def report(event=None):
    citenew("report","Report")
#mod add function here

def edit(event=None):
    
   
    rowtoedit=t[t["Title"]==cur_ref()]
    
    for i in (rowtoedit["Media"]):
        print(i)
        citenew(i)
    
        for x in boxes:
            if x[i]==1:
                x["box"].delete(0, END)
                for z in rowtoedit[x["field"]]:
                    x["box"].insert(0,z)
    for b in boxes:
        if "NaN" in str(b["box"].get()):
            b["box"].delete(0,END)
            
          
        
        
    
mini=False
def minimise(event=None):
    global mini
    
    if (rootwin.focus_get()) == None:
   
        
        rootwin.geometry('%dx%d+%d+%d' % (150, 25, rootwin.winfo_screenwidth(), rootwin.winfo_screenheight()))
        rootwin.wm_attributes("-topmost", True)
    
    
def maximise(event=None):
    global mini
  
    rootwin.wm_attributes("-topmost", True)
    #rootwin.geometry('%dx%d+%d+%d' % (ribbon.winfo_width(), int(ribbon.winfo_height()), rootwin.winfo_screenwidth(), rootwin.winfo_screenheight()))

    
    if (ribbon.tab(ribbon.select(), "text"))=="💬":
        rootwin.geometry('%dx%d+%d+%d' % (ribbon.winfo_width(), int(ribbon.winfo_height()), rootwin.winfo_screenwidth(), rootwin.winfo_screenheight()))
        
    else:
        rootwin.geometry('%dx%d+%d+%d' % (ribbon.winfo_width(), 150, rootwin.winfo_screenwidth(), rootwin.winfo_screenheight()))
    
    





## Link PDF of paper to reference #
def linkpdf(event):
    
    types= (('Open Documents', '*.od*'),('All', '*'),('Microsoft Office Documents', '*docx'))
    for x in files[files["Project"]==cur_proj()]["File"]:
        p=filedialog.askopenfilename(title="Link PDF",filetypes=types,initialdir=(x.replace(plabel.cget("text"),"")))
    PDFbox.insert(0,p)


## Open PDF or URL linked to reference #
def open_pdf(event=None):
    x=""
    for x in t[t["Title"]==cur_ref()]["PDF"]:

        if "nan" in str(x):
            p=filedialog.askopenfilename(title="Link PDF")
            t.loc[(t["Title"]==cur_ref()), "PDF"]=p
            t.to_csv('ref.csv',sep=";")
        else:
            os.system('xdg-open "'+str(x)+'"') #platdep

def open_url(event=None):
    x=""
    for x in t[t["Title"]==cur_ref()]["URL"]:
        os.system('xdg-open "'+str(x)+'"') #platdep



## Clear boxes after media has been cited #
def reset(event=None):
    
    for widget in boxframe.winfo_children():
        try:
            widget.delete(0,END)
        except:
            pass
        widget.grid_forget()
    



## Assemble the citation into the right syntax#
def assemble():
    
    global t
    #global year
    #global title
    def s(x):
        z=t[x].astype(str).str.replace("[","").str.replace("]","").str.replace("'","")
        return z

    def j(media,thingtocount,ac,field,ref): #ac=authorcount

        t.loc[((t["Media"]==media) & (t[thingtocount]==ac)), field]=ref#needs fixing - author count only counts authors not editors or chapter authors

    #numbers come out as decimals. This removes the decimal points from numeric fields
    def makedec(field):
        try:
            t[field]=t[field].astype(int).astype(str)
            return s(field)
        except:
            return(s(field))
    year=makedec("Year")
    ed=makedec("Edition")
    vol=makedec("Volume")
    #issue=makedec("Issue")
    issue=s("Issue")
    title=s("Title")


    book=" ("+year+") "+title+". "+ed+" edn. "+s("CityOfPub")+": "+s("Publisher")+"."
    journal=" ("+year+") '"+title+"', "+s("Journal")+", "+vol+" ("+issue+"), pp. "+s("Pages")+". "+s("URL")
  

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
        j("chap","EdCount",n,"HReference",a+" ("+year+") '"+s("Chap_Title")+"', in "+b+" (ed) "+title+". "+ed+". "+s("CityOfPub")+": "+s("Publisher")+", "+s("Pages")+".")
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
    def cite_pers():
        j("pers","AuthorCount",1,"HCitation",s0+", "+i0+" ("+year+")")
        j("pers","AuthorCount",1,"HReference",s0+", "+i0+" ("+year+") "+s("CommMethod")+" "+s("prep")+" "+s("Receiver")+", "+s("DateAccessed"))
    def cite_report():
        j("report","AuthorCount",0,"HCitation",s("Organisation")+" ("+year+")")
        j("report","AuthorCount",0,"HReference",s("Organisation")+" ("+year+") "+title+". "+"pp. "+s("Pages")+". Available at: "+s("URL")+" (Accessed: "+s("DateAccessed")+")")
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
    cite_pers()
    cite_report()
    
    #mod list function here


## Write the information entered into the boxes to the dataframe##
#This puts the data into fields in the table, but the citation is assembled in the assemble() function.

def cite(event=None):
    global t

    keys=[]
    values=[]
    dictionary={}

    for x in boxes:

        if x[media]==1 and x["field"]!=None:

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
    values.append(cur_proj())

    for i in range(len(keys)):
        dictionary[keys[i]]=values[i]
    t=t._append(dictionary,ignore_index=True)
    assemble()


    list_citations()
    t.to_csv('ref.csv',sep=";") #columns=list(exclude.symmetric_difference(allcol)),sep=";")
    
    for x in t["HCitation"].tail(1):
        ribbon.select(citationtab)
        #citedrop.set(x)
        #sync_cite()
        #copyref()
        rootwin.clipboard_clear()
        rootwin.clipboard_append(x)
    for x in t["HReference"].tail(1):
         messagebox.showinfo(title="Sucessfully Cited", message=x)
    citewin.withdraw()
         
    reset()





## Check for any citations that have been cited in Ref Buddy but haven't been used in the project #
def check_unused(): #find project file and convert to txt
    for x in files[files["Project"]==cur_proj()]["File"]:
        output = pypandoc.convert_file(x, 'plain', outputfile="unused.txt")
        assert output == ""
    file=open("unused.txt")
    filestring=""
    for x in file.readlines():
        filestring=filestring+str(x)


    usedwin=Tk()
    usedwin.title("Unused Citation Checker")
    
    def makeusedlabel(used,mark,color):
            t.loc[((t["HCitation"]==x)), "Used"]=used
            l=Label(usedwin,text=mark+"  "+x,bg=color,justify="left",width=50)
            l.pack()
    
    for x in citations: #if statements are in separate blocks so that the correct ones appear on top. Using an elif mixes them up
        if x in filestring:
            makeusedlabel("Used","🗸","lightgreen")
        
    for x in citations:
        if x not in filestring:
            makeusedlabel("Not Used","✕","red")




## Read project out loud
#if this doesn't work try running sudo apt install pandoc


def check_prog(): #checks whether the function has finished and stops the progress bar
    if proofthread.is_alive():
        rootwin.after(1, check_prog)
    else:
        prog.destroy()

def proofread(event=None): #puts the proofread function in a separate thread so that the progress bar can work
    global proofthread
    global prog
    
    prog=ttk.Progressbar(rootwin,orient=HORIZONTAL,length=500,mode='determinate')
    prog.grid(row=100,column=0,columnspan=100)
    proofthread=threading.Thread(target=generate_audio)
    proofthread.daemon=True
    proofthread.start()
    rootwin.after(1, check_prog)

def inc(n):
    for x in range(n):
        prog ['value']=prog ['value']+1
        time.sleep(0.001)
def generate_audio(event=None): #generates the mp3

    m="This tool may take several minutes to run. A 500 word document will take approximately 45 seconds to generate."
    messagebox.showinfo(title="Slow Process", message=m)
    prog ['value']=0

    for x in files[files["Project"]==cur_proj()]["File"]:
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


## Make menu bar##

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
    style.map("TNotebook.Tab",background=[("selected", accentcolor)],font=[("selected",activetabstyle)])
    style.configure('TNotebook',borderwidth=0)


    def maketab(label):
        f=Frame(ribbon,bg=accentcolor,relief="flat")
        ribbon.add(f,text=label)
        return f
    
    def makegroup(tab,label,r,col):
        l=LabelFrame(tab,text=label,bg=accentcolor2,font=groupstyle,labelanchor="s",bd=3,relief="flat")
        l.grid(row=r,column=col,padx=10,pady=10)
        return l

    # Make tabs#
    filetab=maketab("🖿")
    citationtab=maketab("💬")
    citetab=maketab("🖉")
    prooftab=maketab("👓")

    # Place Ribbon in window #
    ribbon.grid(row=1,column=1,sticky="w")
    # Make groups to organise buttons on tabs##
    filegroup=makegroup(filetab,"File",0,1)
    projgroup=makegroup(filetab,"Project File",0,2)
    opengroup=makegroup(filetab,"Open List",0,3)
    notegroup=makegroup(filetab,"Notepad",0,4)
    copygroup=makegroup(citationtab,"Copy",0,0)
    searchgroup=makegroup(citationtab,"Search",0,100)
    citegroup=makegroup(citetab,"Cite New",0,0)
    authorgroup=makegroup(citetab,"Authors",0,1)
    writegroup=makegroup(citetab,"Cite",0,2)
    chargroup=makegroup(citetab,"Chars",0,10)
    proofgroup=makegroup(prooftab,"Proofread",0,10)
    papergroup=makegroup(citationtab,"Paper",0,1)
    listgroup=makegroup(citationtab,"Citations",1,0)
    listgroup.grid(row=1,column=0,padx=10,pady=10,columnspan=100)
    sortgroup=makegroup(citationtab,"Sort",0,3)
  
    closebtn=Button(rootwin,text="❌",command=exit,relief="flat",bg=bgcolor,highlightthickness=0)
    closebtn.grid(row=1,column=1,sticky="ne")



    # Load icons for buttons#
    global delpersonicon

    
    
    def makeicon(filename):
        return PhotoImage(file='./Icons/'+filename+'.png').subsample(1)
        
    bookicon=makeicon("bookicon")
    copyciteicon=makeicon('copyciteicon')
    copyindexicon=makeicon('copyindexicon')
    copyreficon=makeicon('copyreficon')
    csvicon=makeicon('csvicon')
    delicon=makeicon('delicon')
    delpersonicon=makeicon('delpersonicon')
    journalicon=makeicon('journalicon')
    minimiseicon=makeicon('minimiseicon')
    maximiseicon=makeicon('maximiseicon')
    newicon=makeicon('newicon')
    newicon=makeicon('newicon')
    pdficon=makeicon('pdficon')
    removeallauthors=makeicon('removeallauthors')
    sortauthoricon=makeicon('sortauthoricon')
    sortdownicon=makeicon('sortdownicon')
    sorttitleicon=makeicon('sorttitleicon')
    sortupicon=makeicon('sortupicon')
    soundicon=makeicon('soundicon')
    switchicon=makeicon('switchicon')
    switchicon=makeicon('switchicon')
    txticon=makeicon('txticon')
    urlicon=makeicon('urlicon')
    wordicon=makeicon('wordicon')
    writeicon=makeicon('writeicon')
    usedicon=makeicon('usedicon')
    dataicon=makeicon('dataicon')
    conficon=makeicon('conficon')
    edbookicon=makeicon('edbookicon')
    chapicon=makeicon('chapicon')
    unpubicon=makeicon('unpubicon')
    pinicon=makeicon('pinicon')
    customicon=makeicon('customicon')
    editicon=makeicon('editicon')
    searchicon=makeicon('searchicon')
    mastericon=makeicon('mastericon')
    perscommicon=makeicon('perscommicon')
    reporticon=makeicon('reporticon')

    #mod add path to new icon here


   # Make buttons#
    buttons=[{"image":newicon,"name":"New project","short":"<Control-n>","command":newproj,"menu":filegroup, "row":1,"col":0},
             {"image":delicon,"name":"Delete project","short":None,"command":askdel,"menu":filegroup, "row":1,"col":1},
             #{"image":minimiseicon,"name":"Minimise","short":None,"command":minimise,"menu":filegroup, "row":1,"col":2},
             #{"image":maximiseicon,"name":"Maximise","short":None,"command":minimise,"menu":filegroup, "row":1,"col":3},
             #{"image":pinicon,"name":"Set as Default","short":None,"command":None,"menu":filegroup, "row":1,"col":4},
             {"image":txticon,"name":"Open list as .txt","short":"<Control-o>","command":export_as_txt,"menu":opengroup, "row":0,"col":0},
             {"image":csvicon,"name":"Open list as .csv","short":"<Control-O>","command":export_as_csv,"menu":opengroup, "row":1,"col":0},
             {"image":mastericon,"name":"Open master sheet","short":"<Control-M>","command":openmaster,"menu":opengroup, "row":1,"col":1},
             {"image":wordicon,"name":"Open Project","short":None,"command":openfile,"menu":projgroup, "row":1,"col":0},
             {"image":switchicon,"name":"Change Project File","short":None,"command":changefile,"menu":projgroup, "row":1,"col":1},
          
            {"image":searchicon,"name":"Find","short":"<Control-f>","command":search,"menu":listgroup, "row":1,"col":0},
            {"image":editicon,"name":"Edit","short":None,"command":edit,"menu":listgroup, "row":0,"col":0},
             {"image":copyreficon,"name":"Copy full reference","short":None,"command":copyref,"menu":copygroup, "row":0,"col":1},
             {"image":copyciteicon,"name":"Copy citation","short":None,"command":copycite,"menu":copygroup, "row":0,"col":2},
             {"image":copyindexicon,"name":"Copy index number","short":None,"command":copyindex,"menu":copygroup, "row":1,"col":1},
            {"image":delicon,"name":"Delete citation","short":None,"command":ask_delref,"menu":copygroup, "row":1,"col":2},
             {"image":urlicon,"name":"Open paper URL","short":"<Control-u>","command":open_url,"menu":papergroup, "row":0,"col":0},
             {"image":pdficon,"name":"Open paper PDF","short":"<Control-p>","command":open_pdf,"menu":papergroup, "row":1,"col":0},
            {"image":sortupicon,"name":"Newest First","short":None,"command":sort_newest,"menu":sortgroup, "row":0,"col":0},
            {"image":sortdownicon,"name":"Oldest First","short":None,"command":sort_oldest,"menu":sortgroup, "row":0,"col":1},
            {"image":sortauthoricon,"name":"By Author","short":None,"command":sort_author,"menu":sortgroup, "row":1,"col":0},
            {"image":sorttitleicon,"name":"By Title","short":None,"command":sort_title,"menu":sortgroup, "row":1,"col":1},
             {"image":bookicon,"name":"Cite new book","short":"<Control-b>","command":book,"menu":citegroup, "row":0,"col":0},
             {"image":journalicon,"name":"Cite new journal","short":"<Control-j>","command":journal,"menu":citegroup, "row":0,"col":1},
             {"image":urlicon,"name":"Cite new webpage","short":"<Control-w>","command":web,"menu":citegroup, "row":1,"col":0},
             {"image":dataicon,"name":"Cite new dataset","short":"<Control-d>","command":dataset,"menu":citegroup, "row":1,"col":1},
             {"image":conficon,"name":"Cite new conference paper","short":None,"command":confpapers,"menu":citegroup, "row":0,"col":2},
             {"image":edbookicon,"name":"Cite new edited book","short":"<Control-e>","command":edbook,"menu":citegroup, "row":1,"col":2},
             {"image":chapicon,"name":"Cite new chapter in an edited book","short":"<Control-h>","command":chap,"menu":citegroup, "row":1,"col":3},
             {"image":unpubicon,"name":"Cite new unpublished item","short":"<Control-u>","command":unpub,"menu":citegroup, "row":0,"col":3},
             {"image":customicon,"name":"Manually create custom citation","short":None,"command":custom,"menu":citegroup, "row":1,"col":4},
             {"image":perscommicon,"name":"Cite new personal communication","short":"<Control-p>","command":pers,"menu":citegroup, "row":0,"col":4},
             {"image":reporticon,"name":"Cite new report","short":"<Control-r>","command":report,"menu":citegroup, "row":0,"col":5},
             #{"image":removeallauthors,"name":"Delete all authors in citation","short":None,"command":None,"menu":authorgroup, "row":0,"col":0},
             {"image":writeicon,"name":"Write to file","short":"<Control-Return>","command":cite,"menu":writegroup, "row":1,"col":0},
             {"image":soundicon,"name":"Read out loud","short":None,"command":proofread,"menu":proofgroup, "row":0,"col":0},
            {"image":usedicon,"name":"Check for unused citations","short":None,"command":check_unused,"menu":proofgroup, "row":1,"col":0}]
    #mod add new button here

   
    
    for i in buttons:
        b=Button(i["menu"],command=i["command"],image=i["image"],bg=bgcolor,relief="flat",bd=0,highlightthickness=0)
        b.grid(row=i["row"],column=i["col"],padx=5)
        tip = Hovertip(b,str(i["name"])+" ("+str(i["short"])+")")
        rootwin.bind(i["short"],i["command"])
        citewin.bind(i["short"],i["command"])
    #ribbon.bind("<Double-Button-1>",minimise)



## Bind keyboard shortcuts
def shorts():
    
    rootwin.bind("<Prior>", prevproj)
    rootwin.bind("<Next>", nextproj)
    rootwin.bind("<5>", nextproj) #button 5= scroll up #platdep
    rootwin.bind("<4>", prevproj) #button 4= scroll down #platdep
    
    
    PDFbox.bind("<1>", linkpdf)
    rootwin.bind("<Escape>",closecitewin)
    citewin.bind("<Escape>",closecitewin)
    citewin.bind("<Control-Return>",cite)
    rootwin.bind("<Control-Return>",cite)
    citewin.bind("<Insert>",inscheck)
    citewin.bind("<Tab>",inscheck)



    ribbon.bind("<Motion>",maximise)
    rootwin.bind("<FocusOut>",minimise)
 
    
 

def prog(n):
    print(str(int((100/14)*n))+"%")

##run program
def start():
    print("Loading")
    clean()
    load()
    makestyles()
    makewin()
    makecitewin()
    citewin.withdraw()
    makeboxframes()
    makeboxes()
    makefields()
    makelabels()
    makeribbon()
    list_projects()
    list_citations()
    loadfile()
    shorts()
    prevproj()
    minimise()
    
 

start()
rootwin.mainloop()
citewin.mainloop()
