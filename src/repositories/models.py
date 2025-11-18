# Generoitu koodi alkaa
# models.py
# Yksinkertaiset dataluokat sovellusolioille

from dataclasses import dataclass
from typing import Optional

@dataclass
class user:
    user_id: str
    username: str
    password_hash: str
    salt: str
    weight: Optional[float] = None
    height: Optional[float] = None
    age: Optional[int] = None
    activity_level: Optional[str] = None
    allergies: Optional[str] = None
    calorie_min: Optional[float] = None
    calorie_max: Optional[float] = None
    weight_loss_target: Optional[float] = None

@dataclass
class Food:
    food_id: str
    name: str
    calories_per_portion: float
    carbs_per_portion: float
    protein_per_portion: float
    fat_per_portion: float
# Generoitu koodi päättyy