
from PIL import Image

# Open an image file
image = Image.open('Resources/fire2.png')

# Resize image to a specific width and height
new_width = 3300
new_height = 1854
resized_image = image.resize((new_width, new_height))

# Save resized image
resized_image.save('Resources/fire2.png')

# Optionally, show the resized image
resized_image.show()

'''
def knapsack_01(weights, profits, capacity):
    n = len(weights)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(profits[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(i - 1)
            w -= weights[i - 1]

    selected_items.reverse()
    return dp[n][capacity], selected_items

# Given weights and profits
weight_profit = [(9, 3), (9, 15), (7, 18), (10, 17), (3, 11)]
weights = [item[0] for item in weight_profit]
profits = [item[1] for item in weight_profit]
total_profit = 19

# Compute maximum profit and selected items
max_profit, selected_items = knapsack_01(weights, profits, total_profit)

print(f"Maximum profit: {max_profit}")
print(f"Selected items indices: {selected_items}")


import random

# Problem parameters


# Print the best solution found
print("Best solution (binary representation):", best_solution)
print("Total profit:", best_profit)
'''