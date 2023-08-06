import os
import requests
import time
import pandas as pd
import re
from bs4 import BeautifulSoup
from lxml import html
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
#中文
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False


class Jobs:
    
    def __init__ (self, keyword):
        self.keyword = keyword
        self.job_links = []
        self.jobs = []
        self.data = []
        
    def xpath_match(self, col_name, index):
        match = {"職務類別" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[{index}]/div[2]/div/div//*/div/div/u",
             "工作待遇" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[{index}]/div[2]/div/p[1]",
             "工作性質" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[{index}]/div[2]/div",
             "上班地點" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[{index}]/div[2]/div/div/span[1]",
             "遠端工作" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[{index}]/div[2]/div", 
             "上班時段" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[{index}]/div[2]/div",
             "休假制度" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[{index}]/div[2]/div",
             "可上班日" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[{index}]/div[2]/div",
             "需求人數" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[{index}]/div[2]/div",
             "管理責任" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[{index}]/div[2]/div",
             "出差外派" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[{index}]/div[2]/div",
             "法定項目" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[4]/div[{index + 1}]/div//*/a",
             "其他福利" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[4]/div[{index + 1}]/div//*/a",
             "工作經歷" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[{index}]/div[2]/div",
             "學歷要求" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[{index}]/div[2]/div",
             "科系要求" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[{index}]/div[2]/div",    
             "擅長工具" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[{index}]/div[2]/div//*/a/u",   
             "工作技能" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[{index}]/div[2]/div//*/a/u",
             "具備證照" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[{index}]/div[2]/div//*/p/a/u",
             "其他條件" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div[3]/div/div[2]/div/div/p",
             "具備駕照" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[{index}]/div[2]/div",
            }
        return match.get(col_name)

    def search_links(self, max_pages = 3, ori_url = None):
        page = 1
        data = []
        if ori_url == None:
            ori_url = f'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword={self.keyword}&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=15&asc=0&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob=1'
        print(f"開始搜尋關鍵字: {self.keyword}")
        while True:
            url = ori_url + f"&page={page}"
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, features="lxml")
            jobs = soup.find_all('article', class_='b-block--top-bord job-list-item b-clearfix js-job-item')
            if not jobs:#找不到內容就中斷
                break
            print("現在正在讀取第" + str(page) + "頁")
            for job in jobs:
                title = job['data-job-name'].strip()
                company = job('li')[1].text.strip()
                URL = 'https:' + job.find("a", class_='js-job-link')['href']
                dict1 = {"公司名稱": company, "職缺名稱": title, "職缺連結": URL}
                data.append(dict1)
            if page == max_pages:
                break
            page += 1
        if data:
            self.job_links = pd.DataFrame(columns = data[0].keys(), data = data)
            print("-"*20)
            print("已完成搜尋，請使用find_jobs爬取工作資料")
            print("-"*20)
        else:
            print("查詢失敗")
            self.job_links = pd.DataFrame()
        return self.job_links
        
    def save_jobs_link(self):
        if not self.job_links:
            print("無資料可儲存")
            return
        path = self.keyword + r"-職缺連結.xlsx" #定義檔案路徑 #當檔案名稱有中文要加r
        df.to_excel(path, index = False)
        print("檔案儲存", path)
    
    def load_jobs_link(self, path = None):
        if not path:
            path = self.keyword + "-職缺連結.xlsx"
        if path not in os.listdir:
            print(f"找不到{path} 之資料，請先使用find_jobs & save_to_excel產生職位列表檔案")
            return
        self.job_links = pd.read_excel(path)
        return self.job_links
    
    def list2string(self, list_): #修改list資料變成string，因為在excel中比較好處理
        if type(list_) == str:
            return list_
        elif not list_:#空list
            return ""
        elif type(list_) == list:
            try:
                output = ",".join(list_)
            except:
                output = ""
            return output
        else:
            #print("型態錯誤，非list&str, 回傳空白")
            return ""
    
    #從個別職缺的網頁中取得資料
    def creep_job(self, url):
        res = requests.get(url, timeout=10)
        tree = html.fromstring(res.text)
        data_dict = {}
        title = tree.xpath("/html/body/div[2]/div/div[1]/div[2]/div/div/div[1]/h1")
        company = tree.xpath("/html/body/div[2]/div/div[1]/div[2]/div/div/div[1]/div/a[1]")
        work = tree.xpath("/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/p")
       
        data_dict["職務名稱"] = title[0].text.strip()
        #data_dict["公司名稱"] = company[0].text #上面好像有了
        for index in range(2,15):
            p1 = tree.xpath(f"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[{index}]/div[1]/h3")
            if p1:
                col_name = p1[0].text.strip()     
                xpath = self.xpath_match(col_name, index)
                data_dict[col_name] = []
            else:
                continue
            if not xpath:
                print(i, "no xpath")
                continue
            p2 = tree.xpath(xpath)
            for n in p2:
                data_dict[col_name].append(n.text.strip())
        
        #條件要求
        language = tree.xpath("/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[4]/div[2]/div/p")
        if not language[0].text: #代表並非"不拘"
            language_set = []
            language_set_e = tree.xpath("/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[4]/div[2]/div//*/a/u")
            for n in language_set_e:
                language_set.append(n.text)
        else:
            language_set = "不拘"
        data_dict["語文條件"] = self.list2string(language_set)

        for index in range(10):
            p1 = tree.xpath(f"/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[{index}]/div[1]/h3")
            if p1:
                col_name = p1[0].text.strip()
                if col_name not in data_dict.keys(): #避免蓋掉已經存在的部分
                    data_dict[col_name] = []
                xpath = self.xpath_match(col_name, index)
            else:
                continue
            if not xpath:
                continue
            p2 = tree.xpath(xpath)
            for n in p2:
                data_dict[col_name].append(n.text.strip())
        
        other_requirements = tree.xpath("/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div[3]/div/div[2]/div/div/p")


        #福利相關
        for index in range(1,8):
            p1 = tree.xpath(f"/html/body/div[2]/div/div[2]/div/div[1]/div[4]/div[{index}]/div/h3")
            if p1:
                col_name = p1[0].text.strip()
                data_dict[col_name] = []
                xpath = self.xpath_match(col_name, index)
            else:
                continue
            if not xpath:
                print(f"{col_name}: no xpath")
                continue
            p2 = tree.xpath(xpath)
            for n in p2:
                data_dict[col_name].append(n.text.strip())
        
        recruit_incentives = tree.xpath("/html/body/div[2]/div/div[2]/div/div[1]/div[4]/div[6]/div/p")#div6
        if recruit_incentives:
            data_dict["招募福利"] = recruit_incentives[0].text
            
        #薪資待遇拆解
        salary_dict = self.parse_salary(data_dict["工作待遇"][0])
        data_dict = {**data_dict, **salary_dict}

        return data_dict

    def find_jobs(self, max_jobs = -1):
        #爬取所有頁面的資料
        if max_jobs == -1:
            max_jobs = self.job_links.shape[0]
        data = []
        for i in range(self.job_links.shape[0]):
            company = self.job_links["公司名稱"].iloc[i]
            job = self.job_links["職缺名稱"].iloc[i]
            url = self.job_links["職缺連結"].iloc[i]
            dict_data_jobs = {
                "公司名稱" : company,
                "職缺名稱" : job,
                "職缺連結" : url
            }
            try:
                job_data = self.creep_job(url)
                job_data = {**dict_data_jobs, **job_data}
                data.append(job_data)
                print(f"正在爬取第{i+1}/{min(self.job_links.shape[0], max_jobs)}個工作")
            except KeyboardInterrupt:
                break
            except:
                continue
            if i >= max_jobs-1:
                break        
        fields =['公司名稱', '職缺名稱', '職缺連結', '職務名稱', '職務類別', '工作待遇',
                 '薪資型態', '薪資下限', '薪資上限',
                 '工作性質', '上班地點', '遠端工作', '管理責任', '出差外派', '上班時段',
                 '休假制度', '可上班日', '需求人數', '語文條件', '工作經歷', '學歷要求',
                 '科系要求', '擅長工具', '工作技能', '具備駕照', '具備證照', '法定項目',
                 '其他福利', '招募福利']
        df = pd.DataFrame(columns = fields, data = data)
        self.data = df.copy()
        #針對統計用欄位做處理
        self.data["語文條件"] = self.data["語文條件"].apply(lambda x : x.split(","))#拆分語言
        self.data["科系要求"] = self.data["科系要求"].apply(lambda x: x[0].split("、") if type(x) == list else x)
        self.data["具備駕照"] = self.data["具備駕照"].apply(lambda x: x[0].split("、") if type(x) == list else x)
        self.data["學歷要求"] = self.data["學歷要求"].apply(lambda x: x[0].split("、") if type(x) == list else x)
        self.jobs = df
        print("資料已爬取完畢，請用self.jobs檢視資料或以save_jobs儲存檔案")
        return self.jobs
    
    def save_jobs(self):
        if self.jobs is None:
            print("尚未爬取職位資料，請先find jobs")
            return
        for column in self.jobs.columns:
            self.jobs[column] = self.jobs[column].apply(self.list2string)
        path = self.keyword + r"-職位資料爬蟲.xlsx"
        self.jobs.to_excel(path, index = False)
        print(f"{path}資料已儲存")
        
    def show(self, column, top = 10):
        total = self.data.shape[0]
        if column == "all":#畫出全部的
            for column_ in self.data.columns:
                static = Counter(self.flatten(self.data[column_].dropna().tolist()))
                common = static.most_common()
                if not common:
                    print(f"{column_}: 資料不足無法繪圖")
                    continue
                self.draw(column_, data = common, total = total, top = top )
        else:
            static = Counter(self.flatten(self.data[column].dropna().tolist()))
            common = static.most_common()
            if not common:
                print(print(f"{column}: 資料不足無法繪圖"))
            self.draw(column, data = common, total = total, top = top )
    
    def flatten(self, list_):
        new_list = []
        for n in list_:
            if isinstance(n, list):
                new_list.extend(self.flatten(n))
            else:
                new_list.append(n)
        return new_list
    
    def draw(self, column, data, total, top = 10):
        # 使用中文字體
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
        plt.rcParams['axes.unicode_minus'] = False

        # 將技能和頻率分開，並計算百分比
        skills, frequencies = zip(*data[:top])
        percentages = [f/total*100 for f in frequencies]

        # 繪製水平條形圖
        plt.figure(figsize=(10,10))  # 設定圖形大小
        bars = plt.barh(skills, frequencies, color='skyblue')
        plt.xlabel('次數')  # x軸標籤
        plt.title(column)  # 圖形標題

        # 在條形旁邊添加百分比數據
        for bar, percentage in zip(bars, percentages):
            plt.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2, 
                     '{0:.1f}%'.format(percentage), va='center')

        # 顯示圖形
        plt.gca().invert_yaxis()  # 倒轉y軸，讓最高的頻率在頂部
        plt.show()
    
    def parse_salary(self, s):
        pattern_1 = r"(時薪|面議|月薪|年薪|論件計酬|日薪)([\d,]+)~([\d,]+)元"
        pattern_2 = r"(時薪|面議|月薪|年薪|論件計酬|日薪)([\d,]+)元以上"
        pattern_3 = r"(時薪|面議|月薪|年薪|論件計酬|日薪)([\d,]+)元"
        pattern_4 = r"待遇面議"

        if re.match(pattern_1, s):
            salary_type, min_salary, max_salary = re.match(pattern_1, s).groups()
            return {"薪資型態": salary_type, "薪資下限": min_salary, "薪資上限": max_salary}
        elif re.match(pattern_2, s):
            salary_type, min_salary = re.match(pattern_2, s).groups()
            return {"薪資型態": salary_type, "薪資下限": min_salary, "薪資上限": "無上限"}
        elif re.match(pattern_3, s):
            salary_type, salary = re.match(pattern_3, s).groups()
            return {"薪資型態": salary_type, "薪資下限": salary, "薪資上限": salary}
        elif re.match(pattern_4, s):
            return {"薪資型態": "待遇面議", "薪資下限": "面議", "薪資上限": "面議"}
        else:
            return {"薪資型態": "未知", "薪資下限": "未知", "薪資上限": "未知"}
    
    def draw_box(self):
        df = self.jobs.copy()
        # Filter the dataframe
        df = df[df['薪資型態'] == '月薪']
        df = df[(df['薪資下限'] != '面議') & (df['薪資上限'] != '面議')]
        # Replace '無上限' with '薪資下限'
        df.loc[df['薪資上限'] == '無上限', '薪資上限'] = df.loc[df['薪資上限'] == '無上限', '薪資下限']
        # Convert to numeric values
        df['薪資下限'] = df['薪資下限'].str.replace(',', '').astype(float)
        df['薪資上限'] = df['薪資上限'].str.replace(',', '').astype(float)
        # Plot boxplot
        df[['薪資下限', '薪資上限']].plot(kind='box')
        plt.title('月薪下限和上限的箱型圖')
        plt.ylabel('薪資')
        plt.show()
    
    def draw_density(self):
        df = self.jobs.copy()
        # Filter the dataframe
        df = df[df['薪資型態'] == '月薪']
        df = df[(df['薪資下限'] != '面議') & (df['薪資上限'] != '面議')]

        # Replace '無上限' with '薪資下限'
        df.loc[df['薪資上限'] == '無上限', '薪資上限'] = df.loc[df['薪資上限'] == '無上限', '薪資下限']

        # Convert to numeric values
        df['薪資下限'] = df['薪資下限'].str.replace(',', '').astype(float)
        df['薪資上限'] = df['薪資上限'].str.replace(',', '').astype(float)

        # Plot the kernel density estimation for salary lower and upper limit
        df['薪資下限'].plot(kind='kde', label='薪資下限')
        df['薪資上限'].plot(kind='kde', label='薪資上限')

        plt.title('月薪下限和上限的密度分佈')
        plt.xlabel('薪資')
        plt.ylabel('密度')
        plt.legend()
        plt.show()

if __name__ == "__main__":
    keyword = "數據分析師"
    jobs = Jobs(keyword)
    jobs.search_links(max_pages = 3)#一頁是20個職缺
    jobs.find_jobs()
    jobs.save_jobs()
    jobs.draw_box()
    jobs.draw_density()
    #jobs.show("all") #一次秀出全部
    jobs.show("職務類別")