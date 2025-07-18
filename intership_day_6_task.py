# -*- coding: utf-8 -*-
"""intership day 6 task

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ieXqyuUMCs9vrVyH0uPoNggquRW6JACp
"""

def get_grade(score):
    if score > 100 or score < 0:
        return "Invalid"
    elif score >= 90:
        return "A"
    elif score >= 85:
        return "A-"
    elif score >= 80:
        return "B+"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F"

def print_summary(student_name, score):
    grade = get_grade(score)
    if grade == "Invalid":
        print(f"{student_name} ka score valid nahi hai (0–100 range)")
    else:
        print(f"Student {student_name} scored {score} → Grade: {grade}")

name = input("Enter student name: ")
try:
    score = float(input("Enter score (0–100): "))
    print_summary(student_name=name, score=score)
except ValueError:
    print("Invalid input! Please enter a number.")