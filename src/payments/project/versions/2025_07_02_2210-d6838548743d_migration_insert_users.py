"""migration_insert_users

Revision ID: d6838548743d
Revises: 273007056863
Create Date: 2025-07-02 22:10:59.404051

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.orm import Session
from sqlalchemy import text



# revision identifiers, used by Alembic.
revision: str = 'd6838548743d'
down_revision: Union[str, Sequence[str], None] = '273007056863'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

class User:
    def __init__(self, name, username, password, created_at, email):
        self.name = name
        self.username = username
        self.password = password
        self.created_at = created_at
        self.email = email



def upgrade() -> None:
    
    bind = op.get_bind()
    session = Session(bind=bind)

    
    users_data = [
        ('46262ec5-3785-4148-b23a-721d2e78a9cc','Marcos Pampuch', 'marcos2349', 'T5e2U4r7GmQz', '2025-01-01 12:34:45', 'marcos2349@gmail.com', True),
        ('c6dba2ba-36cc-4b71-a0b2-ff8fdc168dc6','Anna Martinez', 'anna8723', 'P8b1Jk9QwXmE', '2025-01-02 05:21:33', 'anna8723@hotmail.com', True),
        ('8cc97ff5-5b2d-41e0-9fd7-db4fc09c0a4f','Lucas Silva', 'lucas9871', 'J3a0RkT2V6Cp', '2025-01-03 19:45:27', 'lucas9871@outlook.com', True),
        ('6d52e515-086d-4519-a62f-b02442efcf27','Sarah Lee', 'sarah4651', 'Y7hXb2Q1PdUf', '2025-01-04 14:30:12', 'sarah4651@bol.com', True),
        ('015b5dbd-68d7-4a96-ab61-c68068fb124a','William Brown', 'william2309', 'L9w1V4R3KkHu', '2025-01-05 09:02:45', 'william2309@gmail.com', True),
        ('535c41d5-ac8c-4dbd-b4cb-d2bfbdcc1a04','Julia Edwards', 'julia8214', 'M2nF9CwX7ZvD', '2025-01-06 11:22:57', 'julia8214@hotmail.com', True),
        ('9eb7ebc6-4e64-41e1-8fc6-f96baef961d5','James Johnson', 'james1447', 'Q4fV6Tp2M0Xj', '2025-01-07 03:11:38', 'james1447@outlook.com', True),
        ('44538ef3-9f9b-45f7-a2fe-4fe796d8ffe7','Emily Davis', 'emily6349', 'H1tY0J3L9BxR', '2025-01-08 17:50:20', 'emily6349@bol.com', True),
        ('2c3fdbdc-9e06-41f8-b3b4-9a3a87620f6c','David Kim', 'david2201', 'F3nV5J6AkHqB', '2025-01-09 16:23:56', 'david2201@gmail.com', True),
        ('a9e7bfd9-1858-4020-98e5-698b8c67c6ed','Rachel Miller', 'rachel3945', 'W7sF5Y1B2GmO', '2025-01-10 13:12:40', 'rachel3945@hotmail.com', True),
        ('2daef0f4-9eae-4bf8-b38a-681e5478d3a7','Brian Walker', 'brian7248', 'J8qU5Lt0V2Cx', '2025-01-11 10:07:18', 'brian7248@outlook.com', True),
        ('b22f8d2b-cb1d-47f8-b85e-34718dc157d5','Olivia Harris', 'olivia8769', 'I9hK6F2Q3NzJ', '2025-01-12 01:32:59', 'olivia8769@bol.com', True),
        ('fd7f9fa8-bf89-454e-9bed-19910f6e0f93','John Turner', 'john3217', 'W0kM8A3P4DjV', '2025-01-13 06:47:05', 'john3217@gmail.com', True),
        ('fcef7e7c-b37b-45d2-8e63-7970bb57a7dd','Linda Green', 'linda2110', 'P3eZ7Rk1G9Vt', '2025-01-14 09:21:54', 'linda2110@hotmail.com', True),
        ('607a3b07-cab4-4ee5-9e9b-c03d1e182391','Michael Scott', 'michael6532', 'B4zJ5Q1V0CkA', '2025-01-15 19:03:28', 'michael6532@outlook.com', True),
        ('cde3b262-e7a8-4e1a-8b9d-49e2ab9ad37f','Jessica White', 'jessica8452', 'T1qL8R3V4CpY', '2025-01-16 22:47:11', 'jessica8452@bol.com', True),
        ('9c10a609-5690-4d70-96e0-4078042133d2','Joseph Martinez', 'joseph3145', 'H0nF7D9K0GvP', '2025-01-17 04:21:43', 'joseph3145@gmail.com', True),
        ('9ff00e7c-218e-44e3-92bd-7900500bd356','Emma Clark', 'emma2308', 'W5gV2T1H9ZnJ', '2025-01-18 08:55:17', 'emma2308@hotmail.com', True),
        ('200c8181-f44d-4a86-b17a-ec741fe7e0b1','Daniel Lewis', 'daniel9643', 'X2mV9Y1G0PzF', '2025-01-19 06:09:28', 'daniel9643@outlook.com', True),
        ('1e1cf90d-efd8-4dc6-accd-be03ab27c5c3','Samantha Harris', 'samantha2310', 'J6oK9M2V7BzY', '2025-01-20 12:50:22', 'samantha2310@bol.com', True),
        ('04cf1e2e-1419-4302-a690-e89302ae3d42','Henry Clark', 'henry4521', 'G8uW1N0Y9PjD', '2025-01-21 11:12:34', 'henry4521@gmail.com', True),
        ('35af4654-e737-4ef5-81b4-e9cf497d1bf6','Mia Robinson', 'mia1340', 'B7pV0C2J6MqN', '2025-01-22 17:39:55', 'mia1340@hotmail.com', True),
        ('e11e33ce-f297-4468-bfca-7d4080ccca46','Ethan Carter', 'ethan5489', 'L9aV3Z5B6CmS', '2025-01-23 01:17:42', 'ethan5489@outlook.com', True),
        ('86cda25c-ba84-49fc-a47f-c4fdf99d8935','Natalie King', 'natalie9371', 'J3pF9G1V2HuT', '2025-01-24 15:21:19', 'natalie9371@bol.com', True),
        ('f36617fb-4d70-4896-9921-8061ee87db72','Jack Lee', 'jack6713', 'V1rB3X5A0WtG', '2025-01-25 18:49:34', 'jack6713@gmail.com', True),
        ('7f8f062a-1213-4529-a1c5-04fe3faf1485','Lily Evans', 'lily5497', 'D0kP6C9M3RtV', '2025-01-26 08:33:12', 'lily5497@hotmail.com', True),
        ('c487ca3a-0334-40e4-8a00-61fa529142fc','Aiden Moore', 'aiden1205', 'N7hV9Y4T1FpM', '2025-01-27 20:56:03', 'aiden1205@outlook.com', True),
        ('7bf36635-f663-4994-9315-894cd368b580','Grace Walker', 'grace3032', 'T4mC8Z9A1WsD', '2025-01-28 03:12:58', 'grace3032@bol.com', True),
        ('473e10a1-5c6e-4cc8-ab75-d8dcef755e10','Andrew Wilson', 'andrew9061', 'G5wJ2T0C7NxV', '2025-01-29 07:47:24', 'andrew9061@gmail.com', True),
        ('8b1ccf89-3c34-4704-a380-bda5a2e4a79f','Chloe Young', 'chloe8832', 'W0jY7V9D4M3P', '2025-01-30 14:35:18', 'chloe8832@hotmail.com', True)
    ]

    # Using parameterized queries with sqlalchemy.text to avoid SQL injection risks
    for user_id, name, username, password, user_creation_date, email, active in users_data:
        session.execute(
            text("INSERT INTO users (user_id, name, email, username, password, user_creation_date, active)"
                 "VALUES (:user_id, :name, :email, :username, :password, :user_creation_date, :active)"),
            {'user_id': user_id, 'name': name, 'email': email, 'username': username, 'password': password, 'user_creation_date': user_creation_date, 'active': active}
        )


def downgrade() -> None:
    op.execute('DELETE FROM users')
