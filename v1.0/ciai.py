from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession
from rich.progress import Console
import requests,os,sys,rich,unicodedata

c = Console()

def cls():
    if('win' in sys.platform):
        os.system('cls')
    else:
        os.system('clear')

def whois(host):
    try:
        url='https://who.is/domains/search'
        h = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26',
            'content-type':'application/x-www-form-urlencoded'
        }

        pag = bs(requests.post(url,data={'searchString':host},headers=h).text,'html.parser')
        cont = (pag.find_all('pre')[0].text).split('\n')
        conteudo = ''
        for i in cont:
            if(':' in i):
                campo = i.split(':')
                campo = f'[b][red]{campo[0]}[/red][/b]:[i]{campo[1]}[/]'
            else:
                campo = i
            conteudo += f' {campo}\n'
        return conteudo
    except:
        return 'Não encontrado...'

def geo_location(host):
    url = f'https://ipapi.com/ip_api.php?ip={host}'
    pag = requests.get(url).json()
    conteudo = ''
    ip = ''
    for i in pag:
        if('ip' == i):
            ip = pag[i]
        conteudo += f' [b][red]{i}[/red][/b]: [i]{pag[i]}[/]\n'
    return [conteudo,ip]

def ip(i):
    session = HTMLSession()
    url = f'https://pt.infobyip.com/ip-{i}.html'
    r = session.get(url)
    r.html.render()
    cont = str(r.html.find('tr')[3].text).split('Localização')
    dados = (str(cont[0]).replace("(adsbygoogle = window.adsbygoogle || []).push({});",'').replace('Leaflet | © OpenStreetMap contributors','').replace('Tools','').replace('whois','').replace('sibilo','').replace('traceroute','').replace('mtr','').replace('dns','').replace('+−','').replace('\n\n','').replace('Dados Geográficos','')).split('\n')
    conteudo = ''
    for d in dados:
        conteudo += f' {d}\n'
    return conteudo

def separador(title):
    n = 80
    count = '_'*int(n/2)
    count = f'\n\n[bright_black b]{count}[/] [b i cyan]{title}[/] [bright_black b]{count}[/]\n\n'
    return count

def remove_style(t):
    return t.replace('[b]','').replace('[/b]','').replace('[red]','').replace('[/red]','').replace('[/]','').replace('[spring_green2]','').replace('[b red]','').replace('[white i]','').replace('[i]','').replace('[/i]','').replace('[bright_black b]','').replace('[b i cyan]','')

def remove_ac(t):
    normal = unicodedata.normalize('NFD',t)
    return normal.encode('ascii','ignore').decode('utf8').casefold()

banner = """
[spring_green2]
                                                                                                
                                                                                                  
         _____________    ____               __   ______
        / ____/  _/   |  /  _/              /  | / __   | 
       / /    / // /| |  / /       _   _   /_/ || | //| |  
      / /____/ // ___ |_/ /       | | | |    | || |// | | 
      \____/___/_/  |_/___/        \ V /     | ||  /__| | 
                                    \_/      |_(_)_____/   
                                                        
    [/] [b red]by:[/] [white i]https://github.com/xrlplerl[/]
                                    

"""

ajuda = banner + """
 [b red]Para usar:[/]
 [yellow1]*[/yellow1] [i spring_green4]scipt.py -h [green_yellow]'host'[/green_yellow][/]
"""

if(len(sys.argv) > 2):
    if('-h' in sys.argv):
        host = sys.argv[sys.argv.index('-h')+1]
        cls()
        with c.status('Carregando...'):
            banner += separador('Whois')
            banner += whois(host)
            banner += separador('IP Location')
            geo = geo_location(host)
            banner += geo[0]
            banner += separador('INFO IP')
            banner += ip(geo[1])
        if('-s' in sys.argv):
            aq = open(f'{host}.txt','w')
            aq.write(remove_ac(remove_style(banner)))
            aq.close()
        else:
            pass
    elif('--help' in sys.argv):
        cls()
        rich.print(ajuda)
        exit()
    else:
        pass
    cls()
    rich.print(banner)
else:
    cls()
    rich.print(ajuda)
    exit()