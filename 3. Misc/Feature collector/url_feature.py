import re,os
import csv


def url_feature(ff,unix_time):
    try:
        os.mkdir('./csv')
    except:
        pass
    with open(ff, 'r') as f:
        url = f.readlines()

    with open('./csv/'+unix_time+'/url_feature.csv', 'w', encoding='utf-8') as ff:
        ff.write('url'+','+'hangul'+','+'number_len,special_chr_0,special_chr_1,in_dic,total_len\n')
        for i in range(len(url)):
            if re.findall('[가-힣]', url[i]):  #### url 한글 여부
                hangeul = 1
            else:
                hangeul = 0

            tld = re.findall('\.(.+)$', url[i])  # tld

            num, number = 0, (re.findall('([0-9]{1,})', url[i]))  # 숫자 개수

            for n in number:
                num += len(n)

            special_chr = re.findall('([!@#$\-%^&*()_+{}~`?/])', url[i])  # 특수기호 여부

            if not special_chr:
                special_chr_0 = 1
                special_chr_1 = 0
            else:
                special_chr_0 = 0
                special_chr_1 = 1
            with open('word/eng_words.txt', 'r') as f:
                wordlist = f.readlines()
            total_len = re.findall('(.*)\.[a-z]*$', url[i])
            _len = len(total_len[0])

            ww = re.sub('[0-9]', '', url[i])
            ww = re.sub('\.[a-z]*$', '', ww)
            if ww in wordlist:
                word = 1
            else:
                word = 0
            ff.write(url[i].replace('\n', '')+','+str(hangeul)+','+str(num)+','+str(special_chr_0)+','+str(special_chr_1)+','+str(word)+','+str(_len)+'\n')
