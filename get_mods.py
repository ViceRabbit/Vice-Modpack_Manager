import os
import json
import ssl
import requests
import creds
from main import directorylog
from datetime import datetime
from time import sleep
finished = False

directorylogfile = open(os.path.join(os.path.expanduser('~/Vice_UpdFiles'), directorylog), 'r')
officialpath = directorylogfile.read()

headers = {
  'Accept': 'application/json',
  'x-api-key': creds.cfapikey
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
  cf_api = requests.get('https://api.curseforge.com/v1/mods/' + project_id, headers=headers)
  open('curseforgetemp_api.json', "wb").write(cf_api.content)
  with open('curseforgetemp_api.json') as api_json:
    api_data = json.load(api_json)
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
        try:
          installmentresponse = session.get(installationurl, headers=headers)
          finished_file = os.path.join(officialpath, 'mods', os.path.basename(installationurl))
          try:
            open(finished_file, "wb").write(installmentresponse.content)
            sleep(1)
          except TypeError:
            open(finished_file, "w").write(installmentresponse.content)
            sleep(1)
          break
        except ssl.SSLError:
          installmentresponse = session.get(installationurl, headers=headers2)
          finished_file = os.path.join(officialpath, 'mods', os.path.basename(installationurl))
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