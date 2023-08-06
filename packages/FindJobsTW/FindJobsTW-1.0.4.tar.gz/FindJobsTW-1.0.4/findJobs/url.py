def search_url(submit):
    url = "https://www.104.com.tw/jobs/search/?jobsource=2018indexpoc&ro=0"
    ori_url = "https://www.104.com.tw/jobs/search/?jobsource=2018indexpoc&ro=0"
    j = jobtype(submit)
    a = area(submit)
    u = update_date(submit)
    s = salary_type(submit)
    s2 = salary_conditions(submit)
    e = experience(submit)
    url = f"{ori_url}&{j}&{a}&{u}&{s}&{s2}&{e}"
    while "&&" in url:
        url = url.replace("&&", "&")
    return url

jdict = {
    "經營／人資類" : "2001000000" ,
    "行政／總務／法務類" : "2002000000" ,
    "財會／金融專業類" : "2003000000" ,
    "行銷／企劃／專案管理類" : "2004000000" ,
    "客服／門市／業務／貿易類" : "2005000000" ,
    "餐飲／旅遊 ／美容美髮類" : "2006000000" ,
    "資訊軟體系統類" : "2007000000" ,
    "操作／技術／維修類" : "2010000000" ,
    "資材／物流／運輸類" : "2011000000" ,
    "營建／製圖類" : "2012000000" ,
    "傳播藝術／設計類" : "2013000000" ,
    "文字／傳媒工作類" : "2014000000" ,
    "醫療／保健服務類" : "2015000000" ,
    "學術／教育／輔導類" : "2016000000" ,
    "研發相關類" : "2008000000" ,
    "生產製造／品管／環衛類" : "2009000000" ,
    "軍警消／保全類" : "2017000000" ,
    "其他職類" : "2018000000" 
}

def salary_conditions(submit):
    salary = ""
    s1 = submit["薪資待遇"]
    s2 = submit["薪資下限"]
    s3 = submit["薪資上限"]
    if s1 == "default": #不限就沒東西
        return ""
    elif s1 == "any":
        salary = "sr=99"
    elif s1 == "30000":
        salary = "scmin=30000&scstrict=1 "
    elif s1 == "40000":
        salary = "scmin=40000&scstrict=1 "
    elif s1 == "50000":
        salary = "scmin=50000&scstrict=1 "
    elif s1 == "custom":
        salary = f"scmin={s2}&scstrict=1"
        if s3:
            salary = salary + f"&scmax={s3}"
    else:
        print("薪資範圍出錯", s1,s2,s3)
        return ""
            
    stype = salary_type(submit)
    if not stype: #新增stype
        salary = salary + "&sctp=M"
    
    return salary

#職缺類型  目前不會有list input，只是之後擴充可用
def jobtype(submit):
    jobtype = ""
    if isinstance(submit["職務類別"], str):
        if submit["職務類別"] == "不限": #不限就不需要了
            return ""
        jobtype = jdict[submit["職務類別"]]
    elif isinstance(submit["職務類別"], list):
        for n in submit["職務類別"]:
            if jobtype:#如果前面有資料就加逗號
                jobtype += ","
            jobtype += jdict[n] 
    jobtype = "jobcat=" + jobtype
    return jobtype

#地區條件，基本上進來不管幾個都會是list
def area(submit):
    area = ""
    s = submit["地區條件"]
    if not s: #如果地區條件沒內容
        return ""
    if "all" in s: #不限的話就直接全選
        return ""
    for n in s:
        if area:
            area += ","
        area += n
    area = "area=" + area
    return area

#更新日期
def update_date(submit):
    date = ""
    u = submit["更新日期"]
    if u == "不限":
        return ""
    elif u == "本日最新":
        date = "1"
    elif u == "三日內":
        date = "3"
    elif u == "一週內":
        date = "7"
    elif u == "二週內":
        date = "14"
    elif u == "一個月內":
        date = "30"
    else:
        print("日期出錯", u)
    
    date = "isnew=" + date
    return date

#薪資型態
def salary_type(submit):
    s = submit["薪資類型"]
    stype = "" 
    if s == "月薪":
        stype = "M"
    elif s == "年薪":
        stype = "Y"
    elif s == "日薪":
        stype = "D"
    elif s == "時薪":
        stype = "H" 
    elif s == "不限":#不限直接retunr
        return ""
    else:
        print("薪資型態出錯", s)
        return ""
    
    stype = "sctp=" + stype
    return stype
    
#經歷要求
def experience(submit):
    e = submit["經歷要求"]
    exp = ""
    if e == "不限":
        return ""
    elif e == "1年以下":
        exp = "1"
    elif e == "1-3年":
        exp = "3"
    elif e == "3-5年":
        exp = "5"
    elif e == "5-10年":
        exp = "10"
    elif e == "10年以上":
        exp = "99"
    else:
        print("經歷出錯", e)
        return ""
    exp = "jobexp=" + exp
    return exp

if __name__ == "__main__":
    dict1 = dict1 = {'職務類別': '操作／技術／維修類', '地區條件': ['6001002000', '6001011000'], '更新日期': '一週內', '薪資類型': '年薪', '薪資待遇': 'custom', '薪資下限': '35000', '薪資上限': '', '經歷要求': '3-5年'}
    print(search_url(dict1))

    