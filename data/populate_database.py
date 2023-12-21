import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from faker import Faker
import random

# Database connection
engine = create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}")


# Initialize Faker
fake = Faker()

# Insert fake data into the table
with engine.connect() as connection:
    for _ in range(100):  
        first_name = fake.first_name()
        last_name = fake.last_name()
        blood_sugar_level = random.uniform(70, 300) 
        last_checkup_date = fake.date_between(start_date='-1y', end_date='today')
        query = text("INSERT INTO diabetic_patient_info (first_name, last_name, blood_sugar_level, last_checkup_date) "
                     "VALUES (:first_name, :last_name, :blood_sugar_level, :last_checkup_date)")
        connection.execute(query, {
            "first_name": first_name,
            "last_name": last_name,
            "blood_sugar_level": blood_sugar_level,
            "last_checkup_date": last_checkup_date,
        })
