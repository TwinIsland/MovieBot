import requests as rq
import random
from lxml import etree
import itchat

def short_link(original_link):
    try:
        methodLib = ['c7','kks','u6','rrd']
        method = random.choice(methodLib)
        pc = {
            'url' : original_link,
            'type' : method
        }
        g = eval(rq.post('https://create.ft12.com/done.php?m=index&a=urlCreate',pc).content.decode())
        if g['status'] == 1:
            return g['list']
        else:
            return "����ʧ�ܣ�"
    except BaseException:
        return "�����쳣��"

def short(link):
    return short_link(link)


def gain_link(movie_name):
    c = rq.get('https://www.fqsousou.com/s/' + movie_name + '.html').content.decode()
    tree_r = etree.HTML(c)

    r = []
    init = 1
    count = 0

    while True:
        try:
            rr = {}
            xpath = '/html/body/div[3]/div/div/div[2]/div[1]/div[2]/ul/li[' + str(init) + ']/a'
            treer = tree_r.xpath(xpath)
            rr['name'] = treer[0].attrib.get('title')
            rr['naive_link'] = treer[0].attrib.get('href')
            r.append(rr)
            init += 1

        except BaseException:
            break

    def ana_naive_link(naive_link):
        c = rq.get(naive_link).content
        xpath_link = '/html/body/div[3]/div/div/div/div[1]/div[1]/div[3]/p/a[2]'
        xpath_type = '/html/body/div[3]/div/div/div/div[1]/div[1]/div[2]/dl/dt[2]/label/text()'
        c = etree.HTML(c)

        try:
            movie_link = short(c.xpath(xpath_link)[0].attrib.get('href'))
        except BaseException:
            movie_link = c.xpath(xpath_link)[0].attrib.get('href')

        movie_type = c.xpath(xpath_type)

        return [movie_link, movie_type]

    if len(r) < 5:
        gain_num_limit = len(r)
    else:
        gain_num_limit = 5

    for i in range(len(r) - 1):
        try:
            resource = ana_naive_link('https://www.fqsousou.com/' + r[i]['naive_link'])
            r[i]['link'] = resource[0]

            if resource[1] == '':
                r[i]['type'] = 'δ֪'
            else:
                r[i]['type'] = resource[1][0]

            count += 1
            if count == gain_num_limit:
                break
        except BaseException:
            r.pop(i)
            continue
    return r[:gain_num_limit]

itchat.auto_login(hotReload=True)

# initialize
rcv = 'filehelper'
itchat.send('�ɹ�����Wyatt��Ӱ���ַ���ˣ�',rcv)

friend = itchat.get_friends()
myName = friend[0]['UserName']

# ��ʼ��״̬Ϊ������ (1��ʾ����)
mode = 0


# ����װ����
@itchat.msg_register(itchat.content.TEXT)
def main(msg):
    global mode

    # return para: FromUserName ToUserName Content

    if msg['ToUserName'] == rcv:
        if msg['Content'] == '����':
            mode = 1

    if mode:
        if msg['FromUserName'] != myName and msg['Content'][:2] == '����':
            itchat.send('Wyatt��Ӱ�������������������Եȡ�����', msg['FromUserName'])
            try:
                r = gain_link(msg['Content'][2:])

                re = ''
                for i in r:
                    re = re + '��Դ����' + i['name'] + '\n' + '��Դ���ͣ�' + i['type'] + '\n' + '��Դ��ַ��' + i['link'] + \
                         '\n============================\n'

                itchat.send(re, msg['FromUserName'])
            except BaseException:
                itchat.send('�Բ��𣬲����ҵ�������������Դ', msg['FromUserName'])


itchat.run()