FoodieBot - AI Food Recommendation System

A conversational AI chatbot that provides personalized fast food recommendations through natural language interactions.

Overview
FoodieBot is an intelligent food recommendation system that understands your preferences and suggests meals from a comprehensive database of 100 fast food items. Built with modern AI technology to deliver personalized dining experiences.

Quick Start

Prerequisites:
Python 3.8+
pip

Installation:
git clone https://github.com/YOUR_USERNAME/foodiebot-ai-recommendation-system.git
cd foodiebot-ai-recommendation-system
pip install -r requirements.txt

Run the application:
python server.py
streamlit run streamlit_app.py

Open http://localhost:8501 to start chatting with FoodieBot.

Features

Conversational AI: Natural language understanding for food preferences
Smart Recommendations: Context-aware product suggestions based on your taste
Real-time Interest Tracking: Engagement scoring to improve recommendations
Comprehensive Database: 100 fast food items across 10 categories
Dietary Intelligence: Handles restrictions and allergies automatically
Budget Optimization: Finds options within your price range
Modern Interface: Clean chat UI with product cards and menu browsing

Technology Stack

Backend: FastAPI with SQLite database
Frontend: Streamlit for interactive web interface
AI: Natural language processing for conversation understanding
Database: 100 products with rich metadata (ingredients, dietary tags, spice levels)



How it Works

Start a conversation about your food preferences
FoodieBot analyzes your input and tracks engagement
Smart algorithms match your preferences to products
Get personalized recommendations with detailed information
Browse the full menu with filtering options

Example Usage

User: "I want something spicy for under $15"
FoodieBot: "Perfect! Try our Korean BBQ Bulgogi Tacos at $9.99 with a 6/10 spice level..."

User: "I'm vegetarian"
FoodieBot: "Great! Let me show you our delicious plant-based options..."

API Endpoints

/api/chat - Main conversation interface
/api/products - Product search and filtering
/docs - Interactive API documentation

Built with Python, FastAPI, Streamlit, and SQLite
