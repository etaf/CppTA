#!/usr/bin/env python
# encoding: utf-8

################################################
# BY ETAF
# Function: generate random id and random password for each student
# Input: student_list . Require user id , user name , teacher_name
# Output: norm2rand.txt norm2rand.xls
################################################
import string
import random
import xlwt
from student_model import get_st_list
def get_rand_id(single_set):

    rand_id = 'cpp'+''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    while single_set.has_key(rand_id) :
        rand_id = 'cpp'+''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
    single_set[rand_id] = 1
    return rand_id

def get_rand_pwd():
    return ''.join(random.choice(string.ascii_lowercase + string.digits)for _ in range(6))

def write_xls(st_list):

    book = xlwt.Workbook(encoding = "utf-8")
    sheet1 = book.add_sheet("norm2rand")

    items = ["normal id","name","teacher","random id","random password"]

    for i in range(len(items)):
        sheet1.write(0,i,items[i])
    row = 1
    for st in st_list:
        sheet1.write(row,0,st.id)
        sheet1.write(row,1,st.name)
        sheet1.write(row,2,st.teacher_name)
        sheet1.write(row,3,st.rand_id)
        sheet1.write(row,4,st.rand_pwd)
        row+=1

    book.save("norm2rand.xls")
def write_txt(norm2rand):
    fp = open("norm2rand.txt",'w')
    for st in st_list:
        fp.write("%s\t%s\t%s\t%s\t%s\n" %(st.id,st.name,st.teacher_name,st.rand_id,st.rand_pwd))
    fp.close()


def test_self(st_list):
    single_set = {}
    flag = True
    for st in st_list:
        if single_set.has_key(st.rand_id):
            print "Error : rand id not unique!"
            flag = False
            break;
        else:
            single_set[st.rand_id] = 1
    if flag:
        print "test self : OK!"

if __name__ == '__main__':

    st_list = get_st_list("student_list.txt")

    single_set = {}

    for i in range(len(st_list)):
        st_list[i].rand_id = get_rand_id(single_set)
        st_list[i].rand_pwd = get_rand_pwd()

    write_xls(st_list)
    write_txt(st_list)

    test_self(st_list)
