"""
FoodieBot Configuration Settings
"""

import os
from typing import List, Dict

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# API Configuration
GROK_API_KEY = os.getenv("GROK_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "./data/foodiebot.db")

# App Configuration
APP_NAME = "FoodieBot"
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
VERSION = "1.0.0"

# Interest Scoring Configuration (Exact from assignment)
ENGAGEMENT_FACTORS = {
    'specific_preferences': 15,  # "I love spicy Korean food"
    'dietary_restrictions': 10,  # "I'm vegetarian"
    'budget_mention': 5,         # "Under $15"
    'mood_indication': 20,       # "I'm feeling adventurous"
    'question_asking': 10,       # "What's the spice level?"
    'enthusiasm_words': 8,       # "amazing", "perfect", "love"
    'price_inquiry': 25,         # "How much is that?"
    'order_intent': 30,          # "I'll take it", "Add to cart"
}

NEGATIVE_FACTORS = {
    'hesitation': -10,           # "maybe", "not sure"
    'budget_concern': -15,       # "too expensive"
    'dietary_conflict': -20,     # Product doesn't match restrictions
    'rejection': -25,            # "I don't like that"
    'delay_response': -5,        # Long response time
}

# Product Categories
PRODUCT_CATEGORIES = [
    "Burgers", "Pizza", "Fried Chicken", "Tacos & Wraps",
    "Sides & Appetizers", "Beverages", "Desserts",
    "Salads & Healthy Options", "Breakfast Items", "Limited Time Specials"
]
