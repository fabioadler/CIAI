from bs4 import BeautifulSoup as bs
import sys, requests, regex as re

banner = ""

whois = "https://who.is/whois/"
rdap = "https://who.is/rdap/"
dns = "https://who.is/dns/"
host = ""
type_host = ""

def get_whois():
    pag_whois = bs(requests.get(f"{whois}{host}").text,"html.parser")
    conteudo_whois = pag_whois.find_all("div",{"class":"queryResponseBodyValue"})
    dominios_similares = f"Hosts similares:\n{((conteudo_whois[len(conteudo_whois)-4].text).replace("|","\n")).replace(" ","")}"
    return dominios_similares

if(len(sys.argv) >= 2 and "-h" in sys.argv):
    if("-h" in sys.argv):
        host = sys.argv[sys.argv.index("-h") + 1]
        ip_pattern = re.compile("[0-9]+[.][0-9]+[.][0-9]+[.][0-9]")
        if(len(ip_pattern.findall(host)) >= 1):
            type_host = "IP"
        else:
            type_host = "Dominio"
        
else:
    pass