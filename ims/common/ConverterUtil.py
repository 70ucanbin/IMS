"""
    データのフォーマット変換処理

"""
from datetime import time

def NumberToTime(hours, minutes):
    result = time(hour=hours, minute=minutes)
    return result