import requests
import random
import string
import time
import re
from bs4 import BeautifulSoup


def getActiveDomains():
    domains = requests.get("https://www.1secmail.com/api/v1/?action=getDomainList")
    if (domains.status_code == 200):
        domains = domains.json()
    return domains


def createMailbox(domains):
    login = ""
    while len(login) < 16:
        digit = random.randint(0, 9)
        letter = random.choice(string.ascii_lowercase)
        choice = random.randint(1, 2)
        if choice == 1:
            login = login + str(digit)
        elif choice == 2:
            login = login + letter

    domain = domains[random.randint(0, len(domains))]
    print(f"\nYour temporary email address is: {login}@{domain}\n")
    return(login, domain)


def createNewMailbox():
    domains = getActiveDomains()
    address = createMailbox(domains)
    getMail(address[0], address[1])


def getMail(login, domain):
    while True:
        print(f"\nFetching mail for {login}@{domain} ...")
        try:
            mailbox = requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}")
        except:
            print("API error, trying again in 20 seconds...")
            time.sleep(20)

        if (mailbox.status_code == 200):
            mailbox = mailbox.json()
            try:
                if (len(str(mailbox[0]['id'])) > 1):
                    emailCount = len(mailbox)
                    print(f"\nThere is {emailCount} email in your inbox") if emailCount == 1 else print(
                        f"\nThere is {emailCount} emails in your inbox")
                    for email in mailbox:
                        message = requests.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={email['id']}")
                        if (message.status_code == 200):
                            message = message.json()
                            message = message['body']
                            message = BeautifulSoup(
                                message, 'html.parser').get_text(separator="\n")
                        else:
                            message = "Error"
                        print(f"\nFrom: {email['from']}")
                        print(f"Subject: {email['subject']}")
                        print(f"Time: {email['date']}")
                        print(f"Message: \n\n{message}\n----------")
                    print("\nRefreshing in 30 seconds...")
                else:
                    print("Mailbox empty, auto refreshing in 30 seconds...")
            except:
                print("Mailbox empty, auto refreshing in 30 seconds...")
            time.sleep(30)


def readExistingMailbox():
    print("\nWarning: The mailboxes are temporary, emails are deleted periodically\n")
    address = input("Enter the email address: ")
    domains = getActiveDomains()
    r = r'[^@]+@[^@]+\.[^@]+'
    if (re.fullmatch(r, address)):
        address = address.split("@")
        for domain in domains:
            if (address[1] == domain):
                getMail(address[0], address[1])
        print("Invalid Email")
        homeMenu()
    else:
        print("Invalid Email")
        homeMenu()


def homeMenu():
    options = {
        1: createNewMailbox,
        2: readExistingMailbox
    }

    print("\n-- tempmail --\n")
    while True:
        print("1. Create a new temporary mailbox\n2. Read existing mailbox\n")
        choice = input("What would you like to do?\n")
        try:
            options[int(choice)]()
            break
        except:
            print("\nChoose a valid number\n")


homeMenu()
