def addchar( string):
    a =''
    for i in string:
        if i == "|":
            a += ''.join(["\\", i])
            print(i)
        elif i == "\\":
            a += ''.join(["\\", i])
        elif i == "?":
            a += ''.join(["\\", i])
        elif i == ",":
            a += ''.join(["\\", i])
        else:
            a += i
    return a



if __name__ == "__main__":

    print(addchar("alskdf,fsdlkjf,dk,"))
