import json
from faker import Faker

# Create a Faker instance
fake = Faker()

# Initialize an empty list to store user data
users = []

# Generate data for 100 users
for _ in range(100):
    # Each user is a dictionary with the following keys:
    # - name: a fake name
    # - age: a random integer between 18 and 80
    # - email: a fake email address
    # - createdAt: a fake date and time from this decade, in ISO format
    users.append({
        "name": fake.name(),
        "age": fake.random_int(min=1, max=90),
        "email": fake.email(),
        "createdAt": fake.date_time_this_decade().isoformat()
    })

# Write the list of users to a JSON file
with open("./users.json", "w") as f:
    # The JSON file is pretty-printed with an indent of 2 spaces
    json.dump(users, f, indent=2)