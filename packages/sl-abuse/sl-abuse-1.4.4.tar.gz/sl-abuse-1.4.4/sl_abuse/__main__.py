from twilio.rest import Client
import argparse
import sys
import os
import time
import urllib

os.system('clear')

print("")
print("\033[0;36m "" ")
t = input("Enter Your Questions.....")
p = "whatsapp:+94711365399"

def main():
    os.system("clear")
    account_sid = "ACccc5b0a8ad0202a78012e010bb926907"
    auth_token = "1feaef63b07744bbf6715ee212beb335"
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         from_='whatsapp:+14155238886',
                         body= t,
                         to=p
                 )

    print("your requests send sucessfully")
    os.system('figlet END  PROGRAM')

if __name__ == "__main__":
    main()
