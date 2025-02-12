from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类
import re
import requests
from datetime import datetime

api_token = "jilspxxvi6mglxeyubxztg73lnqnkt"
# GET 请求微博热点数据
wb_url = "https://v3.alapi.cn/api/new/wbtop"
weather_url = "https://v3.alapi.cn/api/tianqi"

def format_weather_info(data):
    """
    格式化天气信息并返回一个字符串。
    :param data: 解析后的 JSON 数据（Python 字典格式）
    :return: 美化后的天气信息字符串
    """
    city = data["data"]["city"]
    province = data["data"]["province"]
    weather = data["data"]["weather"]
    temperature = data["data"]["temp"]
    min_temp = data["data"]["min_temp"]
    max_temp = data["data"]["max_temp"]
    wind = data["data"]["wind"]
    humidity = data["data"]["humidity"]
    air_quality = data["data"]["aqi"]["air_level"]
    air_tips = data["data"]["aqi"]["air_tips"]
    sunrise = data["data"]["sunrise"]
    sunset = data["data"]["sunset"]

    # 根据天气类型选择合适的表情符号
    weather_emojis = {
        "晴": "🌞",
        "多云": "🌥️",
        "阴": "🌫️",
        "雨": "🌧️",
        "雪": "🌨️",
        "雷暴": "⛈️",
        "雾霾": "🌫️",
        "寒冷": "🥶",
        "热": "😎"
    }
    emoji = weather_emojis.get(weather, "☁️")  # 默认使用云朵表情
    return f"""
    
城市: {city} ({province})
天气: {weather}{emoji}
当前温度: {temperature}°C
最低温度: {min_temp}°C
最高温度: {max_temp}°C
风速: {wind}
湿度: {humidity}
空气质量: {air_quality} ({air_tips})

日出时间: {sunrise}
日落时间: {sunset}
"""

def fetch_data_from_api(url, params):
    """通用 API 请求方法，返回解析后的 JSON 数据"""
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()  # 直接返回解析后的 JSON 数据
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return {}

def extract_city_from_message(msg):
    """从消息中提取城市名称"""
    pattern = r'([\u4e00-\u9fa5]+市)'
    city_match = re.search(pattern, msg)
    if city_match:
        return city_match.group(0)[:-1]  # 去掉最后的“市”
    return ""

def format_weibo_hotwords(hot_words_data):
    """格式化微博热点数据为字符串"""
    output = ""
    for index, item in enumerate(hot_words_data, 1):
        hot_word = item.get("hot_word", "")
        hot_word_num = item.get("hot_word_num", 0)
        url = item.get("url", "")
        # 添加表情符号
        hot_word_emoji = "🔥"  # 热点词的表情符号
        hot_num_emoji = "🤗"  # 热度的表情符号
        url_emoji = "🌐"  # URL的表情符号
        # 格式化输出
        output += f"{index}. 热点词: {hot_word} {hot_word_emoji}\n   {hot_num_emoji}热度: {hot_word_num}\n   {url_emoji} URL: {url}\n\n"

    return output

# 注册插件
@register(name="LangBotFancyApis", description="旨在为bot提供更多实时信息获取功能，例如今日微博热点，实时地图信息等功能", version="1.0", author="MeiFan")
class MyPlugin(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        pass

    # 异步初始化
    async def initialize(self):
        pass

    # 处理收到的个人消息
    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message  # 获取消息内容
        weibo_match = re.search(r"微博热点", msg)
        weather_match = re.search(r"(天气|weather)", msg)

        if weibo_match:
            self.ap.logger.debug(f"weibo_pattern, {ctx.event.sender_id}")
            # 从消息中提取获取数量
            number = self.extract_number_from_msg(msg)
            params = {'token': api_token, 'num': number}
            response_data = fetch_data_from_api(wb_url, params)
            hot_words_data = response_data.get("data", [])
            output = format_weibo_hotwords(hot_words_data)

            # 获取当前时间并输出
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.ap.logger.debug(f"{current_time} TOP {number} 微博热点\n{output}")
            ctx.add_return("reply", f"{current_time} TOP {number} 微博热点\n{output}")
            ctx.prevent_default()

        elif weather_match:
            self.ap.logger.debug(f"weather_pattern, {ctx.event.sender_id}")
            city = extract_city_from_message(msg)
            if city:
                params = {'token': api_token, 'city': city, 'ip': ""}
                response_data = fetch_data_from_api(weather_url, params)
                output = format_weather_info(response_data)
                self.ap.logger.debug(output)
                ctx.add_return("reply", output)
                ctx.prevent_default()

    # 处理收到的群消息
    @handler(GroupNormalMessageReceived)
    async def group_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message  # 获取消息内容
        weibo_match = re.search(r"微博热点", msg)
        weather_match = re.search(r"(天气|weather)", msg)

        if weibo_match:
            self.ap.logger.debug(f"weibo_pattern, {ctx.event.sender_id}")
            number = self.extract_number_from_msg(msg)
            params = {'token': api_token, 'num': number}
            response_data = fetch_data_from_api(wb_url, params)
            hot_words_data = response_data.get("data", [])
            output = format_weibo_hotwords(hot_words_data)

            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.ap.logger.debug(f"{current_time} TOP {number} 微博热点\n{output}")
            ctx.add_return("reply", f"{current_time} TOP {number} 微博热点\n{output}")
            ctx.prevent_default()

        elif weather_match:
            self.ap.logger.debug(f"weather_pattern, {ctx.event.sender_id}")
            city = extract_city_from_message(msg)
            if city:
                params = {'token': api_token, 'city': city, 'ip': ""}
                response_data = fetch_data_from_api(weather_url, params)
                output = format_weather_info(response_data)
                self.ap.logger.debug(output)
                ctx.add_return("reply", output)
                ctx.prevent_default()

    # 提取数字（微博热点数量）
    def extract_number_from_msg(self, msg):
        """从消息中提取数字，默认返回10"""
        numbers = re.findall(r"\d+", msg)
        if numbers:
            return min(int(numbers[0]), 50)
        return 10

    # 插件卸载时触发
    def __del__(self):
        pass
