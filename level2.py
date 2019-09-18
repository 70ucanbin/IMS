"""任意の数字が与えられた時、その数字を1と2の数字から加算できるユニークのパターン数を計算で出してください。
例えば：
        n=1: {1}                                                                            return:1
        n=2: {1,1} {2}                                                                      return:2
        n=3: {1,1,1} {1,2} {2,1}                                                            return:3
        n=4: {1,1,1,1} {1,1,2} {1,2,1} {2,1,1} {2,2}                                        return:5
        n=5: {1,1,1,1,1} {1,1,1,2} {1,1,2,1} {1,2,1,1} {2,1,2,1} {1,2,2} {2,2,1} {2,1,2}    return:8
        n=.....                                                                             return:....

求めるのはパターンの数です。
"""

def merge(array):                                   # line1
    mid = len(array)                                # line2
    if mid > 1:                                     # line3
        left = merge(array[:(mid/2)])               # line4
        right = merge(array[(mid/2):])              # line5
        array = []                                  # line6
        while len(left) != 0 and len(right) != 0:   # line7
            if left[0] < right[0]:                  # line8
                array.append(left.pop(0))           # line9
            else:                                   # line10
                array.append(right.pop(0))          # line11
        if len(left) != 0:                          # line12
            array.extend(left)                      # line13
        elif len(right) != 0:                       # line14
            array.extend(right)                     # line15
    return array                                    # line16

if __name__ == '__main__':
        array = [6,3,5,1,8,2,4,7]
        merge([6,3,5,1,8,2,4,7])