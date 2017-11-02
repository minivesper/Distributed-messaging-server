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
