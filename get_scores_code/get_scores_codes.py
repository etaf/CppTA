#!/usr/bin/env python
# encoding: utf-8

######################################
# By ETAF
# input: norm2rand.txt 需包含字段：id name teacher rand_id
# output:
# 生成分数表，包含考生每一题的最高分,并检测对于每一题是否包含关键字。保存到文件 final_scores.txt final_scores.xls
# 将每位考生的每一题的最高分代码保存到code文件夹.
######################################

###Configure:
PROBLEM_NUM = 4
NORM2RAND_txt = "norm2rand.txt"

######################################
from student_model import  get_st_dict
from pat_crawler import PAT_crawler
import xlwt
import os
import string
def write_txt(st_dict):
    fp = open("final_scores.txt",'w')
    #problems = [str(x+1001) for x in range(4)]

    problems = [ string.ascii_uppercase[x] for x in range(PROBLEM_NUM)]
    for st in st_dict.values():
        content = st.id + '\t' + st.name + '\t' + st.teacher_name
        for problem_id in problems:
            if problem_id in st.submissions:
                #content+='\t'+str(st.submissions[problem_id].score) + '('+ st.submissions[problem_id].code_url+')'
                content+='\t'+str(st.submissions[problem_id].score)
                content+='(pass_filter='+str(st.submissions[problem_id].pass_filter)+')'
            else:
                content+='\t0()'
        fp.write(content+"\n")
    fp.close()
def write_xls(st_dict):

    book = xlwt.Workbook(encoding = "utf-8")
    sheet1 = book.add_sheet("final_codes")
    #problems = [str(x+1001) for x in range(4)]
    problems = [ string.ascii_uppercase[x] for x in range(PROBLEM_NUM)]

    items = ["normal id","name","teacher","random id",'total_score']+problems

    for i in range(len(items)):
        sheet1.write(0,i,items[i])
    row = 1

    for st in st_dict.values():
        sheet1.write(row,0,st.id)
        sheet1.write(row,1,st.name)
        sheet1.write(row,2,st.teacher_name)
        sheet1.write(row,3,st.rand_id)
        sheet1.write(row,4,st.score)
        i = 0
        col_start =5
        for problem_id in problems:
            if problem_id in st.submissions:
                sheet1.write(row,i+col_start,str(st.submissions[problem_id].score))
                #sheet1.write(row+1,i+col_start,st.submissions[problem_id].code_url)
                sheet1.write(row+1,i+col_start,"keywords="+str(st.submissions[problem_id].pass_filter))
            else:
                sheet1.write(row,i+col_start,"0")
                sheet1.write(row+1,i+col_start,"No submitted code")
            i = i+1
        row = row+2
    book.save("final_codes.xls")
    print "result have been writen to final_scores.xls"
def get_name_pwd_from_console():
    name = raw_input("please input the account: ")
    import getpass
    passwd = getpass.getpass('please input the password: ')
    return [name,passwd]

def save_codes(crawler,st_dict):
    parent_path = "codes/"
    if not os.path.exists(parent_path):
        os.makedirs(parent_path)

    pre_str = '''
        <link href="../media/application-f75b4427de2ad51cdb4f1abe37abcb68.css" media="screen" rel="stylesheet" type="text/css" />
        <script src="../media/application-929ef7194c12152f6707bc1d9a3efde7.js" type="text/javascript"></script>
        '''

    for st in st_dict.values():
        st_path = parent_path+st.teacher_name+"/"+st.id+"_"+st.name + "/"
        if not os.path.exists(st_path):
            os.makedirs(st_path)
        for submission in st.submissions.values():
            submission_path = st_path + submission.problem_id +".html"
            page_html = crawler.get_code_page(submission.code_url)
            fp = open(submission_path,'w')
            fp.write(pre_str+page_html)
            fp.close()

def main():

    st_dict = get_st_dict("tmp")
    tmp = get_name_pwd_from_console()
    crawler = PAT_crawler(tmp[0],tmp[1])

    while crawler.logined() == False:
        print "login error! try your account and password again!\n"
        tmp = get_name_pwd_from_console()
        crawler.login(tmp[0],tmp[1])

    st_dict = crawler.get_submissions(st_dict)
#    print st_dict
    #return
    keywords_set = [ ['cin','cout'],['class'],['operator','class'],['class','virtual'] ]

    #problems = [str(x+1001) for x in range(PROBLEM_NUM)]
    problems = [ string.ascii_uppercase[x] for x in range(PROBLEM_NUM)]
    tmp = {}
    for i in range(len(problems)):
       tmp[problems[i]] = keywords_set[i]


    keywords_set = tmp
    #print keywords_set
    for key in st_dict:
        for problem_id in problems:
            if problem_id in st_dict[key].submissions:
                st_dict[key].score = st_dict[key].score + st_dict[key].submissions[problem_id].score
                if crawler.code_filter(st_dict[key].submissions[problem_id].code_url,keywords_set[problem_id]) == True:
                    st_dict[key].submissions[problem_id].pass_filter = True
    #print st_dict

    write_txt(st_dict)
    write_xls(st_dict)
    save_codes(crawler,st_dict)

if __name__ == '__main__':
    main()
