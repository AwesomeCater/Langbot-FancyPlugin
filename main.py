from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类
import re
import requests
import json
from datetime import datetime

api_token = "jilspxxvi6mglxeyubxztg73lnqnkt"
#  GET 请求微博热点数据
wb_url = "https://v3.alapi.cn/api/new/wbtop"
# 注册插件
@register(name="LangBotFancyApis", description="旨在为bot提供更多实时信息获取功能，例如今日微博热点，实时地图信息等功能", version="1.0", author="MeiFan")
class MyPlugin(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        pass

    # 异步初始化
    async def initialize(self):
        pass


    # 当收到个人消息时触发
    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext):

        msg = ctx.event.text_message  # 这里的 event 即为 PersonNormalMessageReceived 的对象
        weibo_pattern = r"微博热点"
        match = re.search(weibo_pattern, msg)
        if match:  # 如果消息包含微博热点
            # 输出调试信息
            self.ap.logger.debug("weibo_pattern, {}".format(ctx.event.sender_id))
            # 获取该文本中的所有数字
            numbers = re.findall(r"\d+", msg)
            number = 10
            if numbers:  # 如果有数字且小于50才获取
                number = int(numbers[0]) if int(numbers[0]) >= 50 else 10
            # 从api获取数据
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
            # 回复消息
            # 获取当前时间
            current_time = datetime.now()

            # 将当前时间格式化为字符串
            time_string = current_time.strftime('%Y-%m-%d %H:%M:%S')
            self.ap.logger.debug(time_string + " TOP " + str(number) + " 微博热点" + "\n" + output)
            ctx.add_return("reply",time_string + " TOP " + str(number) + " 微博热点" + "\n" + output)

            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()

    # 当收到群消息时触发
    @handler(GroupNormalMessageReceived)
    async def group_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message  # 这里的 event 即为 PersonNormalMessageReceived 的对象
        weibo_pattern = r"微博热点"
        match = re.search(weibo_pattern, msg)
        if match:  # 如果消息包含微博热点
            # 输出调试信息
            self.ap.logger.debug("weibo_pattern, {}".format(ctx.event.sender_id))
            # 获取该文本中的所有数字
            numbers = re.findall(r"\d+", msg)
            number = 10
            if numbers:  # 如果有数字且小于50才获取
                number = int(numbers[0]) if int(numbers[0]) >= 50 else 10
            # 从api获取数据
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
            # 回复消息
            # 获取当前时间
            current_time = datetime.now()

            # 将当前时间格式化为字符串
            time_string = current_time.strftime('%Y-%m-%d %H:%M:%S')
            self.ap.logger.debug(time_string + " TOP " + str(number) + " 微博热点" + "\n" + output)
            ctx.add_return("reply", time_string + " TOP " + str(number) + " 微博热点" + "\n" + output)

            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()
    # 插件卸载时触发
    def __del__(self):
        pass
