import requests
import re,os


def parse(file,unix_time):
    try:
        os.mkdir("url_list_"+unix_time)
    except:
        pass
    with open(file, 'r') as f:
        url_list = f.readlines()

    for url in url_list:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.89 Whale/1.6.81.16 Safari/537.36',
        }
        # print('http://' + url.replace('\n', ''))
        try:
            rq = requests.get('http://' + url.replace('\n', ''), headers=headers)
        except:
            try:
                rq = requests.get('https://' + url.replace('\n', ''), headers=headers)
            except:
                print(url+'에 연결할 수 없음.')
        enc = re.findall('charset=(.*?)[\"|\']', rq.text)
        if enc:
            if enc[0] == 'euc-kr':
                rq.encoding = enc[0]
            elif enc[0] == 'utf-8':
                rq.encoding = 'utf-8'
        with open('./url_list_'+unix_time+'/'+ url.replace('\n', '') + '.txt', 'w', encoding='utf-8') as f:
            f.writelines(rq.text)
