import asyncio
from datetime import datetime
from typing import Optional

from db import users_collection
from auth import hash_password


async def create_user(
    name: str,
    email: str,
    password: str,
    role: str = "admin",
    organisation_id: Optional[str] = None,
) -> None:
    print("START create_user")

    # normalize email
    email = email.strip().lower()
    print("Normalized email:", email)

    print("Checking existing user...")
    existing = await users_collection.find_one({"email": email})
    print("Existing user:", existing)

    if existing:
        print(f"User already exists: {email}")
        return

    now = datetime.utcnow()
    print("Creating user document...")

    user_doc = {
        "name": name,
        "email": email,
        "passwordHash": hash_password(password),
        "role": role,
        "organisationId": organisation_id,
        "isActive": True,
        "lastLoginAt": None,
        "createdAt": now,
        "updatedAt": now,
    }

    print("User doc:\n", user_doc)
    print("Inserting into DB...")

    result = await users_collection.insert_one(user_doc)
    print("Insert result:", result.inserted_id)


if __name__ == "__main__":
    name = "Tsakani Chauke"
    email = "tsakani@greenbdgafrica.com"
    password = "ChangeMe123!"
    organisation_id = None

    print("Running seed...")
    asyncio.run(
        create_user(
            name=name,
            email=email,
            password=password,
            role="admin",
            organisation_id=organisation_id,
        )
    )
