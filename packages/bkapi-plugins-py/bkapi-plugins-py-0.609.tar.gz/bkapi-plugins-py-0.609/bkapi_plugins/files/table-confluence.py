import requests

# Confluence API相关信息
api_url = 'https://confluence.oasis.ubiquant.com/rest/api/content'  # Confluence API端点
space_key = '~ylwen'  # 空间的Key
parent_page_id = '151332518'  # 父页面的ID

# 填写您的个人访问令牌
token = 'MDM1NzIxNzYzNTQyOhIhQp4fLFq538PG+rJoyIMInQ3r'

# 创建周报内容
title = 'Weekly Report - Wee1k 1'

# 表格数据
table_data = [
    ['Task', 'Status'],
    ['Task 1', 'Completed'],
    ['Task 2', 'In Progress'],
    ['Task 3', 'Not Started']
]

# 构建表格内容
table_content = '<table><tbody>'
for row in table_data:
    table_content += '<tr>'
    for cell in row:
        table_content += f'<td>{cell}</td>'
    table_content += '</tr>'
table_content += '</tbody></table>'

# 构建请求头
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# 构建请求体
data = {
    'type': 'page',
    'title': title,
    'space': {'key': space_key},
    'body': {
        'storage': {
            'value': table_content,
            'representation': 'storage'
        }
    },
    'ancestors': [{'id': parent_page_id}]
}

# 发送POST请求创建页面
response = requests.post(api_url, json=data, headers=headers)

# 检查请求的响应
if response.status_code == 200:
    print('周报创建成功！')
    print(f'页面链接：{response.json()["_links"]["webui"]}')
else:
    print('创建周报失败：', response.text)
