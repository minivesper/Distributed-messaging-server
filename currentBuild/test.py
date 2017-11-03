if __name__ == "__main__":

    def addchar(string):
        a =''
        for i in string:
            if i == "|":
                a +=(''.join(["\\", i]))
                print(i)
            elif i == "\\":
                a += ''.join(["\\", i])
            elif i == "?":
                a += ''.join(["\\", i])
            else:
                a += i
        return a

    def decode(parseStr):
        parselist = []
        for i in range(len(parseStr)):

            if parselist:
                # if parseStr[i] == "?":
                #     if parseStr[i-1] != "\\":
                #         parselist.append(parseStr[b+1:])
                if i == len(parseStr)-1:
                    parselist.append(parseStr[b+1:])
                else:
                    if parseStr[i] == "|":
                        if parseStr[i-1] != "\\":
                            parselist.append(parseStr[b+1:i])
                            b = i
                        elif parseStr[i-1] == "\\":
                            if parseStr[i-1] == "\\" and parseStr[i-2] == "\\":
                                parselist.append(parseStr[b+1:i])
                                b = i
            else:
                if parseStr[i] == "|":
                    if parseStr[i-1] != "\\":
                        parselist.append(parseStr[0:i])
                        b=i
        return parselist


    def removechar(parselist):
        nlist=[]
        for p in range(len(parselist)):
            for l in range(len(parselist[p])):
                # print(parselist[p][l])
                if parselist[p][l] == "\\":

                    print("1",parselist[p][l])
                    print("p",p)
                    print("l",l)
                    print("l+1", parselist[p][l+1])

                    #
                    # print("lskdf",parselist[p][l+1])
                    # # print("p",p)
                    if parselist[p][l+1] == "\\":
                        parselist[p][l].replace("\\", "")
                    if parselist[p][l+1] == "|":
                        parselist[p][l].replace("\\", "")
                    if parselist[p][l+1] == "?":
                        parselist[p][l].replace("\\", "")
            nlist.append(parselist[p])
        return(nlist)

#print(decode("CACM\|ldkfjkls\\\|p\\p\|fjkdlfjkd\|ber\?ry\?"))



    # def addchar(string):
    #       lstring = list(string)
    #       lista = []
    #       for i in range(len(lstring)):
    #           if lstring[i] == "|":
    #               print("i", i)
    #               print("1",lstring[i])
    #               lstring.insert(i,"\\")
    #               print('lstring', lstring)
    #           if lstring[i] == "\\":
    #               print("i", i)
    #               print("2",lstring[i])
    #               lstring.insert(i,"\\" )
    #               print('lstring', lstring)
    #           if lstring[i] == "?":
    #               print("i", i)
    #               print("3",lstring[i])
    #               lstring.insert(i, "\\")
    #       s = ''.join(lstring)
    #       return s

#CACM|\\i\\i\||/|ll
#print(decode(a))

    def removechar(string):
        ret = ""
        i = 0
        while i< len(string):
            if string[i] == "?":
                if string[i-1] != "\\":
                    return ret
            elif string[i] == "\\":
                i +=1
            ret += string[i]
            i +=1
        return ret

print(removechar("2?"))




#CACM|ldkfjkls\|p\p|fjkdlfjkd|be\?rry\??
