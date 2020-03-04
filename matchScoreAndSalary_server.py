import logging
from datetime import datetime
from flask import Flask, jsonify, request
from setting.config import csv_path, get_similarity_url
from suggest_salary import match_score, suggest_salary
from utils import *
import pandas as pd
from setting.mlogging import MidnightRotatingFileHandler


app = Flask(__name__)
# # 获得项目根目录
# logging.basicConfig(level=logging.INFO, filemode='a',
#                     filename="./logs/uwsgi.log",
#                     format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
# # logger = logging.getLogger(__name__)
# logger = mlogging.Logger(filename='test.log', level='debug')

def register_log():
    fmt =  "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    if False:
        handler = logging.StreamHandler(sys.stdout)
    else:
        handler = MidnightRotatingFileHandler('./logs/app_logs/app.log')
        # handler = RotatingFileHandler("access1.log", maxBytes=100 * 1024, backupCount=5)

    logging.basicConfig(
        level=logging.INFO,
        format=fmt,
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[handler]
    )
    logging.getLogger(__name__)

register_log()

logger = logging.getLogger(__name__)


@app.route('/')
def hello_world():
    return 'Hello welcome to match Score and suggest salary server!'

@app.route('/match_score_and_salary/', methods=["POST", "GET"])
def match_score_and_salary():
    success = 0
    # try:
    # 数据接收
    base_salary = pd.read_csv(csv_path)
    origal_data = request.get_json()
    jobInfo = origal_data["jobInfo"]
    userInfo = origal_data["userInfo"]
    logger.info("{}, INFO: original data :origal_data:{},success:{}".format(
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'), origal_data, success))
    try:
        # 数据处理
        similarity_data, skill_not_need = process_similarity_data(jobInfo, userInfo)
        user_similarity = get_similarity(get_similarity_url, similarity_data)
        success += 1  # 记录错误位置
        logger.info("{}, INFO: get similarity data :similarity:{},  get_similarity:{},success:{}".format(
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'), similarity_data, user_similarity, success))

        suggest_salary_data, match_score_data = process_match_and_salary_data(user_similarity, jobInfo,
                                                                              userInfo)


        success += 1  # 记录错误位置
        logger.info("{}, INFO: get user similarity data :{}, success:{}".format(
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'), suggest_salary_data, success))

        # 薪资与匹配度

        salary_dict = suggest_salary(suggest_salary_data['jobInfo'], suggest_salary_data['userInfo'],
                                     suggest_salary_data['similarityInfo'], base_salary)
        match_score_and_salary_dict = match_score(salary_dict, match_score_data, skill_not_need)

        # 拼接最终结果
        success += 1  # 记录错误位置
        match_score_and_salary_dict["success"] = True
        match_score_and_salary_dict["tpye"] = 'qa_env'
        logger.info("{}, INFO: the last match score and salary data :{} , success:{}".format(
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'), match_score_and_salary_dict, success))

        return jsonify(match_score_and_salary_dict)
    except:
        logger.exception('when process match score , we find a error')
        match_score_and_salary_dict = {"ifOutput": False, "matchScore": 49.6, "success": False, "suggestSalaryMax":0, "suggestSalaryMin":0}
        return jsonify(match_score_and_salary_dict)



if __name__ == '__main__':
    app.run(debug=False, port=5004)
