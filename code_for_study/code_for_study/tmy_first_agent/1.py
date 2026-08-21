import os

os.environ["TAVILY_API_KEY"]="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"
API_KEY = "sk-b33fc97e510a40788c261e67e68da743"
BASE_URL = "https://api.deepseek.com"
MODEL_ID = "deepseek-v4-flash"

AGENT_SYSTEM_PROMPT = """
你是一个智能旅行助手。你的任务是分析用户的请求，并使用可用工具一步步地解决问题。

# 可用工具:
- `get_weather(city: str)`: 查询指定城市的实时天气。
- `get_attraction(city: str, weather: str)`: 根据城市和天气搜索推荐的旅游景点。

# 输出格式要求:
你的每次回复必须严格遵循以下格式，包含一对Thought和Action：

Thought: [你的思考过程和下一步计划]
Action: [你要执行的具体行动]

Action的格式必须是以下之一：
1. 调用工具：function_name(arg_name="arg_value")
2. 结束任务：Finish[最终答案]

# 重要提示:
- 每次只输出一对Thought-Action
- Action必须在同一行，不要换行
- 当收集到足够信息可以回答用户问题时，必须使用 Action: Finish[最终答案] 格式结束

请开始吧！
"""
import requests

def get_weather(city:str)->str:
    """
    通过调用wtrr.in API查询真实的天气信息
    """
    url = f"https://wttr.in/{city}?format=j1"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

#{'current_condition': [{'FeelsLikeC': '37', 'FeelsLikeF': '99', 'cloudcover': '9', 'humidity': '53', 'observation_time': '04:23 AM', 'precipInches': '0.0', 'precipMM': '0.0', 'pressure': '1006', 'pressureInches': '30', 'temp_C': '33', 'temp_F': '91', 'uvIndex': '11', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '113', 'weatherDesc': [{'value': 'Sunny'}], 'weatherIconUrl': [{'value': 'https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0001_sunny.png'}], 'winddir16Point': 'S', 'winddirDegree': '184', 'windspeedKmph': '16', 'windspeedMiles': '10'}], 'nearest_area': [{'areaName': [{'value': 'Changshashih'}], 'country': [{'value': 'China'}], 'latitude': '28.200', 'longitude': '112.967', 'population': '0', 'region': [{'value': 'Hunan'}], 'weatherUrl': [{'value': 'https://www.worldweatheronline.com/v2/weather.aspx?q=28.2,112.967'}]}], 'request': [{'query': 'Lat 28.19 and Lon 112.98', 'type': 'LatLon'}], 'weather': [{'astronomy': [{'moon_illumination': '94', 'moon_phase': 'Waning Gibbous', 'moonrise': '08:56 PM', 'moonset': '08:01 AM', 'sunrise': '05:51 AM', 'sunset': '07:19 PM'}], 'avgtempC': '29', 'avgtempF': '85', 'date': '2026-08-01', 'hourly': [{'DewPointC': '23', 'DewPointF': '73', 'FeelsLikeC': '29', 'FeelsLikeF': '85', 'HeatIndexC': '29', 'HeatIndexF': '85', 'WindChillC': '27', 'WindChillF': '80', 'WindGustKmph': '22', 'WindGustMiles': '13', 'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '90', 'chanceofovercast': '2', 'chanceofrain': '9', 'chanceofremdry': '91', 'chanceofsnow': '0', 'chanceofsunshine': '91', 'chanceofthunder': '0', 'chanceofwindy': '1', 'cloudcover': '12', 'diffRad': '0.0', 'humidity': '79', 'precipInches': '0.0', 'precipMM': '0.0', 'pressure': '1006', 'pressureInches': '30', 'shortRad': '0.0', 'tempC': '27', 'tempF': '80', 'time': '0', 'uvIndex': '0', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '113', 'weatherDesc': [{'value': 'Clear '}], 'weatherIconUrl': [{'value': 'https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0008_clear_sky_night.png'}], 'winddir16Point': 'SSE', 'winddirDegree': '159', 'windspeedKmph': '11', 'windspeedMiles': '7'}, {'DewPointC': '23', 'DewPointF': '73', 'FeelsLikeC': '28', 'FeelsLikeF': '83', 'HeatIndexC': '28', 'HeatIndexF': '83', 'WindChillC': '26', 'WindChillF': '78', 'WindGustKmph': '20', 'WindGustMiles': '12', 'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '87', 'chanceofovercast': '1', 'chanceofrain': '11', 'chanceofremdry': '89', 'chanceofsnow': '0', 'chanceofsunshine': '95', 'chanceofthunder': '0', 'chanceofwindy': '1', 'cloudcover': '8', 'diffRad': '0.0', 'humidity': '83', 'precipInches': '0.0', 'precipMM': '0.0', 'pressure': '1005', 'pressureInches': '30', 'shortRad': '0.0', 'tempC': '26', 'tempF': '78', 'time': '300', 'uvIndex': '0', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '113', 'weatherDesc': [{'value': 'Clear '}], 'weatherIconUrl': [{'value': 'https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0008_clear_sky_night.png'}], 'winddir16Point': 'SSE', 'winddirDegree': '157', 'windspeedKmph': '10', 'windspeedMiles': '6'}, {'DewPointC': '22', 'DewPointF': '72', 'FeelsLikeC': '27', 'FeelsLikeF': '80', 'HeatIndexC': '27', 'HeatIndexF': '80', 'WindChillC': '25', 'WindChillF': '76', 'WindGustKmph': '17', 'WindGustMiles': '11', 'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '85', 'chanceofovercast': '1', 'chanceofrain': '12', 'chanceofremdry': '78', 'chanceofsnow': '0', 'chanceofsunshine': '95', 'chanceofthunder': '0', 'chanceofwindy': '1', 'cloudcover': '7', 'diffRad': '0.0', 'humidity': '86', 'precipInches': '0.0', 'precipMM': '0.0', 'pressure': '1005', 'pressureInches': '30', 'shortRad': '0.1', 'tempC': '25', 'tempF': '76', 'time': '600', 'uvIndex': '0', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '113', 'weatherDesc': [{'value': 'Sunny'}], 'weatherIconUrl': [{'value': 'https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0001_sunny.png'}], 'winddir16Point': 'SSE', 'winddirDegree': '148', 'windspeedKmph': '9', 'windspeedMiles': '6'}, {'DewPointC': '23', 'DewPointF': '73', 'FeelsLikeC': '33', 'FeelsLikeF': '91', 'HeatIndexC': '33', 'HeatIndexF': '91', 'WindChillC': '29', 'WindChillF': '84', 'WindGustKmph': '21', 'WindGustMiles': '13', 'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '97', 'chanceofovercast': '2', 'chanceofrain': '6', 'chanceofremdry': '94', 'chanceofsnow': '0', 'chanceofsunshine': '94', 'chanceofthunder': '0', 'chanceofwindy': '1', 'cloudcover': '8', 'diffRad': '131.6', 'humidity': '69', 'precipInches': '0.0', 'precipMM': '0.0', 'pressure': '1006', 'pressureInches': '30', 'shortRad': '446.1', 'tempC': '29', 'tempF': '84', 'time': '900', 'uvIndex': '4', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '113', 'weatherDesc': [{'value': 'Sunny'}], 'weatherIconUrl': [{'value': 'https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0001_sunny.png'}], 'winddir16Point': 'S', 'winddirDegree': '175', 'windspeedKmph': '17', 'windspeedMiles': '11'}, {'DewPointC': '22', 'DewPointF': '72', 'FeelsLikeC': '38', 'FeelsLikeF': '100', 'HeatIndexC': '38', 'HeatIndexF': '100', 'WindChillC': '33', 'WindChillF': '91', 'WindGustKmph': '19', 'WindGustMiles': '12', 'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '99', 'chanceofovercast': '2', 'chanceofrain': '2', 'chanceofremdry': '98', 'chanceofsnow': '0', 'chanceofsunshine': '94', 'chanceofthunder': '0', 'chanceofwindy': '1', 'cloudcover': '9', 'diffRad': '136.3', 'humidity': '53', 'precipInches': '0.0', 'precipMM': '0.0', 'pressure': '1006', 'pressureInches': '30', 'shortRad': '699.7', 'tempC': '33', 'tempF': '91', 'time': '1200', 'uvIndex': '11', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '113', 'weatherDesc': [{'value': 'Sunny'}], 'weatherIconUrl': [{'value': 'https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0001_sunny.png'}], 'winddir16Point': 'S', 'winddirDegree': '184', 'windspeedKmph': '16', 'windspeedMiles': '10'}, {'DewPointC': '22', 'DewPointF': '71', 'FeelsLikeC': '39', 'FeelsLikeF': '103', 'HeatIndexC': '39', 'HeatIndexF': '103', 'WindChillC': '35', 'WindChillF': '94', 'WindGustKmph': '19', 'WindGustMiles': '12', 'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '99', 'chanceofovercast': '2', 'chanceofrain': '2', 'chanceofremdry': '98', 'chanceofsnow': '0', 'chanceofsunshine': '92', 'chanceofthunder': '0', 'chanceofwindy': '1', 'cloudcover': '11', 'diffRad': '264.9', 'humidity': '47', 'precipInches': '0.0', 'precipMM': '0.0', 'pressure': '1003', 'pressureInches': '30', 'shortRad': '767.6', 'tempC': '35', 'tempF': '94', 'time': '1500', 'uvIndex': '7', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '113', 'weatherDesc': [{'value': 'Sunny'}], 'weatherIconUrl': [{'value': 'https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0001_sunny.png'}], 'winddir16Point': 'S', 'winddirDegree': '177', 'windspeedKmph': '16', 'windspeedMiles': '10'}, {'DewPointC': '24', 'DewPointF': '75', 'FeelsLikeC': '38', 'FeelsLikeF': '101', 'HeatIndexC': '38', 'HeatIndexF': '101', 'WindChillC': '32', 'WindChillF': '90', 'WindGustKmph': '13', 'WindGustMiles': '8', 'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '99', 'chanceofovercast': '3', 'chanceofrain': '4', 'chanceofremdry': '96', 'chanceofsnow': '0', 'chanceofsunshine': '89', 'chanceofthunder': '0', 'chanceofwindy': '1', 'cloudcover': '14', 'diffRad': '205.9', 'humidity': '61', 'precipInches': '0.0', 'precipMM': '0.0', 'pressure': '1003', 'pressureInches': '30', 'shortRad': '497.4', 'tempC': '32', 'tempF': '90', 'time': '1800', 'uvIndex': '0', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '113', 'weatherDesc': [{'value': 'Sunny'}], 'weatherIconUrl': [{'value': 'https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0001_sunny.png'}], 'winddir16Point': 'S', 'winddirDegree': '180', 'windspeedKmph': '8', 'windspeedMiles': '5'}, {'DewPointC': '23', 'DewPointF': '74', 'FeelsLikeC': '33', 'FeelsLikeF': '91', 'HeatIndexC': '33', 'HeatIndexF': '91', 'WindChillC': '29', 'WindChillF': '84', 'WindGustKmph': '12', 'WindGustMiles': '8', 'chanceoffog': '2', 'chanceoffrost': '0', 'chanceofhightemp': '97', 'chanceofovercast': '78', 'chanceofrain': '39', 'chanceofremdry': '52', 'chanceofsnow': '0', 'chanceofsunshine': '8', 'chanceofthunder': '0', 'chanceofwindy': '1', 'cloudcover': '74', 'diffRad': '0.0', 'humidity': '71', 'precipInches': '0.0', 'precipMM': '0.5', 'pressure': '1005', 'pressureInches': '30', 'shortRad': '0.0', 'tempC': '29', 'tempF': '84', 'time': '2100', 'uvIndex': '0', 'visibility': '9', 'visibilityMiles': '5', 'weatherCode': '176', 'weatherDesc': [{'value': 'Patchy rain nearby'}], 'weatherIconUrl': [{'value': 'https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0025_light_rain_showers_night.png'}], 'winddir16Point': 'SSE', 'winddirDegree': '167', 'windspeedKmph': '6', 'windspeedMiles': '4'}], 'maxtempC': '35', 'maxtempF': '94', 'mintempC': '25', 'mintempF': '76', 'sunHour': '14.0', 'totalSnow_cm': '0.0', 'uvIndex': '11'}, {'astronomy': [{'moon_illumination': '89', 'moon_phase': 'Waning Gibbous', 'moonrise': '09:25 PM', 'moonset': '08:58 AM', 'sunrise': '05:51 AM', 'sunset': '07:19 PM'}], 'avgtempC': '29', 'avgtempF': '84', 'date': '2026-08-02', 'hourly': [{'DewPointC': '23', 'DewPointF': '74', 'FeelsLikeC': '31', 'FeelsLikeF': '87', 'HeatIndexC': '31', 'HeatIndexF': '87', 'WindChillC': '27', 'WindChillF': '81', 'WindGustKmph': '18', 'WindGustMiles': '11', 'chanceoffog': '2', 'chanceoffrost': '0', 'chanceofhightemp': '94', 'chanceofovercast': '74', 'chanceofrain': '50', 'chanceofremdry': '13', 'chanceofsnow': '0', 'chanceofsunshine': '7', 'chanceofthunder': '25', 'chanceofwindy': '1', 'cloudcover': '72', 'diffRad': '0.0', 'humidity': '79', 'precipInches': '0.0', 'precipMM': '0.6', 'pressure': '1005', 'pressureInches': '30', 'shortRad': '0.0', 'tempC': '27', 'tempF': '81', 'time': '0', 'uvIndex': '0', 'visibility': '9', 'visibilityMiles': '5', 'weatherCode': '176', 'weatherDesc': [{'value': 'Patchy rain nearby'}], 'weatherIconUrl': [{'value': 'https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0025_light_rain_showers_night.png'}], 'winddir16Point': 'SSE', 'winddirDegree': '154', 'windspeedKmph': '9', 'windspeedMiles': '5'}, {'DewPointC': '23', 'DewPointF': '73', 'FeelsLikeC': '29', 'FeelsLikeF': '84', 'HeatIndexC': '29', 'HeatIndexF': '84', 'WindChillC': '26', 'WindChillF': '79', 'WindGustKmph': '18', 'WindGustMiles': '11', 'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '89', 'chanceofovercast': '5', 'chanceofrain': '12', 'chanceofremdry': '88', 'chanceofsnow': '0', 'chanceofsunshine': '74', 'chanceofthunder': '0', 'chanceofwindy': '1', 'cloudcover': '24', 'diffRad': '0.0', 'humidity': '84', 'precipInches': '0.0', 'precipMM': '0.0', 'pressure': '1004', 'pressureInches': '30', 'shortRad': '0.0', 'tempC': '26', 'tempF': '79', 'time': '300', 'uvIndex': '0', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '113', 'weatherDesc': [{'value': 'Clear '}], 'weatherIconUrl': [{'value': 'https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0008_clear_sky_night.png'}], 'winddir16Point': 'SE', 'winddirDegree': '131', 'windspeedKmph': '9', 'windspeedMiles': '6'}, {'DewPointC': '23', 'DewPointF': '73', 'FeelsLikeC': '28', 'FeelsLikeF': '83', 'HeatIndexC': '28', 'HeatIndexF': '83', 'WindChillC': '25', 'WindChillF': '78', 'WindGustKmph': '18', 'WindGustMiles': '11', 'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '88', 'chanceofovercast': '5', 'chanceofrain': '13', 'chanceofremdry': '76', 'chanceofsnow': '0', 'chanceofsunshine': '76', 'chanceofthunder': '0', 'chanceofwindy': '1', 'cloudcover': '22', 'diffRad': '0.0', 'humidity': '86', 'precipInches': '0.0', 'precipMM': '0.0', 'pressure': '1005', 'pressureInches': '30', 'shortRad': '0.0', 'tempC': '25', 'tempF': '78', 'time': '600', 'uvIndex': '0', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '113', 'weatherDesc': [{'value': 'Sunny'}], 'weatherIconUrl': [{'value': 'https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0001_sunny.png'}], 'winddir16Point': 'SE', 'winddirDegree': '136', 'windspeedKmph': '9', 'windspeedMiles': '6'}, {'DewPointC': '23', 'DewPointF': '73', 'FeelsLikeC': '33', 'FeelsLikeF': '91', 'HeatIndexC': '33', 'HeatIndexF': '91', 'WindChillC': '29', 'WindChillF': '84', 'WindGustKmph': '18', 'WindGustMiles': '11', 'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '97', 'chanceofovercast': '8', 'chanceofrain': '8', 'chanceofremdry': '93', 'chanceofsnow': '0', 'chanceofsunshine': '64', 'chanceofthunder': '0', 'chanceofwindy': '1', 'cloudcover': '29', 'diffRad': '155.9', 'humidity': '70', 'precipInches': '0.0', 'precipMM': '0.0', 'pressure': '1007', 'pressureInches': '30', 'shortRad': '428.9', 'tempC': '29', 'tempF': '84', 'time': '900', 'uvIndex': '3', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '116', 'weatherDesc': [{'value': 'Partly Cloudy '}], 'weatherIconUrl': [{'value': 'https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0002_sunny_intervals.png'}], 'winddir16Point': 'SSE', 'winddirDegree': '155', 'windspeedKmph': '14', 'windspeedMiles': '9'}, {'DewPointC': '22', 'DewPointF': '72', 'FeelsLikeC': '37', 'FeelsLikeF': '99', 'HeatIndexC': '37', 'HeatIndexF': '99', 'WindChillC': '33', 'WindChillF': '91', 'WindGustKmph': '15', 'WindGustMiles': '9', 'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '99', 'chanceofovercast': '5', 'chanceofrain': '3', 'chanceofremdry': '97', 'chanceofsnow': '0', 'chanceofsunshine': '77', 'chanceofthunder': '0', 'chanceofwindy': '1', 'cloudcover': '22', 'diffRad': '252.3', 'humidity': '54', 'precipInches': '0.0', 'precipMM': '0.0', 'pressure': '1006', 'pressureInches': '30', 'shortRad': '622.5', 'tempC': '33', 'tempF': '91', 'time': '1200', 'uvIndex': '10', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '113', 'weatherDesc': [{'value': 'Sunny'}], 'weatherIconUrl': [{'value': 'https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0001_sunny.png'}], 'winddir16Point': 'SSE', 'winddirDegree': '148', 'windspeedKmph': '13', 'windspeedMiles': '8'}, {'DewPointC': '22', 'DewPointF': '72', 'FeelsLikeC': '37', 'FeelsLikeF': '99', 'HeatIndexC': '37', 'HeatIndexF': '99', 'WindChillC': '33', 'WindChillF': '91', 'WindGustKmph': '20', 'WindGustMiles': '12', 'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '99', 'chanceofovercast': '9', 'chanceofrain': '4', 'chanceofremdry': '96', 'chanceofsnow': '0', 'chanceofsunshine': '59', 'chanceofthunder': '0', 'chanceofwindy': '1', 'cloudcover': '32', 'diffRad': '235.1', 'humidity': '55', 'precipInches': '0.0', 'precipMM': '0.0', 'pressure': '1005', 'pressureInches': '30', 'shortRad': '419.1', 'tempC': '33', 'tempF': '91', 'time': '1500', 'uvIndex': '5', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '116', 'weatherDesc': [{'value': 'Partly Cloudy '}], 'weatherIconUrl': [{'value': 'https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0002_sunny_intervals.png'}], 'winddir16Point': 'ESE', 'winddirDegree': '121', 'windspeedKmph': '15', 'windspeedMiles': '9'}, {'DewPointC': '23', 'DewPointF': '74', 'FeelsLikeC': '34', 'FeelsLikeF': '93', 'HeatIndexC': '34', 'HeatIndexF': '93', 'WindChillC': '30', 'WindChillF': '86', 'WindGustKmph': '23', 'WindGustMiles': '14', 'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '98', 'chanceofovercast': '11', 'chanceofrain': '7', 'chanceofremdry': '93', 'chanceofsnow': '0', 'chanceofsunshine': '52', 'chanceofthunder': '0', 'chanceofwindy': '1', 'cloudcover': '35', 'diffRad': '184.1', 'humidity': '67', 'precipInches': '0.0', 'precipMM': '0.0', 'pressure': '1005', 'pressureInches': '30', 'shortRad': '338.9', 'tempC': '30', 'tempF': '86', 'time': '1800', 'uvIndex': '0', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '116', 'weatherDesc': [{'value': 'Partly Cloudy '}], 'weatherIconUrl': [{'value': 'https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0002_sunny_intervals.png'}], 'winddir16Point': 'ESE', 'winddirDegree': '114', 'windspeedKmph': '14', 'windspeedMiles': '9'}, {'DewPointC': '23', 'DewPointF': '73', 'FeelsLikeC': '30', 'FeelsLikeF': '87', 'HeatIndexC': '30', 'HeatIndexF': '87', 'WindChillC': '27', 'WindChillF': '81', 'WindGustKmph': '16', 'WindGustMiles': '10', 'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '94', 'chanceofovercast': '3', 'chanceofrain': '8', 'chanceofremdry': '92', 'chanceofsnow': '0', 'chanceofsunshine': '88', 'chanceofthunder': '0', 'chanceofwindy': '1', 'cloudcover': '15', 'diffRad': '0.0', 'humidity': '76', 'precipInches': '0.0', 'precipMM': '0.0', 'pressure': '1006', 'pressureInches': '30', 'shortRad': '0.0', 'tempC': '27', 'tempF': '81', 'time': '2100', 'uvIndex': '0', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '113', 'weatherDesc': [{'value': 'Clear '}], 'weatherIconUrl': [{'value': 'https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0008_clear_sky_night.png'}], 'winddir16Point': 'E', 'winddirDegree': '98', 'windspeedKmph': '8', 'windspeedMiles': '5'}], 'maxtempC': '34', 'maxtempF': '92', 'mintempC': '25', 'mintempF': '78', 'sunHour': '14.0', 'totalSnow_cm': '0.0', 'uvIndex': '11'}, {'astronomy': [{'moon_illumination': '81', 'moon_phase': 'Waning Gibbous', 'moonrise': '09:55 PM', 'moonset': '09:55 AM', 'sunrise': '05:52 AM', 'sunset': '07:18 PM'}], 'avgtempC': '28', 'avgtempF': '82', 'date': '2026-08-03', 'hourly': [{'DewPointC': '22', 'DewPointF': '71', 'FeelsLikeC': '28', 'FeelsLikeF': '83', 'HeatIndexC': '28', 'HeatIndexF': '83', 'WindChillC': '26', 'WindChillF': '79', 'WindGustKmph': '12', 'WindGustMiles': '7', 'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '88', 'chanceofovercast': '1', 'chanceofrain': '9', 'chanceofremdry': '91', 'chanceofsnow': '0', 'chanceofsunshine': '96', 'chanceofthunder': '0', 'chanceofwindy': '1', 'cloudcover': '6', 'diffRad': '0.0', 'humidity': '78', 'precipInches': '0.0', 'precipMM': '0.0', 'pressure': '1007', 'pressureInches': '30', 'shortRad': '0.0', 'tempC': '26', 'tempF': '79', 'time': '0', 'uvIndex': '0', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '113', 'weatherDesc': [{'value': 'Clear '}], 'weatherIconUrl': [{'value': 'https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0008_clear_sky_night.png'}], 'winddir16Point': 'ESE', 'winddirDegree': '121', 'windspeedKmph': '6', 'windspeedMiles': '4'}, {'DewPointC': '21', 'DewPointF': '70', 'FeelsLikeC': '27', 'FeelsLikeF': '80', 'HeatIndexC': '27', 'HeatIndexF': '80', 'WindChillC': '25', 'WindChillF': '77', 'WindGustKmph': '10', 'WindGustMiles': '6', 'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '87', 'chanceofovercast': '1', 'chanceofrain': '10', 'chanceofremdry': '90', 'chanceofsnow': '0', 'chanceofsunshine': '95', 'chanceofthunder': '0', 'chanceofwindy': '1', 'cloudcover': '8', 'diffRad': '0.0', 'humidity': '81', 'precipInches': '0.0', 'precipMM': '0.0', 'pressure': '1006', 'pressureInches': '30', 'shortRad': '0.0', 'tempC': '25', 'tempF': '77', 'time': '300', 'uvIndex': '0', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '113', 'weatherDesc': [{'value': 'Clear '}], 'weatherIconUrl': [{'value': 'https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0008_clear_sky_night.png'}], 'winddir16Point': 'SE', 'winddirDegree': '131', 'windspeedKmph': '5', 'windspeedMiles': '3'}, {'DewPointC': '21', 'DewPointF': '70', 'FeelsLikeC': '26', 'FeelsLikeF': '79', 'HeatIndexC': '26', 'HeatIndexF': '79', 'WindChillC': '24', 'WindChillF': '76', 'WindGustKmph': '12', 'WindGustMiles': '8', 'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '83', 'chanceofovercast': '3', 'chanceofrain': '11', 'chanceofremdry': '89', 'chanceofsnow': '0', 'chanceofsunshine': '87', 'chanceofthunder': '0', 'chanceofwindy': '1', 'cloudcover': '16', 'diffRad': '0.0', 'humidity': '82', 'precipInches': '0.0', 'precipMM': '0.0', 'pressure': '1007', 'pressureInches': '30', 'shortRad': '0.0', 'tempC': '24', 'tempF': '76', 'time': '600', 'uvIndex': '0', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '113', 'weatherDesc': [{'value': 'Sunny'}], 'weatherIconUrl': [{'value': 'https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0001_sunny.png'}], 'winddir16Point': 'ESE', 'winddirDegree': '120', 'windspeedKmph': '6', 'windspeedMiles': '4'}, {'DewPointC': '22', 'DewPointF': '71', 'FeelsLikeC': '30', 'FeelsLikeF': '86', 'HeatIndexC': '30', 'HeatIndexF': '86', 'WindChillC': '27', 'WindChillF': '81', 'WindGustKmph': '13', 'WindGustMiles': '8', 'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '92', 'chanceofovercast': '10', 'chanceofrain': '9', 'chanceofremdry': '92', 'chanceofsnow': '0', 'chanceofsunshine': '55', 'chanceofthunder': '0', 'chanceofwindy': '1', 'cloudcover': '33', 'diffRad': '81.9', 'humidity': '72', 'precipInches': '0.0', 'precipMM': '0.0', 'pressure': '1008', 'pressureInches': '30', 'shortRad': '137.3', 'tempC': '27', 'tempF': '81', 'time': '900', 'uvIndex': '4', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '116', 'weatherDesc': [{'value': 'Partly Cloudy '}], 'weatherIconUrl': [{'value': 'https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0002_sunny_intervals.png'}], 'winddir16Point': 'SE', 'winddirDegree': '138', 'windspeedKmph': '10', 'windspeedMiles': '6'}, {'DewPointC': '22', 'DewPointF': '71', 'FeelsLikeC': '36', 'FeelsLikeF': '97', 'HeatIndexC': '36', 'HeatIndexF': '97', 'WindChillC': '32', 'WindChillF': '90', 'WindGustKmph': '15', 'WindGustMiles': '9', 'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '99', 'chanceofovercast': '98', 'chanceofrain': '15', 'chanceofremdry': '76', 'chanceofsnow': '0', 'chanceofsunshine': '0', 'chanceofthunder': '0', 'chanceofwindy': '1', 'cloudcover': '100', 'diffRad': '190.9', 'humidity': '54', 'precipInches': '0.0', 'precipMM': '0.0', 'pressure': '1007', 'pressureInches': '30', 'shortRad': '565.5', 'tempC': '32', 'tempF': '90', 'time': '1200', 'uvIndex': '10', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '176', 'weatherDesc': [{'value': 'Patchy rain nearby'}], 'weatherIconUrl': [{'value': 'https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0009_light_rain_showers.png'}], 'winddir16Point': 'SE', 'winddirDegree': '140', 'windspeedKmph': '13', 'windspeedMiles': '8'}, {'DewPointC': '23', 'DewPointF': '73', 'FeelsLikeC': '36', 'FeelsLikeF': '96', 'HeatIndexC': '36', 'HeatIndexF': '96', 'WindChillC': '31', 'WindChillF': '88', 'WindGustKmph': '13', 'WindGustMiles': '8', 'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '99', 'chanceofovercast': '29', 'chanceofrain': '7', 'chanceofremdry': '93', 'chanceofsnow': '0', 'chanceofsunshine': '23', 'chanceofthunder': '0', 'chanceofwindy': '1', 'cloudcover': '50', 'diffRad': '148.6', 'humidity': '60', 'precipInches': '0.0', 'precipMM': '0.0', 'pressure': '1005', 'pressureInches': '30', 'shortRad': '249.9', 'tempC': '31', 'tempF': '88', 'time': '1500', 'uvIndex': '6', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '116', 'weatherDesc': [{'value': 'Partly Cloudy '}], 'weatherIconUrl': [{'value': 'https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0002_sunny_intervals.png'}], 'winddir16Point': 'SE', 'winddirDegree': '139', 'windspeedKmph': '10', 'windspeedMiles': '6'}, {'DewPointC': '22', 'DewPointF': '72', 'FeelsLikeC': '34', 'FeelsLikeF': '93', 'HeatIndexC': '34', 'HeatIndexF': '93', 'WindChillC': '30', 'WindChillF': '87', 'WindGustKmph': '22', 'WindGustMiles': '14', 'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '98', 'chanceofovercast': '76', 'chanceofrain': '17', 'chanceofremdry': '83', 'chanceofsnow': '0', 'chanceofsunshine': '5', 'chanceofthunder': '0', 'chanceofwindy': '1', 'cloudcover': '73', 'diffRad': '162.4', 'humidity': '62', 'precipInches': '0.0', 'precipMM': '0.1', 'pressure': '1005', 'pressureInches': '30', 'shortRad': '362.2', 'tempC': '30', 'tempF': '87', 'time': '1800', 'uvIndex': '0', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '176', 'weatherDesc': [{'value': 'Patchy rain nearby'}], 'weatherIconUrl': [{'value': 'https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0009_light_rain_showers.png'}], 'winddir16Point': 'SSE', 'winddirDegree': '156', 'windspeedKmph': '14', 'windspeedMiles': '9'}, {'DewPointC': '21', 'DewPointF': '69', 'FeelsLikeC': '28', 'FeelsLikeF': '83', 'HeatIndexC': '28', 'HeatIndexF': '83', 'WindChillC': '26', 'WindChillF': '80', 'WindGustKmph': '20', 'WindGustMiles': '12', 'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '87', 'chanceofovercast': '1', 'chanceofrain': '6', 'chanceofremdry': '94', 'chanceofsnow': '0', 'chanceofsunshine': '95', 'chanceofthunder': '0', 'chanceofwindy': '1', 'cloudcover': '8', 'diffRad': '0.0', 'humidity': '71', 'precipInches': '0.0', 'precipMM': '0.0', 'pressure': '1008', 'pressureInches': '30', 'shortRad': '0.0', 'tempC': '26', 'tempF': '80', 'time': '2100', 'uvIndex': '0', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '113', 'weatherDesc': [{'value': 'Clear '}], 'weatherIconUrl': [{'value': 'https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0008_clear_sky_night.png'}], 'winddir16Point': 'ESE', 'winddirDegree': '106', 'windspeedKmph': '10', 'windspeedMiles': '6'}], 'maxtempC': '33', 'maxtempF': '91', 'mintempC': '24', 'mintempF': '76', 'sunHour': '12.0', 'totalSnow_cm': '0.0', 'uvIndex': '10'}]}


        current_condition = data['current_condition'][0]
        weather_desc = current_condition['weatherDesc'][0]['value']
        temp_c = current_condition['temp_C']

        return f"{city}当前天气:{weather_desc},气温{temp_c}摄氏度"

    except requests.exceptions.RequestException as e:
        return f"网络故障:{e}"
    except (KeyError,IndexError) as e:
        return f"解析数据异常:{e}"

from tavily import TavilyClient
def get_attraction(city:str, weather:str)->str:
    """
    根据城市和天气，使用Tavily Search API搜索并返回优化后的景点推荐。
    """
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        return "错误:未配置TAVILY_API_KEY环境变量。"
    tavily = TavilyClient(api_key=api_key)
    query = f"'{city}' 在'{weather}'天气下最值得去的旅游景点推荐及理由"
    try:
        # 4. 调用API，include_answer=True会返回一个综合性的回答
        response = tavily.search(query=query, search_depth="basic", include_answer=True)

        # 5. Tavily返回的结果已经非常干净，可以直接使用
        # response['answer'] 是一个基于所有搜索结果的总结性回答
        if response.get("answer"):
            return response["answer"]

        # 如果没有综合性回答，则格式化原始结果
        formatted_results = []
        for result in response.get("results", []):
            formatted_results.append(f"- {result['title']}: {result['content']}")
        if not formatted_results:
            return "抱歉，没有找到相关的旅游景点推荐。"

        return "根据搜索，为您找到以下信息:\n" + "\n".join(formatted_results)
    except Exception as e:
        return f"错误:执行Tavily搜索时出现问题 - {e}"

available_tools = {
    "get_weather": get_weather,
    "get_attraction": get_attraction,
}

from openai import OpenAI

class OpenAICompatibleClient:
    """
    一个用于调用任何兼容OpenAI接口的LLM服务的客户端。
    """
    def __init__(self, model: str, api_key: str, base_url: str):
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate(self, prompt: str, system_prompt: str) -> str:
        """调用LLM API来生成回应。"""
        print("正在调用大语言模型...")
        try:
            messages = [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt}
            ]
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False
            )
            answer = response.choices[0].message.content
            print("大语言模型响应成功。")
            return answer
        except Exception as e:
            print(f"调用LLM API时发生错误: {e}")
            return "错误:调用语言模型服务时出错。"
import re

llm = OpenAICompatibleClient(
    model=MODEL_ID,
    api_key=API_KEY,
    base_url=BASE_URL
)

user_prompt = "你好，请帮我查询一下今天湖南省龙山县的天气，然后根据天气推荐一个合适的旅游景点。"
prompt_history = [f"用户请求: {user_prompt}"]
print(f"用户输入: {user_prompt}\n" + "="*40)

# --- 3. 运行主循环 ---
for i in range(5):  # 设置最大循环次数
    print(f"--- 循环 {i + 1} ---\n")

    # 3.1. 构建Prompt
    full_prompt = "\n".join(prompt_history)

    # 3.2. 调用LLM进行思考
    llm_output = llm.generate(full_prompt, system_prompt=AGENT_SYSTEM_PROMPT)
    # 模型可能会输出多余的Thought-Action，需要截断
    match = re.search(r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)', llm_output, re.DOTALL)
    if match:
        truncated = match.group(1).strip()
        if truncated != llm_output.strip():
            llm_output = truncated
            print("已截断多余的 Thought-Action 对")
    print(f"模型输出:\n{llm_output}\n")
    prompt_history.append(llm_output)

    # 3.3. 解析并执行行动
    action_match = re.search(r"Action: (.*)", llm_output, re.DOTALL)
    if not action_match:
        observation = "错误: 未能解析到 Action 字段。请确保你的回复严格遵循 'Thought: ... Action: ...' 的格式。"
        observation_str = f"Observation: {observation}"
        print(f"{observation_str}\n" + "=" * 40)
        prompt_history.append(observation_str)
        continue
    action_str = action_match.group(1).strip()

    if action_str.startswith("Finish"):
        final_answer = re.match(r"Finish\[(.*)\]", action_str).group(1)
        print(f"任务完成，最终答案: {final_answer}")
        break

    tool_name = re.search(r"(\w+)\(", action_str).group(1)
    args_str = re.search(r"\((.*)\)", action_str).group(1)
    kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))

    if tool_name in available_tools:
        observation = available_tools[tool_name](**kwargs)
    else:
        observation = f"错误:未定义的工具 '{tool_name}'"

    # 3.4. 记录观察结果
    observation_str = f"Observation: {observation}"
    print(f"{observation_str}\n" + "=" * 40)
    prompt_history.append(observation_str)
print(prompt_history)