﻿#encoding:utf-8

'''
TODO : ��������

THE WECHAT FUNCTION IN UNDER CONSTRUCTION, USE IT CAREFULLY !

power by Wyatt
2019/3/15

The WeChat Movie Bot, automatically send the movie resource BaiDu Cloud resource link,
the search engine is based on fqsousou.com, and the wechat engine is itchat

Enjoy It !

'''

#########   ��ʼ����ʼ     #########
mode_init = 1 #΢�Ż����˳�ʼ״̬��1��ʾ������0���෴
bot_name = 'Wyatt��Ӱ������beta'
adv = 'Power By Wyatt\nAccuracy search based on Baidu Validate' #������ӹ�棬�� adv=''
get_movie_number = 5  #��ȡ��Դ����
validate_resource_max = 10 #��֤��Դ���ӵ����������������ʹ�ô˹��ܣ���ֵΪ0
get_hot_number =5 #��ȡ���ŵ�Ӱ�ĸ��������Ϊ0���򲻻�ȡ
use_secrete_ip = 0 #�Ƿ�������ip
error_dic = ['�ٶ�����-���Ӳ�����','��ע���ںŻ�ȡ��Դ','��ȡ��Դ��'] #�ٶ����̹ؼ��ʺ�����
send_online_watch_address = 5 # �������߹ۿ����ӵĸ�����0Ϊ������
baidu_short_link_token = '' # https://dwz.cn/console/userinfo ����ٶȶ���ַ��token
#########   ��ʼ������     #########


import requests as rq
import random
from lxml import etree
import itchat
import os
from lxml.html import fromstring
import json


# constant
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'}

if use_secrete_ip:
    try:
        ipLib = []
        url = 'https://www.xicidaili.com/nn/'
        r = etree.HTML(rq.get(url, headers=header).content)
        # //*[@id="ip_list"]/tr[2]/td[2]
        # //*[@id="ip_list"]/tr[3]/td[2]
        # //*[@id="ip_list"]/tr[101]/td[2]
        for i in range(2, 101):
            ip = r.xpath('//*[@id="ip_list"]/tr[' + str(i) + ']/td[2]/text()')[0]
            type = r.xpath('//*[@id="ip_list"]/tr[' + str(i) + ']/td[6]/text()')[0]
            port = r.xpath('//*[@id="ip_list"]/tr[' + str(i) + ']/td[3]/text()')[0]
            ipLib.append([ip,type,port])
    except Exception as e:
        print('����ip��ȡʧ�ܣ���' + str(e))
        os._exit(0)

else:
    ipLib = []


def get_an_ip():
    global ipLib

    if ipLib == []:
        return {}
    choice = random.choice(ipLib)
    return {choice[1]:choice[0] + ':' + choice[2]}


def short(original_link):
    host = 'https://dwz.cn'
    path = '/admin/v2/create'
    url = host + path
    method = 'POST'
    content_type = 'application/json'
    token = '9860706e562a94413cc57f7076da665f'
    bodys = {'url': original_link}

    # ����headers
    headers = {'Content-Type': content_type, 'Token': token}

    # ��������

    response = rq.post(url=url, data=json.dumps(bodys), headers=headers, proxies=get_an_ip())

    if json.loads(response.text)['Code'] == 0:
        return json.loads(response.text)['ShortUrl']
    else:
        return original_link

def validate_resource(test_url):

    global header,\
        error_dic

    r = rq.get(test_url,headers=header, proxies=get_an_ip()).content

    tree = fromstring(r)

    title = tree.findtext('.//title')

    for forbidden_parameter in error_dic:
        if forbidden_parameter in title:
            return 0
    return 1

def get_online_resource(movie_name):

    resource = []
    global header
    global send_online_watch_address

    r = rq.get('http://ifkdy.com/?q='+ movie_name,headers=header,proxies=get_an_ip()).content.decode()
    tree = etree.HTML(r)

    for i in range(1,send_online_watch_address):
        try:
            r = short(tree.xpath('/html/body/div[2]/div[1]/ul/li['+ str(i) +']/a/@href')[0])
        except IndexError:
            break

        resource.append(r)

    return resource

def gain_link(movie_name):

    global \
        header,\
        get_movie_number,\
        validate_resource_max

    c = rq.get('https://www.fqsousou.com/s/' + movie_name + '.html',headers=header, proxies=get_an_ip()).content.decode()
    tree_r = etree.HTML(c)

    r = []
    init = 1
    count = 0
    incorrect = []

    while True:
        try:
            rr = {}
            xpath = '/html/body/div[3]/div/div/div[2]/div[1]/div[2]/ul/li[' + str(init) + ']/a'
            treer = tree_r.xpath(xpath)
            rr['name'] = treer[0].attrib.get('title')
            rr['naive_link'] = treer[0].attrib.get('href')
            r.append(rr)
            init += 1

        # ���ﲻ�ô�ӡerror
        except Exception:
            break

    # ������������
    def ana_naive_link(naive_link):

        c = rq.get(naive_link,headers=header, proxies=get_an_ip()).content
        xpath_link = '/html/body/div[3]/div/div/div/div[1]/div[1]/div[3]/p/a[2]'
        xpath_type = '/html/body/div[3]/div/div/div/div[1]/div[1]/div[2]/dl/dt[2]/label/text()'
        xpath_size = '/html/body/div[3]/div/div/div/div[1]/div[1]/div[2]/dl/dt[3]/label/text()'
        c = etree.HTML(c)

        try:
            movie_link = short(c.xpath(xpath_link)[0].attrib.get('href'))
        except BaseException:
            movie_link = c.xpath(xpath_link)[0].attrib.get('href')

        movie_type = c.xpath(xpath_type)[0]

        if not movie_type == '�ļ���':
            movie_size = c.xpath(xpath_size)[0]
        else:
            movie_size = ''

        return [movie_link, movie_type, movie_size]

    # ���� movie number limit
    if len(r) < get_movie_number:
        gain_num_limit = len(r)
    else:
        gain_num_limit = get_movie_number

    # ����naive�����һ��������Դ��ַ
    for i in range(len(r)):
        try:

            resource = ana_naive_link('https://www.fqsousou.com/' + r[i]['naive_link'])

            # ��test_validate
            if validate_resource_max:
                if not validate_resource(resource[0]):
                    print('ok -- but validate error')
                    incorrect.append(i)
                    if i >= validate_resource_max:
                        break
                    continue

            # ���û��test_validate �� validate ����
            # ע��pop����ҪŲλ
            r[i]['link'] = resource[0]

            if resource[1] == '':
                r[i]['type'] = 'δ֪'
            else:
                r[i]['type'] = resource[1]

            if resource[2] == '':
                r[i]['size'] = 'δ֪'
            else:
                r[i]['size'] = resource[2]


            print('ok')
            count += 1
            if count >= gain_num_limit:
                break


        except Exception as e:
            print('fail: ' + str(e))
            incorrect.append(i)
            continue

    # �������У��������pop�� index �����
    for i in sorted(incorrect,reverse=True):
        r.pop(i)

    # ��ò�����Ҫ�� gain_num_limit����Ӧ��ȫ fail ���������
    return r[:count]

# ΢�Ż����˹���
def start_wechat_bot():

    global bot_name

    #������ڷ��������У�auto_login ���ϲ��� enableCmdQR=2

    itchat.auto_login(hotReload=True)

    # initialize
    rcv = 'filehelper'
    itchat.send('�ɹ�����'+ bot_name +'����ˣ�\n���Ϳ����Կ�������',rcv)

    friend = itchat.get_friends()
    myName = friend[0]['UserName']

    def send_error_report(desc,error):
        itchat.send(desc+ '\n�������ͣ�'+ str(error),rcv)

    # ����װ����
    @itchat.msg_register(itchat.content.TEXT)
    def main(msg):

        # �����ʼ��ֵ
        global mode_init,\
            get_hot_number,\
            adv,\
            send_online_watch_address

        # return para: FromUserName ToUserName Content

        if msg['ToUserName'] == rcv:

            # ���ù���
            if msg['Content'] == '����':
                mode_init = 1
                itchat.send('�ѿ���������',rcv)
            if msg['Content'] == '״̬':
                if mode_init:
                    itchat.send('�ѿ���������\n���͹ر��Թرջ�����',rcv)
                else:
                    itchat.send('δ����������',rcv)
            if msg['Content'] == '�ر�':
                mode_init = 0
                itchat.send('�ѹرջ�����\n���Ϳ���������������', rcv)
            if msg['Content'] == '����':

                try:
                    beautiful_input(gain_link('��'))
                    itchat.send('����ģ��������',rcv)
                except Exception as e:
                    send_error_report('����ģ�����',e)
                try:
                    beautiful_input_for_hot_movie(get_hot())
                    itchat.send('����ģ��������',rcv)
                except Exception as e:
                    send_error_report('����ģ�����',e)

        # ���⹦��
        if mode_init:
            if msg['Content'][:2] == '����':

                # ��ֹ�Լ���������
                if msg['FromUserName'] == myName:
                    msg['FromUserName'] = rcv

                itchat.send(bot_name + '�������������Եȡ�����', msg['FromUserName'])
                try:
                    r = gain_link(msg['Content'][2:])
                    if not r == []:
                        re = beautiful_input(r)
                        itchat.send(re, msg['FromUserName'])
                    else:

                        # ���û�м���
                        itchat.send('�Ѽ�����10�������Դ������ Baidu Validate ϵͳ�ų��� 10 ��������Դ')

                # �����������
                except Exception as e:
                    itchat.send('�Բ��𣬲����ҵ�������������Դ', msg['FromUserName'])
                    send_error_report('����ģ�����δ�ܳɹ���ɼ���',e)

                # ��ȡ���߿���ַ
                try:
                    if send_online_watch_address:
                        r = get_online_resource(msg['Content'][2:])
                        if not r == []:

                            re = '���߿���ַ��\n'
                            for i in r:
                                re = re + short(i) + '\n=====================\n'

                            itchat.send(re, msg['FromUserName'])

                # �������
                except Exception as e:
                    send_error_report('���߿�ģ�����δ�ܳɹ���ɼ���', e)

                # ���Ż�ȡģ��
                try:
                    if get_hot_number:
                        itchat.send(beautiful_input_for_hot_movie(r=get_hot()),msg['FromUserName'])
                except Exception as e:
                    send_error_report('����ģ�����δ�ܳɹ���ɼ���',e)

                # ��� adv ��Ϊ��
                if not adv == '':
                    try:
                        itchat.send(str(adv),msg['FromUserName'])
                    except Exception as e:
                        send_error_report('���ģ�����',e)

    # ��ʼ����
    itchat.run()

# ���Ź���
def get_hot():
    hot_list = []

    global \
        header,\
        get_hot_number

    # ��Ҫ�� proxies����Ȼ�����
    c = rq.get('http://58921.com/boxoffice/live',headers=header,proxies=get_an_ip()).content.decode()
    r = etree.HTML(c)

    for i in range(1,get_hot_number + 1):
        xpath =  '//*[@id="content"]/div/table/tbody/tr['+ str(i+1) +']/td[1]/a/text()'
        try:
            hot_list.append(r.xpath(xpath)[0])
        except Exception as e:
            print(e)
            continue
    return hot_list

def beautiful_input(r):
    re = '�ٶ������ӣ�\n=====================\n'
    for i in r:
        re = re + '��Դ����' + i['name'] + '\n' + '��Դ���ͣ�' + i['type'] + '\n' \
                  '��Դ��С��' + i['size'] + '\n���̵�ַ��' + i[
                  'link'] + '\n=====================\n'
    return re

def beautiful_input_for_hot_movie(r):
    re = ''
    count = 1
    for i in r:
        re = re + str(count) + '. ' + i + '\n'
        count += 1
    return 'Ϊ���Ƽ�Ŀǰ���ȵĵ�Ӱ��\n' + re

def state_config():
    '''
    mode_init = 0
    get_movie_number = 5
    validate_resource_max = 0
    get_hot_number = 5
    use_secrete_ip = 0
    '''
    state = ''
    if mode_init == 0:
        print('΢�Ż����˳�ʼ��״̬Ϊ���ر�')
    else:
        print('΢�Ż����˳�ʼ��״̬Ϊ������')
    print('��ȡ��Ӱ��Դ����ĿΪ��' + str(get_movie_number))
    if validate_resource_max:
        print('���ٶ�����Դ��֤��ĿΪ��'+ str(validate_resource_max))
    if validate_resource_max == 0:
        print('δ������Դ��֤ϵͳ')
    if get_hot_number:
        print('��ȡ���ȵ�Ӱ��Ŀ��' + str(get_hot_number))
    if not get_hot_number:
        print('δ�������ȵ�Ӱϵͳ')
    if use_secrete_ip:
        print('ʹ��ipΪ������ip' )
    else:
        print('δ��������IP')

    if adv == '':
        print('δ�������Ͷ�Ź���')
    else:
        print('���: ' + adv)

def help():
    print(
          '��ӭʹ�� MovieBot ��������������Ե��õĺ�����\n'
          'get_an_ip() -------------------- ��IP�����������ȡһ������IP\n'
          'short(url)  -------------------- ������ַ\n'
          'validate_resource(url) --------- ���ٶ�����Դ�ɲ�����\n'
          'get_online_resource(movie) ------- ��ȡ���߿���Դ\n'
          'gain_link(movie) --------------- ��ȡ��Դ\n'
          'start_wechat_bot() ------------- ����΢�ŷ���\n'
          'get_hot() ---------------------- ��ȡ���ŵ�Ӱ\n'
          'beautiful_input(get_link) ------ ���� get_link �����\n'
          'beautiful_input_for_hot_movie()- ���� get_hot ���\n'
          'state_config() ----------------- ��ӡ�׶��� config\n'
          'help() ------------------------- ��ӡ����\n'
          '\nWARNING: ��ʹ����������ǰ�����ȶԳ�ʼ������и�ֵ'
    )

