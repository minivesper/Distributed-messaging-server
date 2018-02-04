from datetime import datetime, timedelta
import time

if __name__ == "__main__":

dt = datetime.strptime(lg.getTime(), "%Y-%m-%d %H:%M:%S.%f")
    dtt = datetime.now()
    delta = dt - dtt
    d = (dt-dtt).total_seconds()
    print("d",d)
    #if delta < timedelta(seconds = 1):
    if d < 5
        if(session.loginAttempt(lg)):
            print("logged in successfully")
            ret = ("logged in successfully")
        else:
            ret = ("Not a valid login?")
        return(ret)
    else:
        ret = "Timed Out"
        return ret
