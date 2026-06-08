from rich.console import Console
from bs4 import BeautifulSoup as bs
import requests,sys,socket,queue

console = Console()

class CIAI():
    def __init__(self,host:str):
        self.__host=host
        self.__logo = """
 ██████╗██╗ █████╗ ██╗    ██████╗     ██████╗ 
██╔════╝██║██╔══██╗██║    ╚════██╗   ██╔═████╗
██║     ██║███████║██║     █████╔╝   ██║██╔██║
██║     ██║██╔══██║██║    ██╔═══╝    ████╔╝██║
╚██████╗██║██║  ██║██║    ███████╗██╗╚██████╔╝
 ╚═════╝╚═╝╚═╝  ╚═╝╚═╝    ╚══════╝╚═╝ ╚═════╝ 
 by: Fábio Adler de Luna Gomes GitHub: https://github.com/fabioadler
        """
        self.__urls=['https://www.whois.com/search.php?query=','https://ipapi.com/ip_api.php?ip=','https://tools.keycdn.com/geo?host=']
        self.__headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26','content-type':'application/x-www-form-urlencoded'}
        self.__whois__()
        self.__ipapi__()
        self.resultado_final = f"{self.__logo}\n\n{self.__whois__result}\n\n{self.__ipapi__result}\n\n  Maps: https://www.google.com/maps/@{self.__latitude},{self.__longitude},13.00z\n\n"
        print(self.resultado_final)

    def __whois__(self):
        pag = bs(requests.get(url=f"{self.__urls[0]}{self.__host}",headers=self.__headers).text,'html.parser')
        self.__whois__result=""
        conteudo = pag.find_all('div',{'class':'df-row'})
        for con in conteudo:
            self.__whois__result += f"{con.text}\n"
        conteudo2 = pag.find_all('pre',{'class':'df-raw'})
        for con in conteudo2:
            self.__whois__result += f"{con.text}\n"

    def __ipapi__(self):
        pag = requests.get(url=f"{self.__urls[1]}{self.__host}").json()
        self.__ipapi__result=""
        for key in pag.keys():
            if(key != 'location'):
                if(key == 'ip'):
                    self.__ip=pag[key]
                    self.__ipapi__result += f"{key}: {pag[key]}\n"
                elif(key == 'latitude'):
                    self.__latitude=pag[key]
                    self.__ipapi__result += f"{key}: {pag[key]}\n"
                elif(key == 'longitude'):
                    self.__longitude=pag[key]
                    self.__ipapi__result += f"{key}: {pag[key]}\n"
                else:
                    self.__ipapi__result += f"{key}: {pag[key]}\n"
            else:
                self.__ipapi__result += f"{key}:\n"
                for local in pag[key].keys():
                    self.__ipapi__result += f"   {local}: {pag[key][local]}\n"

host = str(input("Digite o host: "))
ciai = CIAI(host=host)