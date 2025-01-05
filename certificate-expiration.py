#!/bin/env python3

# Certificate-expiration.py - python script to check any domain for its certificate expiration.
#
# Based on the check_ssl_cert.py script of Sharuzzaman Ahmat Raslan:
# https://gist.github.com/sharuzzaman/8827ef0d9fff89e4e937579b2b01653f
# check_ssl_cert.py - python get info for expired SSL cert
# Copyright 2022 Sharuzzaman Ahmat Raslan <sharuzzaman@gmail.com>

from cryptography import x509
from datetime import date
from datetime import datetime
import socket
import ssl
import sys

#Check arguments. If not provided - exit with an error code 255
if len(sys.argv) < 2:
    print("255")
    quit()
hostname = sys.argv[1].strip()
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

try:
    sock = socket.create_connection((hostname, 443),5)
    with sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            data = ssock.getpeercert(True)
            pem_data = ssl.DER_cert_to_PEM_cert(data)
            cert_data = x509.load_pem_x509_certificate(str.encode(pem_data))
            #Gettings certificate's NotAfter date and parsing it.
            validity = cert_data.not_valid_after
            certYear = int(validity.strftime("%Y"))
            certMonth = int(validity.strftime("%m"))
            certDay = int(validity.strftime("%d"))
            #Gettings current date and parsing it.
            now = date.today()
            nowYear = int(now.strftime("%Y"))
            nowMonth = int(now.strftime("%m"))
            nowDay = int(now.strftime("%d"))
            if certYear >= nowYear:
                #check month.If cert's month is less or current - go on. Else - everything is ok, we have a time.
                if certMonth <= nowMonth:
                    if (certDay >= nowDay+3):
                        #OK result. We have at least 3 days before the expiration
                        print("0")
                        quit()
                    if (certDay >= nowDay+2) or (certDay >= nowDay+1):
                        #OK but near alarm result. We have at least 1 or 2 days before the expiration
                        print("1")
                        quit()
                    if (certDay <= nowDay):
                        #Alarm. Expired
                        print("2")
                        quit()
                else:
                    #OK result. We have at least 1 month before the expiration
                    print("0")
                    quit()
            else:
                #Alarm.Expired
                print("2")
                quit()
except Exception as msg:
    print("255")
    #Uncomment the string below if need to see exactly the error message
    #print(f"{msg}")
