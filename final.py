import datetime
import glob
import os
import re
import shutil
import time
import tkinter as tk
import threading
from shutil import Error, copyfile, copytree, move
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IRWXG, S_IRWXO, S_IRWXU, S_IWUSR
from tkinter import Scrollbar
from tkinter import messagebox as mb
from tkinter import scrolledtext, ttk
from zipfile import ZipFile
from tkinter.colorchooser import askcolor

from ttkthemes import ThemedTk, ThemedStyle
#import pkg_resources.py2_warn
import Pmw as pmw
from cryptography.fernet import Fernet
from PIL import Image, ImageTk, UnidentifiedImageError

'''import os as pyaudio
import wave
import contextlib
from pydub import AudioSegment as asa
import numpy as np
'''
import sys

import login
'''
from mutagen.mp3 import MP3
from pygame import mixer, error
'''


#Main Variables of application 
filename_withdate=time.strftime("%Y%m%d%H%M%S")
currentime = time.strftime ("%H:%M:%S")
f_address_dup = "Log"
f_address = login.save_location.replace("/", "\\")
f_address= os.path.join(login.save_location, f_address_dup)
f_address=f_address.replace("/", "\\")
try:
    os.makedirs(f_address)
except FileExistsError:
    pass
address = ""
address_1 = ""
address_2 = ""
address_cache = ""
settings_file_location = ""
make_bold_variable =0
sel_first = 0
sel_last = 0
tag_data = ""
listof_files_search=[]
listof_files = []
proceed =0
info_var = 0
exports_var = 0
settings_var =0
exports_path = ""
val_error = 0
new_created_name =""

default_baground = 'black'
default_foreground ='white'
default_font_style ="Segoe UI"
default_font_size = 13
default_cursor_color ='white'
default_window_baground = "#f0f0ed"  #"#000000"
default_window_foreground= "#000000"  #"ffffff"

window_baground = "#000000"
window_foreground= "#ffffff"
baground = 'black'
foreground ='white'
font_style ="Segoe UI"
font_size = 13
cursor_color = 'white'
present_key = b'Qp8dRkIVonbQsCkBm0ZU7aIZj6K11reMlxBn-7mGndY='
colors = ["white", "black", "red", "green", "blue", "cyan", "yellow", "magenta"]
fonts = ['Amazon Ember','@Malgun Gothic', '@Microsoft JhengHei', '@Microsoft YaHei', '@MingLiU-ExtB', '@NSimSun', '@Yu Gothic Medium', 'Alef', 'Arial', 'Cabin Sketch', 'Caladea', 'Calibri', 'Cambria', 'Comic Sans MS', 'Consolas', 'Courier New', 'Ink Free', 'Limelight', 'Roman', 'Segoe Print', "Segoe UI", 'Source Code Pro', 'System', 'Terminal', 'Times New Roman', 'Ubuntu Mono']
times_list = ["-", "30 secs", "1 min", "5 mins"]

current_imagepath =""
images_list = []
'''image_column = 0
image_row = 0
image_num = 0'''

minimise_info_frame_bool =1
minimise_searchfiles_frame_bool =1
minimise_eximport_frame_bool = 1
minimise_image_frame_bool =0
minimise_audio_frame_bool = 1
minimise_settings_frame_bool = 1

'''chunk = 1024
FORMAT = ""#pyaudio.paInt16
CHANNELS = 1
RATE = 64000
output_file = "1.wav"
record_timer = 0
'''
'''record_check = False
record_pause_check = True
song_thread = ""'''

#pa = ""#pyaudio.PyAudio()
#-#stream = pa.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, output = True, frames_per_buffer = chunk)


#Main Variables of application Ends here



#mixer.init() 


#UI starts here
root = tk.Tk()
root.title("Log")
hints = pmw.Balloon(root)

show_hint_bool = tk.BooleanVar()
show_hint_bool.set(True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = int(0.885*screen_width)
window_height = int(0.601*screen_height)

root.minsize(window_width, window_height)  #int(0.885*screen_width), int(0.601*screen_height)                           #1500, 650   #1700, 650
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.iconbitmap("Images/final2.ico")               #r"C:\Users\Avinash Kumar\Documents\Vs code\backup\final2.ico"


#---------------------------------------------------------------------Settings----------------------------------------------------------------

settings_file_location = os.path.join(login.user, "settings.txt")

def settings_file_load():
    global baground, foreground, font_style, font_size, cursor_color, window_baground, window_foreground
    try:    
        with open(settings_file_location, "r") as f:
            for i in f.readlines():
                i= i.split("¿")
                baground = i[0]
                foreground = i[1]
                cursor_color = i[2]
                window_baground = i[3]
                window_foreground = i[4]
                font_style = i[5]
                font_size = int(i[6])
                show_hint_bool.set(i[7])
    except (FileNotFoundError, TypeError, ValueError, IndexError):
        baground = default_baground
        foreground = default_foreground
        cursor_color = default_cursor_color
        window_baground = default_window_baground
        window_foreground = default_window_foreground
        font_style = default_font_style
        font_size = default_font_size
        show_hint_bool.set(True)

settings_file_load()

#=======================================================================================================================================================



#-----------------------------------------minimise and maxmise image view and search files view==============================================================



def minimise_add_images_frame_fn():
    global minimise_image_frame_bool#, minimise_audio_frame_bool
    if minimise_image_frame_bool == 0:
        add_images_frame.grid_forget()
        minimise_add_images_frame.configure(text=">")
        minimise_image_frame_bool =1
    else:
        #add_sound_frame.grid_forget()
        #minimise_audio_frame_bool =1
        add_images_frame.grid(row=0, column=1, sticky=tk.E+tk.W+tk.N+tk.S , padx=5, pady=5)
        minimise_add_images_frame.configure(text="<")
        minimise_image_frame_bool = 0

'''
def minimise_add_audio_frame_fn():
    global minimise_image_frame_bool, minimise_audio_frame_bool
    if minimise_audio_frame_bool == 0:
        add_sound_frame.grid_forget()
        minimise_audio_frame_bool =1
    else:
        add_images_frame.grid_forget()
        minimise_image_frame_bool =1
        add_sound_frame.grid(row=0, column=1, sticky=tk.E+tk.W+tk.N+tk.S , padx=5, pady=5)
        minimise_audio_frame_bool = 0'''


def minimise_searchfiles_frame_fn():
    global minimise_searchfiles_frame_bool, minimise_info_frame_bool, minimise_settings_frame_bool, minimise_eximport_frame_bool
    if minimise_searchfiles_frame_bool:
        settings_frame.grid_forget()
        minimise_settings_frame_bool = 1
        info_data_frame.grid_forget()
        minimise_info_frame_bool = 1
        eximport_frame.grid_forget()
        minimise_eximport_frame_bool =1
        searchfiles_data_frame.grid(row=0, column=3, sticky=tk.E+tk.W+tk.N+tk.S, padx=5, pady=5)
        minimise_searchfiles_frame_bool = 0
    else:
        searchfiles_data_frame.grid_forget()
        minimise_searchfiles_frame_bool =1


def minimise_settings_frame_fn():
    global minimise_settings_frame_bool ,minimise_info_frame_bool, minimise_searchfiles_frame_bool, minimise_eximport_frame_bool
    if minimise_settings_frame_bool:
        info_data_frame.grid_forget()
        minimise_info_frame_bool = 1
        searchfiles_data_frame.grid_forget()
        minimise_searchfiles_frame_bool = 1
        eximport_frame.grid_forget()
        minimise_eximport_frame_bool =1
        settings_frame.grid(row=0, column=3, sticky=tk.E+tk.W+tk.N+tk.S , padx=5, pady=5)
        minimise_settings_frame_bool =0
    else:    
        settings_frame.grid_forget()
        minimise_settings_frame_bool =1


def minimise_eximport_frame_fn():
    global minimise_info_frame_bool, minimise_settings_frame_bool, minimise_searchfiles_frame_bool, minimise_eximport_frame_bool
    if minimise_eximport_frame_bool:
        searchfiles_data_frame.grid_forget()
        minimise_searchfiles_frame_bool = 1
        settings_frame.grid_forget()
        minimise_settings_frame_bool = 1
        info_data_frame.grid_forget()
        minimise_info_frame_bool =1
        eximport_frame.grid(row=0, column=3, sticky=tk.E+tk.W+tk.N+tk.S , padx=5, pady=5)
        minimise_eximport_frame_bool =0
    else:    
        eximport_frame.grid_forget()
        minimise_eximport_frame_bool =1


def minimise_info_frame_fn():
    global minimise_info_frame_bool, minimise_settings_frame_bool, minimise_searchfiles_frame_bool, minimise_eximport_frame_bool
    if minimise_info_frame_bool:
        searchfiles_data_frame.grid_forget()
        minimise_searchfiles_frame_bool = 1
        settings_frame.grid_forget()
        minimise_settings_frame_bool = 1
        eximport_frame.grid_forget()
        minimise_eximport_frame_bool =1
        info_data_frame.grid(row=0, column=3, sticky=tk.E+tk.W+tk.N+tk.S , padx=5, pady=5)
        minimise_info_frame_bool =0
    else:    
        info_data_frame.grid_forget()
        minimise_info_frame_bool =1

#=========================================================================================min and max ends here=============================================

#adding exports option ends here=============================================================================================================




#Adding Menu bar-------------------------------------------------------------
'''
menubar = tk.Menu(root)  #, background='#000099', foreground='white', activebackground='#004c99', activeforeground='white'
options = tk.Menu(menubar, tearoff = 0)  #, background='#000099', foreground='white', activebackground='#004c99', activeforeground='white' 
menubar.add_cascade(label ='Options', menu = options)
options.add_command(label ='Configure')  #, command = settings
options.add_command(label = 'Export', command = exports)
root.config(menu = menubar)
'''
# entered text label Frame ----------------------------------------------------


root.config(bg=window_baground)
style = ttk.Style()
#style.theme_use('alt')
style.configure("TButton", foreground=window_foreground, background=window_baground)
style.configure("TLabel", foreground=window_foreground, background=window_baground)
#style.configure("TScrollbar.vbar", foreground=window_foreground, background=window_baground)
#style.configure("TLabelFrame", foreground=window_foreground, background=window_baground)
style.configure("TRadiobutton", foreground=window_foreground, background=window_baground, selectcolor=window_foreground)
style.map('TButton', background=[('active',window_baground)])
style.map('TRadiobutton',background = [('disabled', window_baground),('pressed', '!focus', window_baground),('active', window_baground)],indicatorcolor=[('selected', window_baground),('pressed', window_baground)])   #, foreground = [('disabled', window_foreground),('pressed', window_foreground),('active', window_foreground)]

enteredtext_label = tk.LabelFrame(root, padx=5, pady=5 , bg=window_baground, fg=window_foreground, text="Write Text")  #relief="flat"
enteredtext_label.grid(row=0, column=0,  sticky=tk.E+tk.W+tk.N+tk.S)            #padx=10, pady=10,
enteredtext_label.rowconfigure(0, weight=1)
enteredtext_label.columnconfigure(0, weight=1)


enteredtags_label = tk.Frame(root, padx=5, pady=5, bg=window_baground) #, text="Enter tags for Current File" 
enteredtags_label.grid(row=1, column=0,  sticky=tk.E+tk.W+tk.N+tk.S, pady =3)               #padx=10, pady=10,

#enteredtags_label.rowconfigure(0, weight=1)
enteredtags_label.columnconfigure(1, weight=1)


add_images_frame = tk.LabelFrame(root, text="Add Images", bg=window_baground, fg=window_foreground)       #, relief="flat"
add_images_frame.grid(row=0, column=1, sticky=tk.E+tk.W+tk.N+tk.S, padx=5, pady=5)               #padx=10, pady=10,  rowspan=2,
#add_images_frame.rowconfigure(1, weight=0)
add_images_frame.columnconfigure(1, weight=1)

#add_sound_frame = tk.LabelFrame(root, text="Add Audio Files", bg=window_baground, fg=window_foreground)
#add_sound_frame.grid(row=0, column=1, sticky=tk.E+tk.W+tk.N+tk.S, padx=5, pady=5)



searchfiles_data_frame = tk.LabelFrame(root, text="Search Your Files", bg=window_baground, fg=window_foreground)
#searchfiles_data_frame.grid(row=0, column=3, sticky=tk.E+tk.W+tk.N+tk.S)               #padx=10, pady=10,  rowspan=2,
#searchfiles_data_frame.grid_forget()
#searchfiles_data_frame.rowconfigure(1, weight=0)
searchfiles_data_frame.columnconfigure(1, weight=1)


settings_frame = tk.LabelFrame(root, text="Settings", bg=window_baground, fg=window_foreground)
#settings_frame.grid(row=0, column=3, sticky=tk.E+tk.W+tk.N+tk.S)
#settings_frame.grid_forget()
settings_frame.columnconfigure(1, weight=1)

eximport_frame = tk.Frame(root, bg=window_baground, relief="flat")
#eximport_frame.grid(row=0, column=3, sticky=tk.E+tk.W+tk.N+tk.S)
#settings_frame.grid_forget()
eximport_frame.columnconfigure(1, weight=1)

export_frame = tk.LabelFrame(eximport_frame, text="Export", padx=2, pady=2, bg=window_baground, fg=window_foreground)
export_frame.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S)
#export_frame.columnconfigure(1, weight=1)

import_frame = tk.LabelFrame(eximport_frame, text="Import", padx=2, pady=2, bg=window_baground, fg=window_foreground)
import_frame.grid(row=1, column=0, sticky=tk.E+tk.W+tk.N+tk.S)
eximport_frame.rowconfigure(1, weight=1)
#import_frame.columnconfigure(1, weight=1)



info_data_frame = tk.LabelFrame(root, text="Info", bg=window_baground, fg=window_foreground)
#info_data_frame.grid(row=0, column=3, sticky=tk.E+tk.W+tk.N+tk.S)
#info_data_frame.grid_forget()
info_data_frame.columnconfigure(1, weight=1)


# entered text label Frame ----------------------------------------------------Ends here





#------------------------------------------------minimise "search your files" lable frame==================================================================== 

config_buttons_frame_1 = tk.Frame(root, bg=window_baground)
config_buttons_frame_1.grid(row=0, column=2, sticky=tk.N+tk.S)


im = Image.open("Images/images.png")
im = im.resize((40, 40), Image.ANTIALIAS)
tkimage = ImageTk.PhotoImage(im)
minimise_add_images_frame = ttk.Button(config_buttons_frame_1, image=tkimage, width=2, command = minimise_add_images_frame_fn)
minimise_add_images_frame.grid(row=0, column=0, sticky=tk.N)#, sticky=tk.N+tk.S)  #+tk.S
minimise_add_images_frame.image = tkimage

'''
im = Image.open("Images/recording.png")
im = im.resize((40, 40), Image.ANTIALIAS)
tkimage = ImageTk.PhotoImage(im)
minimise_add_audio_frame = ttk.Button(config_buttons_frame_1, image= tkimage, width=2, command = minimise_add_audio_frame_fn)
minimise_add_audio_frame.grid(row=1, column=0, sticky=tk.S)#, sticky=tk.N+tk.S)
minimise_add_audio_frame.image=tkimage'''


config_buttons_frame = tk.Frame(root, bg=window_baground)
config_buttons_frame.grid(row=0, column=4, sticky=tk.N+tk.S)


im = Image.open("Images/search.png")   #r"C:\Users\Avinash Kumar\Documents\Vs code\backup\search.jpg"
im = im.resize((40, 40), Image.ANTIALIAS)
tkimage = ImageTk.PhotoImage(im)

minimise_searchfiles_data_frame = ttk.Button(config_buttons_frame, image=tkimage, width=2, command = minimise_searchfiles_frame_fn)
minimise_searchfiles_data_frame.grid(row=1, column=0, sticky=tk.N+tk.S)  #+tk.S
minimise_searchfiles_data_frame.image = tkimage

im = Image.open("Images/settings.png")              #r"C:\Users\Avinash Kumar\Documents\Vs code\backup\settings.png"
im = im.resize((40, 40), Image.ANTIALIAS)
tkimage = ImageTk.PhotoImage(im)

minimise_settings_frame = ttk.Button(config_buttons_frame, image=tkimage, width=2, command = minimise_settings_frame_fn)
minimise_settings_frame.grid(row=2, column=0, sticky=tk.N+tk.S)
minimise_settings_frame.image = tkimage

im = Image.open("Images/eximport.png")          #r"C:\Users\Avinash Kumar\Documents\Vs code\backup\help.png"
im = im.resize((40, 40), Image.ANTIALIAS)
tkimage = ImageTk.PhotoImage(im)

minimise_eximport_frame = ttk.Button(config_buttons_frame, image=tkimage, width=2, command = minimise_eximport_frame_fn)
minimise_eximport_frame.grid(row=3, column=0, sticky=tk.N+tk.S)
minimise_eximport_frame.image = tkimage



im = Image.open("Images/help.png")          #r"C:\Users\Avinash Kumar\Documents\Vs code\backup\help.png"
im = im.resize((40, 40), Image.ANTIALIAS)
tkimage = ImageTk.PhotoImage(im)

minimise_info_frame = ttk.Button(config_buttons_frame, image=tkimage, width=2, command = minimise_info_frame_fn)
minimise_info_frame.grid(row=4, column=0, sticky=tk.N+tk.S)
minimise_info_frame.image = tkimage

#=============================================================================================================================================================




#-----------------------------------------------------------------------Notification------------------------------------------------------------------------------------------------

def clear_notification():
    global val_error
    notification_label.config(text="")
    val_error =0

notification_label = ttk.Label(root, text = "", background=window_baground, foreground=window_foreground)   #'#FFFF66'
notification_label.grid(row=1, column=1, columnspan=4, sticky=tk.E+tk.S)


#===================================================================================================================================================================================



#Time in windows updates here
def update_time():
    global currentime#, record_timer
    currentime = time.strftime ("%H:%M:%S")
    timelabel.config (text=currentime)
    timelabel.after(1000, update_time)
    '''if record_check == True and record_pause_check == True:
        record_timer+=1
        recording_time.config(text=datetime.timedelta(seconds=record_timer))'''
#creatng GUI for timelabel and updating here
timelabel = ttk.Label(root, font=("Courier", 12))
timelabel.grid(row=0, column=0, sticky=tk.N+tk.E)
update_time()
#creatng GUI for timelabel and updating here Ends here
#Time in windows updates here Ends here
    



#update button def function
def change_colour_to_normal():
    #update_button.configure(bg="#ffffff", fg="#000000")
    pass

cache_audio_file_name = ""
audio_list = []
audio_address_list = []

image_name=0
temp_tag_data = ''
def update_user_text_infile(*event):
    #root.update()
    global present_key, image_name, address_2, address_cache, address_1, temp_tag_data
    notification_label.config(text="Updating..")
    image_name=0
    edited_tags =","
    p = os.popen('attrib -h '+address)
    p.close()
    tag_write_data=""
    image_write_data = ""
    #print(entered_text.get("1.0", tk.END)) 
    #update_button.configure(bg="#000000", fg="#ffffff")
    #update_button.after(1000, change_colour_to_normal)
    with open(address, "wb") as f:    #----------------------------------------------------------encrypt=================================================
        data_to_write = entered_text.get("1.0", tk.END)
        data_to_write = data_to_write.encode()
        encrypt_key_type = Fernet(present_key)
        data_to_write = encrypt_key_type.encrypt(data_to_write)
        f.write(data_to_write)
    p = os.popen('attrib +h ' + address)
    p.close()
    address_1 = os.path.join(f_address, "tag_data.txt")
    with open( address_1, "r") as f:
        tag_data = f.read()
    temp_tag_data = address[len(f_address)+1:-4]
    edited_tags = tag_entry.get().lower().split(",")
    for i in range(len(edited_tags)):
        edited_tags[i] = edited_tags[i].strip()
    edited_tags = ",".join(edited_tags)    
    if temp_tag_data not in tag_data:
        with open( address_1, "w") as f:
            f.write(tag_data+temp_tag_data+"¿"+edited_tags+'\n')
    else:
        with open( address_1, "r") as f:
            for i in f.readlines():
                if temp_tag_data in i:
                    tag_write_data+=temp_tag_data+"¿"+edited_tags+"\n"
                else:
                    tag_write_data+=i
        with open( address_1, "w") as f:
            f.write(tag_write_data)          

    address_2 = os.path.join(f_address, temp_tag_data)
    
    final_image_list = []
    try:
        os.mkdir(address_2)
    except FileExistsError:
        pass

    if len(images_list) !=0:
        #print(f_address+"/"+temp_tag_data)
        for i in images_list:
            dst = os.path.join(address_cache, str(image_name)+".JPG")
            #final_image_list.append(dst)
            copyfile(i, dst)
            #copyfile(i, address_cache)
            image_name+=1
            
        files = glob.glob(f_address+"/"+temp_tag_data+"/*JPG")    
        for f in files:
            os.remove(f)
        files = glob.glob(address_cache+"/*.JPG") 
        image_name=0
        for i in files:
            dst = os.path.join(address_2, str(image_name)+".JPG")
            copyfile(i, dst)
            os.remove(i)
            image_name+=1
        
    elif audio_list != []:   
        pass
        '''notification_label.config(text="Importing Record'(s)")
        available_files = glob.glob(address_2+"/*.mp3")
        del_list = []
        for i in available_files:
            if i not in audio_address_list: 
                del_list.append(i)
        #print(del_list)
        proceed_copy = 1
        for i in del_list:
            try:
                os.remove(i)
            except PermissionError:
                notification_label.config("cant deleted is audio in use")
                proceed_copy = 0    
        if proceed_copy:
            for i in audio_list:
                #print(i, i[:13], "satisfied", address_2)
                if i[:13]==".cache_audio/":
                    #print("ok")
                    try:
                        shutil.move(i, os.path.join(address_2, i[13:]))
                    except PermissionError:
                        print("this is playing")  
                    #s = asa.from_file(i, format="wav")
                    #s.export(os.path.join(address_2, i[:-3]+"mp3"), format="mp3")
                else:
                    new_file = os.path.join(address_2, i[:-3]+"mp3")
                    if new_file not in available_files:
                        #print(new_file, available_files)
                        shutil.move(audio_address_list[audio_list.index(i)], new_file)
                        #s = asa.from_file(audio_address_list[audio_list.index(i)])
                        #s.export(new_file, format="mp3")
        
            notification_label.config(text="Record'(s) Imported")
            notification_label.after(2000, clear_notification())'''
    else:
        try:
            shutil.rmtree(address_2)
        except FileNotFoundError:
            pass

    notification_label.config(text="Saved")
    notification_label.after(2000, clear_notification)         


#update button def function


# Create the textbox
entered_text = scrolledtext.ScrolledText(enteredtext_label, wrap =tk.WORD, font=(font_style, font_size), bg=baground, fg=foreground, insertbackground=cursor_color)#"Helvetica" font=("Segoe UI", 13), bg='#000000', fg='#ffffff', 
entered_text.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S)
#entered_text.focus_set()
entered_text.focus_force()
entered_text.propagate(0)
#entered_text.insert(tk.END, )
entered_text.insert(tk.END, time.strftime("%m/%d/%Y")+'  '+currentime+'\n\n')
#entered_text.tag_configure("BOLD", font=("Segoe UI", 13, "bold"))



#Update Button For the scrolled text widget

update_button = ttk.Button(enteredtags_label, text="  Update  ", command=update_user_text_infile)
update_button.grid(row=1, column=3, sticky=tk.E)

#Update Button For the scrolled text widget


#Tags Entry starts here
tag_entry_label = ttk.Label(enteredtags_label, text ="Enter Tags(Seperated by ',')")
tag_entry_label.grid(row=1, column=0, sticky=tk.W)

tag_entry = tk.Entry(enteredtags_label, bg=baground, fg=foreground, insertbackground=cursor_color)   
tag_entry.grid(row=1, column=1, columnspan=2, sticky=tk.W+tk.E)

#Tags Entry ------------------------------------------------Ends here



#Search files methods---------------------------------------starts here

def search_files(*event):
    global listof_files_search, listof_files, val_error, address_1
    listof_files_search = []
    tag_count = 0
    temp_user_tags = []
    temp_saved_tags = []
    temp_tags = []
    listof_files= []
    listof_files_dup= []
    date_check = []
    content_of_description.delete(0, tk.END)
    address_1 = os.path.join(f_address, "tag_data.txt")
    #print(get_text_for_search.get(), choose_search.get())
    if choose_search.get() == "Text Search":
        user_data =  get_text_for_search.get().lower().strip()
        with open(address_1, "r") as f:
            for i in f.readlines():
                listof_files_dup.append(i[:14]+'.txt')
        for i in listof_files_dup:
            address_dup =os.path.join(f_address, i)
            with open(address_dup, "rb") as f:   #----------------------------------------------------------decrypt=================================================
                read_data=f.read()
                encrypt_key_type = Fernet(present_key)
                read_data = encrypt_key_type.decrypt(read_data).decode()
                read_data=read_data.lower()
            if user_data in read_data:
                listof_files.append(i)
        #print(listof_files)

    elif choose_search.get() == "Date Search":
        user_data = get_text_for_search.get().strip()
        if '-' in user_data:
            user_data= user_data.split('-')
            if len(user_data) ==2:
                for i in range(0,2):
                    user_data[i] = user_data[i].strip().split('/')
                    try:
                        ini_date = datetime.datetime(year=int(user_data[i][0]) ,month=int(user_data[i][1]) ,day=int(user_data[i][2]))
                        if ini_date and len(user_data[i][1])==2 and len(user_data[i][2]):
                            date_check.append(ini_date)
                            if i==1:
                                if date_check[0]>date_check[1]:
                                    break
                            user_data[i]="".join(user_data[i])

                    except (ValueError, IndexError) as e:
                        val_error = 1
                        notification_label.config(text="Wrong date Format")
                        notification_label.after(2000, clear_notification)
                
                if not val_error:
                    with open(address_1, "r") as f:
                        for i in f.readlines():
                            final_date = datetime.datetime(year=int(i[:4]) ,month=int(i[4:6]) ,day=int(i[6:8]))        #= i[:4], i[4:6], i[6:8] 2020/05/22, 2020/05/23
                            if date_check[0]<=final_date<=date_check[1]:
                                listof_files.append(i[:14]+'.txt')    

        elif ',' in user_data:
            user_data= user_data.split(',')
            for i in range(len(user_data)):
                user_data[i] = user_data[i].strip()
            user_data = list(set(user_data))
            for i in range(len(user_data)):
                user_data[i] = user_data[i].strip().split('/')
                try:
                    ini_date = datetime.datetime(year=int(user_data[i][0]) ,month=int(user_data[i][1]) ,day=int(user_data[i][2]))
                    if ini_date and len(user_data[i][1])==2 and len(user_data[i][2]):
                        #listof_files_dup.append("".join(user_data))
                        user_data[i] = "".join(user_data[i])
                        with open(address_1, "r") as f:
                            for j in f.readlines():
                                if user_data[i] in j:
                                    listof_files.append(j[:14]+'.txt')
                except ValueError:
                    val_error = 1
                    notification_label.config(text="Wrong date Format")
                    notification_label.after(2000, clear_notification)



        else:
            user_data= user_data.split('/')
            #print(user_data, len(user_data[1]) ,len(user_data[2]))
            try:
                if datetime.datetime(year=int(user_data[0]) ,month=int(user_data[1]) ,day=int(user_data[2])) and len(user_data[1])==2 and len(user_data[2]):
                    user_data="".join(user_data)
                    with open(address_1, "r") as f:
                        for i in f.readlines():
                            if user_data in i:
                                listof_files.append(i[:14]+".txt")
            except ValueError:
                val_error = 1
                notification_label.config(text="Wrong date Format")
                notification_label.after(2000, clear_notification)








    elif choose_search.get() == "Tag Search":
        with open( address_1, "r") as f:
            for i in f.readlines():
                #print(i)
                try:
                    temp_tags.append(i.split("¿")[1].strip())
                    #print(temp_tags)
                except IndexError:
                    pass
            f.seek(0)            
            temp_book_tags = f.read()
        temp_saved_tags = temp_book_tags.split("\n")
        #print(temp_tags)
        temp_user_tags = get_text_for_search.get().split(",")
        for i in range(len(temp_user_tags)):
            temp_user_tags[i] = temp_user_tags[i].strip().lower()
        #print(temp_user_tags)    
        if ex_in_var.get() == 1:
            for j in temp_tags:
                tag_count =0
                for k in j.split(","):
                    for i in temp_user_tags:
                        if i==k:                  #thsi should be == for exact tag search
                            tag_count+=1
                            break
                if tag_count == len(temp_user_tags):
                    listof_files_search.append(j)

        elif ex_in_var.get() == 2:
            for j in temp_tags:
                tag_count =0
                for k in j.split(","):
                    for i in temp_user_tags:
                        if i==k:                   # thsi should be == for exact search
                            tag_count+=1
                            break
                if tag_count>=1:
                    listof_files_search.append(j)
        
        for i in temp_saved_tags:
            for j in listof_files_search:
                if j in i:
                    listof_files.append(i.split("¿")[0]+".txt")  
                    break                        
        #print(listof_files)
    if len(listof_files) == 0 and val_error==0:
        notification_label.config(text="No Matching Entry")
        notification_label.after(2000, clear_notification)

    for i in listof_files:
        content_of_description.insert(tk.END, i)
        
def activate_ex_in(event):
    if choose_search.get()=="Tag Search":
        date_entry_info.grid_remove()
        exclusive_rad_button.grid( row=2, column=0, sticky = tk.W+tk.N)
        inclusive_rad_button.grid( row=2, column=1, sticky = tk.E+tk.N)
        exclusive_rad_button.config(state=tk.ACTIVE)
        inclusive_rad_button.config(state=tk.ACTIVE)
    elif choose_search.get()=="Text Search":
        date_entry_info.grid_remove()
        exclusive_rad_button.grid( row=2, column=0, sticky = tk.W+tk.N)
        inclusive_rad_button.grid( row=2, column=1, sticky = tk.E+tk.N)
        exclusive_rad_button.config(state=tk.DISABLED)
        inclusive_rad_button.config(state=tk.DISABLED)
    elif choose_search.get()=="Date Search":
        exclusive_rad_button.grid_remove()
        inclusive_rad_button.grid_remove()
        date_entry_info.grid( row=2, column=1, columnspan =2, sticky = tk.W+tk.N)

def showcontent(event):
    global address, current_imagepath, images_list, current_showing_image_set, address_1, audio_list, audio_address_list      #, image_row, image_column, image_num
    images_list = []                   # this should be well maintained to revert back using Ctrl-Z--------------------------------------------------------------------------
    fin_tag_index =0
    ini_tag_index=0
    no_file_error = 0
    '''image_num=0'''
    try:
        x = content_of_description.curselection()[0]
        f = content_of_description.get(x)
        root.title(f[:-4])
        #address = "E:\phone\Diary"
        address = os.path.join(f_address, f)
        try:
            with open(address, 'rb') as f:   #, encoding='utf-8'----------------------------------------------------------decrypt=================================================
                f = f.read()
        except FileNotFoundError:
            notification_label.config(text="Entry does not exist")
            notification_label.after(2000, clear_notification)
            no_file_error = 1
            #a notification button should appear------------------------------------------------------------------------------------
        if no_file_error:
            pass
        else:

            encrypt_key_type = Fernet(present_key)
            f = encrypt_key_type.decrypt(f).decode()
            entered_text.delete('1.0', tk.END)
            entered_text.insert(tk.END, f)
            address_1 = os.path.join(f_address, "tag_data.txt")
            with open( address_1, "r") as f:
                tag_data = f.read()
            temp_tag_data = address[len(f_address)+1:-4]   #address[15:27]
            ini_tag_index = tag_data.index(temp_tag_data)
            try:
                fin_tag_index = tag_data[ini_tag_index:].index("\n")+ini_tag_index
            except ValueError:
                pass    
            #print(tag_data.index(temp_tag_data), tag_data[tag_data.index(temp_tag_data):].index("\n"))
            #print(tag_data[tag_data.index(temp_tag_data):tag_data.index(temp_tag_data)+tag_data[tag_data.index(temp_tag_data):].index("\n")])
            #print(tag_data[ini_tag_index+13:fin_tag_index])
            tag_entry.delete(0, tk.END)
            tag_entry.insert(tk.END, tag_data[ini_tag_index+15:fin_tag_index])
            
            #importing images here------------------------------------------------------------------------------------------------------------
            widgets=base_image_canvas.winfo_children()
            widgets.remove(base_1)
            widgets.remove(base_2)
            for widget in widgets:
                widget.destroy()
            local_address= os.path.join(f_address, address[:-4])
            image_row=0
            image_column =0
            files = glob.glob(local_address+"/*.JPG")     #Error1   #should include png files.....********************************************
            if files != []:
                for i in files:
                    images_list.append(i)
                    #current_imagepath=i
                    #print(i)
                current_showing_image_set =0    
                len_of_images_list = len(images_list)
                if len_of_images_list == 0:
                    image_counter_frame.config(text="Showing ({} - {}) of {}".format(0, 0, 0))
                elif len_of_images_list>6:
                    image_counter_frame.config(text="Showing ({} - {}) of {}".format(0, 6, len_of_images_list))
                else:
                    image_counter_frame.config(text="Showing ({} - {}) of {}".format(0, len_of_images_list, len_of_images_list))
                for i in range(0, 6):
                    display_image(i)        #len(images_list)-1
            #importing audio files here---------------------------------------------------------------------------------------------------------
            #audio_import_files = glob.glob(local_address+"/*.mp3")
            #current_playlist_cbox.delete(0, tk.END)
            #audio_list = []
            #audio_address_list = []
            '''if audio_import_files != []:
                for i in audio_import_files:
                    audio_temp_name = i.split("\\")[-1]
                    audio_list.append(audio_temp_name)
                    audio_address_list.append(i)
                    current_playlist_cbox.insert(tk.END, audio_temp_name)'''

                
    except IndexError:
        pass


def del_entry(event):
    global proceed, audio_list, audio_address_list
    proceed_continue =1
    try:
        x = content_of_description.curselection()[0]
    except IndexError:
        notification_label.config(text="Entry does not Exist")
        notification_label.after(2000, clear_notification)
        proceed_continue = 0
    if proceed_continue:    
        f = content_of_description.get(x)
        proceed = mb.askyesno("Warning","You're about to permanent delete your Saved entry\nthe data cannot be recovered, \nDo you want to Proceed?")
        if proceed:
            proceed+=1
            notification_label.config(text="Entry Deleted")
            notification_label.after(2000, clear_notification)
            listof_files.remove(f)
            content_of_description.delete(0, tk.END)
            for i in listof_files:
                content_of_description.insert(tk.END, i)
            new_entry()
            address = os.path.join(f_address, f)
            try:
                os.remove(address)
            except FileNotFoundError:
                pass    
            tag_file_write_data =''
            address_1 = os.path.join(f_address, "tag_data.txt")
            with open( address_1, "r") as tag_file:
                for i in tag_file.readlines():
                    if f[:-4] in i:
                        pass
                    else:
                        tag_file_write_data+=i
            with open( address_1, "w") as tag_file:
                tag_file.write(tag_file_write_data)
            
            #print(address[:-4])
            try:
                shutil.rmtree(address[:-4])
            except PermissionError:
                pass
                #mixer.quit()
            except FileNotFoundError:
                pass    

            widgets=base_image_canvas.winfo_children()
            widgets.remove(base_1)
            widgets.remove(base_2)
            for widget in widgets:
                widget.destroy()
            audio_list = []
            #mixer.quit()
            audio_address_list = []
            #current_playlist_cbox.delete(0, tk.END)


#---------------------------------------search files frame config-------------------------------------------------------------------------------------    

choose_search = ttk.Combobox(searchfiles_data_frame, width =int(45*screen_width/1700), state="readonly")  #width = 45
choose_search['values'] = ("Tag Search", "Text Search", "Date Search")
choose_search.grid(row=0, column=0, columnspan =2)
choose_search.current(0)
choose_search.bind('<<ComboboxSelected>>', activate_ex_in)

get_text_for_search = tk.Entry(searchfiles_data_frame, bg=baground, fg=foreground, insertbackground=cursor_color)
get_text_for_search.grid( row=1, column=0, columnspan =2, sticky = tk.E+tk.N+tk.W, pady=5)
get_text_for_search.bind("<Return>", search_files)

ex_in_var = tk.IntVar()
ex_in_var.set(1)
exclusive_rad_button = ttk.Radiobutton(searchfiles_data_frame, variable=ex_in_var, text="Exclusive", value =1)
exclusive_rad_button.grid( row=2, column=0, sticky = tk.W+tk.N)

inclusive_rad_button = ttk.Radiobutton(searchfiles_data_frame, text="Inclusive", variable=ex_in_var, value =2)
inclusive_rad_button.grid( row=2, column=1, sticky = tk.E+tk.N)

date_entry_info = ttk.Label(searchfiles_data_frame, text="format: 'YYYY/MM/DD', ',' '-'")  #, use ',' for diff dates, '-' for from and to---------------------------------------------------------------

get_text_button = ttk.Button(searchfiles_data_frame, text="Search", command=search_files)
get_text_button.grid( row=3, column=1, sticky = tk.E+tk.N)

description_label = ttk.Label(searchfiles_data_frame, text= "Search Results-")
description_label.grid(row = 4, column=0, columnspan =2, sticky = tk.W+tk.N, pady=5)

content_of_description = tk.Listbox(searchfiles_data_frame, width =int(47*screen_width/1700), bg=baground, fg=foreground) #, height= 27
content_of_description.grid(row = 5, column=0, columnspan =2, sticky = tk.W+tk.N+tk.S+tk.E)
content_of_description.bind("<<ListboxSelect>>", showcontent)
content_of_description.bind('<Delete>', del_entry)
searchfiles_data_frame.rowconfigure(5, weight =1)

content_of_description_scrollbar = Scrollbar(searchfiles_data_frame)
content_of_description_scrollbar.grid(row = 5, column=1, sticky = tk.E+tk.N+tk.S)

content_of_description.config(yscrollcommand=content_of_description_scrollbar.set)
content_of_description_scrollbar.config(command=content_of_description.yview)

#======================================================================================================================================================================



#----------------------------------------------------------------------------------settings frame config---------------------------------------------------------------

#settings_frame
def ask_color_editor_baground():
    global baground
    baground= askcolor()[1]
    if baground !=None:
        baground_label_entry.config(bg=baground)
        update_settings()

def ask_color_editor_text():
    global foreground
    foreground= askcolor()[1]
    if foreground != None:
        foreground_label_entry.config(bg=foreground)
        update_settings()


def ask_color_cursor():
    global cursor_color
    cursor_color = askcolor()[1]
    if cursor_color != None:
        cursor_color_label_entry.config(bg=cursor_color)
        update_settings()


def ask_color_editor_window_baground():
    global window_baground
    window_baground = askcolor()[1]
    if window_baground !=None:
        window_baground_label_entry.config(bg=window_baground)
        window_settings_update()
        notification_label.config(text="Session Settings Updated")
        notification_label.after(2000, clear_notification)
        #update_settings()


def ask_color_editor_window_text():
    global window_foreground
    window_foreground = askcolor()[1]
    if window_foreground !=None:
        window_foreground_label_entry.config(bg=window_foreground)
        window_settings_update()
        notification_label.config(text="Session Settings Updated")
        notification_label.after(2000, clear_notification)
        #update_settings()

def window_settings_update():
    global window_baground ,window_foreground

    root.config(bg=window_baground)
    style = ttk.Style()
    #style.theme_use('alt')
    style.configure("TButton", foreground=window_foreground, background=window_baground)
    style.configure("TLabel", foreground=window_foreground, background=window_baground)
    #style.configure("TScrollbar.vbar", foreground=window_foreground, background=window_baground)
    #style.configure("TLabelFrame", foreground=window_foreground, background=window_baground)
    style.configure("TRadiobutton", foreground=window_foreground, background=window_baground, selectcolor=window_foreground)
    style.map('TButton', background=[('active', window_baground)])
    style.map('TRadiobutton',background = [('disabled', window_baground),('pressed', '!focus', window_baground),('active', window_baground)],indicatorcolor=[('selected', window_baground),('pressed', window_baground)])   #, foreground = [('disabled', window_foreground),('pressed', window_foreground),('active', window_foreground)]

    #font_size_entry.config(bg=baground, fg=foreground, insertbackground=cursor_color)
    hintscheckbutton.config(bg=window_baground)
    #tag_entry.config(bg=baground, fg=foreground, insertbackground=cursor_color)
    config_buttons_frame.config(bg=window_baground)
    searchfiles_data_frame.config(bg=window_baground, fg=window_foreground)
    settings_frame.config(bg=window_baground, fg=window_foreground)
    eximport_frame.config(bg=window_baground)
    export_frame.config(bg=window_baground, fg=window_foreground)
    import_frame.config(bg=window_baground, fg=window_foreground)
    config_buttons_frame_1.config(bg=window_baground)
    info_data_frame.config(bg=window_baground, fg=window_foreground)
    enteredtags_label.config(bg=window_baground)
    enteredtext_label.config(bg=window_baground, fg=window_foreground)
    add_images_frame.config(bg=window_baground, fg=window_foreground)
    image_counter_frame.config(bg=window_baground, fg=window_foreground)
    base_image_canvas.config(bg=window_baground)
    notification_label.config(background=window_baground, foreground=window_foreground)



def update_settings(*event):
    global baground, foreground, font_style, font_size, cursor_color, window_baground ,window_foreground

    if font_style_entry.get().strip() != "":    
        font_style = font_style_entry.get()
    if font_size_entry.get().strip() != "":
        try:
            font_size = int(font_size_entry.get())
        except ValueError:
            pass
            #-------------------------------------------error notification-------------------------------

    entered_text.config(font=(font_style, font_size), bg=baground, fg=foreground, insertbackground=cursor_color)
    font_size_entry.config(bg=baground, fg=foreground, insertbackground=cursor_color)
    tag_entry.config(bg=baground, fg=foreground, insertbackground=cursor_color)
    get_text_for_search.config(bg=baground, fg=foreground, insertbackground=cursor_color)
    notification_label.config(text="Session Settings Updated")
    notification_label.after(2000, clear_notification)


def save_settings():        
    global baground, foreground, font_style, font_size, settings_var, cursor_color
    if font_style_entry.get().strip() != "":    
        font_style = font_style_entry.get()
    if font_size_entry.get().strip() != "":
        try:
            font_size = int(font_size_entry.get())
        except ValueError:
            pass
            #-------------------------------------------error notification-------------------------------    
    '''if baground == "black":
        cursor_color = "white"
    else:
        cursor_color = "black" '''   

    entered_text.config(font=(font_style, font_size), bg=baground, fg=foreground, insertbackground=cursor_color)
    font_size_entry.config(bg=baground, fg=foreground, insertbackground=cursor_color)
    tag_entry.config(bg=baground, fg=foreground, insertbackground=cursor_color)
    get_text_for_search.config(bg=baground, fg=foreground, insertbackground=cursor_color)
    with open(settings_file_location, "w") as f:
        f.write(baground+"¿"+foreground+"¿"+cursor_color+"¿"+window_baground+"¿"+window_foreground+"¿"+font_style+"¿"+str(font_size)+"¿"+str(show_hint_bool.get()))
    notification_label.config(text="Settings Saved")
    notification_label.after(2000, clear_notification)    



def restore_default_settings():
    global baground, foreground, font_style, font_size, cursor_color, window_baground, window_foreground
    baground = default_baground
    foreground = default_foreground
    cursor_color = default_cursor_color
    font_style = default_font_style
    font_size = default_font_size
    window_baground = default_window_baground
    window_foreground = default_window_foreground

    '''if baground == "black":
        cursor_color = "white"
    else:
        cursor_color = "black" '''   

    entered_text.config(font=(font_style, font_size), bg=baground, fg=foreground, insertbackground=cursor_color)
    font_size_entry.config(bg=baground, fg=foreground, insertbackground=cursor_color)
    tag_entry.config(bg=baground, fg=foreground, insertbackground=cursor_color) 
    get_text_for_search.config(bg=baground, fg=foreground, insertbackground=cursor_color)
    window_settings_update()

    baground_label_entry.config(bg=baground)
    foreground_label_entry.config(bg=foreground)
    cursor_color_label_entry.config(bg=cursor_color)
    window_baground_label_entry.config(bg=window_baground)
    window_foreground_label_entry.config(bg=window_foreground)
    font_style_entry.current(fonts.index(font_style))
    font_size_entry.delete(0, tk.END)
    font_size_entry.insert(0, font_size) 
    notification_label.config(text="Default Settings Loaded")
    notification_label.after(2000, clear_notification)



def hint_en_dis():
    if show_hint_bool.get():
        hints.bind(jump_start_images_button, "Goto first page")
        hints.bind(jump_end_images_button, "Goto last page")
        hints.bind(update_button, "Update your Entry")
        hints.bind(minimise_add_images_frame, "Hide/Unhide Images")
        hints.bind(previous_imageset_button, "Previous page")
        hints.bind(next_imageset_button, "Next page")
        hints.bind(add_new_file_button, "Create new Entry")
        hints.bind(minimise_searchfiles_data_frame, "Search Entries")
        hints.bind(minimise_settings_frame, "UI Settings")
        hints.bind(minimise_eximport_frame, "Export/Import")
        hints.bind(minimise_info_frame, "Info")
    else:
        hints.unbind(jump_start_images_button)
        hints.unbind(jump_end_images_button)
        hints.unbind(update_button)
        hints.unbind(minimise_add_images_frame)
        hints.unbind(previous_imageset_button)
        hints.unbind(next_imageset_button)
        hints.unbind(add_new_file_button)
        hints.unbind(minimise_searchfiles_data_frame)
        hints.unbind(minimise_settings_frame)
        hints.unbind(minimise_eximport_frame)
        hints.unbind(minimise_info_frame)  
    notification_label.config(text="Session Settings Updated")
    notification_label.after(2000, clear_notification)
        
          

baground_label =ttk.Label(settings_frame, text ='Background Colour')  #, background="#000000", foreground="#ffffff"
baground_label.grid(row =0, column=0, pady=5, sticky=tk.W)

baground_label_entry = tk.Button(settings_frame, bg=baground, command=ask_color_editor_baground)#ttk.Combobox(settings_frame, width =26, state="readonly")
#baground_label_entry['values'] = colors #("white", "black", "red", "green", "blue", "cyan", "yellow", "magenta")
baground_label_entry.grid(row=0, column=1, padx=5, sticky=tk.W+tk.E, pady=5)
#baground_label_entry.bind('<<ComboboxSelected>>', update_settings)

foreground_label =ttk.Label(settings_frame, text ='Text Colour')
foreground_label.grid(row =1, column=0, sticky=tk.W)

foreground_label_entry = tk.Button(settings_frame, bg=foreground, command=ask_color_editor_text) #ttk.Combobox(settings_frame, width =26, state="readonly")
#foreground_label_entry['values'] = colors #("white", "black", "red", "green", "blue", "cyan", "yellow", "magenta", "light green")
foreground_label_entry.grid(row=1, column=1, padx=5, sticky=tk.W+tk.E, pady=5)
#foreground_label_entry.bind('<<ComboboxSelected>>', update_settings)

cursor_color_label =ttk.Label(settings_frame, text ='Cursor Colour')
cursor_color_label.grid(row =2, column=0, sticky=tk.W)


cursor_color_label_entry = tk.Button(settings_frame, bg=cursor_color, command=ask_color_cursor)
cursor_color_label_entry.grid(row=2, column=1, padx=5, sticky=tk.W+tk.E, pady=5)



window_baground_label =ttk.Label(settings_frame, text ='Window Background')  #, background="#000000", foreground="#ffffff"
window_baground_label.grid(row =3, column=0, pady=5, sticky=tk.W)

window_baground_label_entry = tk.Button(settings_frame, bg=window_baground, command=ask_color_editor_window_baground)#ttk.Combobox(settings_frame, width =26, state="readonly")
window_baground_label_entry.grid(row=3, column=1, padx=5, sticky=tk.W+tk.E, pady=5)

window_foreground_label =ttk.Label(settings_frame, text ='Window Text')
window_foreground_label.grid(row =4, column=0, sticky=tk.W)

window_foreground_label_entry = tk.Button(settings_frame, bg=window_foreground, command=ask_color_editor_window_text) #ttk.Combobox(settings_frame, width =26, state="readonly")
window_foreground_label_entry.grid(row=4, column=1, padx=5, sticky=tk.W+tk.E, pady=5)



font_style_label = ttk.Label(settings_frame, text ='Font Style')
font_style_label.grid(row =5, column=0, pady =5, sticky=tk.W)

font_style_entry = ttk.Combobox(settings_frame, width =int(26*screen_width/1700), state="readonly")
font_style_entry['values'] = fonts #('Amazon Ember','@Malgun Gothic', '@Microsoft JhengHei', '@Microsoft YaHei', '@MingLiU-ExtB', '@NSimSun', '@Yu Gothic Medium', 'Alef', 'Arial', 'Cabin Sketch', 'Caladea', 'Calibri', 'Cambria', 'Comic Sans MS', 'Consolas', 'Courier New', 'Ink Free', 'Limelight', 'Roman', 'Segoe Print', 'Source Code Pro', 'System', 'Terminal', 'Times New Roman', 'Ubuntu Mono')  #"Dancing Script", "Marck Script", "Roboto Google font", "Helvetica"
font_style_entry.bind('<<ComboboxSelected>>', update_settings)
font_style_entry.grid(row=5, column=1, padx=5)

font_size_label =ttk.Label(settings_frame, text ='Text Size')
font_size_label.grid(row =6, column=0, sticky=tk.W)

font_size_entry = tk.Entry(settings_frame, width =int(26*screen_width/1700), bg=baground, fg=foreground, insertbackground=cursor_color)
font_size_entry.grid(row=6, column=1, padx=5, sticky=tk.W+tk.E, pady=5)
font_size_entry.bind('<Return>', update_settings)

hints_label = ttk.Label(settings_frame, text ="Show Hints")
hints_label.grid(row =7, column=0, sticky=tk.W)

hintscheckbutton = tk.Checkbutton(settings_frame, command = hint_en_dis, variable = show_hint_bool, bg=window_baground)
hintscheckbutton.grid(row=7, column=1, padx=5, sticky=tk.W, pady=5)


restore_defaults_button = ttk.Button(settings_frame, text= "Restore Defaults", command=restore_default_settings)
restore_defaults_button.grid(row=8, column=1, padx=5, sticky=tk.E)

save_button = ttk.Button(settings_frame, text= "Save", command=save_settings)
save_button.grid(row=9, column=1, padx=5, sticky=tk.E)
#baground_label_entry.current(colors.index(baground))
#foreground_label_entry.current(colors.index(foreground))
font_style_entry.current(fonts.index(font_style))
font_size_entry.delete(0, tk.END)
font_size_entry.insert(0, font_size)




#======================================================================================================================================================================



#adding exports option---------------------------------------------------------------------------------------------------------------------------


export_type = tk.IntVar()
export_type.set(1)

import_type = tk.IntVar()
import_type.set(1)



def export_path_selector():
    global exports_path
    exports_path=tk.filedialog.askdirectory()
    if exports_path == "":
        export_location_entry.config(state=tk.ACTIVE)
        export_location_entry.delete(0, tk.END)
        export_location_entry.config(state=tk.DISABLED)
    else:
        export_location_entry.config(state=tk.ACTIVE)
        export_location_entry.delete(0, tk.END)
        export_location_entry.insert(0, exports_path)
        export_location_entry.config(state=tk.DISABLED)

imports_path = ""
imports_content_list = []

def import_path_selector():
    global imports_path
    if import_type.get():
        imports_path=tk.filedialog.askopenfilename(filetypes=[("ZIP File",('*.zip'))])
    else:
        imports_path=tk.filedialog.askopenfilename(filetypes=[("Text Files",('.txt'))], multiple=True)
    #imports_path=tk.filedialog.askdirectory()
    if imports_path == "":
        import_location_entry.config(state=tk.ACTIVE)
        import_location_entry.delete(0, tk.END)
        import_location_entry.config(state=tk.DISABLED)
    else:        
        import_location_entry.config(state=tk.ACTIVE)
        import_location_entry.delete(0, tk.END)
        import_location_entry.insert(0, imports_path)
        import_location_entry.config(state=tk.DISABLED)
    if type(imports_path) == tuple:
        imports_content_list = list(imports_path)
        for i in imports_content_list:
            files_to_import.insert(tk.END, i)

def zipdir(path, ziph):
    # ziph is zipfile handle
    encrypt_key_type = Fernet(present_key)
    for root, dirs, files in os.walk(path):
        #print(root,dirs,files)
        pathvar = root[-14:]
        for i in files:
            if i[-4:] == ".txt":
                if i == "tag_data.txt":
                    ziph.write( os.path.join(root, i), i)
                elif export_type.get():
                    ziph.write( os.path.join(root, i), i)
                else:
                    with open(os.path.join(f_address, i), 'rb') as f:
                        f = f.read()
                    f = encrypt_key_type.decrypt(f).decode()
                    with open("cache.txt", "w") as book:
                        book.write(f)
                    ziph.write( "cache.txt", i)
            else:
                ziph.write(os.path.join(root, i), os.path.join(pathvar, i))

def export_fn():
    if exports_path == "":
        notification_label.config(text="No Location is specified")
        notification_label.after(2000, clear_notification)
    else:
        if export_type.get():
            zipObj = ZipFile(os.path.join(exports_path, "Encrypted_backuplog.zip"), 'w')
            zipObj.write(os.path.join(login.user,"login.txt"),"login.txt")
        else:
            zipObj = ZipFile(os.path.join(exports_path, "Decrypted_backuplog.zip"), 'w')
        #zipObj.write(os.path.join(login.user,"login.txt"),"login.txt")
        zipdir(f_address, zipObj)
        zipObj.close()
        notification_label.config(text="Exported Successfully")
        notification_label.after(2000, clear_notification)



def import_fn():
    if imports_path == "":
        notification_label.config(text="No Location is specified")
        notification_label.after(2000, clear_notification)
    else:
        print(imports_path)
        cache_list = []
        if import_type.get():
            with ZipFile(imports_path, 'r') as zipobj:
                for i in zipobj.namelist():
                    cache_list.append(i)
                score=0
                if ("login.txt" in cache_list):
                    score+=1
                if("tag_data.txt" in cache_list):
                    score+=1
                if(score==2):
                    for i in cache_list:
                        zipobj.extract(i,"./cache/")
                    #move("./cache",f_address)
                    '''for i in files:
                            if(i=="login.txt"):
                                pass
                            elif(i=="tag_data.txt"):
                                pass
                            else:
                                #copyfile(os.path.join(root,i), os.path.join(f_address,i))
                                pass'''
                    for folders in list(os.walk("./cache/"))[0][1]:
                        try:
                            move(os.path.join("./cache",folders),f_address)
                        except Error:
                            shutil.rmtree(os.path.join(f_address, folders))
                            move(os.path.join("./cache",folders),f_address)
                    for files in list(os.walk("./cache/"))[0][2]:
                        if(files=="login.txt"):
                                pass
                        elif(files=="tag_data.txt"):
                            try:
                                move(os.path.join("./cache",files),f_address)
                            except Error:
                                originalfiles = []
                                originaltags ={}
                                with open(address_1,"r") as originaltagfile:
                                    for i in originaltagfile.readlines():
                                        st = i.split("¿")
                                        originalfiles.append(st[0])
                                        originaltags[st[0]]=st[1]
                                newfiles = []
                                newtags ={}
                                with open("./cache/tag_data.txt","r") as newtagfile:
                                    for i in newtagfile.readlines():
                                        st = i.split("¿")
                                        newfiles.append(st[0])
                                        newtags[st[0]]=st[1]
                                list1 = list(set(originalfiles).difference(set(newfiles)))
                                with open(address_1,"w") as finalfile:
                                    for i in list1:
                                        finalfile.write(i+"¿"+originaltags[i])
                                    for i in newfiles:
                                        finalfile.write(i+"¿"+newtags[i])
                                
                            
                            
                        else:
                            try:
                                move(os.path.join("./cache",files),f_address)
                            except Error:
                                #shutil.rmtree(os.path.join(f_address, files))
                                os.remove(os.path.join(f_address, files))
                                move(os.path.join("./cache",files),f_address)
                        
                    notification_label.config(text="Imported Successfully")
                    notification_label.after(2000, clear_notification)


                elif(score==1):
                    notification_label.config(text="Corrupted Entries\nThese are \'decrypted Entries\'")
                    notification_label.after(2000,clear_notification)
                else:
                    notification_label.config(text="Corrupted Zip file")
                    notification_label.after(2000,clear_notification)
        else:
            pass


def show_import_content(event):
    x = files_to_import.curselection()[0]
    f = files_to_import.get(x)
    print(x, f)


def del_import_entry():
    pass


def change_button_text():
    global import_location_entry
    if import_type.get():
        import_location_button.config(text="Select Location")
        import_location_entry.config(state=tk.ACTIVE)
        import_location_entry.delete(0, tk.END)
        import_location_entry.config(state=tk.DISABLED)
    else:
        import_location_button.config(text="Select Files")
        import_location_entry.config(state=tk.ACTIVE)
        import_location_entry.delete(0, tk.END)
        import_location_entry.config(state=tk.DISABLED)    

export_rad_button1 = ttk.Radiobutton(export_frame, text = "Normal", variable=export_type, value = 0)
export_rad_button1.grid(row=0, column=0, sticky=tk.W)

export_rad_button2 = ttk.Radiobutton(export_frame, text = "Encrypted", variable=export_type, value = 1)
export_rad_button2.grid(row=0, column=2, sticky=tk.E)


export_location_entry = ttk.Entry(export_frame, state= tk.DISABLED, width=int(47*screen_width/1700))
export_location_entry.grid(row=1, column=0, columnspan=3, sticky=tk.E+tk.W)

export_location_button = ttk.Button(export_frame, text="Select Location", command= export_path_selector)
export_location_button.grid(row=2, column=2, sticky=tk.E)


export_button =ttk.Button(export_frame, text ="Export", command=export_fn)  #, background="#000000", foreground="#ffffff"  , sticky=tk.E+tk.W+tk.N+tk.S
export_button.grid(row=3, column=2, sticky=tk.E)



import_rad_button1 = ttk.Radiobutton(import_frame, text = "Normal", variable=import_type, value = 0, command=change_button_text)
import_rad_button1.grid(row=0, column=0, sticky=tk.W)

import_rad_button2 = ttk.Radiobutton(import_frame, text = "Encrypted", variable=import_type, value = 1, command=change_button_text)
import_rad_button2.grid(row=0, column=2, sticky=tk.E)


import_location_entry = ttk.Entry(import_frame, state= tk.DISABLED)   #, width=35
import_location_entry.grid(row=1, column=0, columnspan=3, sticky=tk.E+tk.W)

import_location_button = ttk.Button(import_frame, text="Select Location", width=int(14*screen_width/1700), command= import_path_selector)
import_location_button.grid(row=2, column=2, sticky=tk.E)


files_to_import = tk.Listbox(import_frame, width =int(47*screen_width/1700))  #, height= 22
files_to_import.grid(row = 3, column=0, columnspan =3, sticky = tk.W+tk.N+tk.E+tk.S)
files_to_import.bind("<<ListboxSelect>>", show_import_content)
files_to_import.bind('<Delete>', del_import_entry)
import_frame.rowconfigure(3, weight=1)

files_to_import_scrollbar = Scrollbar(import_frame)
files_to_import_scrollbar.grid(row = 3, column=2, sticky = tk.E+tk.N+tk.S)

files_to_import.config(yscrollcommand=files_to_import_scrollbar.set)
files_to_import_scrollbar.config(command=files_to_import.yview)


import_button =ttk.Button(import_frame, text ="Import", command=import_fn)  #, background="#000000", foreground="#ffffff"  , sticky=tk.E+tk.W+tk.N+tk.S
import_button.grid(row=4, column=2, sticky=tk.E)




'''
backup_button = ttk.Button(export_frame, text ="Backup", command= backup)
backup_button.grid(row=3, column=2)
'''
#========================================================================================================





#-------------------------------------------------------------------------------info frame config----------------------------------------------------------------------


info_data= '''

F11    - Full screen 
Ctrl+a - Select all
Ctrl+c - copy
Ctrl+v - paste
Ctrl+x - cut
Ctrl+s - Update the current session Data
Ctrl+i - add's date and time to the Entry
Ctrl+n - Opens new file
del    - Delete an entry (Which will be displayed after performing a search)

----------------------------------------------------------

*Add tags for every file to make it easier to access them.

*Add multiple tags by using a ',' as a seperator(tags are not 'case sensitive')

*Deleted entry cannot be recovered

*Date Search-
  -Enter a date in the format of YYYY/MM/DD to fetch all the files saved on that day.
  -Enter multiple dates seperated with ',' to fetch all the files saved on those days.
  -Enter 2 dates chronologically to get all the files between those days.
   
*Tag Search-
  -Access your file's using the tags assignes to them.
  -'Exclusive option' shows the files which consists of all the tag's you've entered.
  -'Inclusive option' shows the files which consists, at least one of tag's you've entered.

*Text Search-
  -Access your file's using a 'word or sentence' used in it..


'''





info_label =ttk.Label(info_data_frame, text =info_data, anchor=tk.N, background="#000000", foreground="#ffffff")
info_label.grid(row=0, column=0, sticky=tk.E+tk.W+tk.S+tk.N)
info_data_frame.rowconfigure(0, weight=1)



#======================================================================================================================================================================


#-----------------------------------------------------------------------------------add images frame config---------------------------------------------------------------

def del_image(but_num):
    global current_imagepath, current_showing_image_set   #image_column, image_row, image_num, 
    #print(but_num, current_showing_image_set)    
    sub=0
    images_list.pop(but_num)
    '''image_column = 0
    image_row = 0
    image_num =0'''
    widgets=base_image_canvas.winfo_children()
    widgets.remove(base_1)
    widgets.remove(base_2)
    if len(widgets) == 1:
        sub = 6
    for widget in widgets:
        #print(widget)
        widget.destroy()
    len_of_images_list = len(images_list)
    current_showing_image_set= current_showing_image_set-sub
    if len_of_images_list-current_showing_image_set>6:
        end =current_showing_image_set+6
    else:
        end =len_of_images_list
            
    image_counter_frame.config(text="Showing ({} - {}) of {}".format(current_showing_image_set+1, end, len_of_images_list))    
    if len(images_list) == 0:
        image_counter_frame.config(text="Showing (0 - 0) of 0")
        current_showing_image_set = 0
        end =0
    for i in range(current_showing_image_set, end):                        #0, len(images_list)
        #print(i)
        #current_imagepath=i
        display_image(i)



def image_path():
    global current_imagepath, images_list, current_showing_image_set         #, image_row, image_column, image_num
    current_imagepath=tk.filedialog.askopenfilename(filetypes=[("Image File",('.jpg','.png'))], multiple=True)
    
    if current_imagepath == "":
        pass
    else:
        #l=len(images_list)
        widgets = base_image_canvas.winfo_children()
        widgets.remove(base_1)
        widgets.remove(base_2)
        for widget in widgets:
            widget.destroy()
        images_list.extend(list(current_imagepath))
        len_of_list = len(images_list)
        l=len_of_list%6
        if l==0:
            l=6
        current_showing_image_set = len_of_list-l
        image_counter_frame.config(text="Showing ({} - {}) of {}".format(current_showing_image_set+1, len_of_list, len_of_list))
        for i in range(len_of_list-l, len_of_list):                #l, len(images_list)
            display_image(i)              #len(images_list)-1

def display_image(indexof_image):
    global current_imagepath, images_list                #, image_row, image_column, image_num
    try:
        im = Image.open(images_list[indexof_image])
        base_width, base_height=im.size
        if base_width>=base_height:
            im = im.resize((150, int((base_height*150)/base_width)), Image.ANTIALIAS)
        else:
            im = im.resize((int((base_width*150)/base_height), 150), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(im)
        myvar=ttk.Button(base_image_canvas ,image = tkimage, command=lambda but_num=indexof_image : del_image(but_num))                  #image_num
        myvar.image = tkimage
        image_row = indexof_image//2
        image_column = indexof_image%2
        myvar.grid(row=image_row, column=image_column)

        
        #image_num+=1
    except (AttributeError, UnidentifiedImageError):
        imgdisp_error = 1

current_showing_image=0
current_showing_image_set = 0
 

image_top_var=0

def close_image_viewer():
    global image_top_var, current_showing_image, check_minimise
    image_viewer.destroy()
    image_top_var = 0
    check_minimise = False
    current_showing_image =0

image_viewer = tk.Toplevel(root)
image_viewer.withdraw()

check_minimise = False
def slide_show():
    global image_top_var, current_showing_image, image_viewer, check_minimise#, cur_image
    if check_minimise:
        image_viewer.deiconify()


    if image_top_var == 0:
        image_top_var =1
        check_minimise=True
        image_viewer = tk.Toplevel(root)
        image_viewer.state('zoomed')
        image_viewer.configure(bg="#000000")
        cur_image=ttk.Label(image_viewer, image="")

        def next_image(event):
            global current_showing_image
            if len(images_list)-1>current_showing_image:
                current_showing_image+=1
                show_image()
                
        def previous_image(event):
            global current_showing_image
            if current_showing_image>0:
                current_showing_image-=1
                show_image()

        def show_image():
            global current_showing_image
            if len(images_list) !=0:
                im = Image.open(images_list[current_showing_image])
                base_width, base_height=im.size
                image_viewer.title("Image "+str(current_showing_image+1))
                if base_width>base_height:
                    im = im.resize((screen_width, int((base_height*screen_width)/base_width)), Image.ANTIALIAS)        #screen_width, int((base_height*screen_width)/base_width)            #(1920, int((base_height*1920)/base_width))
                else:
                    im = im.resize((int((base_width*screen_height)/base_height), screen_height), Image.ANTIALIAS)                       #(int((base_width*1050)/base_height), 1050)
                tkimage = ImageTk.PhotoImage(im)
                cur_image.config(image = tkimage)                   #, bg="#000000")
                cur_image.image = tkimage
                cur_image.place(relx=0.5, rely=0.5, anchor=tk.CENTER)    

        show_image()

        image_viewer.bind('<Right>', next_image)
        image_viewer.bind('<Left>', previous_image)
        image_viewer.protocol("WM_DELETE_WINDOW", close_image_viewer)


def previous_imageset():
    global current_showing_image_set
    if current_showing_image_set-6>=0:
        current_showing_image_set-=6
        len_of_list = len(images_list)
        if len_of_list-current_showing_image_set>6:
            image_counter_frame.config(text="Showing ({} - {}) of {}".format(current_showing_image_set+1, current_showing_image_set+6, len_of_list))
        else:
            image_counter_frame.config(text="Showing ({} - {}) of {}".format(current_showing_image_set+1, len_of_list, len_of_list))
        widgets = base_image_canvas.winfo_children()
        widgets.remove(base_1)
        widgets.remove(base_2)
        for widget in widgets:
            widget.destroy()
        for i in range( current_showing_image_set, current_showing_image_set+6):
            display_image(i)

def next_imageset():
    global current_showing_image_set
    if current_showing_image_set+6<len(images_list):
        current_showing_image_set+=6
        len_of_list = len(images_list)
        if len_of_list-current_showing_image_set>6:
            image_counter_frame.config(text="Showing ({} - {}) of {}".format(current_showing_image_set+1, current_showing_image_set+6, len_of_list))
        else:
            image_counter_frame.config(text="Showing ({} - {}) of {}".format(current_showing_image_set+1, len_of_list, len_of_list))
        widgets = base_image_canvas.winfo_children()
        widgets.remove(base_1)
        widgets.remove(base_2)
        for widget in widgets:
            widget.destroy()
        for i in range(current_showing_image_set, current_showing_image_set+6):
            if i<len(images_list):
                display_image(i)
                #print(i)

def jump_start():
    global current_showing_image_set
    if current_showing_image_set==0:
        pass
    else:
        current_showing_image_set = 0
        len_of_list = len(images_list)
        end =0
        if len_of_list>=6:
            image_counter_frame.config(text="Showing ({} - {}) of {}".format(1, 6, len_of_list))
            end = 6
        else:
            image_counter_frame.config(text="Showing ({} - {}) of {}".format(current_showing_image_set+1, len_of_list, len_of_list))    
            end = len_of_list
        widgets = base_image_canvas.winfo_children()
        widgets.remove(base_1)
        widgets.remove(base_2)
        for widget in widgets:
            widget.destroy()
        for i in range( current_showing_image_set, end):
            display_image(i)    


def jump_end():
    global current_showing_image_set
    len_of_list = len(images_list)
    if current_showing_image_set>=len_of_list-6:
        pass
    else:
        widgets = base_image_canvas.winfo_children()
        widgets.remove(base_1)
        widgets.remove(base_2)
        for widget in widgets:
            widget.destroy()
        l=len_of_list%6
        if l==0:
            l=6
        current_showing_image_set = len_of_list-l
        image_counter_frame.config(text="Showing ({} - {}) of {}".format(current_showing_image_set+1, len_of_list, len_of_list))
        for i in range(len_of_list-l, len_of_list):                #l, len(images_list)
            display_image(i)

jump_start_images_button = ttk.Button(add_images_frame, text= "<<", command=jump_start, width=4)  #int(4*screen_width/1700)
jump_start_images_button.grid(row=0, column =0, sticky=tk.W)

previous_imageset_button = ttk.Button(add_images_frame, text="<", command= previous_imageset, width=4)#int(4*screen_width/1700))
previous_imageset_button.grid(row=0, column=1, sticky=tk.W)

slideshow_button = ttk.Button(add_images_frame, text="Slide Show", command = slide_show, width = 18)#int(18*screen_width/1700))
slideshow_button.grid(row=0, column=2, sticky=tk.E+tk.W)


next_imageset_button = ttk.Button(add_images_frame, text=">", command= next_imageset, width=4)#int(4*screen_width/1700))
next_imageset_button.grid(row=0, column=3, sticky=tk.E)

jump_end_images_button = ttk.Button(add_images_frame, text= ">>", command=jump_end, width=4)#int(4*screen_width/1700))
jump_end_images_button.grid(row=0, column =4, sticky=tk.E)

add_image_button = ttk.Button(add_images_frame, text="Add Images", command = image_path)
add_image_button.grid(row=0, column=5, sticky=tk.E+tk.S)

image_counter_frame = tk.Label(add_images_frame, text="showing (0 - 0) of 0", bg=window_baground, fg=window_foreground)
image_counter_frame.grid(row=1, column=0, columnspan=6, sticky=tk.W+tk.N)

base_image_canvas = tk.Canvas(add_images_frame, bg=window_baground, width=300*screen_width/1700, highlightthickness=0)
base_image_canvas.grid(row=2, column=0, columnspan=6, sticky=tk.E+tk.W+tk.N+tk.S)


im = Image.open("Images/base1.png")                   #"C:\Users\Avinash Kumar\Desktop\base.JPG"  r"C:\Users\Avinash Kumar\Documents\Vs code\backup\base.JPG"
#im= im.resize((150, 10), Image.ANTIALIAS)
tkimage = ImageTk.PhotoImage(im)
base_1=ttk.Label(base_image_canvas ,image = tkimage)
base_1.grid(row=0, column=0)

base_2=ttk.Label(base_image_canvas ,image = tkimage)
base_2.grid(row=0, column=1)






#=========================================================================================================================================================================


#-------------------------------------------add audio files frame---------------------------------------------------------------------------------------------------------
'''total_audio_runtime = 0
audio_run_time = 0
queue_start =False
progress_value = 0
duration =0

current_song_index = 0




def update_current_playlist_cbox():
    global audio_list
    current_playlist_cbox.delete(0, tk.END)
    for i in audio_list:
        current_playlist_cbox.insert(tk.END, i)
    #print(audio_list)

def add_songs():
    global audio_list, audio_address_list
    temp_files_list = list(tk.filedialog.askopenfilename(filetypes=[("Audio File",('*.mp3'))], multiple=True))
    if temp_files_list != []:
        for i in temp_files_list:
            audio_list.append(i.split("/")[-1])
            audio_address_list.append(i)
            update_current_playlist_cbox()

cache_audio_file_address = ".cache_audio/"
def start_record():
    global record_check, record_pause_check, record_timer, cache_audio_file_name, audio_list, audio_address_list
    record_timer = 0
    cache_audio_file_name =str(time.strftime("%Y%m%d%H%M%S"))
    #print(cache_audio_file_name, f_address+"/"+new_created_name)
    cache_audio_file_name_withformat = cache_audio_file_name+".wav"
    complete_cache_audio_file_with_address_and_format = cache_audio_file_address+cache_audio_file_name_withformat
    wf = wave.open(complete_cache_audio_file_with_address_and_format, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pa.get_sample_size(FORMAT))
    wf.setframerate(RATE)

    while record_check:
        if record_pause_check:
            notification_label.config(text="Recording")
            data = "#-#"#stream.read(chunk)
            wf.writeframes(data)
            audio_intensity = np.fromstring(data, dtype=np.int16)
            audio_intensity = np.average(np.abs(audio_intensity))*2
            audio_frequency_progress_bar['value']= int(250*audio_intensity/2**16)   #50*audio_intensity/2**16  
        else:
            #audio_frequency_progress_bar['value'] = 0
            notification_label.config(text="Recording Paused")

    s = asa.from_wav(complete_cache_audio_file_with_address_and_format)#from_file(complete_cache_audio_file_with_address_and_format, format="wav")
    s.export(cache_audio_file_address+cache_audio_file_name+".mp3", format="mp3")
    #stream.stop_stream()
    #stream.close()
    #pa.terminate()
    wf.close()
    audio_list.append(cache_audio_file_address+cache_audio_file_name+".mp3")#cache_audio_file_name_withformat)
    audio_address_list.append("")
    notification_label.config(text="Record Saved")
    notification_label.after(2000, clear_notification)
    update_current_playlist_cbox()
    



def record_song_thread():
    global song_thread, record_check
    if record_check == False:
        song_thread =  threading.Thread(target=start_record)
        song_thread.daemon = True
        song_thread.start()
        notification_label.config(text= "Recording")
        record_check = True
    else:
        record_check = False    

def pause_record():
    global record_check, record_pause_check
    if record_check == True:
        if record_pause_check == True:
            record_pause_check=False
            #notification_label.config(text="Recording Paused")
        else:
            record_pause_check=True
            #notification_label.config(text="Recording Resumed")





def play_song(*event):
    global audio_list, audio_address_list, current_song_index, duration, audio_run_time, progress_value
    event = list(event)
    progress_value = 0
    progressbar['value'] = progress_value
    audio_run_time = 0
    mixer.quit()
    try:
        current_song_index=event[1]
    except IndexError:    
        current_song_index = current_playlist_cbox.curselection()[0]
    song_name = current_playlist_cbox.get(current_song_index)
    song_cache_address = audio_address_list[current_song_index]'''
'''    if audio_address_list[current_song_index] == "" or song_name[-4:]==".wav" :
        song_cache_address = current_playlist_cbox.get(current_song_index)
        with contextlib.closing(wave.open(song_cache_address,'r')) as f:
            frames = f.getnframes()
            framerate = f.getframerate()
            duration = frames / float(framerate)
        mixer.init(frequency=framerate)'''
'''    if audio_address_list[current_song_index] == "":
        song_cache_address = song_name    
    song = MP3(song_cache_address)
    mixer.init(frequency=song.info.sample_rate)
    duration = song.info.length
    #print(duration)
    if len(song_name)>23:
        song_name = f'{song_name[0:20]}...'
    audio_name_label.config(text=song_name)    
    mixer.music.load(song_cache_address)
    mixer.music.set_volume(0.5)
    mixer.music.play()
    



def previous_song_fn():
    global current_song_index
    if current_song_index > 0:
        current_song_index-=1
        play_song(0, current_song_index)

def next_song_fn():
    global current_song_index
    if current_song_index < len(audio_list)-1:   
        current_song_index+=1
        play_song(0, current_song_index)


play_pause_toggle =False
song_play_time_toggle = True

def play_pause_fn(*event):
    global play_pause_toggle, song_play_time_toggle
    try:
        if mixer.music.get_busy():
            #print(play_pause_toggle)
            play_pause_toggle = not play_pause_toggle
            #print(play_pause_toggle)
        if play_pause_toggle:    
            mixer.music.pause()
            song_play_time_toggle = False
            print("pause")
        else:
            mixer.music.unpause()
            song_play_time_toggle = True
    except error:
        notification_label.config(text="No file to play")
        notification_label.after(2000, clear_notification)


def seek_song(event):
    global progress_value, total_audio_runtime, audio_run_time
    x = event.x
    if x>327:
        x=327
    elif x<0:
        x=0
    progress_value = int(x*100/327)
    progressbar["value"] = int(x*100/327)
    #mixer.music.play(loops=0, start=60)
    try:
        audio_run_time = (x*duration)//327
        mixer.music.set_pos(0)
        mixer.music.set_pos(audio_run_time)
    except (ValueError, error):#(IndexError, error):
        pass
        #print("error")

def del_queue_entry(event):
    remove_index = current_playlist_cbox.curselection()[0]
    if remove_index == current_song_index:
        mixer.quit()
    audio_list.pop(remove_index)
    audio_address_list.pop(remove_index)
    current_playlist_cbox.delete(0, tk.END)
    for i in audio_list:
        current_playlist_cbox.insert(tk.END, i)

player_frame = tk.Frame(add_sound_frame)
player_frame.grid(row=0, column=0, columnspan =2, sticky=tk.N+tk.W)   #, sticky=tk.E+tk.W+tk.N+tk.S  , columnspan =2

record_audio_frame = tk.LabelFrame(add_sound_frame, text="Record audio")
record_audio_frame.grid(row=4, column=0, columnspan=2, sticky=tk.W+tk.S+tk.E+tk.N)

player_buttons_frame=ttk.Frame(player_frame)
player_buttons_frame.grid(row=0, column=0, sticky=tk.W+tk.N)

previous_button = tk.Button(player_buttons_frame, text="◄", font=("helvetica", 9), bg="#000000", fg="#ffffff", command = previous_song_fn)
previous_button.grid(row=0, column=1, sticky =tk.W)


im = Image.open("Images/play_pause.png")
im = im.resize((50, 50), Image.ANTIALIAS)
tkimage = ImageTk.PhotoImage(im)
play_pause = tk.Button(player_buttons_frame, image = tkimage, relief=tk.FLAT, command = play_pause_fn)
play_pause.image = tkimage
play_pause.grid(row=0, column=2, sticky =tk.W)


next_button = tk.Button(player_buttons_frame, text="►", font=("helvetica", 9), bg="#000000", fg="#ffffff", command = next_song_fn)
next_button.grid(row=0, column=3, sticky =tk.W)

audio_label = tk.Label(player_buttons_frame, text="  Playing :", font=("helvetica", 9))
audio_label.grid(row=0, column=4, sticky =tk.W+tk.N)

audio_name_label = tk.Label(player_buttons_frame, text="-", font=("helvetica", 9))
audio_name_label.grid(row=0, column=5, sticky =tk.W+tk.N)

progressbar = ttk.Progressbar(add_sound_frame, length = 327, orient = tk.HORIZONTAL, mode = 'determinate')   #, length = 400
progressbar.grid(row=1, column=0, columnspan=2, sticky=tk.E+tk.W)
progressbar.bind("<Button-1>", seek_song)
progressbar.bind("<B1-Motion>", seek_song)

fin_progress_time = tk.Label(add_sound_frame, text="0:00:00 / 0:00:00")
fin_progress_time.grid(row=0, column=1, sticky=tk.E+tk.S)



current_playlist_cbox = tk.Listbox(add_sound_frame, width =55, height=23)
current_playlist_cbox.grid(row = 2, column=0, columnspan =2, sticky = tk.E+tk.W+tk.N+tk.S, pady=3)
current_playlist_cbox.bind("<Double-Button-1>", play_song)   #"<<ListboxSelect>>"
current_playlist_cbox.bind("<Return>", play_song)
current_playlist_cbox.bind('<Delete>', del_queue_entry)

content_of_description_scrollbar = Scrollbar(add_sound_frame)
content_of_description_scrollbar.grid(row = 2, column=1, sticky = tk.E+tk.N+tk.S)

current_playlist_cbox.config(yscrollcommand=content_of_description_scrollbar.set)
content_of_description_scrollbar.config(command=current_playlist_cbox.yview)



add_songs_button = ttk.Button(add_sound_frame, text="Add Audio", command=add_songs)
add_songs_button.grid(row=3, column=1, sticky =tk.E)




im = Image.open("Images/record.png")
im = im.resize((60, 60), Image.ANTIALIAS)
tkimage = ImageTk.PhotoImage(im)
record_button = tk.Button(record_audio_frame, image = tkimage, relief=tk.FLAT, command=record_song_thread)
record_button.grid(row=0, column=0, sticky =tk.W)
record_button.image = tkimage

im = Image.open("Images/pause_recording.png")
im = im.resize((30, 30), Image.ANTIALIAS)
tkimage = ImageTk.PhotoImage(im)
pause_recording_button = tk.Button(record_audio_frame, image = tkimage, relief=tk.FLAT, command=pause_record)
pause_recording_button.grid(row=0, column=1, sticky =tk.W)
pause_recording_button.image = tkimage

audio_frequency_progress_bar = ttk.Progressbar(record_audio_frame, length = 210, orient = tk.HORIZONTAL, mode = 'determinate')
audio_frequency_progress_bar.grid(row=0, column=2, sticky =tk.W+tk.E, padx=4)

recording_time = tk.Label(add_sound_frame, text="0:00:00")
recording_time.grid(row=4, column=1, sticky =tk.E+tk.S, padx=2, pady=2)

quit_mixer_var = 0
def update():
    global current_song_index, progress_value, song_play_time_toggle, total_audio_runtime, audio_run_time, quit_mixer_var
    #print(datetime.timedelta(seconds=song_play_time))#run_time))
    try:
        run_time = mixer.music.get_pos()//1000
        if run_time != -1:
            quit_mixer_var = 1
            #ini_progress_time.config(text=datetime.timedelta(seconds=song_play_time))#run_time))
            fin_progress_time.config(text=str(datetime.timedelta(seconds=audio_run_time))+" / "+str(datetime.timedelta(seconds=int(duration))))
            progressbar["value"] = progress_value
            if song_play_time_toggle:
                #quit_mixer_var = 0
                progress_value += (100/int(duration))
                audio_run_time+=1
        else:
            if quit_mixer_var and song_play_time_toggle == False:
                mixer.quit()
                quit_mixer_var = 0 
    except error:
        pass    
    fin_progress_time.after(1000, update)

update()'''
#==============================================================================================================================================================================



#function to create the file to save.

def open_file():
    global address, tag_data, present_key, new_created_name, address_2, address_cache, address_1
    #address = "E:\phone\Diary"
    new_created_name = time.strftime("%Y%m%d%H%M%S")
    root.title(new_created_name)
    address = os.path.join(f_address, new_created_name+".txt")
    address_1 = os.path.join(f_address, "tag_data.txt")
    address_cache = os.path.join(f_address, ".cache")
    try:
        os.mkdir(address_cache)
    except FileExistsError:
        pass    
    #os.chmod(address, S_IWUSR|S_IREAD)      #, S_IREAD|S_IRGRP|S_IROTH
    try:
        os.chmod(address_1, S_IWUSR|S_IREAD)
    except FileNotFoundError:
        pass    
    '''try:    
        os.mkdir(".cache_audio")
    except FileExistsError:
        pass   '''
    f =  open(address_1, "a")
    f.close()
       

open_file()

#Basic acceleratrs for application
def Full_screen_toggle(event):
    if root.attributes("-fullscreen")==1:
        root.attributes("-fullscreen", False)
    else:
        root.attributes("-fullscreen", True)

#print(root.attributes("-fullscreen"))

def new_entry(*event):
    global address, proceed, new_created_name, address_2, images_list, audio_list, audio_address_list                 #, image_num, image_row, image_column
    if proceed==0:
        proceed = mb.askyesno("Warning","You're about to open \"New File\", \nany unsaved data will be lost, \nproceed?")
    if proceed:
        images_list =[]
        time_tupple=time.localtime()
        image_counter_frame.config(text="Showing ({} - {}) of {}".format(0, 0, 0))
        #address = "E:\phone\Diary"
        new_created_name = time.strftime("%Y%m%d%H%M%S")
        root.title(new_created_name)
        address = os.path.join(f_address, new_created_name+".txt")
        entered_text.delete("0.1",tk.END)
        tag_entry.delete('0', tk.END)  #"0.1",tk.END
        #entered_text.insert(tk.END, )
        entered_text.insert(tk.END, time.strftime("%m/%d/%Y")+'  '+currentime+'\n\n')
        #address_2 = os.path.join(f_address, new_created_name)
        #os.mkdir(address_2)
        '''image_column = 0
        image_row = 0
        image_num =0'''
        #image related clear
        widgets=base_image_canvas.winfo_children()
        widgets.remove(base_1)
        widgets.remove(base_2)
        for widget in widgets:
            widget.destroy()
        #audio_related clear
        #audio_list = []
        #audio_address_list = []
        #current_playlist_cbox.delete(0, tk.END)
        #mixer.quit()
        if proceed==1:    
            notification_label.config(text="New Entry")
            notification_label.after(2000, clear_notification)
        proceed =0

#UI button-----------------------------------------------------------------------------------------------------------
add_new_file_button_image = Image.open("Images/add.png")
add_new_file_button_image = add_new_file_button_image.resize((40, 40), Image.ANTIALIAS)
add_new_file_button_image = ImageTk.PhotoImage(add_new_file_button_image)


add_new_file_button = ttk.Button(config_buttons_frame, image=add_new_file_button_image, width=2, command =new_entry)
add_new_file_button.grid(row=0, column=0, sticky=tk.N+tk.S)  #+tk.S
add_new_file_button.image = add_new_file_button_image

#=====================================================================================================================

def make_bold(event):
    global make_bold_variable, sel_first, sel_last
    #print(entered_text.get(tk.SEL_FIRST, tk.SEL_LAST))
    try:
        entered_text.tag_add("BOLD", tk.SEL_FIRST, tk.SEL_LAST)  
        print(tk.SEL_FIRST, tk.SEL_LAST)
    except tk.TclError:
        make_bold_variable+=1
        if make_bold_variable%2==0:
            sel_last=entered_text.index(tk.INSERT)
            entered_text.tag_add("BOLD", sel_first, sel_last)
        else:
            sel_first=entered_text.index(tk.INSERT)
        

def add_time(event):
    entered_text.insert(tk.INSERT, '\n\n'+time.strftime("%m/%d/%Y")+'  '+currentime+'\n\n')
    #entered_text.insert(tk.END, '\n')

def right_bracket(event):
    pointer = entered_text.index(tk.INSERT)
    #print(float(pointer)+0.1)
    entered_text.insert(tk.INSERT, ")")
    entered_text.mark_set("insert", pointer)



root.bind('<Control-n>', new_entry)
root.bind('<F11>', Full_screen_toggle)
#root.bind('<F1>', info)
root.bind('<Control-s>', update_user_text_infile)
#root.bind('<Control-b>', make_bold)
root.bind('<Control-i>', add_time)
root.bind('<Shift-(>', right_bracket)
#root.bind('<Control-o>', settings)

hint_en_dis()

root.bind('<Control-N>', new_entry)
root.bind('<Control-S>', update_user_text_infile)
root.bind('<Control-I>', add_time)
#root.bind('<Control-O>', settings)
#Basic acceleratrs for application Ends here

def make_readonly():
    f = list(os.walk(f_address))[0][2]    
    p = os.popen('attrib +h '+f_address)
    p.close()
    for i in f:
        p = os.popen('attrib +h '+os.path.join(f_address, i))
        p.close()
        os.chmod(os.path.join(f_address, i), S_IREAD|S_IRGRP|S_IROTH)
    #print(login.user)
    f = list(os.walk(login.user))[0][2]
    for i in f:
        os.chmod(os.path.join(login.user, i), S_IREAD|S_IRGRP|S_IROTH)
    '''try:
        shutil.rmtree(".cache_audio")
    except PermissionError:
        pass
        #shutil.rmtree(".cache_audio")'''
    sys.exit()
    root.destroy()


if login.access==1:
    f = list(os.walk(f_address))[0][2]
    for i in f:
        if i == "tag_data.txt":
            p = os.popen('attrib -h '+os.path.join(f_address, i))
            p.close()
        os.chmod(os.path.join(f_address, i), S_IWUSR|S_IREAD)
    f = list(os.walk(login.user))[0][2]
    for i in f:
        os.chmod(os.path.join(login.user, i), S_IWUSR|S_IREAD)
    root.protocol("WM_DELETE_WINDOW", make_readonly)
    root.mainloop()