# Examples

# ================================================================
sample_data = [
    {"userId": 1, "name": "rahul", "completed": False},
    {"userId": 1, "name": "rohit", "completed": False},
    {"userId": 1, "name": "ram", "completed": False},
    {"userId": 1, "name": "ravan", "completed": True},
]

# Approach uses Walrus Operator

for entry in sample_data:
    if name := entry.get("name"):
        print(name)

print("Without Walrus operator:")
for entry in sample_data:
    name = entry.get("name")
    if name:
        print(f'Found name: "{name}"')

# ==============================================================

foods = list()
while True:
    food = input("What food do you like?: ")
    if food == "quit":
        break
        foods.append(food)

# Below Approach uses Walrus Operator

foods = list()

while (food := input("what is favourate food ")) != "quit":
    foods.append(food)

print(foods)


# =============================================================
