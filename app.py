from pymongo import MongoClient
from flask import Flask, app, render_template

app = Flask(__name__)

@app.route('/')
def SortLocation():
    # region MongoDB配置
    conn = MongoClient('localhost', 27017)
    db = conn['QSTHERanking']  # 建立数据库
    my_set_QS = db['QSRanking2020']  # 集合相当于表
    # endregion
    #region 按国家分类统计
    nation_num = []
    nation = my_set_QS.find().distinct('location')    #各个国家的数量
    for country in nation:
        nation_num.append({'name':country, 'value':my_set_QS.find({'location':country}).count()})
    # data = []
    # for i in range(0, 28):
    #     data.append({'name': nation[i], 'value': num[i]})
    nation_num = sorted(nation_num, key=lambda x: x['value'], reverse=True)[0:10]
    #endregion
    # region 取美国三个小分的中位数
    US_Scores = my_set_QS.find({"location": " United States"})   #得到美国学校
    sorted_US_S = sorted(US_Scores, key=lambda x : x['citationPstuff'])
    citScore = sorted_US_S[len(sorted_US_S) // 2]['citationPstuff']

    US_Scores2 = my_set_QS.find({"location": " United States"})
    sorted_US_S2 = sorted(US_Scores2, key=lambda x: x['IntStudent'])
    IntStuScore = sorted_US_S2[len(sorted_US_S2) // 2]['IntStudent']

    US_Scores3 = my_set_QS.find({"location": " United States"})
    sorted_US_S3 = sorted(US_Scores3, key=lambda x: x['IntStuff'])
    IntStuffScore = sorted_US_S3[len(sorted_US_S3) // 2]['IntStuff']
    #endregion
    # region 取英国三个小分的中位数
    UK_Scores = my_set_QS.find({"location": " United Kingdom"})  # 得到美国学校
    sorted_UK_S = sorted(UK_Scores, key=lambda x: x['citationPstuff'])
    UK_citScore = sorted_UK_S[len(sorted_UK_S) // 2]['citationPstuff']

    UK_Scores2 = my_set_QS.find({"location": " United Kingdom"})
    sorted_UK_S2 = sorted(UK_Scores2, key=lambda x: x['IntStudent'])
    UK_IntStuScore = sorted_UK_S2[len(sorted_UK_S2) // 2]['IntStudent']

    UK_Scores3 = my_set_QS.find({"location": " United Kingdom"})
    sorted_UK_S3 = sorted(UK_Scores3, key=lambda x: x['IntStuff'])
    UK_IntStuffScore = sorted_UK_S3[len(sorted_UK_S3) // 2]['IntStuff']
    # endregion
    # region 取中国三个小分的中位数
    CHI_Scores = my_set_QS.find({"location": " China (Mainland)"})  # 得到美国学校
    sorted_CHI_S = sorted(CHI_Scores, key=lambda x: x['citationPstuff'])
    CHI_citScore = sorted_CHI_S[len(sorted_CHI_S) // 2]['citationPstuff']

    CHI_Scores2 = my_set_QS.find({"location": " China (Mainland)"})
    sorted_CHI_S2 = sorted(CHI_Scores2, key=lambda x: x['IntStudent'])
    CHI_IntStuScore = sorted_UK_S2[len(sorted_CHI_S2) // 2]['IntStudent']

    CHI_Scores3 = my_set_QS.find({"location": " China (Mainland)"})
    sorted_CHI_S3 = sorted(CHI_Scores3, key=lambda x: x['IntStuff'])
    CHI_IntStuffScore = sorted_UK_S3[len(sorted_CHI_S3) // 2]['IntStuff']
    # endregion
    #region 封装三个国家数据
    US_3scores = [citScore, IntStuScore, IntStuffScore]
    UK_3scores = [UK_citScore, UK_IntStuScore, UK_IntStuffScore]
    CHI_3scores = [CHI_citScore, CHI_IntStuScore, CHI_IntStuffScore]
    #endregion
    return render_template('index.html', data=nation_num, nation = [x['name'] for x in nation_num], US_3scores = US_3scores, UK_3scores = UK_3scores, CHI_3scores = CHI_3scores)

if __name__ == '__main__':
    app.run()
