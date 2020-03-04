# -*- coding:utf-8 -*-
""" 
Author:hel 
License: Apache Licence 
File: utils.py 
Time: 2019/10/23
Version: 1.0
@Function:
"""

import json
import requests
from setting.config import edu_map


def process_similarity_data(job_dict, user_dict):
    """
    :param job_dict: from jobInfo
    :param user_dict: from userInfo
    :return: similarity_data
    """


    # join  skill list
    user_skill_list = []
    job_skill_list = []
    try:
        for each_skill in user_dict["skill"]:
            user_skill_list.append(each_skill["name"])
        user_skill = ",".join(user_skill_list)
    except:
        user_skill = None

    try:
        for each_skill in job_dict["skill"]:
            job_skill_list.append(each_skill["name"])
        job_skill = ",".join(job_skill_list)
    except:
        job_skill = None

    if job_skill is None:
         skill_not_need = True
    else:
         skill_not_need = False


    # join experience info dict
    user_experiences = {}

    for index, each_businessBackgroundInfo in enumerate(user_dict["businessBackgroundInfos"]):
        user_experiences["experience"+str(index)] = {}
        user_experiences["experience"+str(index)]["title"] = user_dict["jobTitle"]
        user_experiences["experience"+str(index)]["describe"] = each_businessBackgroundInfo["description"]
        user_experiences["experience"+str(index)]["skill"] = user_skill

    # join job info dict
    job_info = {}
    job_info["title"] = job_dict["name"]
    job_info["describe"] = job_dict["description"]
    job_info["skill"] = job_skill

    # generate similarity dict
    similarity_data = {"简历信息": {}, "工作信息": {}}
    similarity_data["简历信息"]["user_info"] = user_experiences
    similarity_data["工作信息"]["job_info"] = job_info

    return similarity_data, skill_not_need


def process_match_and_salary_data(similarity_dict, job_dict, user_dict):
    # create suggest salary dict and match_score
    suggest_salary = {"jobInfo": {}, "userInfo": {}}
    match_score = {"jobInfo": {}, "userInfo": {}}

    # suggest salary jobInfo
    suggest_salary["jobInfo"]["name"] = job_dict["orgName"]
    suggest_salary["jobInfo"]["city"] = job_dict["city"]
    suggest_salary["jobInfo"]["salaryMin"] = job_dict["salaryMin"]
    suggest_salary["jobInfo"]["salaryMax"] = job_dict["salaryMax"]
    suggest_salary["jobInfo"]["education"] = job_dict["education"]
    suggest_salary["jobInfo"]["negotiable"] = job_dict["negotiable"]
    suggest_salary["jobInfo"]["workExperienceMin"] = job_dict["workExperienceMin"]
    suggest_salary["jobInfo"]["industry"] = job_dict["industry"]


    # education
    try:
        edu_lst = []
        for i in user_dict["educationBackgroundInfos"]:
            edu_lst.append(edu_map[i["education"]])
        suggest_salary["userInfo"]["education"] = max(edu_lst)
    except:
        suggest_salary["userInfo"]["education"] = edu_map[user_dict["education"]]


    # suggest salary userInfo
    suggest_salary["userInfo"]["jobTitle"] = user_dict["orgJobTitle"]
    suggest_salary["userInfo"]["workExperience"] = user_dict["workExperience"]
    suggest_salary["userInfo"]["city"] = user_dict["city"]
    suggest_salary["userInfo"]["JobSimilarity"] = job_dict["jobSimilarity"]
    suggest_salary["userInfo"]["industry"] = user_dict["industry"]

    # suggest salary similarityInfo
    suggest_salary["similarityInfo"] = similarity_dict["user_info"]["job_info"]

    # match score jobInfo
    match_score["jobInfo"] = suggest_salary["jobInfo"]


    # match score userInfo
    match_score["userInfo"] = suggest_salary["userInfo"]

    # match score similarityInfo
    match_score["similarityInfo"] = suggest_salary["similarityInfo"]

    return suggest_salary, match_score


def get_similarity(url, data, timeout=20):
    """
    :param url: api address
    :param data: api data structure
    :param timeout: default 20
    :return: {user_info': {
                  'job_info': {
                                'describes': '0.4152254',
                                'skills': '0.8542752228029453',
                                'title': '1'
                              }
                          }
             }
    """
    headers = {"Content-Type": "application/json"}
    data1 = json.dumps(data)
    try:
        r = requests.post(url, data=data1, headers=headers, timeout=timeout)
        return r.json()
    except:
        similarity_dict= {'user_info':
                                {'job_info':
                                           {'describes': '0.5052254',
                                            'skills': '0.5042752228029453',
                                            'title': '0.95'}
                                }
                         }
        return similarity_dict






if __name__ == "__main__":
    data ={'jobInfo': {'addPost': True, 'assistants': [], 'businessBackground': None, 'city': '上海', 'cityId': 310000, 'code': None, 'companyId': 8464, 'createTime': 1574934824000, 'departmentId': 240, 'departmentName': '技术部门', 'description': '1123123123131', 'diathesis': None, 'education': [{'id': 5, 'must': True, 'name': '本科'}], 'enterpriseInfo': {'associates': '李云龙2', 'associatesId': 21, 'cellphone': '15000000132', 'companyFinance': '无需融资', 'companyId': 8464, 'companyLogo': 'https://tarsimg.tinyzk.com/crm/977a199deb934a3a959a702492a3aa2b.png', 'companyNature': '民营企业', 'contactEmail': '20191120@kyms.com', 'contactName': '永迪2', 'crmFollowerInfo': None, 'expirationBegin': '2019-11-20', 'expirationEnd': '2031-03-20', 'id': 120, 'industry': '互联网/移动互联网/电子商务', 'name': '湖南左右市场研究有限公司', 'size': '20-99人', 'telephone': '0210212131132'}, 'function': '技术', 'functionId': 2, 'headCount': 1, 'id': 40836, 'industry': [{'id': 15, 'must': True, 'name': '互联网/移动互联网/电子商务', 'year': 3}], 'jobSimilarity': 1.0, 'name': 'ios', 'negotiable': True, 'orgName': '高级ios开发工程师', 'publish': {'email': '20191120@kyms.com', 'id': 218, 'name': '永迪2', 'phone': '15000000132', 'telephone': '0210212131132'}, 'reportTo': '项目经理', 'salaryMax': None, 'salaryMin': None, 'shareOption': None, 'skill': None, 'status': 1, 'stockRight': None, 'updateTime': 1575708813000, 'workExperienceMax': None, 'workExperienceMin': 2}, 'userInfo': {'age': 33, 'businessBackgroundInfos': [{'beginDate': '2019-03', 'city': '上海', 'cityId': 310000, 'company': 'IBM', 'companyId': 197895, 'companyUrl': 'https://img.tinyzk.com/company_logo/7f5c348fee12035ed29945ead35415aa', 'description': 'iOS %', 'endDate': '4000-01', 'id': 284, 'industry': '互联网/移动互联网/电子商务', 'industryId': 15, 'jobSimilarity': 1.0, 'jobTitle': '高级ios开发工程师', 'jobTitleId': 96, 'more': None, 'orgJobTitle': '高级ios开发工程师', 'salary': None, 'salaryNumber': None, 'shareOption': False, 'stockRight': False, 'superior': None, 'underling': 0}, {'beginDate': '2017-08', 'city': '上海', 'cityId': 310000, 'company': '阿里云计算有限公司', 'companyId': 1261, 'companyUrl': 'https://img.tinyzk.com/company_logo/59b94e1f80dcef5afe741e5206bae6a8', 'description': 'iOS', 'endDate': '2019-03', 'id': 286, 'industry': '互联网/移动互联网/电子商务', 'industryId': 15, 'jobSimilarity': 1.0, 'jobTitle': '高级ios开发工程师', 'jobTitleId': 96, 'more': None, 'orgJobTitle': '高级ios开发工程师', 'salary': None, 'salaryNumber': None, 'shareOption': False, 'stockRight': False, 'superior': None, 'underling': 0}, {'beginDate': '2015-05', 'city': '上海', 'cityId': 310000, 'company': '上海小砖块网络科技有限公司', 'companyId': 196608, 'companyUrl': 'https://img.tinyzk.com/image/company_logo/61dd7d0e19c371a2937a691512644c11', 'description': '1、负责iOS平台客户端软件的开发和优化；\n2、研究新兴技术满足产品需求；\n3、参与项目重点、难点的技术攻坚；\n4、参与相关系统文档的撰写和维护；\n5、根据研发过程中的体验对产品提出建议；', 'endDate': '2017-06', 'id': 212, 'industry': '互联网/移动互联网/电子商务', 'industryId': 15, 'jobSimilarity': 1.0, 'jobTitle': '高级ios开发工程师', 'jobTitleId': 96, 'more': None, 'orgJobTitle': '高级ios开发工程师', 'salary': None, 'salaryNumber': None, 'shareOption': False, 'stockRight': False, 'superior': None, 'underling': 0}, {'beginDate': '2012-03', 'city': '上海', 'cityId': 310000, 'company': '谷歌(google)', 'companyId': 196851, 'companyUrl': 'https://img.tinyzk.com/company_logo/dfd787060575ac6712be154eb9bfa07d', 'description': 'iOS\n', 'endDate': '2015-03', 'id': 248, 'industry': '互联网/移动互联网/电子商务', 'industryId': 15, 'jobSimilarity': 1.0, 'jobTitle': '高级ios开发工程师', 'jobTitleId': 96, 'more': None, 'orgJobTitle': '高级ios开发工程师', 'salary': None, 'salaryNumber': None, 'shareOption': False, 'stockRight': False, 'superior': None, 'underling': 0}], 'careerMotivation': '{"ach":4,"aff":4,"pwr":9}', 'city': '上海', 'company': '谷歌(google)', 'completion': 100, 'createToday': False, 'education': '硕士', 'educationBackgroundInfos': [{'beginDate': '2014-09', 'education': '硕士', 'educationId': 4, 'endDate': '2017-07', 'enrollment': True, 'id': 249, 'profession': '数学类', 'professionId': 30, 'school': '上海外国语大学', 'schoolId': 16419, 'schoolUrl': 'https://img.tinyzk.com/image/gndx/c7474fbbeead7ce247ba9ca5e45940ce'}, {'beginDate': '2009-09', 'education': '本科', 'educationId': 5, 'endDate': '2013-07', 'enrollment': True, 'id': 243, 'profession': '数据科学', 'professionId': 636, 'school': '多伦多大学', 'schoolId': 17435, 'schoolUrl': 'https://img.tinyzk.com/image/hwdx/1955820a6bd71187dc2b91090cda50cb'}], 'email': None, 'gender': 1, 'id': 1, 'ifOutput': None, 'imgUrl': None, 'industry': '互联网/移动互联网/电子商务', 'jobIntention': '积极看新机会', 'jobSimilarity': 1.0, 'jobStatus': None, 'jobTitle': '高级ios开发工程师', 'matching': None, 'name': 'Ryan', 'orgJobTitle': '高级ios开发工程师', 'phone': '17040992580', 'privacy': {'contactTime': '随时联系', 'showEmail': False, 'showName': True, 'showPortrayal': False, 'showSalary': False, 'userShieldCompanyInfos': []}, 'salaryMax': None, 'salaryMin': None, 'school': '上海外国语大学', 'skill': [{'id': 1162, 'name': 'ios开发'}, {'id': 2211, 'name': 'swift'}, {'id': 1555, 'name': 'git'}], 'suggestSalaryMax': None, 'suggestSalaryMin': None, 'userExpectInfos': {'bindWeixin': False, 'expectAnnualSalary': 15.5, 'expectCities': None, 'expectIndustries': None, 'expectJobTitles': None, 'interviewSms': '19:00', 'inviteSms': False, 'jobIntention': '积极看新机会', 'jobIntentionId': 1, 'jobStatus': 0, 'progressSms': False}, 'workExperience': 10}}
    url = r'http://127.0.0.1:5000/get_similarity'
    similarity_data = process_similarity_data(data["jobInfo"], data["userInfo"])
    print(similarity_data)
    user_similarity = get_similarity(url, similarity_data)

    suggest_salary_data, match_score_data = process_match_and_salary_data(user_similarity, data["jobInfo"],
                                                                          data["userInfo"])
    print(json.dumps(match_score_data))

    salary_dic = suggest_salary(suggest_salary_data['jobInfo'], suggest_salary_data['userInfo'],
                                suggest_salary_data['similarityInfo'], base_salary)
    result = match_score(salary_dic, match_score_data)
    print(match_score_data)

