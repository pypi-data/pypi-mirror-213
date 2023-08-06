#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#把md用pandoc转成pdf

import os,sys,re,difflib
import z7z8

def filemtime(wj):
    if not os.path.isfile(wj):
        return 0
    return os.stat(wj).st_mtime

def pandoc(md):
    pdf=md[:-3]+".pdf"
    if filemtime(md)>filemtime(pdf):
        数据目录=os.path.join(os.path.dirname(os.path.abspath(z7z8.__file__)),"datafile")
        配置文件=os.path.join(数据目录,"md2pdf.yaml")
        cmd="pandoc -s --pdf-engine=xelatex -o %s %s %s" %(pdf,配置文件,md)
        print(cmd)
        os.system(cmd)

def main():
    for i in range(1,len(sys.argv)):
        pandoc(sys.argv[i])

if __name__ == "__main__":
    main()
