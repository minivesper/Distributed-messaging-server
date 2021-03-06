import re
import getpass

class inputHandle:
    def __init__(self):
        return

    def deleteHandle(self, messages):
        if(len(messages) != 0):
            message_int = 0
            while 1 > message_int or len(messages) < message_int:
                try:
                    message_int = int(input("delete which message number?: "))
                except ValueError:
                    print("please enter a number between 1 and %d"%(len(messages)))
            return message_int
        else:
            print("no messages to delete")
            return 0

    def sendHandle(self):
        sendTo = input("who send to: ")
        msgtxt = input("what send: ")
        return sendTo,msgtxt

    def updateHandle(self):
        userupdt = input("which user do you want to update? ")
        permname = input("what permission do you want to change? ")
        while (permname not in("LOGN", "SMSG", "RMSG", "CMSG", "UPDT", "CACM","DMSG")):
            print("Need to input LOGN, RMSG, CMSG, UPDT, CACM, or DMSG")
            permname = input("what permission do you want to change? ")
        permbool = input("Input change: ")
        while (permbool not in("0","1")):
            print("Need to input 0 or 1")
            permbool = input("Input change: ")
        x = [userupdt, permname, permbool]
        return x

    def getCredentials(self):
        print("please enter a username with only letters and numbers")
        user = input("Username: ")
        while (re.search("[a-z|0-9]", user)) is None:
            print("please enter a username with only letters and numbers")
            user = input("Username: ")
            while (len(user))>15:
                print("please enter a username with 15 characters")
                user = input("Username: ")
        print("Please create a password")
        pwd = getpass.getpass("Password for " + user + ":")
        # while(len(pwd))<8:
        #     print("Password needs to be a minimum of 8 characters")
        #     pwd = getpass.getpass("Password for " + user + ":")
        # while(len(pwd))>15:
        #     print("Password needs to be a max of 15 characters")
        #     pwd = getpass.getpass("Password for " + user + ":")
        # while(re.search("[a-z]", pwd)) is None:
        #     print("Password needs to contain 1 lowercase value")
        #     pwd = getpass.getpass("Password for " + user + ":")
        # while(re.search("[A-Z]", pwd)) is None:
        #     print("Password needs to contain 1 uppercase value")
        #     pwd = getpass.getpass("Password for " + user + ":")
        # while(re.search("[0-9]", pwd)) is None:
        #     print("Password needs to contain 1 number")
        #     pwd = getpass.getpass("Password for " + user + ":")
        # while(re.search("[!@#$%^&*]", pwd)) is None:
        #     print("Password needs to contain a special character (!@#$%^&*)")
        #     pwd = getpass.getpass("Password for " + user + ":")
        permission = input("Permission code: ")
        while permission != "1" and permission != "2":
            print("Permission code needs to be 1 for member or 2 for admin access")
            permission = input("Permission code: ")
        return user, pwd, permission
