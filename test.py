from datetime import datetime
import requests
import json

api_token = "jilspxxvi6mglxeyubxztg73lnqnkt"
#  GET 请求微博热点数据
wb_url = "https://v3.alapi.cn/api/new/wbtop"
number = 10
params = {
    'token': api_token,
    'num': number
}
responses = requests.get(wb_url, params=params)

# 解析 JSON 数据
response_data = json.loads(responses.text)

# 提取 data 部分
hot_words_data = response_data.get("data", [])

# 创建输出字符串
output = ""
for index, item in enumerate(hot_words_data, 1):
    hot_word = item.get("hot_word", "")
    hot_word_num = item.get("hot_word_num", 0)
    url = item.get("url", "")

    # 格式化输出
    output += f"{index}. 热点词: {hot_word}\n   热度: {hot_word_num}\n   URL: {url}\n\n"

current_time = datetime.now()

# 将当前时间格式化为字符串
time_string = current_time.strftime('%Y-%m-%d %H:%M:%S')
# 输出结果
print(time_string + " TOP " + str(number) + " 微博热点" + "\n" + output);

# 回复消息
# 获取当前时间
current_time = datetime.now()

# 将当前时间格式化为字符串
time_string = current_time.strftime('%Y-%m-%d %H:%M:%S')

print(time_string + " TOP " + str(number) + " 微博热点：" + "\n" + output)