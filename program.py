n=7
p=97
m=8
B=3

def keygen():
    A=np.random.randint(0,p,(m,n))
    s=np.random.randint(0,p,(n,1))
    e=np.random.rand(m,1)*B
    b=As+e
    return s,(A,b)

def encry(pk,x):
    r=np.random.randint(0,1,(m,1))
    return r.T*A, r.T*b+97*x/2

def decry(sk,ct):
    cf,cs=ct
    x=cs-cf*sk
    if x<97/4:
        return 0
    else:
        return 1
