import tkinter as tk 
import os.path 
from tkinter import ttk
import tkinter.filedialog
from cryptography.fernet import Fernet
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR

root_login=tk.Tk()
root_login.resizable(0,0)
root_login.iconbitmap("Images/login2.ico")   #r"C:\Users\Avinash Kumar\Documents\Vs code\backup\login2.ico"

#--------------------------------------------------main variables------------------------------------------------------------------

user_exp=1
password = ""
sec_question = ""
sec_answer = ""
save_location = ""
forgot_pass = 0
access = 0
reset = 0
key = b'c_uh6ikiQXQuTIQakHR-rPIys3mw-jVRH4yUOq1fpaM='


#=================================================================================================================================

# Checking if the user is new.----------------------------------------------
user = os.path.expanduser('~')
user = os.path.join(user, "Documents\Log")
try:
    os.mkdir(user)
except FileExistsError:
    pass    
settings_path = os.path.join(user, "login.txt")

try:
    with open(settings_path, "r") as f: 
        pass
except FileNotFoundError:
    user_exp =0


def reset_pass():
    global reset, password, access
    error_label.config(text="")
    password = password_entry.get().strip()
    if password=="":
        error_label.config(text="Password cannot be empty")
    else:    
        with open(settings_path, "wb") as f: #-----------------------------------------------------encrypt
            data_to_write = password+"¿"+sec_question+"¿"+sec_answer+"¿"+save_location
            data_to_write = data_to_write.encode()
            encrypt_key_type = Fernet(key)
            data_to_write = encrypt_key_type.encrypt(data_to_write)
            f.write(data_to_write)
        access =1
        root_login.destroy()
        reset =0

def login_user(*event):
    global sec_answer, sec_question, password, save_location, access, reset
    if reset == 1:
        reset_pass()
    else:    
        password= password_entry.get().strip()
        if forgot_pass ==0:
            with open(settings_path, "rb") as f:  #-----------------------------------------------------decrypted
                for i in f.readlines():
                    encrypt_key_type = Fernet(key)
                    i = encrypt_key_type.decrypt(i).decode()
                    i = i.split("¿")
                    save_location = i[3]
                    if i[0] == password:
                        access = 1
                        root_login.destroy()
                    else:
                        error_label.config(text="Incorrect Password")
        elif forgot_pass==1:
            if answer_entry.get().strip() == sec_answer:
                question_label.grid_remove()
                answer_entry.grid_remove()
                password_label.config(text="Enter new password")
                password_label.grid(row=0, column=0, sticky=tk.W, padx=5)
                password_entry.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E, padx=5, pady=5)
                show_password_check.grid(row=0, column=2, sticky=tk.W)
                show_password_label.grid(row=0, column=1, sticky=tk.E)
                reset =1
                #access =1 #-------------------------------------------------------thi smust be edited-----------------------------
                #root_login.destroy()
            else:
                error_label.config(text= "Your Answer does not match")    
        #print(access)      


def forgot_password():
    root_login.title("Reset Password")
    error_label.config(text="")
    global sec_answer, sec_question, password, save_location, access, forgot_pass
    password_label.grid_remove()
    password_entry.grid_remove()
    password_entry.delete(0, tk.END)
    show_password_check.grid_remove()
    show_password_label.grid_remove()
    forgotpassword_button.grid_remove()
    with open(settings_path, "rb") as f:     #-----------------------------------------------------decrypted
        for i in f.readlines():
            encrypt_key_type = Fernet(key)
            i = encrypt_key_type.decrypt(i).decode()
            i = i.split("¿")
            password = i[0]
            sec_question = i[1]
            sec_answer = i[2]
            save_location = i[3]
    question_label.grid(row=2, column=0, padx=5, sticky = tk.W)
    question_label.config(text="Security Question: "+sec_question)
    answer_entry.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky =tk.W+tk.E)
    forgot_pass = 1

def save_user(*event):
    global sec_answer, sec_question, password, save_location, access
    cont =1
    sec_answer = Security_answer_entry.get().strip()
    sec_question = Security_question_entry.get().strip()
    password = password_entry.get().strip()
    if sec_answer=="" or sec_question=="" or password=="" or save_location=="":
        cont=0
        error_label.config(text="Your Entries can't be Empty")

    if cont: #-----------------------------------------------------encrypted
        with open(settings_path, "wb") as f:
            data_to_write = password+"¿"+sec_question+"¿"+sec_answer+"¿"+save_location
            data_to_write = data_to_write.encode()
            encrypt_key_type = Fernet(key)
            data_to_write = encrypt_key_type.encrypt(data_to_write)
            f.write(data_to_write)
        access =1
        root_login.destroy()


def ask_directory():
    global save_location
    save_location = tk.filedialog.askdirectory()
    ask_openfolder_entry.config(state= tk.ACTIVE)
    ask_openfolder_entry.delete(0,tk.END)
    ask_openfolder_entry.insert(0,save_location)
    ask_openfolder_entry.config(state= tk.DISABLED)

def show_password(*a):
    if show_password_check_var.get():
        password_var.set(password_get.get())
    else:
        password_var.set("")    

if user_exp:
    root_login.title("Login")

    password_label=ttk.Label(root_login, text="Password")
    password_label.grid(row=0, column=0, sticky=tk.W, padx=5)

    password_get = tk.StringVar()
    password_get.trace('w', show_password)
    password_entry=ttk.Entry(root_login, show="*", width = 45, textvariable= password_get)
    password_entry.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E, padx=5, pady=5)
    password_entry.focus_set()

    forgotpassword_button=ttk.Button(root_login, text="Forgot Password", command =forgot_password)
    forgotpassword_button.grid(row=1, column=2, sticky=tk.W)

    show_password_check_var = tk.BooleanVar()
    show_password_check= ttk.Checkbutton(root_login, text ="Show Password", variable =show_password_check_var, command=show_password)
    show_password_check.grid(row=0, column=2, sticky=tk.W)

    password_var = tk.StringVar()
    show_password_label = ttk.Label(root_login, textvariable=password_var)
    show_password_label.grid(row=0, column=1, sticky=tk.E)



    question_label = ttk.Label(root_login, width=49)

    answer_entry = ttk.Entry(root_login)

    error_label = ttk.Label(root_login)
    error_label.grid(row=4, column=0, columnspan =2, sticky=tk.W+tk.E)

    enter_button=ttk.Button(root_login, text="Enter", command=login_user)
    enter_button.grid(row=4, column=2, sticky=tk.W+tk.E)

    root_login.bind('<Return>', login_user)



else:
    root_login.title("Register")

    password_label=ttk.Label(root_login, text="Enter Password")
    password_label.grid(row=0, column=0, sticky=tk.W, padx=5)

    password_get = tk.StringVar()
    password_get.trace('w', show_password)
    password_entry=ttk.Entry(root_login, show="*", width = 45, textvariable= password_get)
    password_entry.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E, padx=5, pady=5)
    password_entry.focus_set()

    show_password_check_var = tk.BooleanVar()
    show_password_check= ttk.Checkbutton(root_login, text ="Show Password", variable =show_password_check_var, command=show_password)
    show_password_check.grid(row=0, column=2, sticky=tk.W)

    password_var = tk.StringVar()
    show_password_label = ttk.Label(root_login, textvariable=password_var)
    show_password_label.grid(row=0, column=1, sticky=tk.E)


    ask_openfolder_label=ttk.Label(root_login, text="Save location")
    ask_openfolder_label.grid(row=2, column=0, sticky=tk.W, padx=5)

    ask_openfolder_entry=ttk.Entry(root_login, state=tk.DISABLED)
    ask_openfolder_entry.grid(row=3, column=0, columnspan=2, sticky=tk.W+tk.E, padx=5, pady=5)

    openfolder_button=ttk.Button(root_login, text="Open Folder", command=ask_directory)
    openfolder_button.grid(row=3, column=2, sticky=tk.E)

    Security_question_label=ttk.Label(root_login, text="Security Question")
    Security_question_label.grid(row=4, column=0, sticky=tk.W, padx=5)

    Security_question_entry=ttk.Entry(root_login)
    Security_question_entry.grid(row=5, column=0, columnspan=2, sticky=tk.W+tk.E, padx=5, pady=5)

    Security_answer_label=ttk.Label(root_login, text="Answer")
    Security_answer_label.grid(row=6, column=0, sticky=tk.W, padx=5)

    Security_answer_entry=ttk.Entry(root_login)
    Security_answer_entry.grid(row=7, column=0, columnspan=2, sticky=tk.W+tk.E, padx=5, pady=5)

    error_label = ttk.Label(root_login)
    error_label.grid(row=8, column=0, columnspan =2, sticky=tk.W+tk.E)

    signup_button=ttk.Button(root_login, text="Register User", command=save_user)
    signup_button.grid(row=8, column=2, sticky=tk.E)

    root_login.bind('<Return>', save_user)

f = list(os.walk(user))[0][2]
for i in f:
    os.chmod(os.path.join(user, i), S_IWUSR|S_IREAD)

root_login.mainloop()