"""
FoodieBot Main FastAPI Application
Complete conversational AI system with interest scoring and recommendations
"""

import os
import json
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Import our modules
from app.models.database import init_database, get_db_manager
from app.services.scoring_service import scoring_service
from app.services.ai_service import ai_service
from app.api.products import router as products_router

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="FoodieBot - Conversational AI Food System",
    description="Complete AI-powered food recommendation system with interest scoring",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(products_router, prefix="/api", tags=["products"])

# Pydantic models for requests/responses
class ChatRequest(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    response: str
    interest_score: float
    recommended_products: List[Dict]
    session_id: str

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database and check for products"""
    db_path = os.getenv("DATABASE_URL", "./data/foodiebot.db")
    init_database(db_path)
    
    # Check if products exist
    try:
        db = get_db_manager()
        with db.get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM products")
            count = cursor.fetchone()[0]
            
            if count == 0:
                print("⚠️  No products found in database!")
                print("🔧 Run: python scripts/populate_database.py")
            else:
                print(f"✅ Found {count} products in database")
    except Exception as e:
        print(f"❌ Database check failed: {e}")
    
    print("🚀 FoodieBot API is ready!")

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "🤖 FoodieBot Conversational AI API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/chat",
            "products": "/api/products",
            "analytics": "/api/analytics"
        },
        "docs": "/docs"
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint - processes user messages and returns AI responses
    with interest scoring and product recommendations
    """
    try:
        # Calculate interest score (0-100%)
        interest_score = scoring_service.calculate_interest_score(
            request.message, 
            request.session_id
        )
        
        # Get user preferences and AI response
        ai_response, preferences = ai_service.process_message(
            request.message, 
            request.session_id
        )
        
        # Get product recommendations based on preferences
        recommended_products = get_recommendations_from_preferences(preferences)
        
        # Update AI response with product information
        if recommended_products:
            final_response, _ = ai_service.process_message(
                request.message, 
                request.session_id, 
                recommended_products
            )
        else:
            final_response = ai_response
        
        # Save conversation to database
        db = get_db_manager()
        with db.get_connection() as conn:
            conn.execute("""
            INSERT INTO conversations (
                session_id, user_message, bot_response, interest_score, 
                recommended_products, user_preferences
            ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                request.session_id, 
                request.message, 
                final_response,
                interest_score, 
                json.dumps([p['product_id'] for p in recommended_products]),
                json.dumps(preferences)
            ))
            conn.commit()
        
        return ChatResponse(
            response=final_response,
            interest_score=interest_score,
            recommended_products=recommended_products[:3],  # Top 3 recommendations
            session_id=request.session_id
        )
        
    except Exception as e:
        print(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics")
async def get_analytics():
    """Get conversation analytics and metrics"""
    try:
        db = get_db_manager()
        
        with db.get_connection() as conn:
            stats = {}
            
            # Total conversations
            cursor = conn.execute("SELECT COUNT(*) FROM conversations")
            stats['total_conversations'] = cursor.fetchone()[0]
            
            # Average interest score
            cursor = conn.execute("SELECT AVG(interest_score) FROM conversations WHERE interest_score > 0")
            avg_score = cursor.fetchone()[0]
            stats['average_interest_score'] = round(avg_score, 1) if avg_score else 0
            
            # Active sessions
            cursor = conn.execute("SELECT COUNT(DISTINCT session_id) FROM conversations")
            stats['active_sessions'] = cursor.fetchone()[0]
            
            # Recent conversations
            cursor = conn.execute("""
            SELECT user_message, bot_response, interest_score, timestamp 
            FROM conversations 
            ORDER BY timestamp DESC 
            LIMIT 20
            """)
            recent_conversations = []
            for row in cursor.fetchall():
                recent_conversations.append({
                    "user_message": row[0][:100] + "..." if len(row[0]) > 100 else row[0],
                    "bot_response": row[1][:100] + "..." if len(row[1]) > 100 else row[1],
                    "interest_score": row[2],
                    "timestamp": row[3]
                })
            
            stats['recent_conversations'] = recent_conversations
            
            return stats
            
    except Exception as e:
        print(f"Analytics error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def get_recommendations_from_preferences(preferences: Dict) -> List[Dict]:
    """Get product recommendations based on user preferences"""
    if not preferences:
        return []
    
    try:
        db = get_db_manager()
        
        with db.get_connection() as conn:
            query = "SELECT * FROM products WHERE 1=1"
            params = []
            
            # Filter by budget
            if 'max_budget' in preferences:
                query += " AND price <= ?"
                params.append(preferences['max_budget'])
            
            # Filter by dietary preferences
            if 'dietary' in preferences:
                for diet in preferences['dietary']:
                    query += " AND (dietary_tags LIKE ? OR mood_tags LIKE ?)"
                    params.extend([f"%{diet}%", f"%{diet}%"])
            
            # Filter by mood preferences
            if 'mood' in preferences:
                mood_conditions = []
                for mood in preferences['mood']:
                    mood_conditions.append("(mood_tags LIKE ? OR dietary_tags LIKE ?)")
                    params.extend([f"%{mood}%", f"%{mood}%"])
                if mood_conditions:
                    query += " AND (" + " OR ".join(mood_conditions) + ")"
            
            query += " ORDER BY popularity_score DESC LIMIT 5"
            
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
            
            return [db.parse_json_fields(dict(row)) for row in rows]
            
    except Exception as e:
        print(f"Recommendation error: {e}")
        return []

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
