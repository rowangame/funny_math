
"""
幻方（Magic Square）是一种将数字安排在正方形格子中，使每行、列和对角线上的数字和都相等的方法。
幻方包括：奇数幻方、单偶数幻方和双偶数幻方
单偶数幻方（即4n+2式）：幻方阶数n为不能被4整除的偶数，比如6、10、14
双偶数幻方（即4n式）：幻方行列数n能被4整除的幻方，比如4、8、12
"""

import numpy as np

def oddMagic(rank: int):
    if (rank < 3) or (rank % 2) == 0:
        print("Rank数据必须大于2,且是奇数")
        return None
    if rank > 1000:
        print("rank数值太大")
        return None

    curRow = 0
    curCol = rank // 2
    magic = np.zeros((rank, rank), dtype=np.uint32)
    magic[curRow, curCol] = 1

    i = 2
    endNum = rank * rank
    while i <= endNum:
        tmpRow = curRow - 1
        tmpCol = curCol + 1
        # row,col正常数值范围
        if (0 <= tmpRow <= rank-1) and (0 <= tmpCol <= rank-1):
            # 前面有数字(row-1,col不变)
            if magic[tmpRow, tmpCol] > 0:
                curRow = curRow + 1
            else:
                curRow = tmpRow
                curCol = tmpCol
            magic[curRow, curCol] = i

        # row越界
        if (tmpRow < 0) and (0 <= tmpCol <= rank-1):
            # row-> rank - 1
            curRow = rank - 1
            curCol = tmpCol
            magic[curRow, curCol] = i

        # col越界
        if (0 <= tmpRow <= rank - 1) and (tmpCol > rank - 1):
            curRow = tmpRow
            curCol = 0
            magic[curRow, curCol] = i

        # row,col都越界
        if (tmpRow < 0) and (tmpCol > rank - 1):
            curRow = curRow + 1
            magic[curRow, curCol] = i
        i = i + 1
    return magic

# 交换方阵的对角元素
def swapHypotenuseEle(magic: np.ndarray):
    tmpRank = magic.shape[0]
    semiRank = tmpRank // 2
    semiHigh = tmpRank - 1
    centerPntY = int((semiHigh / 2 + 0) * 2)
    centerPntX = int((semiHigh / 2 + 0) * 2)
    for index in range(semiRank):
        tmpRowA = index
        tmpColA = index
        tmpRowB = centerPntY - tmpRowA
        tmpColB = centerPntX - tmpColA
        tmpValue = magic[tmpRowA, tmpColA]
        magic[tmpRowA, tmpColA] = magic[tmpRowB, tmpColB]
        magic[tmpRowB, tmpColB] = tmpValue

        tmpRowA = semiHigh - index
        tmpColA = index
        tmpRowB = centerPntY - tmpRowA
        tmpColB = centerPntX - tmpColA
        tmpValue = magic[tmpRowA, tmpColA]
        magic[tmpRowA, tmpColA] = magic[tmpRowB, tmpColB]
        magic[tmpRowB, tmpColB] = tmpValue
    return magic

def evenMagicDouble(rank: int):
    if (rank < 4) or (rank % 4 != 0):
        print("rank值必须是4的倍数,且大于4!")
        return None
    if rank > 1000:
        print("rank数值太大")
        return None

    # 对每个元素按行列依次赋值
    # refer: https://hanspub.org/journal/PaperInformation?paperID=64877
    magic = np.zeros((rank, rank), dtype=np.int32)
    for tmpRow in range(rank):
        for tmpCol in range(rank):
            magic[tmpRow, tmpCol] = rank * tmpRow + (tmpCol + 1)
    print("step1:\n", magic)

    # 分成n*n个4x4的小方阵(对角线上的元素标记为0)
    maskMagic = np.ones((rank, rank), dtype=np.int32)
    nDim = rank // 4
    nSpan = 4
    for tmpY in range(nDim):
        for tmpX in range(nDim):
            offsetY = nSpan * tmpY
            offsetX = nSpan * tmpX
            for index in range(nSpan):
                # 主对角线
                tmpRow = index + offsetY
                tmpCol = index + offsetX
                maskMagic[tmpRow, tmpCol] = 0
                # 副对象线
                tmpRow = nSpan - 1 - index + offsetY
                tmpCol = index + offsetX
                maskMagic[tmpRow, tmpCol] = 0
    #print("step2:\n", maskMagic)

    # 将n*n平方个小方阵的对角线元素按(rank*rank方阵的中点)对称交换
    # 元素交换的互补值
    compleValue = rank * rank + 1
    for tmpRow in range(rank):
        for tmpCol in range(rank):
            if maskMagic[tmpRow, tmpCol] == 0:
                magic[tmpRow, tmpCol] = compleValue - magic[tmpRow, tmpCol]
    #print("step3:\n", magic)
    return magic

def evenMagicSingle(rank: int):
    if not (rank >= 6 and ((rank % 2 == 0) and (rank % 4 != 0))):
        print("rank值必须是2的奇数倍,且大于5!")
        return None
    if rank > 1000:
        print("rank数值太大")
        return None
    # 罗伯法
    divRank = rank // 2
    oriMagic = oddMagic(divRank)
    offsetValue = divRank * divRank
    mags = []
    for index in range(4):
        tmpMagic = oriMagic + offsetValue * index
        mags.append(tmpMagic)
    print("step1:\n")
    for i in range(len(mags)):
        print(f"[{i}]:\n", mags[i])

    """
    4个小方阵按ACDB(原来的顺序是ABCD)方式合成一个大的方阵
    A B  =>  A C
    C D      D B
    """
    mH1 = np.hstack((mags[0], mags[2]))
    mH2 = np.hstack((mags[3], mags[1]))
    magic = np.vstack((mH1, mH2))
    print("step2:\n", magic)
    """
    refer1: https://zhidao.baidu.com/question/1608589126045729347.html
    A象限和D象限对换数据(相对应的位置的元素)
    在A每行取m个小格（中心格及一侧对角线格为必换格，其余m-1格只要不是另一侧对角线格即可），
    简单地说，就是说在A中间一行取包括中心格在内的m个小格，其他行左侧（或右侧）边缘取m个小格，将其与D相应方格内交换；
    B与C在任取m-1列相互交换（6阶幻方m=1，m-1=0，B与C列不用相互交换）
    """
    mGrid = divRank // 2
    # 记录对角线元素的状态值(1)
    maskMagic = np.zeros((divRank, divRank))
    for index in range(divRank):
        maskMagic[index, index] = 1
        maskMagic[divRank-1-index, index] = 1
    print("maskMagic:\n", maskMagic)

    # 每一行需要交换mGrid个元素(一侧对角线格为必换格)
    for tmpRow in range(divRank):
        # 交换对象线元素
        for tmpCol in range(divRank):
            if maskMagic[tmpRow, tmpCol] == 1:
                # 小方阵的元素行列索引值要相对应
                curRowA = tmpRow
                curColA = tmpCol
                curRowD = curRowA + divRank
                curColD = curColA
                tmpValue = magic[curRowA, curColA]
                magic[curRowA, curColA] = magic[curRowD, curColD]
                magic[curRowD, curColD] = tmpValue
                break
        # 其它非对角线上元素交换
        rmnCnt = 0
        while rmnCnt < mGrid - 1:
            for tmpCol in range(divRank):
                if maskMagic[tmpRow, tmpCol] != 1:
                    curRowA = tmpRow
                    curColA = tmpCol
                    curRowD = curRowA + divRank
                    curColD = curColA
                    tmpValue = magic[curRowA, curColA]
                    magic[curRowA, curColA] = magic[curRowD, curColD]
                    magic[curRowD, curColD] = tmpValue
                    # 标记已交换的状态
                    maskMagic[tmpRow, tmpCol] = 1
                    break
            rmnCnt += 1

    # B与C再任取m-1列相互交换
    tmpColCnt = 0
    while tmpColCnt < mGrid - 1:
        for tmpRow in range(divRank):
            curRowC = tmpRow
            curColC = tmpColCnt + divRank
            curRowB = curRowC + divRank
            curColB = curColC
            tmpValue = magic[curRowC, curColC]
            magic[curRowC, curColC] = magic[curRowB, curColB]
            magic[curRowB, curColB] = tmpValue
        tmpColCnt += 1
    print("step3:\n", magic)
    return magic


def validateMagic(magic: np.ndarray, rank: int):
    maxNum = rank * rank
    sumTotal = (1 + maxNum) * maxNum // 2
    perValue = sumTotal // rank
    print(f"sumTotal={sumTotal}, perValue={perValue}")

    # validate row
    for tmpRow in range(rank):
        tmpSum = np.sum(magic[tmpRow,0:rank])
        if tmpSum != perValue:
            print(f"error row:{tmpSum} != {perValue}", magic[tmpRow,0:rank])
            return False

    # validate col
    for tmpCol in range(rank):
        tmpSum = np.sum(magic[0:rank, tmpCol])
        if tmpSum != perValue:
            print(f"error col:{tmpSum} != {perValue}", magic[0:rank, tmpCol])
            return False

    # validate hypotenuse 1
    tmpSum = 0
    for index in range(rank):
        tmpSum += magic[index,index]
    if tmpSum != perValue:
        print(f"error hypotenuse1: col:{tmpSum} != {perValue}")
        return False

    # validate hypotenuse 2
    tmpSum = 0
    for index in range(rank):
        tmpSum += magic[rank-1-index,index]
    if tmpSum != perValue:
        print(f"error hypotenuse1: col:{tmpSum} != {perValue}")
        return False

    return True

def testOddMagic():
    rank = 15
    tmpMagic = oddMagic(rank)
    boSuccess = validateMagic(tmpMagic, rank)
    print("validate->:", boSuccess)
    print(tmpMagic)

def testEvenMagicDouble():
    rank = 16
    tmpMagic = evenMagicDouble(rank)
    boSuccess = validateMagic(tmpMagic, rank)
    print("validate->:", boSuccess)
    print(tmpMagic)

def testEvenMagicSingle():
    rank = 18
    tmpMagic = evenMagicSingle(rank)
    boSuccess = validateMagic(tmpMagic, rank)
    print("validate->:", boSuccess)
    print(tmpMagic)

if __name__ == "__main__":
    testOddMagic()
    # testEvenMagicDouble()
    # testEvenMagicSingle()