from datetime import datetime
import requests
import sys
import time
import plotly
import smtplib
import Config

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
date_now = time.strftime('%Y-%m-%d')
config = Config.Configure()


def login_orig(username, password, user_id):
    url = 'https://online.as-invest.co.il/login/'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'https://online.as-invest.co.il/login/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'he-IL,he;q=0.8,en-US;q=0.6,en;q=0.4',
        'Host': 'online.as-invest.co.il',
        'Connection': 'keep-alive',
        'Content-Length': '1623',
        'Cache-Control': 'max-age=0',
        'Origin': 'https://online.as-invest.co.il',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.'
                      '2704.103 Safari/537.36',
        'Cookie': 'undefined-co-3=true; type-undefined-co-3=Funds_Title_Compensation_Part; optimizelyEndUser'
                  'Id=oeu1462348143930r0.19029230579517487; optimizelySegments=%7B%225348950219%22%3A%22gc%22'
                  '%2C%225344960299%22%3A%22false%22%2C%225331082252%22%3A%22campaign%22%7D; optimizelyBuckets'
                  '=%7B%7D; as-product-status=open; ASP.NET_SessionIdNew=1abmnw55u00fwt55gpn5jj45gmJkP7/ScMAhx'
                  'xteHfn2zaVQzpE=; __utmt=1; TSeb7983_77=8584_6ba9652e59c32879_rsb_0_rs_https%3A%2F%2Fonline.'
                  'as-invest.co.il%2F_rs_1_rs_0; __utma=9962661.273612805.1456742116.1468345754.1468495490.43;'
                  ' __utmb=9962661.7.9.1468495727569; __utmc=9962661; __utmz=9962661.1465933451.14.8.utmcsr=go'
                  'ogle|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=9962661.|5=Customer=%2'
                  'C%D7%92%D7%9E%D7%9C%20%D7%95%D7%94%D7%A9%D7%AA%D7%9C%D7%9E%D7%95%D7%AA%2C%D7%A4%D7%95%D7%9C'
                  '%D7%99%D7%A1%D7%95%D7%AA%20%D7%91%D7%99%D7%98%D7%95%D7%97=1; TSeb7983=c1e4a3729fee6290c82bc8'
                  'b13134d1a990b45a82420b862257877682330e5c4dc627ed1d5d65bffc4399df73'
    }

    cookie = {
        'ASP.NET_SessionIdNew': '1abmnw55u00fwt55gpn5jj45gmJkP7/ScMAhxxteHfn2zaVQzpE=',
        'TSeb7983': '7bd980cc275545bd1c4fd4457bdd384890b45a82420b8622578796ef330e5c4dc627ed1d5d65bffcb1f9cee7',
        'TSeb7983_77': '8584_6ba9652e59c32879_rsb_0_rs_https%3A%2F%2Fonline.as-invest.co.il%2F_rs_1_rs_0',
        '__utma': '9962661.273612805.1456742116.1468495490.1468503315.44',
        '__utmb': '9962661.7.9.1468503797879',
        '__utmc': '9962661',
        '__utmt': '1',
        '__utmv': '9962661.|5=Customer=%2C%D7%92%D7%9E%D7%9C%20%D7%95%D7%94%D7%A9%D7%AA%D7%9C%D7%9E%D7%95%D7%AA%2C%D7'
                  '%A4%D7%95%D7%9C%D7%99%D7%A1%D7%95%D7%AA%20%D7%91%D7%99%D7%98%D7%95%D7%97=1',
        '__utmz': '9962661.1465933451.14.8.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
        'as-product-status': 'open',
        'optimizelyBuckets': '%7B%7D',
        'optimizelyEndUserId': 'oeu1462348143930r0.19029230579517487',
        'optimizelySegments': '%7B%225348950219%22%3A%22gc%22%2C%225344960299%22%3A%22false%22%2C%225331082252%22%3A%22'
                              'campaign%22%7D',
        'type-undefined-co-3': 'Funds_Title_Compensation_Part',
        'undefined-co-3': 'true'
    }

    data = '__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwUENTM4MQ9kFgJmD2QWAmYPZBYCAgEPZBYGZg9kFgQCBA9kFgICBQ8' \
           'WAh4HVmlzaWJsZWdkAg8PFgIfAGhkAgEPFgIfAGhkAgIPZBYEAgUPZBYCAgEPZBYCAgMPZBYCAgMPFCsAAhYCHgtfIUl0ZW1Db3VudAID' \
           'ZBYGAgEPZBYCZg8VBQdjb250YWN0ATAJL2NvbnRhY3QvBV9zZWxmDdem15XXqCDXp9ep16hkAgIPZBYCZg8VBQNmYXEBMQUvZmFxLwVfc' \
           '2VsZhnXqdeQ15zXldeqINeV16rXqdeV15HXldeqZAIDD2QWAmYPFQUHbWFpbnRvcAEyBi9tYWluLwVfc2VsZhPXnNei157XldeTINeU15' \
           'HXmdeqZAIJD2QWAgIDD2QWAmYPZBYEZg8WAh8AaGQCAg8UKwACFgIfAQIDZBYGAgEPZBYCZg8VAzBodHRwczovL3d3dy5hcy1pbnZlc3Q' \
           'uY28uaWwvdXNhZ2Vjb25kaXRpb24vLmFzcHgGX2JsYW5rE9eq16DXkNeZINep15nXnteV16lkAgIPZBYCZg8VAxgvZmlsZXMvZ2lsdXlf' \
           'bmFvdF85NC5wZGYGX2JsYW5rE9eS15nXnNeV15kg16DXkNeV16pkAgMPZBYCZg8VAy9odHRwczovL3d3dy5hcy1pbnZlc3QuY28uaWwvc' \
           'HJpdmFjeXBvbGljeS8uYXNweAZfYmxhbmsR15TXkteg16og157XmdeT16JkZIz%2F0zFViLRnXK0gGcMzkF4RaUhe&__VIEWSTATEGENE' \
           'RATOR=CA0B0334&ctl00%24ctl00%24ctlPageContentPlaceHolder%24SVSrvPrezZoneHolder0%24ctl00%24fldUserName=' \
           + username + '&ctl00%24ctl00%24ctlPageContentPlaceHolder%24SVSrvPrezZoneHolder0%24ctl00%24fldUserID=' + \
           user_id + '&ctl00%24ctl00%24ctlPageContentPlaceHolder%24SVSrvPrezZoneHolder0%24ctl00%24fldPassword=' + \
           password + '&ctl00%24ctl' '00%24ctlPageContentPlaceHolder%24SVSrvPrezZoneHolder0%24ctl00%24cmdLogin=%D7%9B' \
                      '%D7%A0%D7%99%D7%A1%D7%94+%D7%9C%D7%97%D7%A9%D7%91%D7%95%D7%9F&ctl00%24ctl00%24ctlPageContentPlaceHolder' \
                      '%24SVSrvPrezZoneHolder0%24ctl00%24ctl07=&ctl00%24ctl00%24ctlPageContentPlaceHolder%24SVSrvPrezZoneHolder0' \
                      '%24ctl00%24ctl09=&ctl00%24ctl00%24ctlPageContentPlaceHolder%24SVSrvPrezZoneHolder0%24ctl00%24ctl11=&ctl00' \
                      '%24ctl00%24ctlPageContentPlaceHolder%24SVSrvPrezZoneHolder0%24ctl00%24ctl13='

    return requests.post(url, data=data, headers=headers, cookies=cookie, verify=False)


def get_study_fund_amount(content, request):
    return \
    request.content.split('ctl00_ctl00_ctlPageContentPlaceHolder_SVSrvPrezZoneHolder0_ctl03_ctlItems_ctl02_rptCusto'
                          'merFundsList_ctl02_lblFundTotal')[1].split('</article>')[0].split('\n')[7][:-10].strip()


def get_savings_fund_amount(content, request):
    return \
    request.content.split('ctl00_ctl00_ctlPageContentPlaceHolder_SVSrvPrezZoneHolder0_ctl05_ctlItems_ctl01_rptSaving'
                          'sPolicies_ctl02_lblSavingsPoliciesTotal')[1].split('\n')[1].split('role="presentation">'
                                                                                             )[1][3:-6].strip()


def check_if_run_already(date_now, log_file):
    with open(log_file, 'r') as f:
        for line in f.read().split('\n'):
            if line.split('|')[0] == date_now:
                return True
        return False


def parse_log(log_path):
    date = []
    study_fund = []
    stocks_fund = []
    solid_fund = []
    with open(log_path, 'r') as f:
        for line in f.read().split('\n'):
            if line != '':
                line = line.split('|')
                date.append(datetime.strptime(line[0], '%Y-%m-%d'))
                stocks_fund.append(line[1])
                study_fund.append(line[2])
                solid_fund.append(line[3])
    return date, study_fund, stocks_fund, solid_fund


def plot_data(x, stock, study, solid):
    trace0 = Scatter(
        x=x,
        y=stock,
        name='Stocks Policy'
    )
    trace1 = Scatter(
        x=x,
        y=study,
        name='Study Fund'
    )
    trace2 = Scatter(
        x=x,
        y=solid,
        name='Solid Fund'
    )
    data = Data([trace0, trace1, trace2])
    return plotly.offline.plot(data, filename='/home/pi/Desktop/webApp/templates/funds.html')


def get_funds(today_date, savings_account, study_fund, ):
    if savings_account is not None and study_fund is not None:
        with open('fundLog.txt', 'a') as file_writer:
            file_writer.write(today_date + '|' + savings_account + '|' + study_fund + '\n')
    return parse_log('fundLog.txt')


if __name__ == '__main__':
    savings_fund = study_fund = None
    graph_data = []
    try:
        if check_if_run_already(date_now, 'fundLog.txt'):
            print 'Script ran already. Not checking for online data.'
        else:
            req1 = login_orig('Maorg123', 'FitzAbir12', '204367387')
            req2 = login_orig('bioamos1547', '022822134', '')
            saving1 = get_savings_fund_amount(req1.content, req1)
            study1 = get_study_fund_amount(req1.content, req1)
            solid_savings = get_savings_fund_amount(req2.content, req2)
            with open('fundLog.txt', 'a') as f:
                f.write(date_now + '|' + saving1 + '|' + study1 + '|' + solid_savings + '\n')
    except requests.exceptions.ConnectionError, e:
        print '{0}. Not checking for online data.'.format(e)
        if e[0][0] == 'Connection aborted.':
            sys.exit()

    print get_funds(date_now, savings_fund, study_fund)
    # for d in date:
    #     graph_data.append(datetime(year=d.year, month=d.month, day=d.day))
    # plot_data(graph_data, stock_fund, study_fund, solid_fund)
