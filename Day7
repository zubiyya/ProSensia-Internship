#!/usr/bin/env python
# coding: utf-8

# In[1]:


def manual_sort(numbers):
    for i in range(len(numbers)):
        min_index = i
        for j in range(i+1, len(numbers)):
            if numbers[j] < numbers[min_index]:
                min_index = j
        numbers[i], numbers[min_index] = numbers[min_index], numbers[i]
    return numbers

def calculate_stats(numbers):
    total = 0
    minimum = numbers[0]
    maximum = numbers[0]
    for num in numbers:
        total += num
        if num < minimum:
            minimum = num
        if num > maximum:
            maximum = num
    average = total / len(numbers)
    return {
        "Sorted List": numbers,
        "Sum": total,
        "Average": average,
        "Minimum": minimum,
        "Maximum": maximum
    }

def display_results(results):
    print("\nSummary of List Analysis:\n")
    for index, (key, value) in enumerate(results.items(), start=1):
        print(f"{index}. {key}: {value}")

def get_user_input():
    while True:
        try:
            user_input = input("Enter numbers separated by commas (e.g. 5,3,8,2): ")
            num_list = [int(x.strip()) for x in user_input.split(",")]
            if not num_list:
                raise ValueError
            return num_list
        except ValueError:
            print("Invalid input. Please enter a list of integers separated by commas.")

print("Smart List Analyzer")
numbers = get_user_input()
sorted_list = manual_sort(numbers.copy())
results = calculate_stats(sorted_list)
display_results(results)


# In[ ]:




