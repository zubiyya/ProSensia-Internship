import datetime
from horoscope_utils import get_zodiac_sign, get_horoscope

def main():
    print("🔮 Welcome to Zubia's DOB-based Horoscope CLI App")
    dob_input = input("📅 Enter your date of birth (DD-MM): ").strip()
    try:
        day, month = map(int, dob_input.split('-'))
        zodiac = get_zodiac_sign(day, month)
        print(f"✨ Zodiac Sign: {zodiac}\n")
        print("🔍 Your Horoscope:")
        print(get_horoscope(zodiac))
    except Exception as e:
        print("❌ Something went wrong:", str(e))

if __name__ == "__main__":
    main()
