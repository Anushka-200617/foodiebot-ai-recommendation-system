"""
Lightweight Real AI Service - Uses APIs, not local models
"""

import os
import sqlite3
import json
import requests
from typing import Dict, List, Tuple, Optional
from dotenv import load_dotenv

load_dotenv()

class LightweightAIService:
    def __init__(self):
        self.hf_key = os.getenv("HUGGINGFACE_API_KEY")
        self.db_path = "./data/foodiebot.db"
        self.user_profiles = {}
        
        if self.hf_key:
            print(f"✅ HuggingFace API key loaded: {self.hf_key[:8]}...")
        else:
            print("⚠️ No API key found - will use intelligent system")

    def process_message_with_ai(self, user_message: str, session_id: str) -> Tuple[str, Dict, List[Dict]]:
        """
        Process message with real AI and database integration
        """
        # Initialize user profile
        if session_id not in self.user_profiles:
            self.user_profiles[session_id] = {
                'preferences': {},
                'dietary_restrictions': [],
                'dislikes': [],
                'conversation_history': []
            }
        
        profile = self.user_profiles[session_id]
        
        # Extract preferences intelligently
        preferences = self._extract_preferences_smartly(user_message, profile)
        
        # Update profile
        self._update_user_profile(profile, preferences, user_message)
        
        # Query database based on preferences
        matching_products = self._query_database_intelligently(user_message, preferences, profile)
        
        # Generate AI response
        ai_response = self._generate_real_ai_response(user_message, profile, matching_products)
        
        # Store conversation
        profile['conversation_history'].append({
            'user': user_message,
            'bot': ai_response,
            'products_shown': [p['product_id'] for p in matching_products]
        })
        
        print(f"🤖 AI processed: {len(matching_products)} products found")
        return ai_response, preferences, matching_products

    def _extract_preferences_smartly(self, message: str, profile: Dict) -> Dict:
        """
        Smart preference extraction using pattern matching and context
        """
        preferences = {}
        message_lower = message.lower().strip()
        
        # Category detection with context
        category_patterns = {
            'Pizza': ['pizza', 'slice', 'pepperoni', 'margherita', 'cheese pizza'],
            'Burgers': ['burger', 'patty', 'sandwich', 'beef burger', 'chicken burger'],
            'Fried Chicken': ['chicken', 'wings', 'fried chicken', 'crispy chicken', 'tenders'],
            'Tacos & Wraps': ['taco', 'wrap', 'burrito', 'mexican', 'quesadilla'],
            'Desserts': ['dessert', 'sweet', 'cake', 'ice cream', 'chocolate'],
            'Beverages': ['drink', 'beverage', 'juice', 'soda', 'smoothie', 'shake'],
            'Salads & Healthy Options': ['salad', 'healthy', 'fresh', 'greens', 'bowl'],
            'Breakfast Items': ['breakfast', 'morning', 'pancakes', 'eggs', 'brunch']
        }
        
        detected_categories = []
        for category, patterns in category_patterns.items():
            if any(pattern in message_lower for pattern in patterns):
                detected_categories.append(category)
        
        if detected_categories:
            preferences['categories'] = detected_categories
        
        # Dietary restrictions with intelligent detection
        dietary_patterns = {
            'vegetarian': ['vegetarian', 'veggie', 'no meat', 'plant based', 'veg option'],
            'vegan': ['vegan', 'plant-based', 'no animal products', 'dairy free'],
            'gluten-free': ['gluten-free', 'gluten free', 'no gluten', 'celiac'],
            'keto': ['keto', 'low-carb', 'no carbs', 'ketogenic'],
            'healthy': ['healthy', 'light', 'fresh', 'clean', 'nutritious']
        }
        
        dietary_prefs = []
        for diet, patterns in dietary_patterns.items():
            if any(pattern in message_lower for pattern in patterns):
                dietary_prefs.append(diet)
        
        if dietary_prefs:
            preferences['dietary'] = dietary_prefs
        
        # Mood/flavor preferences with context
        mood_patterns = {
            'spicy': ['spicy', 'hot', 'fire', 'heat', 'kick', 'jalapeño', 'chili', 'sriracha'],
            'sweet': ['sweet', 'dessert', 'sugar', 'chocolate', 'vanilla', 'caramel'],
            'comfort': ['comfort', 'hearty', 'filling', 'satisfying', 'cozy'],
            'fresh': ['fresh', 'light', 'crisp', 'refreshing', 'clean'],
            'rich': ['rich', 'creamy', 'indulgent', 'decadent', 'luxurious']
        }
        
        mood_prefs = []
        for mood, patterns in mood_patterns.items():
            if any(pattern in message_lower for pattern in patterns):
                mood_prefs.append(mood)
        
        if mood_prefs:
            preferences['mood'] = mood_prefs
        
        # Budget extraction with smart patterns
        import re
        budget_patterns = [
            r'under \$?(\d+)', r'less than \$?(\d+)', r'below \$?(\d+)',
            r'budget.*?(\d+)', r'around \$?(\d+)', r'maximum \$?(\d+)'
        ]
        
        for pattern in budget_patterns:
            match = re.search(pattern, message_lower)
            if match:
                budget = int(match.group(1))
                preferences['max_budget'] = budget
                break
        
        return preferences

    def _update_user_profile(self, profile: Dict, new_preferences: Dict, message: str):
        """
        Update user profile with intelligent context tracking
        """
        message_lower = message.lower()
        
        # Update dietary restrictions permanently
        if 'dietary' in new_preferences:
            for diet in new_preferences['dietary']:
                if diet not in profile['dietary_restrictions']:
                    profile['dietary_restrictions'].append(diet)
        
        # Track dislikes intelligently
        rejection_patterns = ['don\'t like', 'dont like', 'hate', 'dislike', 'not interested', 'no thanks']
        if any(rejection in message_lower for rejection in rejection_patterns):
            # Detect what they're rejecting
            if 'burger' in message_lower:
                if 'Burgers' not in profile['dislikes']:
                    profile['dislikes'].append('Burgers')
            elif 'pizza' in message_lower:
                if 'Pizza' not in profile['dislikes']:
                    profile['dislikes'].append('Pizza')
            elif 'chicken' in message_lower:
                if 'Fried Chicken' not in profile['dislikes']:
                    profile['dislikes'].append('Fried Chicken')
        
        # Update preferences with context
        profile['preferences'].update(new_preferences)

    def _query_database_intelligently(self, message: str, preferences: Dict, profile: Dict) -> List[Dict]:
        """
        Query database with intelligent filtering based on user context
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            
            # Build smart query
            query = "SELECT * FROM products WHERE 1=1"
            params = []
            query_reasons = []
            
            # Exclude dislikes first (highest priority)
            for dislike in profile.get('dislikes', []):
                query += " AND category != ?"
                params.append(dislike)
                query_reasons.append(f"Excluded {dislike} (user dislike)")
            
            # Apply dietary restrictions (high priority)
            if profile.get('dietary_restrictions'):
                for restriction in profile['dietary_restrictions']:
                    if restriction == 'vegetarian':
                        query += " AND (dietary_tags LIKE '%vegetarian%' OR dietary_tags LIKE '%veggie%')"
                        query_reasons.append("Filtered for vegetarian options")
                    elif restriction == 'vegan':
                        query += " AND dietary_tags LIKE '%vegan%'"
                        query_reasons.append("Filtered for vegan options")
                    elif restriction == 'gluten-free':
                        query += " AND dietary_tags LIKE '%gluten-free%'"
                        query_reasons.append("Filtered for gluten-free options")
                    elif restriction == 'healthy':
                        query += " AND (dietary_tags LIKE '%healthy%' OR category = 'Salads & Healthy Options')"
                        query_reasons.append("Filtered for healthy options")
            
            # Apply mood preferences
            if 'mood' in preferences:
                mood_conditions = []
                for mood in preferences['mood']:
                    if mood == 'spicy':
                        mood_conditions.append("spice_level >= 5")
                        query_reasons.append("Looking for spicy items (spice level 5+)")
                    mood_conditions.append(f"mood_tags LIKE '%{mood}%'")
                    mood_conditions.append(f"dietary_tags LIKE '%{mood}%'")
                
                if mood_conditions:
                    query += f" AND ({' OR '.join(mood_conditions)})"
            
            # Apply category preferences
            if 'categories' in preferences:
                category_conditions = []
                for category in preferences['categories']:
                    category_conditions.append("category = ?")
                    params.append(category)
                    query_reasons.append(f"Looking in {category} category")
                
                if category_conditions:
                    query += f" AND ({' OR '.join(category_conditions)})"
            
            # Apply budget constraints
            if 'max_budget' in preferences:
                query += " AND price <= ?"
                params.append(preferences['max_budget'])
                query_reasons.append(f"Budget limit: ${preferences['max_budget']}")
            
            # Intelligent ordering
            if 'mood' in preferences and 'spicy' in preferences['mood']:
                query += " ORDER BY spice_level DESC, popularity_score DESC LIMIT 8"
            elif profile.get('dietary_restrictions'):
                query += " ORDER BY popularity_score DESC LIMIT 8"
            else:
                query += " ORDER BY popularity_score DESC, RANDOM() LIMIT 8"
            
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
            
            products = []
            for row in rows:
                product = dict(row)
                # Parse JSON fields safely
                for field in ['ingredients', 'dietary_tags', 'mood_tags', 'allergens']:
                    if product[field]:
                        try:
                            product[field] = json.loads(product[field])
                        except:
                            product[field] = []
                    else:
                        product[field] = []
                products.append(product)
            
            conn.close()
            
            print(f"🔍 Database query: {len(products)} products found")
            print(f"📋 Query logic: {', '.join(query_reasons) if query_reasons else 'General search'}")
            
            return products[:5]  # Return top 5 matches
            
        except Exception as e:
            print(f"❌ Database query error: {e}")
            return []

    def _generate_real_ai_response(self, message: str, profile: Dict, products: List[Dict]) -> str:
        """
        Generate response using real AI API or intelligent contextual system
        """
        # Build context for AI
        context = self._build_context_for_ai(message, profile, products)
        
        # Try HuggingFace API first
        if self.hf_key:
            api_response = self._call_huggingface_api(context, message)
            if api_response and len(api_response.strip()) > 15:
                print("✅ Generated using HuggingFace AI API")
                return self._enhance_response_with_products(api_response, products)
        
        # Use intelligent contextual generation
        print("🧠 Using intelligent contextual generation")
        return self._generate_intelligent_contextual_response(message, profile, products)

    def _build_context_for_ai(self, message: str, profile: Dict, products: List[Dict]) -> str:
        """
        Build rich context for AI generation
        """
        context_parts = [
            "You are FoodieBot, an enthusiastic food consultant. Be natural, helpful, and specific about food recommendations."
        ]
        
        # Add user context
        if profile.get('dietary_restrictions'):
            context_parts.append(f"User dietary needs: {', '.join(profile['dietary_restrictions'])}")
        
        if profile.get('dislikes'):
            context_parts.append(f"User dislikes: {', '.join(profile['dislikes'])}")
        
        # Add product context
        if products:
            product = products[0]
            context_parts.append(f"Recommend: {product['name']} (${product['price']:.2f}) - {product['description'][:80]}")
            
            if len(products) > 1:
                others = [f"{p['name']} (${p['price']:.2f})" for p in products[1:3]]
                context_parts.append(f"Alternatives: {', '.join(others)}")
        
        context_parts.append(f"User said: {message}")
        context_parts.append("Respond naturally:")
        
        return "\n".join(context_parts)

    def _call_huggingface_api(self, context: str, message: str) -> str:
        """
        Call HuggingFace API for real AI generation
        """
        try:
            models = [
                "microsoft/DialoGPT-medium",
                "facebook/blenderbot-400M-distill"
            ]
            
            for model in models:
                try:
                    url = f"https://api-inference.huggingface.co/models/{model}"
                    headers = {
                        "Authorization": f"Bearer {self.hf_key}",
                        "Content-Type": "application/json"
                    }
                    
                    payload = {
                        "inputs": f"{context}\nFoodieBot:",
                        "parameters": {
                            "max_new_tokens": 120,
                            "temperature": 0.8,
                            "do_sample": True,
                            "top_p": 0.9,
                            "repetition_penalty": 1.1
                        },
                        "options": {"wait_for_model": True}
                    }
                    
                    response = requests.post(url, json=payload, headers=headers, timeout=20)
                    
                    if response.status_code == 200:
                        result = response.json()
                        if isinstance(result, list) and len(result) > 0:
                            generated = result[0].get('generated_text', '')
                            
                            # Extract response
                            if 'FoodieBot:' in generated:
                                response_text = generated.split('FoodieBot:')[-1].strip()
                                response_text = response_text.split('User:')[0].strip()
                                response_text = response_text.split('\n')[0].strip()
                                
                                if len(response_text) > 15:
                                    return response_text
                    
                except Exception as e:
                    print(f"Model {model} failed: {e}")
                    continue
            
            return ""
            
        except Exception as e:
            print(f"API generation error: {e}")
            return ""

    def _generate_intelligent_contextual_response(self, message: str, profile: Dict, products: List[Dict]) -> str:
        """
        Generate intelligent contextual responses (not templates)
        """
        message_lower = message.lower()
        has_products = len(products) > 0
        
        # Build response contextually
        response_parts = []
        
        # Analyze message type and context
        if any(greeting in message_lower for greeting in ['hi', 'hello', 'hey']) and len(message_lower.split()) <= 2:
            response_parts.append("Hello! I'm FoodieBot, your AI food consultant.")
            
            if profile.get('dietary_restrictions'):
                dietary = ', '.join(profile['dietary_restrictions'])
                response_parts.append(f"I see you have {dietary} preferences - I'll find perfect matches for you.")
            
            response_parts.append("What type of food experience sounds perfect today?")
        
        elif has_products:
            product = products[0]
            
            # Context-aware product introduction
            if 'spicy' in message_lower:
                spice_level = product.get('spice_level', 1)
                response_parts.append(f"Perfect! I found something with exactly the right heat level.")
                response_parts.append(f"The {product['name']} has {spice_level}/10 spice intensity")
            elif profile.get('dietary_restrictions'):
                dietary = profile['dietary_restrictions'][0]
                response_parts.append(f"Great news! I found an excellent {dietary} option for you.")
                response_parts.append(f"The {product['name']}")
            else:
                response_parts.append(f"I have the perfect recommendation!")
                response_parts.append(f"The {product['name']}")
            
            # Add product details contextually
            response_parts.append(f"costs ${product['price']:.2f} and {product['description'][:70]}...")
            
            # Multiple options context
            if len(products) > 1:
                response_parts.append(f"I also found {len(products)-1} other great options.")
            
            # Ask contextual follow-up
            if 'spicy' in message_lower:
                response_parts.append("Does this spice level sound perfect for you?")
            elif profile.get('dietary_restrictions'):
                response_parts.append("This fits your dietary needs perfectly - interested?")
            else:
                response_parts.append("What do you think of this choice?")
        
        else:
            # No products found - contextual guidance
            if profile.get('dislikes'):
                dislikes = ', '.join(profile['dislikes'])
                response_parts.append(f"I understand you're not interested in {dislikes.lower()}.")
            
            if profile.get('dietary_restrictions'):
                dietary = ', '.join(profile['dietary_restrictions'])
                response_parts.append(f"For {dietary} options, let me understand your flavor preferences better.")
            else:
                response_parts.append("I want to find you something perfect.")
            
            response_parts.append("What flavors or cuisines typically make you excited about food?")
        
        return " ".join(response_parts)

    def _enhance_response_with_products(self, ai_response: str, products: List[Dict]) -> str:
        """
        Enhance AI response with specific product information
        """
        if not products:
            return ai_response
        
        product = products[0]
        
        # If AI response doesn't mention specific products, add them
        if product['name'] not in ai_response and len(ai_response) < 150:
            enhanced = f"{ai_response} The {product['name']} at ${product['price']:.2f} sounds perfect for you!"
            return enhanced
        
        return ai_response

# Global lightweight AI service
real_ai_service = LightweightAIService()
