from transformers import  pipeline
from typing import Dict, Any
import re
import os
import requests
from tavily import TavilyClient
import copy
# 1. 你的原始模型路径和加载逻辑
model_path = r"C:\Users\Administrator\.cache\huggingface\hub\models--openbmb--MiniCPM5-1B\snapshots\4e9de7a0778dc1c362e983e6858f0e77542cbdca"

os.environ["TAVILY_API_KEY"]="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"

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

ReAct_Message = [
    {
"role":"system",
"content":"""
你是一个旅游规划小助手,有能力调用外部工具
"""

    },
    {
"role":"user",
"content": """
你是一个智能旅行助手。你的任务是分析用户的请求，并使用可用工具一步步地解决问题。

# 可用工具:
{tools}

# 输出格式要求:
请严格按照以下格式进行回应输出2行,不要输出其他任何消息:

Thought: 你的思考过程和下一步计划
Action: 你要执行的具体行动

Action的格式必须是以下之一：
1. 调用工具：function_name(arg_name="arg_value")
2. 结束任务：Finish[最终答案]

如果已经获得足够的信息，输出：

# 重要提示:
- 每次只输出一对Thought-Action
- Action必须在同一行，不要换行
- 当收集到足够信息可以回答用户问题时，必须使用 Action: Finish[最终答案] 格式结束

# 用户问题
{question}
"""
    }
]

class ToolExecutor():
    def __init__(self):
        self.tools: Dict[str,Dict[str,Any]] = {}
    def registerTool(self,name:str,description:str,func:callable):
        if name in self.tools:
            print("️⚠️️Tool {} already registered".format(name))
        self.tools[name] = {'description':description,'func':func}
        print(f"⭐Tool registered: {name}")
    def getTool(self,name:str)->callable:
        if name in self.tools:
            return self.tools[name]['func']
        else:
            print("⚠️Tool {} not registered".format(name))
    def getAvailableTools(self)->str:
        """
        获取所有已注册工具的格式化字符串
        """
        return "\n".join(f"💫{name}:{info['description']}" for name,info in self.tools.items())

class ReActAgent:
    def __init__(self,chat_model,toolexectuor,max_steps = 15):
        self.chat_model = chat_model
        self.toolexectuor = toolexectuor
        self.max_steps = max_steps
        self.all_message =copy.deepcopy(ReAct_Message)
    def run(self,question:str):
        self.all_message[1]["content"] = self.all_message[1]["content"].format(tools=self.toolexectuor.getAvailableTools(),question = question)
        for step in range(self.max_steps+1):
            print(f"😀第{step+1}步")


            result_message = self.chat_model(self.all_message)

            print(result_message)
            if result_message is None:
                print("⚠️指令生成失败")

            thought, action = self._parse_output(result_message[0]['generated_text'][-1]["content"])

            if thought:
                print(f"😀思考:{thought}")
            else:
                print("解析思考失败")

            if not action:
                print("解析行动失败")
                break
            else:
                print(f"😀行动:{action}")

            if action.startswith("Finish"):
                final_answer = re.search(r"Finish\[(.*)\]",action,re.DOTALL).group(1)
                print(f"🌷最终答案:{final_answer}")
                break

            func_name, param = self._parse_action(action)

            if not func_name:
                print("⚠️无效处理函数名格式")
                observation =("⚠️无效处理函数名格式")
                continue

            tool_func = self.toolexectuor.getTool(func_name)
            if not tool_func:
                print("⚠️没有找到该工具")
                observation = ("⚠️没有找到该工具")
                continue
            else:
                observation = tool_func(param)
                print(f"😀反馈:{observation}")
            self.all_message.append({"role": "user", "content": {"thought":thought, "action":action, "observation":observation}})

    def _parse_output(self,output):
        thought_match = re.search(r"Thought:\s*(.*)",output)
        # Action: 匹配到文本末尾
        action_match = re.search(r"Action:\s*(.*)",output)
        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None
        return thought, action

    def _parse_action(self,action):
        """解析Action字符串，提取工具名称和输入。
        """
        match = re.match(r"(\w+)\[(.*)\]", action, re.DOTALL)
        if match:
            return match.group(1), match.group(2)
        return None, None

if __name__ == "__main__":

    pipe = pipeline(
        "text-generation",
        model=model_path,
        tokenizer=model_path,
        max_new_tokens=200,
        # 如果需要更丰富的生成控制，可以加这些参数：
        # do_sample=True,
        # temperature=0.1,
        # top_p=0.9,
    )


    toolexecutor = ToolExecutor()

    toolexecutor.registerTool(name="get_weather(city: str)",description="一个网页搜索引擎可以用于查询地方景点",func=get_attraction)

    toolexecutor.registerTool(name="get_attraction(city: str, weather: str)",description="获取所在地的天气信息",func=get_weather)

    reactagent = ReActAgent(pipe,toolexecutor)

    reactagent.run(question="长沙的旅游攻略")


