FoodieBot - AI Food Recommendation System

Complete Database-Driven Conversational AI System for Fast Food Recommendations

Assignment Overview
Tecnvirons Pvt LTD - AI Food Agent Assignment
Submission Date: September 16, 2025
Project Type: Database-Driven Conversational Fast Food System

Assignment Phases Completed:
PHASE 1: Product Data Generation and Database Setup (100 products)
PHASE 2: Conversational AI with Interest Scoring (0-100%)
PHASE 3: Smart Recommendation and Analytics System

Quick Start Guide

Prerequisites:
- Python 3.8 or higher
- pip package manager

Installation and Setup:

1. Clone Repository:
git clone https://github.com/YOUR_USERNAME/foodiebot-ai-recommendation-system.git
cd foodiebot-ai-recommendation-system

2. Install Dependencies:
pip install -r requirements.txt

3. Start API Server:
python server.py
Server runs at: http://localhost:8000

4. Start UI (New Terminal):
streamlit run streamlit_app.py
UI opens at: http://localhost:8501

Core Features

Advanced Conversational AI:
- Natural Language Processing: Understands food preferences in plain English
- Context Memory: Remembers dietary restrictions and conversation history
- Smart Responses: Generates contextual, engaging responses about food
- Multi-turn Conversations: Maintains context across multiple exchanges

Real-Time Interest Scoring (0-100%):
- Tracks user engagement through conversation analysis
- Calculates interest based on enthusiasm, questions, and preferences
- Adjusts recommendations based on interest level

Smart Recommendation Engine:
- Preference Matching: Maps keywords to product attributes
- Dietary Intelligence: Filters for allergies and restrictions
- Mood-Based Filtering: Matches emotions to product categories
- Budget Optimization: Finds best value within price range
- Real-time Queries: Sub-100ms database response time

Comprehensive Database:
- 100 Fast Food Products with complete metadata
- 10 Categories: Burgers, Pizza, Fried Chicken, Tacos, Sides, Beverages, Desserts, Salads, Breakfast, Specials
- Rich Data: Ingredients, dietary tags, mood tags, allergens, spice levels
- SQLite Implementation: Fast, reliable, zero-configuration

Technical Architecture

System Flow:
User Input → Conversation AI → Interest Calculator → Database Query
Response Generation ← Smart Recommender ← Product Matcher ← Results Filter

Backend (FastAPI):
- RESTful API with chat, products, and analytics endpoints
- Database Integration with optimized SQLite queries
- Interest Scoring with real-time engagement calculation
- Smart Filtering with multi-parameter product matching

Frontend (Streamlit):
- Modern Chat Interface with message bubbles
- Product Cards with rich information display
- Menu Browser with category filtering and search
- Responsive Design for mobile and desktop

Assignment Compliance

100 Products Generated: Creative templates across 10 categories
Database Integration: SQLite with sub-100ms query performance
Conversational AI: Context-aware NLP with memory retention
Interest Scoring (0-100%): Real-time calculation with assignment factors
Smart Recommendations: Multi-algorithm product matching system
User Interface: Professional Streamlit chat application
Analytics Dashboard: Conversation metrics and insights
Performance Requirements: Sub-100ms queries, concurrent user support

Project Structure

foodiebot-ai-recommendation-system/
│
├── README.md
├── requirements.txt
├── server.py
├── streamlit_app.py
├── .gitignore
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── database.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_service.py
│   │   ├── scoring_service.py
│   │   └── recommendation_service.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── products.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   │
│   └── utils/
│       └── __init__.py
│
├── data/
│   └── foodiebot.db
│
└── scripts/
    └── generate_products.py



Usage Examples

Example Conversations:
Bot: "Hi! I'm FoodieBot. What food adventure are you craving today?"
User: "Something spicy and under $15"
Bot: "Perfect! Korean BBQ Bulgogi Tacos at $9.99 with 6/10 spice level..."

Bot: "What dietary preferences should I know about?"
User: "I'm vegetarian"
Bot: "Great! I'll focus on our amazing plant-based options..."

API Endpoints:
/api/chat - Main chat interface with AI responses
/api/products - Product search and filtering
/api/analytics - Conversation metrics and insights
/docs - Interactive API documentation
