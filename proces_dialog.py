#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from dateutil.parser import parse
import os
import re

def removeSpecificCharacters(text):
    return re.sub('[!@#$\n<>]', '', text)

def isTimeFormat(input):
    try:
        try:
            parse(input)
            return True
        except Exception as e:
            print()
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
    if indices != [] :return indices[0]
    else: return None

### TODO
def correctSentenceQA(Ldialog):
    listdialog, listDialogTotal = [], []
    sentence = ''
    for item in Ldialog:
        for id in range(len(item)):
            splittext = removeSpecificCharacters(item[id]).split('\t')
            if len(splittext) > 1 and splittext[len(splittext) -1] =='\n':
                continue
            ##
            splitTextNext = []
            if id < len(item) - 1:
                splitTextNext = removeSpecificCharacters(item[id + 1]).split('\t')
            splitTextPre = []
            if id > 0:
                splitTextPre = removeSpecificCharacters(item[id -1]).split('\t')
            if isTimeFormat(splittext[0]):
                if id == len(item) - 1:
                    sentence = item[id].strip('\n')
                    sentenceSplit = sentence.split('\t')
                    listdialog.append(checkStringTime(sentenceSplit))
                    sentence = ''
                elif (splitTextNext != [] or len(splitTextNext) < 2) and isTimeFormat(splitTextNext[0]):
                    try:
                        if splitTextNext[1].strip() == splittext[1].strip():
                            ## TODO
                            if len(splitTextPre) > 1 and splittext[1] == splitTextPre[1]:
                                sentence = sentence + ' ' + splittext[2].strip('\n')
                            else: sentence = item[id].strip('\n')
                        else:
                            sentence = item[id].strip('\n')
                            sentenceSplit = sentence.split('\t')
                            listdialog.append(checkStringTime(sentenceSplit))
                            sentence = ''
                    except Exception as e:
                        print(splitTextNext)
                        print(splittext)
                else:
                    ##TODO
                    if len(splitTextPre) > 1 and len(splittext) > 2 and len(splitTextPre) > 2 and splittext[1] == splitTextPre[1]:
                        sentence = sentence + ' ' + splittext[2].strip('\n')
                    else:
                        sentence = item[id].strip('\n')
            else:
                sentence = sentence + ' ' + item[id].strip('\n')
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
        if seuil == None:
            return listDialog
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
        if read_data('data/'+ path) != None:
            listData.append(read_data('data/'+ path))
        else:
            continue
    return listData

def extract_respons_sentenses(listDt):
    dictionary = {}
    for item in listDt:
        if len(item) < 2 :
            continue
        else:
            for id in range(len(item)):
                if len(item[id]) < 2:
                    continue
                t = item[id][0]
                if item[id][0] == 'FPT Telecom':
                    if len(item[id]) > 1 and id > 0:
                        try:
                            dictionary[item[id-1][1]] = item[id][1]
                        except Exception as e :
                            continue
    return dictionary

# if __name__ == "__main__":
#     ## for comment
#     listNameFile = os.listdir('data')
#     listPath = os.path.realpath('data')
#     for path in listNameFile:
#         listDataReader = read_data('data/'+ path)
#         listData = correctSentenceQA(listDataReader)
#         print(listDataReader)
