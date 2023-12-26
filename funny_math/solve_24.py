"""
21,24点问题:
1.全排列组合和笛卡尔积实现
2.迭代法实现
注:当前算法并没有将问题的所有解全部列出来
  求所有解参考方案:需要对每个不同的数字进行掉换然后重新再计算(问题复杂度上升几个数量级)
"""
from itertools import permutations, product

# 记录运行的总次数
totalTimes: int = 0
# 结果集(除去重复的表达式)
expSet = set()
# 浮点数相等比较误差值
epsilon = 0.0000001

def solve_exp21(nums):
    if len(nums) != 4:
        print("Error:数字个数必须为4")
        return
    global totalTimes
    # 生成所有可能的排列和运算符组合
    for perm in permutations(nums):
        # print(perm)
        # 笛卡尔积(repeat=3?数字中间最多只有3个符号,可重复使用)
        for ops in product('+-*/', repeat=3):
            # d:digit o:ops
            fmt0 = "d" * 7
            fmt1 = "(dod)odod"
            fmt10 = "((dod)od)od"
            fmt11 = "(dod)o(dod)"
            fmt2 = "do(dod)od"
            fmt20 = "(do(dod))od"
            fmt21 = "do((dod)od)"
            fmt3 = "dodo(dod)"
            fmt30 = "(dod)o(dod)"
            fmt31 = "do(do(dod))"
            fmtlst = [fmt0, fmt1, fmt10, fmt11, fmt2, fmt20, fmt21, fmt3, fmt30, fmt31]
            for tmpFmt in fmtlst:
                totalTimes += 1
                tmpFmt = tmpFmt.replace("d","{}")
                tmpFmt = tmpFmt.replace("o","{}")
                tmpExp = tmpFmt.format(perm[0], ops[0], perm[1], ops[1], perm[2], ops[2], perm[3])
                value = eval(tmpExp)
                if abs(value - 21) < epsilon:
                    expSet.add(tmpExp)

# 将表达式内的括号运算变成一个数字符号(用于是否需要加小上括号运算)
def squeezeExp(exp: str):
    while True:
        eIdx = exp.find(")")
        sIdx = exp[0:eIdx].rfind("(")
        if eIdx == -1:
            break
        exp = exp[0:sIdx] + "x" + exp[eIdx + 1:]
    return exp

# 统计运算符数量(用于是否需要加上括号运算)
def histSymbols(exp):
    CON_SYMS = ["+", "-", "*", "/"]
    rlts = [0] * len(CON_SYMS)
    for index in range(len(CON_SYMS)):
        tmpSym = CON_SYMS[index]
        tmpCnt = 0
        for tmpC in exp:
            if tmpC == tmpSym:
                tmpCnt += 1
        rlts[index] = tmpCnt
    totalSys = 0
    for tmpCnt in rlts:
        totalSys += tmpCnt
    return rlts, totalSys

# 生成计算表达式(在支持四则运算优先级的情况下,减少冗余括号)
def getExp(exp1: str, exp2: str, opTag: str):
    if opTag == "+":
        return f"{exp1}+{exp2}"
    elif opTag == "-":
        squExpA = squeezeExp(exp1)
        squExpB = squeezeExp(exp2)
        expA = exp1
        expB = exp2
        if len(squExpB) > 1:
            # 全*/号不需要加括号
            symsHist, total = histSymbols(squExpB)
            if symsHist[2] + symsHist[3] != total:
                expB = "(" + expB + ")"
        return f"{expA}-{expB}"
    elif opTag == "*":
        squExpA = squeezeExp(exp1)
        squExpB = squeezeExp(exp2)
        expA = exp1
        expB = exp2
        if len(squExpA) > 1:
            symsHist, total = histSymbols(squExpA)
            if symsHist[2] + symsHist[3] != total:
                expA = "(" + expA + ")"
        if len(squExpB) > 1:
            symsHist, total = histSymbols(squExpB)
            if symsHist[2] + symsHist[3] != total:
                expB = "(" + expB + ")"
        return f"{expA}*{expB}"
    elif opTag == "/":
        squExpA = squeezeExp(exp1)
        squExpB = squeezeExp(exp2)
        expA = exp1
        expB = exp2
        if len(squExpA) > 1:
            symsHist, total = histSymbols(squExpA)
            if symsHist[2] + symsHist[3] != total:
                expA = "(" + expA + ")"
        if len(squExpB) > 1:
                expB = "(" + expB + ")"
        return f"{expA}/{expB}"


def solve24(dgs: list, numLen: int, exp: list):
    global totalTimes
    totalTimes += 1
    # 验证结果值
    if numLen == 1:
        boFound = abs(dgs[0] - 24) < epsilon
        if boFound:
            # 用求表达式的值函数验证结果
            real = eval(exp[0])
            print("boFound:", exp[0], dgs, f"real={real} {real==dgs[0]}")
            expSet.add(exp[0])
        return boFound

    # 分析表达式的每一个数字的+-*/是否可以得到目标值,且从第0,1,...个索引值开始两两计算并合并
    for i in range(numLen - 1):
        tmpDgs = []
        tmpExp = []
        # 分析加法能否满足条件(第i个值和第i+1个值)
        tmpV = dgs[i] + dgs[i + 1]
        tmpVExp = getExp(exp[i], exp[i + 1], "+")
        j = 0
        while j < numLen:
            if j in [i, i + 1]:
                tmpDgs.append(tmpV)
                tmpExp.append(tmpVExp)
                j += 1
            else:
                tmpDgs.append(dgs[j])
                tmpExp.append(f"{exp[j]}")
            j += 1
        if not solve24(tmpDgs, len(tmpDgs), tmpExp):
            tmpDgs.clear()
            tmpExp.clear()

        # 分析减法能否满足条件(第i个值和第i+1个值)
        tmpV = dgs[i] - dgs[i + 1]
        tmpVExp = getExp(exp[i], exp[i + 1], "-")
        j = 0
        while j < numLen:
            if j in [i, i + 1]:
                tmpDgs.append(tmpV)
                tmpExp.append(tmpVExp)
                j += 1
            else:
                tmpDgs.append(dgs[j])
                tmpExp.append(f"{exp[j]}")
            j += 1
        if not solve24(tmpDgs, len(tmpDgs), tmpExp):
            tmpDgs.clear()
            tmpExp.clear()

        # 分析乘法能否满足条件(第i个值和第i+1个值)
        tmpV = dgs[i] * dgs[i + 1]
        tmpVExp = getExp(exp[i], exp[i + 1], "*")
        j = 0
        while j < numLen:
            if j in [i, i + 1]:
                tmpDgs.append(tmpV)
                tmpExp.append(tmpVExp)
                j += 1
            else:
                tmpDgs.append(dgs[j])
                tmpExp.append(f"{exp[j]}")
            j += 1
        if not solve24(tmpDgs, len(tmpDgs), tmpExp):
            tmpDgs.clear()
            tmpExp.clear()

        # 分析除法能否满足条件(第i个值和第i+1个值)
        if dgs[i + 1] != 0:
            tmpV = dgs[i] / dgs[i + 1]
            tmpVExp = getExp(exp[i], exp[i + 1], "/")
            j = 0
            while j < numLen:
                if j in [i, i + 1]:
                    tmpDgs.append(tmpV)
                    tmpExp.append(tmpVExp)
                    j += 1
                else:
                    tmpDgs.append(dgs[j])
                    tmpExp.append(f"{exp[j]}")
                j += 1
            if not solve24(tmpDgs, len(tmpDgs), tmpExp):
                tmpDgs.clear()
                tmpExp.clear()

def solve1000(dgs: list, numLen: int, exp: list):
    global totalTimes
    totalTimes += 1
    # 验证结果值
    if numLen == 1:
        boFound = abs(dgs[0] - 1000) < epsilon
        if boFound:
            # 用求表达式的值函数验证结果
            real = eval(exp[0])
            print("boFound:", exp[0], dgs, f"real={real} {real==dgs[0]}")
            expSet.add(exp[0])
        return boFound

    # 分析表达式的每一个数字的+-*/是否可以得到目标值,且从第0,1,...个索引值开始两两计算并合并
    for i in range(numLen - 1):
        tmpDgs = []
        tmpExp = []
        # 分析加法能否满足条件(第i个值和第i+1个值)
        tmpV = dgs[i] + dgs[i + 1]
        tmpVExp = getExp(exp[i], exp[i + 1], "+")
        j = 0
        while j < numLen:
            if j in [i, i + 1]:
                tmpDgs.append(tmpV)
                tmpExp.append(tmpVExp)
                j += 1
            else:
                tmpDgs.append(dgs[j])
                tmpExp.append(f"{exp[j]}")
            j += 1
        if not solve1000(tmpDgs, len(tmpDgs), tmpExp):
            tmpDgs.clear()
            tmpExp.clear()

        # 分析减法能否满足条件(第i个值和第i+1个值)
        tmpV = dgs[i] - dgs[i + 1]
        tmpVExp = getExp(exp[i], exp[i + 1], "-")
        j = 0
        while j < numLen:
            if j in [i, i + 1]:
                tmpDgs.append(tmpV)
                tmpExp.append(tmpVExp)
                j += 1
            else:
                tmpDgs.append(dgs[j])
                tmpExp.append(f"{exp[j]}")
            j += 1
        if not solve1000(tmpDgs, len(tmpDgs), tmpExp):
            tmpDgs.clear()
            tmpExp.clear()

        # 分析乘法能否满足条件(第i个值和第i+1个值)
        tmpV = dgs[i] * dgs[i + 1]
        tmpVExp = getExp(exp[i], exp[i + 1], "*")
        j = 0
        while j < numLen:
            if j in [i, i + 1]:
                tmpDgs.append(tmpV)
                tmpExp.append(tmpVExp)
                j += 1
            else:
                tmpDgs.append(dgs[j])
                tmpExp.append(f"{exp[j]}")
            j += 1
        if not solve1000(tmpDgs, len(tmpDgs), tmpExp):
            tmpDgs.clear()
            tmpExp.clear()

        # 分析除法能否满足条件(第i个值和第i+1个值)
        if dgs[i + 1] != 0:
            tmpV = dgs[i] / dgs[i + 1]
            tmpVExp = getExp(exp[i], exp[i + 1], "/")
            j = 0
            while j < numLen:
                if j in [i, i + 1]:
                    tmpDgs.append(tmpV)
                    tmpExp.append(tmpVExp)
                    j += 1
                else:
                    tmpDgs.append(dgs[j])
                    tmpExp.append(f"{exp[j]}")
                j += 1
            if not solve1000(tmpDgs, len(tmpDgs), tmpExp):
                tmpDgs.clear()
                tmpExp.clear()

def solve24_test():
    global totalTimes
    totalTimes = 0
    expSet.clear()
    dgs = [5] * 5
    numLen = len(dgs)
    exp = ["5"] * 5
    solve24(dgs, numLen, exp)
    print("totalTimes=", totalTimes)
    index = 0
    for tmpExp in expSet:
        print("[%d] %s" % (index, tmpExp))
        index += 1

def solve1000_test():
    global totalTimes
    totalTimes = 0
    expSet.clear()
    dgs = [8] * 8
    numLen = len(dgs)
    exp = ["8"] * 8
    solve1000(dgs, numLen, exp)
    print("totalTimes=", totalTimes)
    index = 0
    for tmpExp in expSet:
        print("[%d] %s" % (index, tmpExp))
        index += 1

def solve_exp_test():
    global totalTimes
    totalTimes = 0
    expSet.clear()
    # 测试
    nums = [4, 5, 6, 7]
    solve_exp21(nums)
    print("totalTimes=", totalTimes)
    index = 0
    for tmpExp in expSet:
        print("[%d] %s" % (index, tmpExp))
        index += 1

if __name__ == "__main__":
    # solve24_test()
    # solve1000_test()
    solve_exp_test()