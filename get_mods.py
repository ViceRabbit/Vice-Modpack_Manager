import os
import json
import ssl
import requests
from requests.packages import urllib3
import creds
import urllib3
from main import directorylog
from datetime import datetime
from time import sleep
finished = False

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

directorylogfile = open(os.path.join(os.path.expanduser('~/Vice_UpdFiles'), directorylog), 'r')
officialpath = directorylogfile.read()

headers = {
  'Accept': 'application/json',
  'x-api-key': creds.cfapikey,
  'User-Agent': "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/81.0.4044.141 Safari/537.36"
}

headers2 = {
  'Accept': 'application/json',
  'x-api-key': creds.cfapikey2
}

modsrawlink = "https://raw.githubusercontent.com/ViceRabbit/MCModpack-Isha-Reforged/master/modpack.json"

rrr = requests.get(modsrawlink)

open(os.path.basename(modsrawlink), "wb").write(rrr.content)

with open('modpack.json') as modpack_json:
  data = json.load(modpack_json)


if not os.path.isdir(os.path.join(officialpath, 'mods')):
  os.makedirs(os.path.join(officialpath, 'mods'))
data_mods = data['mods']

verfchecklistuser = [file for file in os.listdir(os.path.join(officialpath, 'mods'))]
verfchecklistapi = [] # - Will be transferred to set() for no duplicates
verfupdatefaultapi = []
updatefault = []


for x in data_mods:
  project_id = x['p_id']
  fileid = x['url'].split('/')[7]
  name = x['name']
  print(name)
  session = requests.Session()
  while True:
    worked = False
    try:
      cf_api = session.get('https://api.curseforge.com/v1/mods/' + project_id, headers=headers)
      worked = True
    except requests.exceptions.ConnectionError:
      print("Wowzers, your internet is so trash! At attempt to retrieve " + name + ", sleeping for 5 seconds and " \
                                                                                 "retrying. . ")
      sleep(5)
    if worked == True:
      break
  open('curseforgetemp_api.json', "wb").write(cf_api.content)
  with open('curseforgetemp_api.json') as api_json:
    if "504 Gateway Time-out" in open('curseforgetemp_api.json', 'r').read():
      print(name, "experienced a 504 gateway timeout! (While retrieving data from json!)")
      print("awe gotta slow down now, sleeping for 4 seconds!")
      sleep(4)
      print("\033[93mrepeating the session again! hope this doesnt timeout again - if you experience the next error, "
            "pls tell vice\033[0m")
      session.close()
      session = requests.Session()
      print("\033[92mSuccessfully closed and re-opened session, now tiem to do the bigboy work")
      open('curseforgetemp_api.json', "wb").write(cf_api.content)
    print("Aboutt'a json load!")
    api_data = json.load(open('curseforgetemp_api.json', "r"))
  api_dataindex = api_data['data']['latestFilesIndexes']
  api_name = api_data['data']['name']

  for y in api_dataindex:
    if fileid == str(y['fileId']):
      verfupdatefaultapi.append(api_name)
      verfchecklistapi.append(y['filename'])
      if y['filename'] not in verfchecklistuser:
        modprogresscall = y['filename']
        proper_urlsect = fileid[:4] + "/" + fileid[4:] + "/"
        session = requests.Session()
        installationurl = "https://edge.forgecdn.net/files/" + proper_urlsect + y['filename']
        print(name, 'prepared for install')
        while True:
          worked1 = False
          try:
            try:
              installmentresponse = session.get(installationurl, headers=headers, verify=False)
              worked1 = True
              finished_file = os.path.join(officialpath, 'mods', os.path.basename(installationurl))
              try:
                open(finished_file, "wb").write(installmentresponse.content)
                sleep(1)
              except TypeError:
                open(finished_file, "w").write(installmentresponse.content)
                sleep(1)
              break
            except requests.exceptions.SSLError:
              print("\033[92mExperienced SSL Error! Turning 'verify' off, adding new headers, and opening a new "
                    "session!\033[0m")
              session.close()
              session = requests.Session()
              installmentresponse = session.get(installationurl, headers=headers2, verify=False)
              worked1 = True
              finished_file = os.path.join(officialpath, 'mods', os.path.basename(installationurl))
          except requests.exceptions.ConnectionError:
            print("Wowzers, your internet is so trash! At attempt to retrieve " + name + ", sleeping for 5 seconds "
                        "and retrying. . ")
            sleep(5)
          if worked1 == True:
            break
          try:
            open(finished_file, "wb").write(installmentresponse.content)
            sleep(1)
          except TypeError:
            open(finished_file, "w").write(installmentresponse.content)
            sleep(1)
          break
    else:
      updatefault.append(name)


for x in set(updatefault):
  if x not in set(verfupdatefaultapi):
      print("\033[91m" + x, "failed to install! Logged in ViceUpdFiles . . .\033[0m")
      open(os.path.join(os.path.expanduser('~'), 'Vice_UpdFiles', 'modfails.txt'), 'a').write(x + " failed to install ("
            "ERROR: ID Miss-match)! Perhaps an update is required?.. or vice fucked up - " + datetime.today().strftime(
        '%Y-%m-%d %H:%M:%S') + '\n')



for x in verfchecklistuser:
  if x not in set(verfchecklistapi):
    os.remove(os.path.join(officialpath, 'mods', x))

directorylogfile.close()
os.remove('curseforgetemp_api.json')
os.remove('modpack.json')
finished = True
print("\033[92mMod-initialization finished! (thank god) - Initalizing config files\033[0m")
print("\033[93mConfig files will not show status reports like mods, just give it a few minutes!\033[0m")
