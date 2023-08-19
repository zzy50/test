import math
import matplotlib.pyplot as plt

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

total = 22500
usage_per_one = 1570

current_usage = 0
usages = []  # List to store current_usage values
sleep_times = []  # List to store sleep_time values

while current_usage < total-usage_per_one:
    current_usage += usage_per_one
    used_ratio = current_usage / total
    sigmoid_ratio = sigmoid(used_ratio * 20 - 10)  # Adjusting for better scaling
    sleep_time = 300 * sigmoid_ratio
    usages.append(current_usage)
    sleep_times.append(sleep_time)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(usages, sleep_times, marker='o', linestyle='-', color='b')
plt.title('Relationship between current_usage and sleep_time with Sigmoid applied')
plt.xlabel('current_usage')
plt.ylabel('sleep_time')
plt.grid(True)
plt.show()
