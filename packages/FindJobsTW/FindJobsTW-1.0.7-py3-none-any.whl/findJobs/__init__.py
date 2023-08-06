from flask import Flask
from .app import app

def create_app():
    # app 是從 app.py 中匯入的 Flask 應用
    return app

def help():
    print("在瀏覽器中執行請參考下列代碼:")
    print()
    text1 = '''
        from threading import Timer
        import webbrowser
        from findJobs import create_app, hlep

        def open_browser():
            webbrowser.open_new('http://127.0.0.1:5000/')

        app = create_app()

        if __name__ == '__main__':
            Timer(1, open_browser).start()
            app.run(debug=True, use_reloader=False)
        '''
    print(text1)
    print()
    print()
    print("直接於程式碼中執行，請參考下列代碼:")
    print()
    text2 = '''
        from findJobs.FindJobs import Jobs
        keyword = "ESG"
        job = Jobs(keyword)
        job.search_links(max_pages=1) #設定爬取的頁數，一頁20個
        job.find_jobs()#找工作
        job.save_jobs()#把找到的工作存成excel檔案
        job.draw_box()
        job.draw_density()
        job.show(column = "all") #查看想統計的欄位，如果欄位名稱輸入"all"，會統計所有欄位，
        #若要快速關閉視窗可按ctrl+w
        '''
    print(text2)
    print()