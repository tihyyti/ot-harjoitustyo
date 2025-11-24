# Generoitu koodi alkaa
# models.py
# Dataluokat sovellusolioille

from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
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


@dataclass
class Foodlog:
    log_id: str
    user_id: str
    food_id: str
    date: str
    portion_size_g: float


@dataclass
class Activity:
    activity_id: str
    name: str
    unit: str
    calories_per_unit: float


@dataclass
class Activitylog:
    log_id: str
    user_id: str
    activity_id: str
    date: str
    activity_count: float
    calories_burned: float


@dataclass
class Statistics:
    user_id: str
    date: str
    total_calories_consumed: float
    total_weight: float
    weight_change: float
