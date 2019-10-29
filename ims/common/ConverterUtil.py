from datetime import time

def NumberToTime(hours, minutes):
    """データのフォーマット変換処理
    """
    result = time(hour=hours, minute=minutes)
    return result