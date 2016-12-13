#flaten json data ex:   d ={'a':1,'c':{'g':7,'d':{'e':5,'f':6}},'b':10}

d = {'a':1,'c':{'g':7,'d':{'e':5,'f':6}},'b':10}

if type(d) is dict:
    for k,v in d.iteritems():
        if type(v) is dict:
            for i,j in v.iteritems():
                print k,'.',i,':',j
                if type(j) is dict:
                    for l,m in j.iteritems():
                        print k,'.',i,'.',l,':',m
        else:
            print k,':',v
