from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession
import requests,os,sys

Host = ""
Save = False
Sys_type = ""
Encode_type = "ISO-8859-1"
Ip = ''

banner = """\n\n
         ██████╗██╗ █████╗ ██╗    ██╗   ██╗██████╗     ██████╗         
        ██╔════╝██║██╔══██╗██║    ██║   ██║╚════██╗   ██╔═████╗        
        ██║     ██║███████║██║    ██║   ██║ █████╔╝   ██║██╔██║        
        ██║     ██║██╔══██║██║    ╚██╗ ██╔╝██╔═══╝    ████╔╝██║        
        ╚██████╗██║██║  ██║██║     ╚████╔╝ ███████╗██╗╚██████╔╝        
         ╚═════╝╚═╝╚═╝  ╚═╝╚═╝      ╚═══╝  ╚══════╝╚═╝ ╚═════╝     
         
    GITHUB: https://github.com/fabioadler\n\n"""

if('win' in sys.platform):
    Sys_type = "Windows"
else:
    Sys_type = "Linux"

def cls():
    if(Sys_type == "Windows"):
        os.system('cls')
    else:
        os.system('clear')

def modo_de_uso():
    print(f'{banner}\n]===> Modo de uso: py ciai.py -h [host]\n]===> Caso queira salvar um relatorio use: py ciai.py -h [host] -s')

if(len(sys.argv) >= 3):
    if('--help' in sys.argv):
        cls()
        modo_de_uso()
        exit()
    else:
        pass
    if('-h' in sys.argv):
        Host = str(sys.argv[sys.argv.index('-h') + 1])
    else:
        cls()
        modo_de_uso()
        exit()
    if('-s' in sys.argv):
        Save = True
    else:
        Save = False
else:
    cls()
    modo_de_uso()
    exit()

def Geo_location():
    global Ip
    url = f'https://ipapi.com/ip_api.php?ip={Host}'
    pag = requests.get(url).json()
    conteudo = ''
    for i in pag:
        if('ip' == i):
            Ip = pag[i]
        elif('location' in i):
            break
        else:
            conteudo += f'{i}: {pag[i]}\n'
    return conteudo

def Rota(ip):
    if(Sys_type == "Windows"):
        dados = ((str(os.popen(f"tracert -h 100 -w 1000 -4 {ip}").read().encode(Encode_type)).replace("b'","")).replace("'","")).split('\\n')
    else:
        dados = ((str(os.popen(f"traceroute -m 100 -w 1000 -4 {ip}").read().encode(Encode_type)).replace("b'","")).replace("'","")).split('\\n')
    conteudo = ''
    for dt in dados:
        if(dt != ''):
            conteudo += f"{dt}\n"
        else:
            pass
    return conteudo

def Whois():
    pag = bs(requests.get(f"https://who.is/whois/{Host}").text,'html.parser')
    conteudo = pag.find_all('div',{'class':'queryResponseContainer'})
    cont = str(conteudo[0].text).split('\n')
    cnt = ""
    for c in cont:
        if(c != ''):
            if('Registrar Info' in c):
                cnt += f"\n{c}\n\n"
            elif(('Important Dates' in c) or ('Name Servers' in c) or ('Referral URL' in c)):
                cnt += f"\n\n{c}:\n\n"
            elif('Status' in c):
                cnt += f"\n{c}:\n\n"
            elif('On' in c):
                cnt += f"{c} "
            elif(('MarkMonitor' in c) or ('Name' in c) or ('Whois Server' in c) or ('ns' in c)):
                cnt += f"{c}: "
            #elif('Registrar Data' in c):
            #    break
            else:
                cnt += f"{c}\n".replace(",","\n")
        else:
            pass
    return cnt

def IP(ip):
    session = HTMLSession()
    url = f'https://pt.infobyip.com/ip-{ip}.html'
    r = session.get(url)
    r.html.render()
    cont = str(r.html.find('tr')[3].text).split('Localização')
    dados = (str(cont[0]).replace("(adsbygoogle = window.adsbygoogle || []).push({});",'').replace('Leaflet | © OpenStreetMap contributors','').replace('Tools','').replace('whois','').replace('sibilo','').replace('traceroute','').replace('mtr','').replace('dns','').replace('+−','').replace('\n\n','').replace('Dados Geográficos','')).split('\n')
    conteudo = ''
    for d in dados:
        if(d != ''):
            if(('Domínio' in d) or ('ISP' in d) or ('ASN' in d) or ('Continente' in d) or ('País' in d) or ('Lat / Long' in d)):
                conteudo += f'{d}: '
            elif('Dados IP' in d):
                conteudo += f'\n{d}\n\n'
            elif('Ferramentas' in d):
                pass
            else:
                conteudo += f'{d}\n'
        else:
            pass
    session.close()
    cls()
    return conteudo


def main():
    cls()
    msg = f"{banner}\nSeja bem vindo a nossa ferramente de analise\nVamos começar a analise!\nAnalizando..."
    print(msg)
    conteudo = f"{banner}\n\nDados Whois:\n\n"
    conteudo += Whois()
    conteudo += f"\n\nDados Geo Loaction:\n\n"
    conteudo += Geo_location()
    conteudo += f"\n\nDados IP:\n\n"
    conteudo += IP(Ip)
    cls()
    print(msg)
    conteudo += f"\n\nRotas:\n\n"
    conteudo += Rota(Ip)
    if(Save):
        print('Salvando resultado...')
        arquivo = open(f'{Host}.txt','w',encoding="UTF-8")
        arquivo.write(conteudo)
        arquivo.close()
    else:
        pass
    cls()
    print(conteudo)

main()