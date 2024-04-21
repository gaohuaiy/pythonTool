import requests  
import json  
  
def delete_repository(owner, repo_name, access_token):  
    """  
    删除一个GitHub仓库  
    :param owner: 仓库的所有者用户名或组织名  
    :param repo_name: 仓库名  
    :param access_token: GitHub个人访问令牌  
    :return: 删除操作的结果  
    """  
    url = f"https://api.github.com/repos/{owner}/{repo_name}"  
    headers = {  
        "Authorization": f"token {access_token}",  
        "Accept": "application/vnd.github.v3+json"  
    }  
  
    response = requests.delete(url, headers=headers)  
    return response 
arr = [
    "exam"
] 
if __name__ == "__main__":  
    OWNER = "gaohuaiy"  # 替换为你的用户名或组织名  
    REPO_NAME = "30-Days-Of-Python"  # 替换为你要删除的仓库名  
    ACCESS_TOKEN = "xx"  # 替换为你的GitHub个人访问令牌  
  
    # result = delete_repository(OWNER, REPO_NAME, ACCESS_TOKEN)  
    for rep in arr:
        result = delete_repository(OWNER, rep, ACCESS_TOKEN)  
        print(result)
