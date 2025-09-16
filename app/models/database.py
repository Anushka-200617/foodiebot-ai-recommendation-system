"""
Database connection and management for FoodieBot
Uses SQLite with proper JSON handling
"""

import sqlite3
import json
import os
from typing import Dict, List, Optional, Any
from contextlib import contextmanager

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database and create tables"""
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            # Create products table
            conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                ingredients TEXT NOT NULL,
                price REAL NOT NULL,
                calories INTEGER NOT NULL,
                prep_time TEXT NOT NULL,
                dietary_tags TEXT NOT NULL,
                mood_tags TEXT NOT NULL,
                allergens TEXT NOT NULL,
                popularity_score INTEGER DEFAULT 50,
                chef_special BOOLEAN DEFAULT FALSE,
                limited_time BOOLEAN DEFAULT FALSE,
                spice_level INTEGER DEFAULT 1,
                image_prompt TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # Create conversations table
            conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                user_message TEXT NOT NULL,
                bot_response TEXT NOT NULL,
                interest_score REAL DEFAULT 0.0,
                recommended_products TEXT,
                user_preferences TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # Create indexes for performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_product_category ON products(category)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_product_price ON products(price)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_conversation_session ON conversations(session_id)")
            
            conn.commit()
            print("Database tables created successfully")
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable dict-like access
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def parse_json_fields(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """Parse JSON string fields back to Python objects"""
        json_fields = ['ingredients', 'dietary_tags', 'mood_tags', 'allergens']
        parsed_row = dict(row)
        
        for field in json_fields:
            if field in parsed_row and parsed_row[field]:
                try:
                    parsed_row[field] = json.loads(parsed_row[field])
                except:
                    parsed_row[field] = []
            else:
                parsed_row[field] = []
        
        return parsed_row

# Global database manager
db_manager: Optional[DatabaseManager] = None

def get_db_manager() -> DatabaseManager:
    """Get global database manager instance"""
    global db_manager
    if db_manager is None:
        raise RuntimeError("Database not initialized")
    return db_manager

def init_database(db_path: str):
    """Initialize global database manager"""
    global db_manager
    db_manager = DatabaseManager(db_path)
    print(f"Database initialized: {db_path}")
