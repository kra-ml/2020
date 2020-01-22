import requests as r
import re
import sys
from datetime import date



class whois_parse:
    hds = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.89',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'DNT': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Sec-Fetch-Site': 'none',
        'Referer': 'https://domainbigdata.com/buyautoparts.com',
    }


    def same_ip_domain(self,url, text):
        ip_address = re.findall('whois\s([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', text)
        rq = r.get('https://domainbigdata.com/' + ip_address[0])
        sd = re.findall('<a rel="nofollow" .+>(.+)</a>', rq.text)
        return len(sd)


    def date_calc(self,url, text):
        try:
            _date = re.findall('<td>Date creation</td>.*\s*.*<td>(.*?)</td>', text)
            _date = _date[0].split('-')
            d0 = date(2019, 9, 19)  # date 객체1
            d1 = date(int(_date[0]), int(_date[1]), int(_date[2]))  # date 객체2
            delta = d0 - d1  # 빼기
            return delta.days  # 날짜로 계산
        except:
            return 0


    def same_name_domain(self,url, text):
        try:
            name = re.findall('<td>Name</td>\r\n\s*<td><a href="(.*)" title=', text)
            name_rq = r.get('https://domainbigdata.com' + name[0])
            name_domain = re.findall('rel="nofollow">(.*)</a>', name_rq.text)
            return len(name_domain)
        except:
            return 0


    def same_email_domain(self,url, text):
        try:
            Email = re.findall('<td>Email</td>\r\n\s*<td><a href="(.*)" title=', text)
            Email_rq = r.get('https://domainbigdata.com' + Email[0])
            Email_domain = re.findall('rel="nofollow">(.*)</a>', Email_rq.text)
            return len(Email_domain)
        except:
            return 0


    def whois_protect(self,url, text):
        try:
            pt = re.findall('whoisguard protected', text)
            pt += re.findall('whois privacy protection service', text)
            if pt:
                return 1
            else:
                return 0
        except:
            return 0


    def main(self,unix_time):
        with open('url_'+unix_time+'.txt', 'r', encoding='utf-8') as f:
            url_list = f.readlines()
        with open('./csv/'+unix_time+'/whois_feature.csv', 'w', encoding='utf-8') as ff:
            ff.write('url,ip,web_age,name,email\n')
            for url in url_list:
                rq = r.get('https://domainbigdata.com/' + url.replace('\n', ''))
                try:
                    id = self.same_ip_domain(url, rq.text)
                except:
                    print('\t Error!! whois 피처 수집 불가')
                    sys.exit()
				# print(url)
                dc = self.date_calc(url, rq.text)
                pt = self.whois_protect(url, rq.text)
                if pt:
                    nd = 200
                    ed = 100
                else:
                    nd = self.same_name_domain(url, rq.text)
                    ed = self.same_email_domain(url, rq.text)
                # print(
                #     url.replace('\n', '') + ',' + str(id).replace(',', '') + ',' + str(dc).replace(',', '') + ',' + str(nd).replace(
                #         ',', '') + ',' + str(ed).replace(',', '') + ',' + str(pt) + '\n')

                    ff.write(url.replace('\n', '') + ',' + str(id).replace(',', '') + ',' + str(dc).replace(',', '') + ',' + str(
                        nd).replace(',', '') + ',' + str(ed).replace(',', '') + '\n')
