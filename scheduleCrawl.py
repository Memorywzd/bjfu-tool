import json  # json 解析
import requests  # http 请求库

id = ''    # 学号
pwd = '' # 密码
semester = '2022-2023-1'  # 学期
week= '8'   # 周次选择

def Crawl():
    loginLink="http://newjwxt.bjfu.edu.cn/app.do?method=authUser&xh="+id+"&pwd="+pwd
    rep = requests.get(loginLink)
    res = json.loads(rep.text)
    # 使用账号密码换取网站 token
    token = res["token"]
   # tableUrl = "http://newjwxt.bjfu.edu.cn/app.do?method=getKbcxAzc&xh=201002423&xnxqid=2022-2023-1&zc=3"
    tableUrl = "http://newjwxt.bjfu.edu.cn/app.do?method=getKbcxAzc&xh="+id+"&xnxqid="+semester+"&zc="+week
    header = {
        "token": token  # 传入 token ，鉴权
    }
    res = requests.get(url=tableUrl, headers=header)
    schedule = json.loads(res.text)  # 读取课表 json
    print(schedule)  # 打印课表 json


if __name__ == "__main__":
    Crawl()
