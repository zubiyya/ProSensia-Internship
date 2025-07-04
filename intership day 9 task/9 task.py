#!/usr/bin/env python
# coding: utf-8

# In[ ]:


print('Welcome to Student Marks Checker\n')

def load_student_marks(file_path):
    invalid_lines = 0
    student_data = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                try:
                    name, marks = line.strip().split(',')
                    
                    if name.strip() == '' or marks.strip() == '':
                        raise ValueError("Missing name or marks")
                    
                    student_data[name.strip()] = int(marks.strip())
                    
                except ValueError:
                    invalid_lines += 1
                    
    except FileNotFoundError:
        print("File not found at the specified location.")
        return {}
    
    print(f"File read complete. Skipped {invalid_lines} invalid entries.\n")
    return student_data


def display_summary(data):
    if not data:
        print("No valid student records found.")
        return
    
    print("Student Marks Summary:\n")
    for student, mark in data.items():
        print(f"{student} scored {mark}")
    
    try:
        average_score = sum(data.values()) / len(data)
        print(f"\nClass Average: {average_score:.2f}")
    except ZeroDivisionError:
        print("No data available to compute average.")

path = input(r"Please enter the path of your marks file: ")
students = load_student_marks(path)
display_summary(students)


# In[ ]:




