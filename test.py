"""あおり運転の目撃者が警察にこう言いました。
    目撃者A:ナンバープレートの前2桁は同じ数字です
    目撃者B:後2桁も同じ数字ですが、前2桁の数字とは違う数字です
    目撃者C:この4桁のナンバーの平方根は自然数です
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

"""
    長さが一緒のリストが二つあります。X{} と y{}

    二つのリストと一つのターゲット値を渡した時に、
    x{} と y{}の中の値を加算した結果が　ターゲットに一番近いペアを全部出してください    

    例：X = {5,9,6,7,4}   y = {8,5,3,7,4} ターゲット：13
    
    加算で一番近いペア: {6,5}

"""