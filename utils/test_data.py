import random

from faker import Faker

fake = Faker()


def create_user_payload():
    gender = random.choice(["male", "female"])

    return {
        "firstName": (
            fake.first_name_female() if gender == "female" else fake.first_name_male()
        ),
        "lastName": fake.last_name(),
        "maidenName": fake.last_name(),
        "age": random.randint(18, 60),
        "gender": gender,
        "email": fake.email(),
        "phone": fake.phone_number(),
        "username": fake.user_name(),
        "password": fake.password(length=10),
        "birthDate": str(fake.date_of_birth(minimum_age=18, maximum_age=60)),
        "image": "https://dummyjson.com/icon/user/128",
        "bloodGroup": random.choice(["A+", "A-", "B+", "B-", "O+", "O-", "AB+"]),
        "height": round(random.uniform(150, 200), 2),
        "weight": round(random.uniform(45, 100), 2),
        "eyeColor": random.choice(["Brown", "Black", "Blue", "Green"]),
        "hair": {
            "color": random.choice(["Black", "Brown", "Blonde"]),
            "type": random.choice(["Straight", "Curly", "Wavy"]),
        },
        "ip": fake.ipv4(),
        "address": {
            "address": fake.street_address(),
            "city": fake.city(),
            "state": fake.state(),
            "stateCode": fake.state_abbr(),
            "postalCode": fake.postcode(),
            "coordinates": {
                "lat": float(fake.latitude()),
                "lng": float(fake.longitude()),
            },
            "country": fake.country(),
        },
        "macAddress": fake.mac_address(),
        "university": fake.company(),
        "bank": {
            "cardExpire": "05/28",
            "cardNumber": fake.credit_card_number(),
            "cardType": fake.credit_card_provider(),
            "currency": random.choice(["USD", "INR", "GBP"]),
            "iban": fake.iban(),
        },
        "company": {
            "department": random.choice(["Engineering", "QA", "HR"]),
            "name": fake.company(),
            "title": fake.job(),
            "address": {
                "address": fake.street_address(),
                "city": fake.city(),
                "state": fake.state(),
                "stateCode": fake.state_abbr(),
                "postalCode": fake.postcode(),
                "coordinates": {
                    "lat": float(fake.latitude()),
                    "lng": float(fake.longitude()),
                },
                "country": fake.country(),
            },
        },
        "ein": fake.ssn(),
        "ssn": fake.ssn(),
        "userAgent": fake.user_agent(),
        "crypto": {
            "coin": random.choice(["Bitcoin", "Ethereum"]),
            "wallet": fake.sha1(),
            "network": random.choice(["ERC20", "BEP20"]),
        },
        "role": random.choice(["admin", "user"]),
    }
