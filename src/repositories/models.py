# Refactoroituaiemmin generoitu koodi alkaa
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
    length: Optional[float] = None
    age: Optional[int] = None
    activity_level: Optional[int] = None
    allergies: Optional[str] = None
    kcal_min: Optional[float] = None
    kcal_max: Optional[float] = None
    weight_loss_target: Optional[float] = None


@dataclass
class Food:
    food_id: str
    name: str
    kcal_per_portion: float
    carbs_per_portion: float
    protein_per_portion: float
    fat_per_portion: float


# Refactoroitu, aiemmin generoitu koodi päättyy


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
    unit: int
    kcal_per_unit: float


@dataclass
class Activitylog:
    log_id: str
    user_id: str
    activity_id: str
    date: str
    activity_count: int
    kcal_burned: float


@dataclass
class Statistics:
    user_id: str
    date: str
    total_kcal_consumed: float
    total_weight: float
    weight_change: float


@dataclass
class WeightLog:
    log_id: str
    user_id: str
    date: str
    weight: float
    notes: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class DietaryPeriod:
    period_id: str
    user_id: str
    start_date: str
    period_name: str
    end_date: Optional[str] = None
    description: Optional[str] = None
    protocol_type: Optional[str] = None
    notes: Optional[str] = None
    is_active: int = 1
    created_at: Optional[str] = None
