#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from dateutil.parser import parse
import os

def isTimeFormat(input):
    try:
        parse(input)
        return True
    except ValueError:
        return False

def checkStringTime(listText):
    listTemp = []
    for item in listText:
        if not isTimeFormat(item):
            listTemp.append(item)
    return listTemp

def getIDtextList(mylist):
    indices = [i for i, s in enumerate(mylist) if '--- Conversation ---' in s]
    return indices[0]

### TODO
def correctSentenceQA(Ldialog):
    listdialog, listDialogTotal = [], []
    sentence = ''
    for item in Ldialog:
        for id in range(len(item)):
            splittext = item[id].split('\t')
            ##
            #simulair = 0
            splitTextNext = []
            if id < len(item) - 1:
                splitTextNext = item[id + 1].split('\t')
                #if splittext[1]
            if id > 0:
                splitTextPre = item[id -1].split('\t')

            if isTimeFormat(splittext[0]):
                if id == len(item) - 1:
                    sentence = item[id]
                    sentenceSplit = sentence.split('\t')
                    listdialog.append(checkStringTime(sentenceSplit))
                    sentence = ''
                elif splitTextNext != [] and isTimeFormat(splitTextNext[0]):
                    if splitTextNext[1].strip() == splittext[1].strip():
                        ## TODO
                        if len(splitTextPre) > 1 and splittext[1] == splitTextPre[1]:
                            sentence = sentence + ' ' + splittext[2]
                        else: sentence = item[id]
                    else:
                        sentence = item[id]
                        sentenceSplit = sentence.split('\t')
                        listdialog.append(checkStringTime(sentenceSplit))
                        sentence = ''
                else:
                    sentence = item[id]
            else:
                sentence = sentence + ' ' + item[id]
                #if id < len(item) - 1:
                if splitTextNext != [] and isTimeFormat(splitTextNext[0]):
                    splitSentence = sentence.split('\t')
                    listdialog.append(checkStringTime(splitSentence))
                    sentence = ''
        listDialogTotal.append(listdialog)
        listdialog = []
    return listDialogTotal


def read_data(fileName):
    listNameData = []
    listDialog = []
    with open(fileName,"r") as file:
        content = file.readlines()
        seuil = getIDtextList(content)
        for id in range(len(content)):
            if id > seuil and content[id] != '\n':
                listDialog.append(content[id])
                # splitRow = content[id].split('\t')
                # if len(splitRow) > 1:
                #     listNameData.append(checkStringTime(splitRow))
                # else:
    return listDialog


def getListData():
    listData = []
    listNameFile = os.listdir('data')
    for path in listNameFile:
        listData.append(read_data('data/'+ path))
    return listData

def extract_respons_sentenses(listDt):
    dictionary = {}
    for item in listDt:
        for id in range(len(item)):
            t = item[id][0]
            if item[id][0] == 'FPT Telecom':
                dictionary[item[id-1][1]] = item[id][1]
    return dictionary

# if __name__ == "__main__":
#     ## for comment
#     listNameFile = os.listdir('data')
#     listPath = os.path.realpath('data')
#     for path in listNameFile:
#         listDataReader = read_data('data/'+ path)
#         listData = correctSentenceQA(listDataReader)
#         print(listDataReader)
