"""
FOODIEBOT SERVER - No Analytics, Focus on Chat & Products
"""

import sys
import os
import json
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Simple imports
from app.models.database import init_database, get_db_manager

app = FastAPI(title="FoodieBot - Impressive UI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
print("🤖 Starting FoodieBot...")
db_path = "./data/foodiebot.db"
init_database(db_path)
print("✅ Database ready!")

# Models
class ChatRequest(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    response: str
    interest_score: float
    recommended_products: List[Dict]
    session_id: str
    debug_info: Dict

# SMART AI SERVICE
class SmartFoodieBotService:
    def __init__(self):
        self.user_context = {}
        
    def process_message(self, message: str, session_id: str) -> tuple:
        """Process with smart recommendations"""
        
        # Initialize user context
        if session_id not in self.user_context:
            self.user_context[session_id] = {
                'messages': [],
                'preferences': {},
                'stage': 'discovery'
            }
        
        context = self.user_context[session_id]
        context['messages'].append(message)
        
        # Update preferences
        self.update_user_preferences(message, context)
        
        # Get smart recommendations
        products = self.get_smart_recommendations(message, context)
        
        # Generate response
        response = self.generate_smart_response(message, products, context)
        
        # Calculate interest score
        interest_score = self.calculate_smart_interest(message, context)
        
        return response, products, interest_score
    
    def update_user_preferences(self, message: str, context: Dict):
        """Extract and update user preferences"""
        message_lower = message.lower()
        
        # Dietary preferences
        if 'vegetarian' in message_lower:
            context['preferences']['dietary'] = 'vegetarian'
        elif 'vegan' in message_lower:
            context['preferences']['dietary'] = 'vegan'
        elif 'healthy' in message_lower:
            context['preferences']['dietary'] = 'healthy'
        
        # Flavor preferences
        if any(word in message_lower for word in ['spicy', 'hot', 'fire']):
            context['preferences']['flavor'] = 'spicy'
        elif 'sweet' in message_lower:
            context['preferences']['flavor'] = 'sweet'
        
        # Category preferences
        if 'pizza' in message_lower:
            context['preferences']['category'] = 'Pizza'
        elif 'burger' in message_lower:
            context['preferences']['category'] = 'Burgers'
        elif 'salad' in message_lower:
            context['preferences']['category'] = 'Salads & Healthy Options'
        elif 'chicken' in message_lower:
            context['preferences']['category'] = 'Fried Chicken'
        elif 'dessert' in message_lower:
            context['preferences']['category'] = 'Desserts'
    
    def get_smart_recommendations(self, message: str, context: Dict) -> List[Dict]:
        """Get intelligent recommendations"""
        try:
            db = get_db_manager()
            prefs = context['preferences']
            
            with db.get_connection() as conn:
                query = "SELECT * FROM products WHERE 1=1"
                params = []
                
                # Apply filters based on preferences
                if 'dietary' in prefs:
                    if prefs['dietary'] == 'vegetarian':
                        query += " AND dietary_tags LIKE '%vegetarian%'"
                    elif prefs['dietary'] == 'vegan':
                        query += " AND dietary_tags LIKE '%vegan%'"
                    elif prefs['dietary'] == 'healthy':
                        query += " AND category = 'Salads & Healthy Options'"
                
                if 'category' in prefs:
                    query += " AND category = ?"
                    params.append(prefs['category'])
                
                if 'flavor' in prefs:
                    if prefs['flavor'] == 'spicy':
                        query += " AND spice_level >= 6"
                    elif prefs['flavor'] == 'sweet':
                        query += " AND category = 'Desserts'"
                
                # Conversation stage ordering
                if len(context['messages']) <= 2:
                    query += " ORDER BY popularity_score DESC LIMIT 3"
                    context['stage'] = 'discovery'
                else:
                    query += " ORDER BY popularity_score DESC LIMIT 2"
                    context['stage'] = 'recommendation'
                
                cursor = conn.execute(query, params)
                rows = cursor.fetchall()
                
                products = []
                for row in rows:
                    product = dict(row)
                    for field in ['ingredients', 'dietary_tags', 'mood_tags', 'allergens']:
                        if product[field]:
                            try:
                                product[field] = json.loads(product[field])
                            except:
                                product[field] = []
                    products.append(product)
                
                return products
                
        except Exception as e:
            print(f"❌ Recommendation error: {e}")
            return []
    
    def generate_smart_response(self, message: str, products: List[Dict], context: Dict) -> str:
        """Generate smart responses"""
        message_lower = message.lower().strip()
        
        # Greetings
        if any(word in message_lower for word in ['hi', 'hello', 'hey']):
            return "Hi! I'm FoodieBot, your AI food consultant! 🤖 I specialize in finding the perfect meal for you. What type of food experience are you craving today?"
        
        # With products
        if products:
            product = products[0]
            
            if 'spicy' in message_lower:
                spice_level = product.get('spice_level', 5)
                return f"🌶️ Perfect! I found the **{product['name']}** with {spice_level}/10 heat level for ${product['price']:.2f}. {product['description'][:70]}... This will definitely bring the fire you're looking for!"
            
            elif 'sweet' in message_lower or 'dessert' in message_lower:
                return f"🍰 Sweet choice! The **{product['name']}** at ${product['price']:.2f} is absolutely divine. {product['description'][:70]}... Perfect for satisfying that sweet craving!"
            
            elif context['preferences'].get('dietary') == 'vegetarian':
                return f"🌱 Excellent! The **{product['name']}** is completely vegetarian at ${product['price']:.2f}. {product['description'][:70]}... Full of flavor and plant-based goodness!"
            
            else:
                return f"I recommend the **{product['name']}** for ${product['price']:.2f}! {product['description'][:70]}... It's incredibly popular and I think you'll love it!"
        
        # No products
        else:
            return "I'm excited to help you discover something delicious! What type of flavors or cuisines interest you most?"
    
    def calculate_smart_interest(self, message: str, context: Dict) -> float:
        """Calculate interest score"""
        message_lower = message.lower()
        
        base_score = 35.0 if context['stage'] == 'discovery' else 65.0
        
        if any(word in message_lower for word in ['love', 'like', 'want']):
            base_score += 20
        if any(word in message_lower for word in ['yes', 'perfect', 'great']):
            base_score += 25
        if '?' in message_lower:
            base_score += 10
        if '!' in message_lower:
            base_score += 8
        
        base_score += len(context['preferences']) * 10
        base_score += min(len(context['messages']) * 3, 15)
        
        return min(100.0, round(base_score, 1))

# Create bot instance
bot = SmartFoodieBotService()

# Routes
@app.get("/")
async def root():
    return {
        "message": "🤖 FoodieBot - Impressive UI Version!",
        "status": "operational"
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Chat endpoint"""
    try:
        response, products, interest_score = bot.process_message(
            request.message, 
            request.session_id
        )
        
        return ChatResponse(
            response=response,
            interest_score=interest_score,
            recommended_products=products,
            session_id=request.session_id,
            debug_info={
                "products_found": len(products),
                "conversation_stage": bot.user_context.get(request.session_id, {}).get('stage', 'discovery')
            }
        )
        
    except Exception as e:
        return ChatResponse(
            response="I'm here to help you find amazing food! What are you in the mood for?",
            interest_score=30.0,
            recommended_products=[],
            session_id=request.session_id,
            debug_info={"error": str(e)}
        )

@app.get("/api/products")
async def get_products(category: str = None, search: str = None, 
                      min_price: float = None, max_price: float = None,
                      limit: int = 24):
    """Get products for impressive UI"""
    try:
        db = get_db_manager()
        
        with db.get_connection() as conn:
            query = "SELECT * FROM products WHERE 1=1"
            params = []
            
            if category and category != "all":
                query += " AND category = ?"
                params.append(category)
            
            if search:
                query += " AND (name LIKE ? OR description LIKE ?)"
                search_term = f"%{search}%"
                params.extend([search_term, search_term])
            
            if min_price is not None:
                query += " AND price >= ?"
                params.append(min_price)
            
            if max_price is not None:
                query += " AND price <= ?"
                params.append(max_price)
            
            query += " ORDER BY popularity_score DESC LIMIT ?"
            params.append(limit)
            
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
            
            products = []
            for row in rows:
                product = dict(row)
                for field in ['ingredients', 'dietary_tags', 'mood_tags', 'allergens']:
                    if product[field]:
                        try:
                            product[field] = json.loads(product[field])
                        except:
                            product[field] = []
                products.append(product)
            
            # Get categories
            cursor = conn.execute("SELECT DISTINCT category FROM products ORDER BY category")
            categories = [row[0] for row in cursor.fetchall()]
            
            return {
                "products": products,
                "total": len(products),
                "categories": categories
            }
            
    except Exception as e:
        return {"products": [], "total": 0, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("🌐 Starting FoodieBot with Impressive UI...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
