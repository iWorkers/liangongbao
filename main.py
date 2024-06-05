#pyinstaller -F -c main.py
#nuitka --mingw64 --standalone --show-progress --show-memory --output-dir=out --onefile main.py
from get_wechat_secret import get_tok_uid
from http_utils import HTTPClient
from url_conf import URLS
import json
from LgbConfig import MIN_TIME, MAX_TIME
import datetime
import random
import time
import logging
import traceback
import string
import copy
import requests

logging.basicConfig(filename='log.txt',
                    level=logging.DEBUG,
                    filemode='a+',
                    format='[%(asctime)s] [%(levelname)s] >>> \n%(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S')

try:
    memberId, token ,cookie= get_tok_uid()
    user_info = {'memberId': memberId, 'token': token,'cookie': cookie}
    with open('mul_token.txt', 'a', encoding='utf-8') as f:
        f.write(str(user_info) + '\n')
    
    http_client = HTTPClient()
    http_client.memberId=memberId
    http_client.token=token
    #print('---------------------------------------------------')
    cookie_string = cookie +'token='+token+'; '+'memberId='+memberId
    #print(cookie_string)
    #cookie_dict = dict(item.split("=") for item in cookie_string.split("; "))
    #cookie_jar = requests.utils.cookiejar_from_dict(cookie_dict)
    #cookie_list = [cookie_jar.get_dict()]

    http_client.cookie=cookie_string
    #print('---------------------------------------------------')
    #print(http_client.cookie)

    flag=True

    while flag :
        
        zl=input("【查询积分按c  |  答题按a  |  抽奖按m   |   退出按q  】 :").upper()
        if zl == 'C':
        
            result_dict = http_client.send(URLS['lgb2023_competition'])
            #print(result_dict)
            print('当前积分为：'+str(result_dict['data']['points']))
            print('---------------------------------------------------')
        if zl == 'A':
            with open("answerdict.json", 'r', encoding='utf-8') as fw:
                right_answer = json.load(fw)
            lgb2023_activity_url = copy.deepcopy(URLS['lgb2023_activity'])
            lgb2023_activity_url['req_url'] += http_client.memberId
            lgb2023_activity_url['token']=http_client.token
            lgb2023_activity_url['memberId']=http_client.memberId
            res1 = http_client.send(lgb2023_activity_url)
            result_dict1 = http_client.send(URLS['lgb2023_competition'])
            result_dict = http_client.send(URLS['lgb2023_start'])
            
            if '成功' not in str(result_dict):
                if '挑战已完成' in str(result_dict):
                    print('今天已答题，明天再来!')
                print('---------------------------------------------------')
                continue
            flag3=True
            while flag3:
                qus=result_dict['data']['ques']['content']
                qus_id=result_dict['data']['ques']['quesId']
                qus_type=result_dict['data']['ques']['quesTypeStr']
                qus_no=result_dict['data']['ques']['quesNo']
                qus_option=result_dict['data']['ques']['options']
                answer=[]
                print(str(qus_no)+":"+qus)
                j=0
                xuhao=list(string.ascii_uppercase)
                answer_list={}
                for res in qus_option:
                    print(xuhao[j]+"、"+res)
                    answer_list[xuhao[j]]=res
                    j=j+1
                if qus in right_answer.keys():
                    
                    answer = list(right_answer[qus])
                    data1=json.dumps({"quesId":"%s" % qus_id,"answerOptions":answer})
                else:
                
                    if '多选' in qus_type:
                        
                        temp_ans=[]
                        zl=input("多选题连续输入答案序号如ABC按enter提交！").upper()
                        for al in list(zl):
                            temp_ans.append(answer_list[al])
                        answer =list(temp_ans)
                        data1=json.dumps({"quesId":"%s" % qus_id,"answerOptions":answer})
                    else:
                        zl=input("单选题输入答案序号如A按enter提交！").upper()
                        answer=list(answer_list[zl])
                        data1=json.dumps({"quesId":"%s" % qus_id,"answerOptions":answer})
                #print(data1)
                
                result_dict = http_client.send(URLS['lgb2023_answer'],data=data1)
                if qus_no == 5:
                    result = http_client.send(URLS['lgb2023_submitcompetition'])
                    print('---------------------------------------------------')
                    print("答题结束！")
                    print('本次答对题目数：', result.get('data', {}).get("correctNum"))
                    flag3=False
        if zl == 'M':
            result_dict = http_client.send(
                URLS['getdrawsurplusnum'])
            surplusNum = int(result_dict['data']['surplusNum'])
            if surplusNum == 0:
                print("您的抽奖次数已用完！")
            for i in range(surplusNum):
                result_dict = http_client.send(URLS['drawprize'])
                data = result_dict['data']
                if not data:  # 无数据
                    print("您的抽奖次数已用完！")
                    print('---------------------------------------------------')
                    continue
                prizeName = data['prizeName']
                print('第%s次抽奖获得:' % (i+1), prizeName)
                time.sleep(random.randint(MIN_TIME, MAX_TIME))
            print('---------------------------------------------------')
        if zl == 'Q':
            flag=False
except Exception as e:
    traceback.print_exc() # 打印到控制台
    logging.error(traceback.format_exc())
