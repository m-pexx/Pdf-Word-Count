#!/usr/bin/env python3

import multiprocessing as mp
import os
import sys
import re
import time
import PyPDF2

def getPageCount(pdf_file):
    pdfFileObj = open(pdf_file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pages = pdfReader.numPages
    return pages


def extractData(pdf_file, page):
    pdfFileObj = open(pdf_file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pageObj = pdfReader.getPage(page)
    data = pageObj.extractText()
    return data


def getWordCount(data):
    data = data.split()
    return len(data)

def parCount(values):
    text = extractData(values[0], values[1])
    return(getWordCount(text))


def parallelize(fun,vec,pool):
    with mp.Pool(pool) as p:
        res = p.map(fun,vec)
    return(res)


def main():
    if len(sys.argv)!=2:
        print('command usage: python word_count.py FileName')
        exit(1)
    else:
        pdfFile = sys.argv[1]
        # check if the specified file exists or not
        try:
            if os.path.exists(pdfFile):
                print("file found!")
        except OSError as err:
            print(err.reason)
            exit(1)
    # get the word count in the pdf file
    totalWords = 0
    numPages = getPageCount(pdfFile)
    ncpu = mp.cpu_count()
    if ncpu ==1:
        for i in range(numPages):
            text = extractData(pdfFile, i)
            totalWords+=getWordCount(text)
    else:
        totalWords = sum(parallelize(fun=parCount,
                                     vec=zip([pdfFile]*numPages,
                                     range(numPages)),pool=ncpu))

    print (totalWords)

if __name__ == '__main__':
    main()
