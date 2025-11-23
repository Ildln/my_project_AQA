# utils/generator.py
import random

def new_user_generate_payload():
    random_id = random.randint(10000, 99999)
    random_username = f"user{random_id}"
    # Генерация тестового пользователя
    return  {
        "id": random_id,
        "username": random_username,
        "firstName": "Test",
        "lastName": "User",
        "email": f"{random_username}@example.com",
        "password": "password123",
        "phone": "1234567890",
        "userStatus": 1
    }

def new_order_generate_payload():
    """Генерация тестового заказа"""
    return {
            "id": random.randint(1000, 9999),
            "petId": random.randint(1, 10),
            "quantity": 1,
            "shipDate": "2025-11-22T12:00:00.000Z",
            "status": "placed",
            "complete": True
    }

def new_pet_generate_payload():
    """Генерация тестового питомца"""
    return {
      "id": random.randint(1000, 9999),
      "name": f"Dog-{random.randint(1, 100)}",
      "category": {"id": 1, "name": "Dogs"},
      "photoUrls": [],
      "tags": [
        {
          "id": 1,
          "name": "cate"
        }
      ],
      "status": "available"
    }