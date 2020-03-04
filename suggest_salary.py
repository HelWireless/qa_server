import math
from setting.config import edu_map, csv_path

def suggest_salary(jobInfo, userInfo, similarity, base_salary):
    try:
        if jobInfo['negotiable'] is False and float(jobInfo['salaryMin']) >= 8 and float(jobInfo['salaryMax']) <= 500:
            salary_min = jobInfo['salaryMin']
            salary_max = jobInfo['salaryMax']
        else:
            salary_min = base_salary[base_salary.func_name == jobInfo['name']].salary_from.values[0]
            salary_max = base_salary[base_salary.func_name == jobInfo['name']].salary_to.values[0]
    except:
        salary_min = base_salary[base_salary.func_name == jobInfo['name']].salary_from.values[0]
        salary_max = base_salary[base_salary.func_name == jobInfo['name']].salary_to.values[0]

        # 工作城市
    user_city = userInfo['city']
    com_city = jobInfo['city']

    try:
        user_edu = userInfo['education']

    except:
        user_edu = 0

    try:
        edu_must = edu_map[[i['name'] for i in match_score_data['jobInfo']['education'] if i['must'] == True][0]]
    except:
        edu_must = 6

    try:
        edu_pre = edu_map[[i['name'] for i in match_score_data['jobInfo']['education'] if i['must'] == False][0]]
    except:
        edu_pre = 10

    # 工作年限要求
    user_exp = userInfo['workExperience']
    com_exp = jobInfo['workExperienceMin']

    if user_exp > 10:
        user_exp = 10
    else:
        pass

    # 相似度
    for i in similarity:
        if (similarity[i] is None) or (similarity[i] == "nan"):
            similarity[i] = 0
        else:
            similarity[i] = float(similarity[i])

    des_sim = similarity['describes']
    ski_sim = similarity['skills']
    ti_sim = similarity['title']

    salary_dif = salary_max-salary_min

    # 工作年限规则
    exp_dif = com_exp-user_exp
    if exp_dif < -com_exp:
        salary_min_exp = salary_min+abs(exp_dif)*2
    elif -com_exp <= exp_dif < 0:
        salary_min_exp = salary_min+abs(exp_dif)
    elif exp_dif == 0:
        salary_min_exp = salary_min
    elif 0 < exp_dif <= 2:
        salary_min_exp = salary_min-3*exp_dif
    else:
        salary_min_exp = salary_min*0.6

    if salary_min_exp >= salary_min:
        salary_min_exp = salary_min+(salary_min_exp-salary_min)/3*0.25*salary_dif
    else:
        pass

    # 学历规则：
    edu_must_dif = edu_must-user_edu
    edu_pre_dif = edu_pre-user_edu
    if edu_must_dif < 0:
        if edu_pre_dif < 0:
            salary_min_edu = salary_min+abs(edu_pre_dif)*2
        else:
            salary_min_edu = salary_min+1
    elif edu_must_dif == 0:
        salary_min_edu = salary_min
    elif edu_must_dif == 1:
        salary_min_edu = salary_min-4
    else:
        salary_min_edu = salary_min*0.6

    if salary_min_edu >= salary_min:
        salary_min_edu = salary_min+(salary_min_edu-salary_min)/2*0.25*salary_dif
    else:
        pass

    # 判断学历和工作年限和salary_min的关系
    if (salary_min_edu <= salary_min) or (salary_min_exp <= salary_min):
        salary_min_new = min(salary_min_edu, salary_min_exp)
    else:
        salary_min_dif = (salary_min_exp-salary_min)+(salary_min_edu-salary_min)
        salary_min_new = salary_min+salary_min_dif

    # 城市规则
    if user_city == com_city:
        salary_min_new = salary_min_new
    else:
        salary_min_new = salary_min_new-2

    # # 学历规则
    # if user_edu >= edu_must:
    #     if user_edu >= edu_pre:
    #         salary_min_new += 2.5
    #     else:
    #         salary_min_new += 0.5
    # else:
    #     salary_min_new -= 4

    # #工作经历规则
    # if user_exp >= com_exp:
    #     salary_min_new += 1
    # else:
    #     exp_dif = com_exp-user_exp
    #     salary_min_new = salary_min_new-exp_dif*2

    # 相似度规则

    # 描述相似度
    if des_sim >= 0.75:
        salary_min_des = salary_min_new+des_sim*4
    else:
        salary_min_des = salary_min_new-(1-des_sim)*3

    if salary_min_des > salary_min_new:
        salary_min_new = salary_min_new+(salary_min_des-salary_min_new)/3*0.2*salary_dif
    else:
        salary_min_new = salary_min_des

    # 技能相似度
    if ski_sim >= 0.6:
        salary_min_ski = salary_min_new+ski_sim*3
    else:
        salary_min_ski = salary_min_new-(1-ski_sim)*2

    if salary_min_ski > salary_min_new:
        salary_min_new = salary_min_new+(salary_min_ski-salary_min_new)*0.1*salary_dif
    else:
        salary_min_new = salary_min_ski

    salary_min_new = salary_min_new-(1-ti_sim)*10
    salary_max_new = salary_min_new+(salary_max-salary_min)*ti_sim*0.5

    if salary_min_new < 8:
        salary_min_new = 8
        salary_max_new = 8+(salary_max-salary_min)*ti_sim*0.5
    else:
        pass

    if ti_sim < 0.77:
        if_output = False
    else:
        if_output = True

    salary_dic = {}
    salary_dic['suggestSalaryMin'] = math.floor(salary_min_new)
    salary_dic['suggestSalaryMax'] = math.ceil(salary_max_new)
    salary_dic['ifOutput'] = if_output

    return salary_dic


def match_score(salary_dict, match_score_data, skill_not_need):
    """
    :param salary_dict: {'suggestSalaryMin': 9, 'suggestSalaryMax': 11, 'if_output': False}
    :param match_score_data:
    :return: {MatchScore:1, }
    """
    # 初始匹配度
    org_match_score = 19

    # 工作城市
    user_city = match_score_data['userInfo']['city']
    com_city = match_score_data['jobInfo']['city']

    if user_city == com_city:
        org_match_score += 2

    # 学历要求
    user_edu = match_score_data['userInfo']['education']
    try:
        edu_must = edu_map[[i['name'] for i in match_score_data['jobInfo']['education'] if i['must'] == True][0]]
    except:
        edu_must = 5
    try:
        edu_pre = edu_map[[i['name'] for i in match_score_data['jobInfo']['education'] if i['must'] == False][0]]
    except:
        edu_pre = 10

    # 行业加分
    try:
        user_industry = match_score_data['userInfo']['industry']
        industry_tmps = match_score_data['jobInfo']['industry']
        job_industry_tmp = []
        if industry_tmps.__len__() >0:
            for i in industry_tmps:
                job_industry_tmp.append(i['name'])
            job_industry = "".join(job_industry_tmp)
        else:
            job_industry = ""
        industry_score = 0
        for i in user_industry.split("/"):
            if i in job_industry:
                industry_score += 1
        if industry_score >= 5 : industry_score = 5
    except:
        industry_score = 0

    org_match_score += industry_score

    # 工作年限要求
    user_exp = match_score_data['userInfo']['workExperience']
    com_exp = match_score_data['jobInfo']['workExperienceMin']


    # 相似度
    similarity = match_score_data["similarityInfo"]
    for i in similarity:
        if (similarity[i] is None) or (similarity[i] == "nan"):
            similarity[i] = 0
        else:
            similarity[i] = float(similarity[i])

    des_sim = similarity['describes']
    skill = similarity['skills']
    title_sim = similarity['title']

    # 教育加分
    edu_tmp = (user_edu - edu_must)
    if edu_tmp >= 2:
        if user_edu >= edu_pre:
            org_match_score += 3
        else:
            org_match_score += 1
    elif 2 > edu_tmp >= 0:
        if user_edu >= edu_pre:
            org_match_score += 1
    elif edu_tmp <= -2:
        org_match_score -= 12
    else:
        org_match_score -= 6

    # 工作年限加分
    exp_tmp = (user_exp - com_exp)
    if exp_tmp >= 3:
        org_match_score += 6
    elif 3 > exp_tmp >= 0:
        org_match_score += 2
    elif exp_tmp<= -3:
        org_match_score -= 12
    else:
        org_match_score -= 6



    # title_sim 惩罚
    if title_sim < 0.912:
        title_tmp_sim = -0.5
        #des_sim += 0.2
        skill += 0.1
    else:
        title_tmp_sim = title_sim

    # 内容过度不一致，对整体做惩罚
    if des_sim <= 0.15:
        des_sim = -1
    elif 0.15 < des_sim <= 0.3:
        des_sim = -0.3
    elif des_sim >= 0.96:
        des_sim = -0.5
    elif 0.3 < des_sim <= 0.4:
        des_sim = des_sim**5
    elif 0.4 < des_sim <= 0.5:
        des_sim = des_sim**4
    elif 0.5 < des_sim <= 0.6:
        des_sim = des_sim**3
    elif 0.6 < des_sim <= 0.7:
        des_sim = des_sim**2
    else:
        des_sim += 0.1



    if skill_not_need: skill += 0.2

    tmp_score = des_sim*12 + skill*6 + 10 * title_tmp_sim
    org_match_score += tmp_score
    if (salary_dict["ifOutput"]) and (org_match_score <= 30): org_match_score += 3
    MatchScore = (org_match_score*100)/60
    if MatchScore <= 40: MatchScore = 40 + title_sim*5 + user_edu*0.8
    if MatchScore >= 95: MatchScore = 98 - skill*title_sim*10

    temp_dict = {"matchScore": round(MatchScore, 1)}

    salary_dict.update(temp_dict)
    return salary_dict


if __name__ == "__main__":
    import pandas as pd
    base_salary = pd.read_csv(csv_path)

    #salary_dict = {'suggestSalaryMin': 9, 'suggestSalaryMax': 11, 'ifOutput': True}
    match_score_data = {
             'jobInfo':
                  {'name': '高级ios开发工程师', 'city': '上海', 'salaryMin': 22.0, 'salaryMax': 40.0,
                   'education': [{'id': 5, 'must': True, 'name': '本科'}, {'id': 4, 'must': False, 'name': '硕士'}],
                   'negotiable': False, 'workExperienceMin': 6,
                   'industry': [{'id': 15, 'must': True, 'name': '互联网/移动互联网/电子商务', 'year': 1}, {'id': 15, 'must': False, 'name': '互联网/移动互联网/电子商务', 'year': 1}]},
              'userInfo': {'education': 6, 'jobTitle': '高级ios开发工程师', 'workExperience': 6, 'city': '上海', 'JobSimilarity': 0.8979574, 'industry': '互联网/移动互联网/电子商务'},
              'similarityInfo': {'describes': '0.707274', 'skills': '0.4', 'title': '1'}
            }
    salary_dic = suggest_salary(match_score_data['jobInfo'], match_score_data['userInfo'], match_score_data['similarityInfo'], base_salary)
    b = match_score(salary_dic, match_score_data, False)
    print(b)
