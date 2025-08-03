import requests

def get_zodiac_sign(day, month):
    zodiac_signs = [
        (120, "Capricorn"), (218, "Aquarius"), (320, "Pisces"),
        (420, "Aries"), (521, "Taurus"), (621, "Gemini"),
        (722, "Cancer"), (823, "Leo"), (923, "Virgo"),
        (1023, "Libra"), (1122, "Scorpio"), (1222, "Sagittarius"),
        (1231, "Capricorn")
    ]
    value = month * 100 + day
    for cutoff, sign in zodiac_signs:
        if value <= cutoff:
            return sign
    return "Capricorn"

def get_horoscope(sign):
    try:
        url = f"https://aztro.sameerkumar.website/?sign={sign.lower()}&day=today"
        response = requests.post(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("description", "No horoscope available.")
        else:
            return "Could not fetch horoscope. Try again later."
    except Exception as e:
        return f"Error fetching horoscope: {str(e)}"
