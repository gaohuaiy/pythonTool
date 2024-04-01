import requests  
  
# Jira的REST API地址  
url = "http://jira.xquant.com:8888/issues/?filter=28446"  
  
# 请求头信息  
headers = {  
    "Host":"jira.xquant.com:8888",
    "Origin":"http://jira.xquant.com:8888",
    "Referer":"http://jira.xquant.com:8888/issues/?filter=28446",
    "Cookie":"seraph.rememberme.cookie=79144%3A6d43b021fddc2409f93410cce27975387c50c35e; JSESSIONID=2D5E132EC4D3257431DAFDD0F144F15E; atlassian.xsrf.token=B0RE-6DUN-05MB-NLYY_a0c1d75f19e10b4fc858af2d2f804ed40d54461f_lin"
}  
data = {
    "startIndex": 0,
    "filterId": "28446",
    "jql": 'project = P013XEQ AND issuetype = 标准需求 AND status in (新建, 需求分析, 待开发, 重新打开, 待测试, 待提交) AND fixVersion = "恒利EQ 1.0.5" ORDER BY status DESC, created DESC',
    "layoutKey": "list-view",
}
# 发送GET请求并获取响应  
response = requests.post(url, headers=headers,data=data)  
  
# 解析响应内容并打印问题列表  
print(response.text)
# issues = response.json()['issues']  
# for issue in issues:  
#     print(issue['key'])