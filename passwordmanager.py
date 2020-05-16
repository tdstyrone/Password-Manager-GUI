from tkinter import *
from tkinter import messagebox
import tkinter.messagebox

objects = []
win = Tk()
win.withdraw()
win.title("Password Manager")  # Create Window Title
access = "tyronesmith"  # Password Manager Access Key

class PopUpWindow:  # Create Pop-Up Window

    loop = False
    attempts = 0

    def __init__(self, master):
        top = self.top = Toplevel(master)
        top.title("Password Manager - Input Password")  # Pop-up Window title
        top.geometry(f'{350}x{100}')  # Pop-up Window Size
        top.resizable(False, False)  # Makes window not resizeable
        self.label_field = Label(top, text=" PASSWORD: ", font=('Courier', 15), justify=CENTER)
        self.label_field.pack()
        self.entry_field = Entry(top, show='*', width=35)
        self.entry_field.pack(pady=5)
        self.submit_button = Button(top, text='Submit', command=self.cleanup, font=('Courier', 15), fg="blue")
        self.submit_button.pack()

    def cleanup(self):
        value = self.entry_field.get()
        if value == access:
            self.loop = True
            self.top.destroy()
            win.deiconify()
        else:
            self.attempts += 1
            if self.attempts == 5:
                win.quit()
            self.entry_field.delete(0, 'end')
            messagebox.showerror('Incorrect Password',
                                 'Incorrect password, attempts remaining: ' + str(5 - self.attempts))


class AddEntity:

    def __init__(self, master, account, pwd, email_address):
        self.password = pwd
        self.name = account
        self.email = email_address
        self.window = master

    def write(self):
        file = open('passwords.txt', "a")

        encrypted_n = ""
        encrypted_e = ""
        encrypted_p = ""
        for letter in self.name:
            if letter == ' ':
                encrypted_n += ' '
            else:
                encrypted_n += chr(ord(letter) + 5)

        for letter in self.email:
            if letter == ' ':
                encrypted_e += ' '
            else:
                encrypted_e += chr(ord(letter) + 5)

        for letter in self.password:
            if letter == ' ':
                encrypted_p += ' '
            else:
                encrypted_p += chr(ord(letter) + 5)

        file.write(encrypted_n + ',' + encrypted_e + ',' + encrypted_p + ', \n')
        file.close()


class DisplayEntity:

    def __init__(self, master, account, email_address, pwd, i):
        self.password = pwd
        self.name = account
        self.email = email_address
        self.window = master
        self.i = i

        dencrypted_n = ""
        dencrypted_e = ""
        dencrypted_p = ""
        for letter in self.name:
            if letter == ' ':
                dencrypted_n += ' '
            else:
                dencrypted_n += chr(ord(letter) - 5)

        for letter in self.email:
            if letter == ' ':
                dencrypted_e += ' '
            else:
                dencrypted_e += chr(ord(letter) - 5)

        for letter in self.password:
            if letter == ' ':
                dencrypted_p += ' '
            else:
                dencrypted_p += chr(ord(letter) - 5)

        self.label_name = Label(self.window, text=dencrypted_n, font=('Courier', 14))
        self.label_email = Label(self.window, text=dencrypted_e, font=('Courier', 14))
        self.label_pass = Label(self.window, text=dencrypted_p, font=('Courier', 14))
        self.deleteButton = Button(self.window, text='X', fg='red', command=self.delete)

    def display(self):
        self.label_name.grid(row=6 + self.i, sticky=W)
        self.label_email.grid(row=6 + self.i, column=1)
        self.label_pass.grid(row=6 + self.i, column=2, sticky=E)
        self.deleteButton.grid(row=6 + self.i, column=3, sticky=E)

    def delete(self):
        answer = tkinter.messagebox.askquestion('Delete', 'Are you sure you want to delete this entry?')

        if answer == 'yes':
            for i in objects:
                i.destroy()

            file = open('passwords.txt', 'r')
            lines = file.readlines()
            file.close()

            file = open('passwords.txt', "w")
            count = 0

            for line in lines:
                if count != self.i:
                    file.write(line)
                    count += 1

            file.close()
            readfile()

    def destroy(self):
        self.label_name.destroy()
        self.label_email.destroy()
        self.label_pass.destroy()
        self.deleteButton.destroy()


# ******* FUNCTIONS *********


def on_submit():
    email_address = email.get()
    pwd = password.get()
    account = name.get()
    elements = AddEntity(win, account, pwd, email_address)
    elements.write()
    name.delete(0, 'end')
    email.delete(0, 'end')
    password.delete(0, 'end')
    messagebox.showinfo('Account Added', 'Successfully Added, \n' + 'Account Name: ' + account + '\nEmail: ' + email_address + '\nPassword: ' + pwd)
    readfile()


def clearfile():
    file = open('passwords.txt', "w")
    file.close()


def readfile():
    file = open('passwords.txt', 'r')
    count = 0

    for line in file:
        entity_list = line.split(',')
        elements = DisplayEntity(win, entity_list[0], entity_list[1], entity_list[2], count)
        objects.append(elements)
        elements.display()
        count += 1
    file.close()


password_interface = PopUpWindow(win)


entity_label = Label(win, text='Add Account', font=('Courier', 18))
name_label = Label(win, text='Account Name: ', font=('Courier', 14))
email_label = Label(win, text='Email/Username: ', font=('Courier', 14))
pass_label = Label(win, text='Password: ', font=('Courier', 14))
name = Entry(win, font=('Courier', 14))
email = Entry(win, font=('Courier', 14))
password = Entry(win, show='*', font=('Courier', 14))
submit = Button(win, text='Add Account', command=on_submit, font=('Courier', 14), fg="blue")

entity_label.grid(columnspan=3, row=0)
name_label.grid(row=1, sticky=E, padx=3)
email_label.grid(row=2, sticky=E, padx=3)
pass_label.grid(row=3, sticky=E, padx=3)

name.grid(columnspan=3, row=1, column=1, padx=2, pady=2, sticky=W)
email.grid(columnspan=3, row=2, column=1, padx=2, pady=2, sticky=W)
password.grid(columnspan=3, row=3, column=1, padx=2, pady=2, sticky=W)

submit.grid(columnspan=3, pady=4)

name_label2 = Label(win, text='Account Name: ', font=('Courier', 14))
email_label2 = Label(win, text='Email/Username: ', font=('Courier', 14))
pass_label2 = Label(win, text='Password: ', font=('Courier', 14))

name_label2.grid(row=5)
email_label2.grid(row=5, column=1)
pass_label2.grid(row=5, column=2)

readfile()
win.mainloop()
