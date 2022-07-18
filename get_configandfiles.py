import os
import requests
from requests.packages import urllib3
from time import sleep
from github import Github
from main import directorylog
from datetime import datetime
import ssl
import creds # - Private File
g = Github(creds.gkey)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

directorylogfile = open(os.path.join(os.path.expanduser('~/Vice_UpdFiles'), directorylog), 'r')
officialpath = directorylogfile.read()

myrepo = g.get_repo("ViceRabbit/MCModpack-Isha-Reforged")

contents = myrepo.get_contents("config")
contents2 = myrepo.get_contents("screenshots")

if not os.path.isdir(os.path.join(officialpath, "config")):
    os.makedirs(os.path.join(officialpath, "config"))
if not os.path.isdir(os.path.join(officialpath, "screenshots")):
    os.makedirs(os.path.join(officialpath, "screenshots"))

verifyusercontent1 = []
verifyusercontent2 = []
apicontent1 = []
apicontent2 = []

for root, dirs, files in os.walk(os.path.join(officialpath, "config")):
    for name in files:
        verifyusercontent1.append(os.path.normpath(os.path.join(root, name)))
for root, dirs, files in os.walk(os.path.join(officialpath, "screenshots")):
    for name in files:
        verifyusercontent2.append(os.path.normpath(os.path.join(root, name)))

def filecontent_add(cont):
    rawlink = "https://raw.githubusercontent.com/ViceRabbit/MCModpack-Isha-Reforged/master/" + cont
    passivelink = cont
    session = requests.Session()
    while True:
        worked = False
        try:
            try:
                linkcont = session.get(rawlink, headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) "
                                                                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                                                                       "Chrome/81.0.4044.141 Safari/537.36"}, verify=False)
                worked = True
            except requests.exceptions.SSLError:
                print("Experienced SSL Error! Opening a new session with new headers! (get_configandfiles.py) ")
                session.close()
                session = requests.Session()
                linkcont = session.get(rawlink, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/53"
                    "7.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}, verify=False)
                worked = True
        except requests.exceptions.ConnectionError:
            print("Wowzers, your internet is so trash! At attempt to retrieve " + name + ", sleeping for 5 seconds "
                    "and retrying. . ")
            sleep(5)
        if worked == True:
            break


    normpath = os.path.normpath(passivelink)
    directory = normpath.split(os.sep)
    directory.pop(len(directory) - 1)

    if len(directory) <= 1:
        if not os.path.exists(os.path.join(officialpath, directory[0])):
            os.makedirs(os.path.join(officialpath, directory[0]))
    else:
        if not os.path.exists(os.path.join(officialpath, *directory)):
            os.makedirs(os.path.join(officialpath, *directory))

    finishedfile = os.path.join(officialpath, *directory, os.path.basename(rawlink))
    if os.path.basename(rawlink) not in verifyusercontent1:
        if os.path.basename(rawlink) not in verifyusercontent2:
            try:
                open(finishedfile, "wb").write(linkcont.content)
            except TypeError:
                open(finishedfile, "w").write(linkcont.content)
        else:
            print("Skipped", cont, "due to the file already existing!")
    else:
        print("Skipped", cont, "due to the file already existing!")




def recursivedir(path):
    newcontent = myrepo.get_contents(path.path)
    for x in newcontent:
        if x.type == 'dir':
            recursivedir(x)
        else:
            filecontent_add(x.path)
            if "config" in x.path:
                apicontent1.append(os.path.normpath(os.path.join(officialpath, x.path)))
            elif "screenshots" in x.path:
                apicontent2.append(os.path.normpath(os.path.join(officialpath, x.path)))



for x in contents:
    if x.type == "dir":
        recursivedir(x)
    else:
        link = x.path
        filecontent_add(link)
        apicontent1.append(os.path.normpath(os.path.join(officialpath, link)))

for x in contents2:
    if x.type == "dir":
        recursivedir(x)
    else:
        link = x.path
        filecontent_add(link)
        apicontent2.append(os.path.normpath(os.path.join(officialpath, link)))

for x in verifyusercontent1:
    if x not in apicontent1:
        if x not in apicontent2:
            print("\033[93mRemoved", x, "due to no entry given! If this was a mistake, please contact Vice!\033[0m")
            os.remove(x)
for x in verifyusercontent2:
    if x not in apicontent2:
        if x not in apicontent1:
            print("\033[91mRemoved", x, "due to no entry given! If this was a mistake, please contact Vice!\033[0m")
            os.remove(x)

directorylogfile.close()
print("\033[92mConfig-initialization finished!\033[0m")
