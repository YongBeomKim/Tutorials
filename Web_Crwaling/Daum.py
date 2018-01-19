# Yahoo의 기업코드명으로 입력을 해야만 된다
# ks(코스피), kq(코스닥) 기호는 대소문자 무관
#
#from Daum import daum_trader
#daum_trader('005930.ks')


# 1개 기업을 입력하면 1개만 나오고,
# 여러기업을 list 객체로 저장하면 여럿이 함께 처리된 묶음 결과를 출력
#
#from Daum import daum_trader
#codes = ['005930.KS', '000020.ks']
#daum_trader(codes)



def daum_trader(codes):
    import requests, time
    import pandas as pd
    from lxml.html import fromstring
    result = [] ; err=[]; t1 = time.time(); no = 0
    if type(codes) == list:
        for code in codes:
            try:
                url = 'http://finance.daum.net/item/trader.daum?code='+code[:-3]+\
                      '&nil_profile=stockprice&nil_menu=b015'
                response = requests.get(url)
                html_code = fromstring(response.text)
                text = html_code.xpath('//table[@id="traderTable"]//tbody/tr/td//text()')
                df = []
                for i in range(int(len(text)/4)):
                    df.append([ code.upper(), text[i*4], text[i*4+1],text[i*4+2],text[i*4+3] ])
                df = pd.DataFrame(df)
                result.append(df)
            except:
                pass
            no += 1
            if no % 30 == 0 :
                time.sleep(0.1)
                print('{0:4} / {1:4} {2:2} min {3:2} sec, [Estimate {4:2} min, {5:2} sec ]'.format(\
                        no, len(codes),
                        int(time.time() - t1)//60,
                        int(time.time() - t1)%60,
                        int((time.time() - t1)/no*len(codes)//60),
                        int((time.time() - t1)/no*len(codes)%60) ))
        df = pd.concat(result)
        df = df.drop_duplicates(df.columns, keep='first')
        df.reset_index(drop=True, inplace=True)
        df = df.rename(columns={0:'Code', 1:'거래원', 2:'매도', 3:'매수', 4:'순매매'})
        print('Error Codes : ', err)
    else:
        url = 'http://finance.daum.net/item/trader.daum?code='+codes[:-3]+\
              '&nil_profile=stockprice&nil_menu=b015'
        response = requests.get(url)
        html_code = fromstring(response.text)
        text = html_code.xpath('//table[@id="traderTable"]//tbody/tr/td//text()')
        df = []
        for i in range(int(len(text)/4)):
            df.append([ codes.upper(), text[i*4], text[i*4+1],text[i*4+2],text[i*4+3] ])
        df = pd.DataFrame(df)
        df = df.drop_duplicates(df.columns, keep='first')
        df.reset_index(drop=True, inplace=True)
        df = df.rename(columns={0:'Code', 1:'거래원', 2:'매도', 3:'매수', 4:'순매매'})
    return df
