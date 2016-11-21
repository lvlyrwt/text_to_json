import re
import parser
import json
import os
import sys
import urllib.request
import codecs
from tkinter import *
from tkinter import ttk,messagebox
from tkinter.filedialog import askopenfilename
root = Tk()

def processing(fname):
    # fname=input("Please enter the file name with directory: ")
    # fname="1342-0.txt"
    data={}
    output=[]
    # fname=gui_interface()
    with open(fname,"r",encoding='utf8') as txtfile:
        count=0
        details=""
        content=""
        reg='\*\*\*'
        for a in txtfile.readlines():
            match=re.search(reg,a)
            if match:
                count+=1
                reg='End of the Project Gutenberg'
                continue
            if count<3:
                if(re.search('Title',a,re.IGNORECASE) or re.search('Author',a,re.IGNORECASE) or re.search('Language',a,re.IGNORECASE)):
                    key,val=a.split(':')
                    data[key]=val.strip()
                    output.append(data)
                    count+=1
                    data={}
            elif count==5:
                break
            else:
                if re.search('Chapter',a,re.IGNORECASE):
                    data[key]=content
                    if not(len(content)<50):
                        output.append(data)
                    data={}
                    key=a.strip()
                    content=''
                    continue
                if re.search('Chapter',key,re.IGNORECASE):
                    content+=a
    wname=output[0]
    title=wname.get('Title').lower().strip().replace(" ","_").replace("\\n","")
    genre,image,average_rating,total_count=googlebookapi(title)
    data = {}
    data['genre'] = genre
    output.insert(1, data)
    data = {}
    data['images'] = image
    output.insert(4, data)
    data = {}
    data['rating'] = average_rating
    output.insert(5, data)
    data = {}
    data['total_rating_count'] = total_count
    output.insert(6, data)
    jsoncreator(title, output)
    messagebox.showinfo("Done", "JSON created for "+title)


def googlebookapi(title):
    googlesearch=urllib.request.urlopen("https://www.googleapis.com/books/v1/volumes?q="+title).read()
    data=json.loads(googlesearch.decode("utf8"))
    i=0
    genre=image=rating=ratingcount=''
    average_rating=0.0
    final_count_rating=0
    for par in data['items']:
        try:
            if(re.match(str(data['items'][i]['volumeInfo']['title']).strip(),title.replace('_',' '),re.IGNORECASE)):
                genre+=" "+(str(data['items'][i]['volumeInfo']['categories']))
                image+="\n "+str(data['items'][i]['volumeInfo']['imageLinks'])
                rating+="\n "+str(data['items'][i]['volumeInfo']['averageRating'])
                ratingcount+="\n "+str(data['items'][i]['volumeInfo']['ratingsCount'])
                average_rating+=float(data['items'][i]['volumeInfo']['averageRating'])*int(data['items'][i]['volumeInfo']['ratingsCount'])
                final_count_rating+=int(data['items'][i]['volumeInfo']['ratingsCount'])
        except KeyError:
            pass
        except IndexError:
            pass
        i += 1
    average_rating=average_rating/final_count_rating
    genre=' '.join(unique_genre(genre.split())).replace('] [',',')
    # print(average_rating)
    return (genre,image,average_rating,final_count_rating)


def jsoncreator(wname1,output):
    if not os.path.exists(wname1):
        os.makedirs(wname1)
        
    with open((wname1+"/"+wname1+"_ascii.json"),"w") as writefile:
        json.dump(output,writefile,ensure_ascii=True)
    with open((wname1+"/"+wname1+"_utf8.json"),"w", encoding='utf8') as writefile:
        json.dump(output,writefile)

def unique_genre(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist


def change_color():
    current_color = root.cget("background")
    next_color = "green" if current_color == "red" else "red"
    root.config(background=next_color)
    root.after(1000, change_color)


def OpenFile():
    name = askopenfilename(#initialdir="C:/argo/Documents/git/Sto",
                           filetypes =(("Text File", "*.txt"),("All Files","*.*")),
                           title = "Choose the txt File"
                           )
    try:
        with open(name,'r',encoding='utf-8') as UseFile:
            processing(name)
    except:
        messagebox.showerror("Error", "Process Incomplete!!!!!")

def about():
    text="Developed by : Arghya(argo)\n Email:arghyasaha26@gmail.com"
    messagebox.showinfo("Txt-2-Json v1.0", text)

def no_operation():
    messagebox.showinfo("Coming Soon!!", "Under Construction")

def main():
    root.title("txt-2-JSON toolkit v0.1")
    label = ttk.Label(root, text="txt-2-JSON", foreground="maroon", font=("Times", 30,"bold"))
    label.pack()
    # Menu Bar

    img = PhotoImage(file="story_mirror_logo.png")

    panel = Label(root, image=img)
    panel.place(relx=0.5, rely=0.5, anchor=CENTER)
    panel.pack(side="bottom", fill="both", expand="yes")

    button1 = Button(root, height=2, width=10, text="Open", command=OpenFile,bg="Blue",fg="white",font=("Times",13,"bold"))  # .pack()
    button1.place(relx=.87, rely=0.75, anchor=CENTER)
    button2 = Button(root, height=2, width=10, text="exit", command=lambda: exit(),bg="red" ,font=("Times",13,"bold"))  # .pack()
    button2.place(relx=.13, rely=0.75, anchor=CENTER)

    menubar = Menu(root)
    file=Menu(menubar,tearoff=0)
    file.add_command(label='Open', command=OpenFile)
    file.add_separator()
    file.add_command(label='Exit', command=lambda: exit())
    menubar.add_cascade(label='File', menu=file)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help Index", command=no_operation)
    helpmenu.add_command(label="About...", command=about)
    menubar.add_cascade(label="Help", menu=helpmenu)

    root.geometry("740x680")
    # root.resizable(width=False, height=False)
    root.config(menu=menubar)
    root.mainloop()

if __name__ =='__main__':
    main()
