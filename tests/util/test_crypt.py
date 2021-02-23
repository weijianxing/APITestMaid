#-*- coding: utf-8 -*-
# ------ wuage.com testing team ---------
# __author__ : weijx.cpp@gmail.com
def split(word):
    return [char for char in word]

def test_crypt2():
    letter :str = u"a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z"
    let = letter.split("," ,maxsplit=26)
    # let = ["X", "Y"]
    # print(let.index('Y'))
    
    #print(let)


    cypterdata :str = "yriry gjb cnffjbeq ebggra"
    #cypterdata :str = "yriry"
    cypterwords = cypterdata.split(" ")
    for i in range(1,26):
        print("++++++++++++++++++++++")
        for word in cypterwords:
            #print(word)
            letters = split(word)
            plain_w = ""
            for alf in letters:
                cpyterindex = let.index(alf)
                p_index = (cpyterindex + i) % 26
                plain_w = plain_w +  let[p_index]
            print(plain_w)


if __name__ == '__main__':
    letter :str = u"a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z"
    let = letter.split("," ,maxsplit=26)
    print(let[2:])
    # print(let.index('c'))
    # test_crypt2()