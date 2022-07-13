from io import BytesIO
from github import Github
import requests
import os
from time import sleep
from tkinter import ttk, messagebox
import tkinter as tk
from urllib.request import urlopen
from PIL import ImageTk, Image
from threading import *


directorylog = 'IshaReforged_directorylog.txt'

if __name__ == '__main__':
    if not os.path.exists(os.path.join(os.path.expanduser('~'), 'Vice_UpdFiles')):
        os.makedirs(os.path.join(os.path.expanduser('~'), 'Vice_UpdFiles'))

    if not os.path.exists(os.path.join(os.path.expanduser('~'), 'Vice_UpdFiles', 'vicelogo.ico')):
        icourl = "https://raw.githubusercontent.com/ViceRabbit/vicerabbit.github.io/main/fm-webtextorimage/vicelogo.ico"
        responseico = requests.get(icourl)
        open(os.path.join(os.path.expanduser('~'), 'Vice_UpdFiles', 'vicelogo.ico'), 'wb').write(responseico.content)

    def disablebutton(btn):
        btn['state'] = 'disabled'
        btn['background'] = '#374237'
        btn['relief'] = 'flat'

    def undisable(btn):
        btn['state'] = 'normal'
        btn['background'] = 'green'
        btn['relief'] = 'raised'


    root = tk.Tk()
    root.geometry("700x350")
    root.resizable(False,False)
    root.title("Vice's Modpack Manager (v1.0)")
    root['background'] = '#1E1E1E'
    root.iconbitmap(os.path.join(os.path.expanduser('~'), 'Vice_UpdFiles', 'vicelogo.ico'))

    versURL = "https://raw.githubusercontent.com/ViceRabbit/vicerabbit.github.io/main/fm-webtextorimage/modpack-server-check.md"
    openu = requests.get(versURL)
    version = openu.text


    URL = "https://raw.githubusercontent.com/ViceRabbit/vicerabbit.github.io/main/fm-webtextorimage/ishareforgedforapp.jpg"
    u = urlopen(URL)
    raw_data = u.read()
    img = Image.open(BytesIO(raw_data))
    iimage = ImageTk.PhotoImage(img.resize((530, 158)))


    isha_reforgedlg = tk.Label(root, image=iimage, borderwidth=0, highlightthickness=0)
    isha_reforgedlg.place(relx=0.22, rely=0.1)


    frame = tk.LabelFrame(root, text="Pack Utilities:", padx=10, pady=40, foreground='white', background='#1E1E1E')
    frame.pack(side=tk.LEFT, padx=10, pady=10)

    firstbutton = tk.Button(frame, text=" Install Modpack ", foreground='white', background='green')
    firstbutton.pack(pady=20)


    secondbutton = tk.Button(frame,text="Update Modpack", foreground='white', background='green')
    secondbutton.pack()


    thirdbutton = tk.Button(frame, text=" Open Directory ", foreground='white', background='green')
    thirdbutton.pack(pady=20)


    directorylabel = tk.Label(root, text="Linked Directory:", foreground='white', background='#1E1E1E')
    directorylabel.place(relx=0.22, rely=0.7)

    versionlabel = tk.Label(root, text="Modpack Version (Server): " + version, foreground='white', background='#1E1E1E')
    versionlabel.place(relx=0.22, rely=0.6)

    def opendirectory():
        thedirectory = open(os.path.join(os.path.expanduser('~/Vice_UpdFiles'), directorylog), 'r')
        os.system('explorer.exe ' + thedirectory.read())
        thedirectory.close()

    thirdbutton['command'] = opendirectory

    def releaseandlock():
        undisable(firstbutton)
        undisable(secondbutton)
        undisable(thirdbutton)
        supposeddirect = open(os.path.join(os.path.expanduser('~/Vice_UpdFiles'), directorylog), 'r')
        try:
            filesearch = [file for file in os.listdir(os.path.join(supposeddirect.read(), 'mods'))]
            supposeddirect.close()
            if len(filesearch) == 0:
                disablebutton(secondbutton)
                disablebutton(thirdbutton)
            else:
                disablebutton(firstbutton)
        except FileNotFoundError:
            disablebutton(secondbutton)
            disablebutton(thirdbutton)



    def getuserdirectory():

        id_window = tk.Toplevel(root)
        id_window.title("Verify your directory!")
        id_window.geometry("500x200")
        id_window['background'] = '#1E1E1E'
        id_window.resizable(False, False)

        directoryinfo = tk.Label(id_window, text="Input the path/directory of your Minecraft/TLauncher instance!",
                                 foreground='white', background='#1E1E1E')
        directoryinfo.place(relx=0.15, rely=0.15)
        directoryq1 = tk.Label(id_window, text = "Select your launcher type! (Ask Vice if not seen in list) - ",
                                  foreground='white', background='#1E1E1E')
        directoryq1.place(relx=0.2, rely=0.30)

        q1choices = ["aumi uwu", "TLauncher", "Curseforge"]
        directorychoiceval = tk.StringVar(id_window)
        directoryq1choice = ttk.OptionMenu(id_window, directorychoiceval, *q1choices)
        directoryq1choice.place(relx=0.35, rely=0.53)
        directorychoiceval.set("Choose a launcher:")



        q1confirmbutton = tk.Button(id_window, text="      Confirm Launcher      ", foreground='white',
                                    background='green')

        def q1trigger():
            if directorychoiceval.get() != "Choose a launcher:":
                directoryq1.place_forget()
                directoryq1choice.place_forget()
                q1confirmbutton.place_forget()
                chosenlauncher = directorychoiceval.get()
                trulychosenlauncher = False
                if chosenlauncher == "Curseforge":
                    if os.path.isdir(os.path.normpath('C:\Curseforge\Instances')):
                        semifilepath = 'C:\Curseforge\Instances'
                        trulychosenlauncher = True
                elif chosenlauncher == "TLauncher":
                    if os.path.isdir(os.path.normpath(os.path.expandvars(r'%APPDATA%\.minecraft\versions'))):
                        semifilepath = os.path.expandvars(r'%APPDATA%\.minecraft\versions')
                        trulychosenlauncher = True
                if trulychosenlauncher:
                    file_pathinstances = [file for file in os.listdir(os.path.normpath(semifilepath)) if \
                            os.path.isdir(os.path.join(semifilepath, file))]
                    instancechoicevar = tk.StringVar(id_window)
                    instancechoices = ttk.OptionMenu(id_window, instancechoicevar, "Choose an instance: ",
                                                     *file_pathinstances)
                    instancechoices.place(relx=0.35, rely=0.53)

                    instancechoiceq2 = tk.Label(id_window, text="Select your game instance from this list; if you do not "
                        "see yours, msg vice", foreground='white', background='#1E1E1E')
                    instancechoiceq2.place(relx=0.1, rely=0.30)
                    instancechoicebtn = tk.Button(id_window, text="      Confirm Instance      ", foreground='white',
                                                  background='green')
                    def instancechoicetrig():
                        if instancechoicevar.get() != "Choose an instance: ":
                            choiceinstance = instancechoicevar.get()
                            instancechoices.place_forget()
                            instancechoiceq2.place_forget()
                            instancechoicebtn.place_forget()
                            directoryinfo.place_forget()
                            fulldirpath = os.path.join(semifilepath, choiceinstance)
                            fulldirpath_sl = tk.Label(id_window, text="Succesfully set your directory path!",
                                                      foreground='#90ee90', background='#1E1E1E')
                            fulldirpath_sl.place(relx=0.3, rely=0.3)
                            fulldirpath_path = tk.Label(id_window, text="Modpack Directory: " + fulldirpath,
                                                        foreground='white', background='#1E1E1E')
                            fulldirpath_path.place(relx=0.5, rely=0.53, anchor='center')
                            pathokbutton = tk.Button(id_window, text="Save & close", foreground='white',
                                                     background='green')
                            def savedirectory():
                                if not os.path.exists(os.path.join(os.path.expanduser('~/Vice_UpdFiles'), directorylog)):
                                    directory_verifyinfo.place_forget()
                                    directory_verifybtn.place_forget()
                                    if not os.path.exists(os.path.join(os.path.expanduser('~'), 'Vice_UpdFiles')):
                                        os.makedirs(os.path.join(os.path.expanduser('~'), 'Vice_UpdFiles'))
                                    open(os.path.join(os.path.expanduser('~/Vice_UpdFiles'), directorylog),
                                         'w').write(fulldirpath)
                                    supposeddirect = open(os.path.join(os.path.expanduser('~/Vice_UpdFiles'),
                                                                       directorylog), 'r')
                                    pathlabel = tk.Label(root, text=supposeddirect.read(), foreground='#90ee90',
                                                         background='#1E1E1E')
                                    supposeddirect.close()
                                    pathlabel.place(relx=0.36, rely=0.7)
                                else:
                                    if not os.path.exists(open(os.path.join(os.path.expanduser('~/Vice_UpdFiles'),
                                        directorylog), 'r').read()):
                                        directory_verifyinfo.place_forget()
                                        directory_verifybtn.place_forget()
                                        if not os.path.exists(os.path.join(os.path.expanduser('~'), 'Vice_UpdFiles')):
                                            os.makedirs(os.path.join(os.path.expanduser('~'), 'Vice_UpdFiles'))
                                        open(os.path.join(os.path.expanduser('~/Vice_UpdFiles'), directorylog),
                                             'w').write(fulldirpath)
                                        supposeddirect = open(os.path.join(os.path.expanduser('~/Vice_UpdFiles'),
                                                                           directorylog), 'r')
                                        pathlabel = tk.Label(root, text=supposeddirect.read(), foreground='#90ee90',
                                                             background='#1E1E1E')
                                        supposeddirect.close()
                                        pathlabel.place(relx=0.36, rely=0.7)
                                    else:
                                        supposeddirect = open(os.path.join(os.path.expanduser('~/Vice_UpdFiles'),
                                                                           directorylog), 'r')
                                        labelpath['text'] = supposeddirect.read()
                                        supposeddirect.close()
                                        warninglabel = tk.Label(root, text="(Re-open application to update path!)",
                                                                foreground='white', background='#1E1E1E')
                                        warninglabel.place(relx=0.4, rely=0.8)
                                open(os.path.join(os.path.expanduser('~/Vice_UpdFiles'), directorylog), 'w').write(
                                    fulldirpath)
                                releaseandlock()
                                id_window.destroy()


                            pathokbutton['command'] = savedirectory
                            pathokbutton.place(relx=0.4, rely=0.75)

                    instancechoicebtn.place(relx=0.33, rely=0.75)
                    instancechoicebtn['command'] = instancechoicetrig
        q1confirmbutton['command'] = q1trigger
        q1confirmbutton.place(relx=0.33, rely=0.75)
        id_window.focus_set()

    if not os.path.exists(os.path.join(os.path.expanduser('~/Vice_UpdFiles'), directorylog)):
        disablebutton(firstbutton)
        disablebutton(secondbutton)
        disablebutton(thirdbutton)
        directory_verifybtn = tk.Button(root, text="  Verify Directory  ", foreground='white', background='green',
                                        command=getuserdirectory)
        directory_verifybtn.place(relx=0.368, rely=0.7)

        directory_verifyinfo = tk.Label(root, text="Verify your Modpack Directory! (Your Instance/Version Folder)",
                                        foreground='red', background='#1E1E1E')
        directory_verifyinfo.place(relx=0.22, rely=0.8)
    else:
        if not os.path.exists(open(os.path.join(os.path.expanduser('~/Vice_UpdFiles'), directorylog), 'r').read()):
            disablebutton(firstbutton)
            disablebutton(secondbutton)
            disablebutton(thirdbutton)
            directory_verifybtn = tk.Button(root, text="  Verify Directory  ", foreground='white', background='green',
                                            command=getuserdirectory)
            directory_verifybtn.place(relx=0.368, rely=0.7)

            directory_verifyinfo = tk.Label(root, text="Verify your Modpack Directory! (Your Instance/Version Folder)",
                                            foreground='red', background='#1E1E1E')
            directory_verifyinfo.place(relx=0.22, rely=0.8)
        else:
            releaseandlock()
            supposeddirect = open(os.path.join(os.path.expanduser('~/Vice_Updfiles'), directorylog), 'r')
            labelpath = tk.Label(root, text=supposeddirect.read(), foreground='#90ee90', background='#1E1E1E')
            supposeddirect.close()
            labelpath.place(relx=0.36, rely=0.7)
            changedirectbutton = tk.Button(root, text="  Change Directory  ", foreground='white', background='green',
                                           command=getuserdirectory)
            changedirectbutton.place(relx=0.22, rely=0.8)

    progresstext = tk.Label()

    def installpack():
        global install_window
        install_window = tk.Toplevel(root)
        install_window.title('Install Modpack')
        install_window.geometry("500x200")
        install_window['background'] = '#1E1E1E'
        install_window.resizable(False, False)

        install_info = tk.Label(install_window, text="Modpack installation for Minecraft: Isha Reforged -",
                                foreground='white', background='#1E1E1E')
        install_info.place(relx=0.23, rely=0.15)
        supposeddirect = open(os.path.join(os.path.expanduser('~/Vice_UpdFiles'), directorylog), 'r')
        path_info = tk.Label(install_window, text="Installation Path - " + supposeddirect.read(), foreground='yellow',
                             background='#1E1E1E')
        path_info.place(relx=0.5, rely=0.4, anchor='center')
        supposeddirect.close()
        path_info2 = tk.Label(install_window, text="Are you sure you'd like to continue with the installation?",
                              foreground='white', background='#1E1E1E')
        path_info2.place(relx=0.2, rely=0.53)
        confirminstallbutton = tk.Button(install_window, text="Confirm Installation", foreground='white',
                                         background='green')
        confirminstallbutton.place(relx=0.33, rely=0.75)

        def installationtime():
            path_info.place_forget()
            path_info2.place_forget()
            confirminstallbutton.place_forget()
            global installprogress
            installprogress = ttk.Progressbar(install_window, orient=tk.HORIZONTAL, length=250, mode='indeterminate')
            t1 = Thread(target=threadrunfile)
            t1.start()
            installprogress.place(relx=0.25, rely=0.6)
            installprogress.start(20)
            global modinfo1
            modinfo1 = tk.Label(install_window, text="Installing main-file mods for modpack. . .",
                                foreground='yellow', background='#1E1E1E')
            modinfo1.place(relx=0.5, rely=0.4, anchor='center')
            global install_phases
            install_phases = tk.Label(install_window, text="(Process can take a while! u can do other stuff while "
                                                           "this is happening)",
                                      foreground='grey',
                                      background='#1E1E1E')
            install_phases.place(relx=0.5, rely=0.85, anchor='center')

        def threadrunfile():
            import get_mods
            modinfo1.config(text="Installing Configuration/Additional Files. . .")
            installprogress.stop()
            installprogress.start(5)
            import get_configandfiles
            modinfo1.config(text='Minecraft: Isha Reforged is successfully installed!', foreground='#90ee90')
            installprogress.place_forget()
            install_phases.place_forget()
            thxily = tk.Button(install_window, text="tysm bro ily <3", foreground='white', background='green')
            thxily.place(relx=0.5, rely=0.75, anchor='center')
            def ilytoo():
                install_window.focus_set()
                messagebox.showinfo("no homo", "ily too :)")
            thxily['command'] = ilytoo
            releaseandlock()

        confirminstallbutton['command'] = installationtime
    firstbutton['command'] = installpack

    def updatepack():
        global update_window
        update_window = tk.Toplevel(root)
        update_window.title('Update Modpack')
        update_window.geometry("500x200")
        update_window['background'] = '#1E1E1E'
        update_window.resizable(False, False)

        update_info = tk.Label(update_window, text="Updating Modpack for Minecraft: Isha Reforged -",
                                foreground='white', background='#1E1E1E')
        update_info.place(relx=0.23, rely=0.15)
        supposeddirect = open(os.path.join(os.path.expanduser('~/Vice_UpdFiles'), directorylog), 'r')
        path_info = tk.Label(update_window, text="Update from Path - " + supposeddirect.read(), foreground='yellow',
                             background='#1E1E1E')
        path_info.place(relx=0.5, rely=0.4, anchor='center')
        supposeddirect.close()
        path_info2 = tk.Label(update_window, text="Are you sure you'd like to continue with the update?",
                              foreground='white', background='#1E1E1E')
        path_info2.place(relx=0.2, rely=0.53)
        confirmupdatebutton = tk.Button(update_window, text="Confirm Update", foreground='white',
                                         background='green')
        confirmupdatebutton.place(relx=0.33, rely=0.75)

        def updatetime():
            path_info.place_forget()
            path_info2.place_forget()
            confirmupdatebutton.place_forget()
            global updateprogress
            updateprogress = ttk.Progressbar(update_window, orient=tk.HORIZONTAL, length=250, mode='indeterminate')
            t1 = Thread(target=threadrunfile)
            t1.start()
            updateprogress.place(relx=0.25, rely=0.6)
            updateprogress.start(20)
            global modinfo1
            modinfo1 = tk.Label(update_window, text="Updating main-file mods for modpack. . .",
                                foreground='yellow', background='#1E1E1E')
            modinfo1.place(relx=0.5, rely=0.4, anchor='center')
            global update_phases
            update_phases = tk.Label(update_window, text="(Process can take a while! u can do other stuff while "
                                                           "this is happening)",
                                      foreground='grey',
                                      background='#1E1E1E')
            update_phases.place(relx=0.5, rely=0.85, anchor='center')

        def threadrunfile():
            import get_mods
            modinfo1.config(text="Updating Configuration/Additional Files. . .")
            updateprogress.stop()
            updateprogress.start(5)
            import get_configandfiles
            modinfo1.config(text='Minecraft: Isha Reforged is successfully updated!', foreground='#90ee90')
            updateprogress.place_forget()
            update_phases.place_forget()
            thxily = tk.Button(update_window, text="tysm bro ily <3", foreground='white', background='green')
            thxily.place(relx=0.5, rely=0.75, anchor='center')

            def ilytoo():
                update_window.focus_set()
                messagebox.showinfo("no homo", "ily too :)")

            thxily['command'] = ilytoo
            releaseandlock()

        confirmupdatebutton['command'] = updatetime
    secondbutton['command'] = updatepack
    tk.mainloop()
