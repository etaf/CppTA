#!/usr/bin/env python
# encoding: utf-8
import argparse
import sys
import xlwt
##########################################
# BY ETAF
# Function: 统计平时成绩
##########################################
class Student(object):


    def __init__(self,student_number):
        self.student_number = student_number
        self.scores = []
        self.student_name = None
        self.pos = 0
    #def __cmp__(self,other):
        #return self.student_number <  other.student_number
    def __repr__(self):
        return self.student_number +" "+ self.student_name +" "+str(self.scores)+"\n"


def get_tried_student_list(filename):
    try:
        fp = open(filename,"r")
    except IOError:
        print "Error:",filename,"does not exist!"
        exit(1)

    student_list = []

    for line in fp.readlines():
        items = line.split()
        st = Student(items[1])
        st.scores.append( float(items[2]))
        if len(st.scores) > 1:

            print "Error: line:",sys._getframe().f_lineno
            print st.scores
            exit(1)
        student_list.append(st);
    fp.close()
    return student_list

def get_student_list(filename):
    if filename == None:
       filename = "student_list.txt"
    try:
        fp = open(filename,"r")
    except IOError:
           print "Error: student list file does not exist!"
           exit(1)
    student_list = []
    for line in fp.readlines():
        items = line.split()
        st = Student(items[0])
        st.student_name = items[1]
        st.student_scores = []
        student_list.append(st)

    fp.close()
    return student_list

def args_process():
#args process
    parser = argparse.ArgumentParser(prog="",description="A tool for cppLecture by ETAF")
    parser.add_argument("--list",action = 'store',dest = 'student_list_file',help='student_list_file',default = 'student_list.txt')
    parser.add_argument("--files",nargs = '*',action = 'store',dest = 'files',help='files from PAT rankpage',required = True)
    return parser.parse_args()

def write_xls(files,student_list):
    if len(files)!=len(student_list[0].scores):
        print "Error: line ",sys._getframe().f_lineno
        exit(1)
    n = len(files)
    book = xlwt.Workbook(encoding = "utf-8")
    sheet1 = book.add_sheet("statistic")
    items = ["学号" , "姓名","座位"]
    for filename in files:
        words = filename.split(".")
        items.append(words[0])
    for i in range(len(items)):
        sheet1.write(0,i,items[i])
    row = 1
    for st in student_list:
        sheet1.write(row,0,st.student_number)
        sheet1.write(row,1,st.student_name)
        sheet1.write(row,2,st.pos)
        for col in range(3,3+n):
            sheet1.write(row,col,st.scores[col-3])
        row+=1

    book.save("result.xls")

def show_list(student_list):
    for st in student_list:
        print st.student_number , st.student_name , st.scores

def main():
    args = args_process()
    print args
    student_list = get_student_list(args.student_list_file)
    for filename in args.files:
        print 'processing data_file: ',filename
        tried_student_list = get_tried_student_list(filename)
        for i in range(len(student_list)):
            flag = False
            for j in range(len(tried_student_list)):
                if student_list[i].student_number == tried_student_list[j].student_number:
                    student_list[i].scores.append(tried_student_list[j].scores[0])
                    flag = True;
                    break;
            if flag == False:
                student_list[i].scores.append(-1)
        print 'processing data_file: ',filename,"end"

    print "arranging position"

    arranged_list = arrange_pos(student_list)

    print "writing to result.xls"
    write_xls(args.files,arranged_list)

    print "Done!"

def arrange_pos(student_list):

    sorted_list = sorted(student_list , key=lambda student:student.student_number,reverse=True)
    black_list = []
    arranged_list = []
    for st in sorted_list:
        flag = True
        for i in st.scores:
            if i != -1:
                flag = False
                break;
        if flag:
            black_list.append(st)
        else:
            arranged_list.append(st)
    print "black_list:" , len(black_list)
    print black_list


    arranged_list = black_list + arranged_list
    start_pos = 41
    start_pos -= 1
    for i in range(len(arranged_list)):
        arranged_list[i].pos = i+1
    for i in range(len(black_list)):
        tmp = arranged_list[i].pos
        arranged_list[i].pos = arranged_list[start_pos+i].pos
        arranged_list[start_pos+i].pos = tmp

    return sorted(arranged_list,key = lambda student:student.pos)

main()

