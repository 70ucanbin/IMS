"""あおり運転の目撃者が警察にこう言いました。
    目撃者A:ナンバープレートの前2桁は同じ数字です
    目撃者B:ナンバープレートの後2桁は同じ数字です
    目撃者C:前2桁は後2桁の数字とは違う数字で、この4桁のナンバーの平方根は自然数です
    以上の情報から犯人のナンバープレートを特定してください
"""

def test():
    for i in range(1,10):
        #前2文字
        AA = (i*1000+i*100)
        for j in range(1,10):
            #後ろ2文字
            BB = (j*10+j)
            if i == j:
                pass
            else:
                AABB = AA+BB
                for k in range(31,AABB):
                    if k*k == AABB:
                        print(AABB)
                        return AABB
                    elif k*k > AABB:
                        break

if __name__ == '__main__':
    test()