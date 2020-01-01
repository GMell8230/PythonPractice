# -*- coding: utf-8 -*-
# 模拟扑克发牌并统计同花顺出现的次数
# ======================================================
import random
import re

def initPokers():
    '''
    初始化扑克
    :return:返回一副未洗牌的扑克
    '''
    pokers = []
    for i in ['♥', '♠', '♦', '♣']:
        for j in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K','A']:
            poker = {"color": i, "value": j}
            pokers.append(poker)
    return pokers


def sortCards(curList):
    '''
    将玩家手中的13张牌按照花色、数值排序
    :return:排序后的牌，同花顺出现的次数
    '''
    # 先按照花色排序
    colorSortList = ['♥', '♠', '♦', '♣']
    curList = sorted(curList, key=lambda item: colorSortList.index(item["color"]))

    # 再按照数值排序
    valueSortList = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    # 玩家手中的同花顺计数
    playerFlushCount = 0
    # 记录list中各个花色牌的顺序
    hongtaoPOS = 0
    heitaoPOS = 0
    fangpianPOS = 0
    for i in range(len(curList)):
        if curList[i]['color'] == '♥':
            hongtaoPOS = i;
        if curList[i]['color'] == '♠':
            heitaoPOS = i;
        if curList[i]['color'] == '♦':
            fangpianPOS = i;
    # 将各个花色的牌分别排序存入AllList
    AllList = []
    hongtaoList= sorted(curList[0:hongtaoPOS+1], key=lambda item: valueSortList.index(item["value"]))
    heihaoList= sorted(curList[hongtaoPOS+1:heitaoPOS+1], key=lambda item: valueSortList.index(item["value"]))
    fangpianList= sorted(curList[heitaoPOS+1:fangpianPOS+1], key=lambda item: valueSortList.index(item["value"]))
    meihuaList= sorted(curList[fangpianPOS+1:], key=lambda item: valueSortList.index(item["value"]))
    AllList.append(hongtaoList)
    AllList.append(heihaoList)
    AllList.append(fangpianList)
    AllList.append(meihuaList)
    # 查看所有排序好的牌中是否有同花顺
    for i in range(len(AllList)):
        seriesNum = 0
        tempList = AllList[i]
        if len(tempList) > 5:
            for pos in range(len(tempList) - 1):
                if valueSortList.index(tempList[pos+1]['value']) - valueSortList.index(tempList[pos]['value']) != 1:
                    # 出现如此情况：1234 7  910 qka则同花断了
                    if seriesNum <= 5:
                        seriesNum = 0
                if valueSortList.index(tempList[pos+1]['value']) - valueSortList.index(
                        tempList[pos]['value']) == 1:
                    seriesNum = seriesNum + 1
                    # 5个连续五张同花牌 记录一次同花顺
                    if seriesNum == 5:
                        playerFlushCount = playerFlushCount + 1
                        seriesNum = 0
    # 将各个花色的牌写回curList
    curList[0:hongtaoPOS + 1] = hongtaoList
    curList[hongtaoPOS + 1:heitaoPOS + 1] = heihaoList
    curList[heitaoPOS + 1:fangpianPOS + 1] = fangpianList
    curList[fangpianPOS + 1:] = meihuaList
    return curList, playerFlushCount


def playGames(number):
    '''
    开始扑克游戏
    :param number:输入准备进行的轮次
    :return:输出每轮次的发牌结果，及同花顺出现的概率
    '''
    # 全部游戏轮次总同花顺计数
    AllFlushCount = 0
    FlushRoundsCount = 0
    # 游戏进行的轮数
    for i in range(number):
        # 初始化牌
        poker = initPokers()
        # 洗牌
        random.shuffle(poker)
        random.shuffle(poker)
        random.shuffle(poker)
        # 记牌器，记录各个玩家手中的牌
        li = {}
        # 向4个玩家发牌
        for k in ['E', 'S', 'W', 'N']:
            # 每个玩家获得13张牌
            b = random.sample(poker, 13)
            for s in b:
                poker.remove(s)
            # 记录各个玩家手中的牌
            li.setdefault(k, b)
        oneFlushCount = 0
        # 各个玩家手中的牌排序,并重新存入记牌器,并统计本局游戏中同花出现次数
        print("第%d次发牌>>>\n" % i)
        for k in ['E', 'S', 'W', 'N']:
            li[k], playerFlushCount = sortCards(li[k])
            oneFlushCount = oneFlushCount + playerFlushCount

        AllFlushCount = AllFlushCount + oneFlushCount
        for k in ['E', 'S', 'W', 'N']:
            print('         {} :'.format(k), end="")
            for i in range(len(li[k])):
                print(" " + li[k][i]['color'] + " " + li[k][i]['value'], end="")
            print()
        if oneFlushCount == 0:
            print('未出现同花顺...')
        else:
            FlushRoundsCount = FlushRoundsCount + 1
            print('出现{}个同花顺!!!累计已出现{}个同花顺。'.format(oneFlushCount, AllFlushCount))
    print('出现同花顺的总个数', AllFlushCount)
    print('出现同花顺的发牌次数', FlushRoundsCount)
    print('发牌总次数', number)
    print('出现同花顺的发牌概率', AllFlushCount / number)


if __name__ == '__main__':
    patStr = "^[0-9]*$"
    pattern = re.compile(patStr)
    number = input('请输入发牌总次数:')
    while not pattern.match(number) or len(number) == 0:
        number = input('请输入发牌总次数:')
    playGames(int(number))