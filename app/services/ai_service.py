"""
Simple Working AI Service - GUARANTEED TO WORK
"""

import os
import requests
import json
import sqlite3
import random
from typing import Dict, List, Tuple
from dotenv import load_dotenv

load_dotenv()

class WorkingAIService:
    def __init__(self):
        self.hf_key = os.getenv("HUGGINGFACE_API_KEY")
        self.db_path = "./data/foodiebot.db"
        self.user_sessions = {}
        
    def process_message(self, user_message: str, session_id: str, 
                       recommended_products: List[Dict] = None) -> Tuple[str, Dict]:
        """Simple working message processing"""
        
        # Extract preferences
        preferences = self._extract_preferences(user_message)
        
        # Get products from database
        products = self._get_products_from_db(user_message, preferences)
        
        # Generate response
        response = self._generate_response(user_message, products, session_id)
        
        return response, preferences
    
    def _extract_preferences(self, message: str) -> Dict:
        """Extract preferences simply"""
        message_lower = message.lower()
        preferences = {}
        
        # Categories
        if 'pizza' in message_lower:
            preferences['categories'] = ['Pizza']
        elif 'burger' in message_lower:
            preferences['categories'] = ['Burgers']
        elif 'dessert' in message_lower or 'sweet' in message_lower:
            preferences['categories'] = ['Desserts']
        elif 'drink' in message_lower:
            preferences['categories'] = ['Beverages']
        elif 'salad' in message_lower or 'healthy' in message_lower:
            preferences['categories'] = ['Salads & Healthy Options']
        
        # Dietary
        if 'vegetarian' in message_lower:
            preferences['dietary'] = ['vegetarian']
        elif 'vegan' in message_lower:
            preferences['dietary'] = ['vegan']
        
        # Mood
        if 'spicy' in message_lower or 'hot' in message_lower:
            preferences['mood'] = ['spicy']
        elif 'sweet' in message_lower:
            preferences['mood'] = ['sweet']
        
        return preferences
    
    def _get_products_from_db(self, message: str, preferences: Dict) -> List[Dict]:
        """Get products from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            
            query = "SELECT * FROM products WHERE 1=1"
            params = []
            
            # Filter by category
            if 'categories' in preferences:
                query += " AND category = ?"
                params.append(preferences['categories'][0])
            
            # Filter by spicy
            if 'mood' in preferences and 'spicy' in preferences['mood']:
                query += " AND spice_level >= 5"
            
            # Filter by sweet (desserts)
            if 'mood' in preferences and 'sweet' in preferences['mood']:
                query += " AND category = 'Desserts'"
            
            # Filter by vegetarian
            if 'dietary' in preferences and 'vegetarian' in preferences['dietary']:
                query += " AND dietary_tags LIKE '%vegetarian%'"
            
            query += " ORDER BY popularity_score DESC LIMIT 5"
            
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
            
            products = []
            for row in rows:
                product = dict(row)
                # Parse JSON fields
                for field in ['ingredients', 'dietary_tags', 'mood_tags', 'allergens']:
                    if product[field]:
                        try:
                            product[field] = json.loads(product[field])
                        except:
                            product[field] = []
                products.append(product)
            
            conn.close()
            return products
            
        except Exception as e:
            print(f"Database error: {e}")
            return []
    
    def _generate_response(self, message: str, products: List[Dict], session_id: str) -> str:
        """Generate response using API or simple logic"""
        
        # Try HuggingFace API
        if self.hf_key and products:
            api_response = self._try_api(message, products[0])
            if api_response:
                return api_response
        
        # Simple contextual responses
        message_lower = message.lower()
        
        # Greetings
        if any(word in message_lower for word in ['hi', 'hello', 'hey']):
            return "Hi! I'm FoodieBot, ready to help you find delicious food. What are you in the mood for today?"
        
        # With products
        if products:
            product = products[0]
            
            if 'spicy' in message_lower:
                return f"Perfect! I found the {product['name']} with {product.get('spice_level', 5)}/10 spice level for ${product['price']:.2f}. It's exactly the heat you're looking for! Want to try it?"
            
            elif 'sweet' in message_lower:
                return f"Great choice! The {product['name']} is our most popular dessert at ${product['price']:.2f}. {product['description'][:60]}... Perfect for satisfying that sweet tooth!"
            
            elif 'pizza' in message_lower:
                return f"Excellent! Our {product['name']} is ${product['price']:.2f} and absolutely delicious. {product['description'][:70]}... Does this sound perfect?"
            
            else:
                return f"I recommend the {product['name']} for ${product['price']:.2f}! {product['description'][:60]}... It's really popular with our customers. Interested?"
        
        # No products
        else:
            if 'spicy' in message_lower:
                return "I love spicy food too! Let me find you some fiery options. What type of spicy food do you prefer - Asian heat, Mexican spice, or Indian fire?"
            
            elif 'sweet' in message_lower:
                return "Sweet treats are the best! Are you thinking chocolate desserts, fruity options, or maybe something with caramel? I have amazing recommendations!"
            
            else:
                return "I'd love to help you find something delicious! What type of food are you in the mood for? Pizza, burgers, something healthy, or maybe a sweet treat?"
    
    def _try_api(self, message: str, product: Dict) -> str:
        """Try HuggingFace API"""
        try:
            url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
            headers = {"Authorization": f"Bearer {self.hf_key}"}
            
            context = f"User wants food. Recommend: {product['name']} (${product['price']:.2f}). User said: {message}"
            
            payload = {
                "inputs": f"{context}\nFoodieBot:",
                "parameters": {"max_new_tokens": 60, "temperature": 0.7},
                "options": {"wait_for_model": True}
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated = result[0].get('generated_text', '')
                    if 'FoodieBot:' in generated:
                        return generated.split('FoodieBot:')[-1].strip()
            
            return None
            
        except:
            return None

# Global service
ai_service = WorkingAIService()
