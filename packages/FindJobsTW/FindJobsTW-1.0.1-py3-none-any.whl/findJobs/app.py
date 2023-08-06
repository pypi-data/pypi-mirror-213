from flask import Flask, render_template, request, redirect, url_for
import webbrowser
from threading import Timer
from .url import search_url
import pandas as pd
from .FindJobs import Jobs

app = Flask(__name__)



def findjobs(conditions):
    text = f"findjobs function has been executed with:<br>" 
    for k,v in conditions.items():
        text += f"{k}: {v}<br>"
    return text

@app.route('/', methods=['GET', 'POST'])
def home():
    message = ''
    global JobKeyword
    JobKeyword = ''
    global jobNumber
    jobNumber = ''
    global job_type
    job_type = ''
    global area_condition
    area_condition = ''
    global update_date
    update_date = ''
    global attendance_system
    attendance_system = ''
    global salarytype
    salarytype = ''
    global salary_condition
    salary_condition = ''
    global custom_salary_min
    custom_salary_min = ''
    global custom_salary_max
    custom_salary_max = ''
    global experience
    experience = ''
    message = ""
    df = None
    table = None
    if request.method == 'POST':
        if 'clear' in request.form:
            # 如果按下了 "清除" 按鈕，將所有的模板變數設為空
            return render_template('index.html', message="", 
                           table = "",
                           current_JobKeyword = "",
                           current_JobNumber = "",
                           current_job_type="", 
                           current_area_condition = "",
                           current_update_date = "",
                           current_attendance_system = "",
                           current_salarytype = "",
                           current_salary_condition = "",
                           current_custom_salary_min = "",
                           current_custom_salary_max = "",
                           current_experience = "")
        JobKeyword = request.form.get('JobKeyword')
        jobNumber = request.form.get('JobNumber')
        job_type = request.form.get('job_type')
        area_condition = request.form.getlist('area_condition')
        update_date = request.form.get('update_date')
        attendance_system = request.form.get('attendance_system')
        salarytype = request.form.get('salarytype')
        salary_condition = request.form.get('salary_condition')
        custom_salary_min = request.form.get('custom_salary_min')
        custom_salary_max = request.form.get('custom_salary_max')
        experience = request.form.get('experience')
        conditions = {}
        conditions["關鍵字"] = JobKeyword
        conditions["搜尋數量"] = jobNumber
        conditions["職務類別"] = job_type
        conditions["地區條件"] = area_condition
        conditions["更新日期"] = update_date
        conditions["薪資類型"] = salarytype
        conditions["薪資待遇"] = salary_condition
        conditions["薪資下限"] = custom_salary_min
        conditions["薪資上限"] = custom_salary_max
        conditions["經歷要求"] = experience
        print(conditions)
        url = search_url(conditions)
        print(url)
        message = findjobs(conditions)
        
        job = Jobs(JobKeyword)
        job.search_links(max_pages=int(int(jobNumber)/20)+1, ori_url = url)
        job.find_jobs(max_jobs = int(jobNumber))
        job.save_jobs()
        df = job.jobs.head(10)
        table = df.to_html(classes='data', header="true", index="false")
        
    
    return render_template('index.html', message=message, 
                           table = table,
                           current_JobKeyword = JobKeyword,
                           current_JobNumber = jobNumber,
                           current_job_type=job_type, 
                           current_area_condition = area_condition,
                           current_update_date = update_date,
                           current_attendance_system = attendance_system,
                           current_salarytype = salarytype,
                           current_salary_condition = salary_condition,
                           current_custom_salary_min = custom_salary_min,
                           current_custom_salary_max = custom_salary_max,
                           current_experience = experience)

@app.route('/execute')
def execute_findjobs():
    result = findjobs()
    if result is None:
        result = "No result returned from findjobs"
    return render_template('index.html', message=result)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)