import json

from faker import Faker

fake = Faker()

users = []

for _ in range(100):
    users.append({
        "name": fake.name(),
        "age": fake.random_int(min=18, max=80),
        "email": fake.email(),
        "createdAt": fake.date_time_this_decade().isoformat()
    })

with open("./users.json", "w") as f:
    json.dump(users, f, indent=2)
