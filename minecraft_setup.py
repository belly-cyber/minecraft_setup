import re
import os
import subprocess
import requests
import socket


download_page      = 'https://www.minecraft.net/en-us/download/server'
server_version1171 = "https://launcher.mojang.com/v1/objects/a16d67e5807f57fc4e550299cf20226194497dc2/server.jar"
startup = 'sudo java -Xmx1024M -Xms1024M -jar /home/minecraft/minecraft_server.jar nogui'

HEADERS = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-Encoding": "gzip, deflate, br",
        "referer": "https://www.minecraft.net/en-us/download/server",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        "Upgrade-Insecure-Requests": "1",
        "content-type": "text/html;charset=utf-8",
        'Connection': 'keep-alive',
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
          }
command_list=['apt update','sudo add-apt-repository ppa:linuxuprising/java',
              'apt install default-jdk','apt install openjdk-16-jdk',
              'apt install screen','mkdir /home/minecraft'
             ]

session  = requests.Session()
session.headers = HEADERS

for x in command_list:null=subprocess.call(x.split())

os.chdir('/home/minecraft')

print('downloading server file')
try:
    minecraft_page = session.get(download_page)
    latest_server  = re.findall('https.*?\.jar',minecraft_page.text)[0]
    server_jar     = session.get(latest_server).content
    print('download latest version complete')
except:
    latest_server = server_version1171
    server_jar    = session.get(latest_server).content
    print('download version 1.17.1 complete')

with open('/home/minecraft/minecraft_server.jar','wb') as f: 
    f.write(server_jar)
    
print('download complete')

subprocess.call(startup.split())

with open('/home/minecraft/eula.txt','r') as f:eula=f.read()
new_eula='\n'.join(['eula=true' if 'eula=false' in x else x for x in eula.split('\n')])

with open('/home/minecraft/eula.txt','w') as f:f.write(new_eula)
#subprocess.call(startup.split())

print('\n'*os.get_terminal_size().lines)

public_ip    = requests.get('https://api.ipify.org?format=json').json()['ip']
minecraft_ip = socket.gethostbyname(socket.gethostname())
message=f'''now configure your router for port-forwarding/NAT
this machine\'s IP: {minecraft_ip}
port: 25565
here is your public ip to share with your friends: {public_ip}'''
print(message)
print(f"final step: run '{startup}'")




