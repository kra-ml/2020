import re,os


def index(unix_time):
    with open('./csv/'+unix_time+'/index_feature.csv', 'w', encoding='utf-8') as ff:
        ff.write('url,source_len'+','+'hangul_num'+','+'input'+','+'submit'+','+'rediraction_1'+','+'rediraction_0'+','+'js_func'+','+'js_filename\n')
        url=os.listdir('./url_list_'+unix_time)
        for url_list in url:
            with open('./url_list_'+unix_time +'/'+ url_list, 'r', encoding='utf-8') as f:
                url_text = '\n'.join(f.readlines())

                # 소스길이
                url_len = len(url_text)

                # 한글여부
                han_len = 0
                url_han = re.findall('[가-힣]{2,}', url_text)
                if not url_han:
                    pass
                else:
                    with open('./word/han_words.txt', 'r', encoding='utf-8') as f:
                        while 1:
                            line = f.readline()
                            if not line: break
                            if line.replace('\n', '') in url_han:
                                han_len += 1

                # input
                p = re.compile("<input type=", re.I)
                url_input = len(p.findall(url_text))

                # submit
                p = re.compile("<input type=[\'|\"]submit", re.I)
                url_submit = len(p.findall(url_text))

                # 리다이렉션 <a href // http-equiv="refresh" // <frame>  // <iframe>
                url_rd = []
                p = re.compile("http-equiv=[\'|\"]refresh[\'|\"]", re.I)
                url_rd += p.findall(url_text)
                p = re.compile("(<iframe|<frame)", re.I)
                url_rd += p.findall(url_text)
                p = re.compile("<a href", re.I)
                url_rd += p.findall(url_text)
                url_rd = len(url_rd)
                if url_rd > 0:
                    url_rd_1 = 1
                    url_rd_0 = 0
                else:
                    url_rd_0 = 1
                    url_rd_1 = 0

                # 자바스크립트 함수 이름
                fun_len = 0
                p = re.compile("function \((.+?)\)", re.I)
                url_function = p.findall(url_text)

                if not url_function:
                    pass
                else:
                    with open('./word/func_words.txt', 'r', encoding='utf-8') as f:
                        while 1:
                            line = f.readline()
                            if not line: break
                            if line.replace('\n', '') in url_function:
                                fun_len += 1

                # 자바스크립트 파일 이름
                js_len = 0
                p = re.compile("src=[\"|\'].*/(.*)\.js[\"|\']", re.I)
                url_jsname = p.findall(url_text)

                if not url_jsname:
                    pass
                else:
                    with open('./word/js_words.txt', 'r', encoding='utf-8') as f:
                        while 1:
                            line = f.readline()
                            if not line: break
                            if line.replace('\n', '') in url_jsname:
                                js_len += 1


                ####
                # print(
                #     url_list + ',' + str(url_len) + ',' + str(han_len) + ',' + str(url_input) + ',' + str(
                #         url_submit) + ',' + str(
                #         url_rd) + ',' + str(fun_len) + ',' + str(js_len) + ',' + str(img_len))

                ff.write(url_list + ',' + str(url_len) + ',' + str(han_len) + ',' + str(url_input) + ',' + str(url_submit) + ',' + str(url_rd_1) + ',' + str(url_rd_0) + ',' + str(fun_len) + ',' + str(js_len) + '\n')
