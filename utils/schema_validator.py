from jsonschema import validate, ValidationError

PRODUCT_SCHEMA_STRICT = {
    "type": "object",
    "required": ["id", "title", "price", "category", "stock", "rating", "brand"],
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "price": {"type": "number"},
        "category": {"type": "string"},
        "stock": {"type": "integer"},
        "rating": {"type": "number"},
        "brand": {"type": "string"}
    }
}

PRODUCT_SCHEMA_RELAXED = {
    "type": "object",
    "required": ["id", "title", "price", "category", "stock", "rating"],
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "price": {"type": "number"},
        "category": {"type": "string"},
        "stock": {"type": "integer"},
        "rating": {"type": "number"},
        "brand": {"type": "string"}  # optional
    }
}

PRODUCTS_LIST_SCHEMA = {
    "type": "object",
    "required": ["products", "total", "skip", "limit"],
    "properties": {
        "products": {
            "type": "array",
            "items": PRODUCT_SCHEMA_RELAXED  # 👈 IMPORTANT CHANGE
        },
        "total": {"type": "integer"},
        "skip": {"type": "integer"},
        "limit": {"type": "integer"}
    }
}

AUTH_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["accessToken", "refreshToken", "id", 
                 "username", "email"],
    "properties": {
        "accessToken": {"type": "string", "minLength": 10},
        "refreshToken": {"type": "string", "minLength": 10},
        "id": {"type": "integer"},
        "username": {"type": "string"},
        "email": {"type": "string"}
    }
}

def validate_schema(data, schema):
    try:
        validate(instance=data, schema=schema)
        return {"valid": True, "error": None}
    except ValidationError as e:
        return {"valid": False, "error": e.message}