"""
API endpoints for product operations
"""

from typing import Optional, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.database import get_db_manager

# Create API router
router = APIRouter()

# Response models
class ProductResponse(BaseModel):
    products: List[dict]
    total: int

@router.get("/products", response_model=ProductResponse)
async def get_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 50
):
    """Get products with optional filtering"""
    try:
        db = get_db_manager()
        
        with db.get_connection() as conn:
            query = "SELECT * FROM products"
            params = []
            conditions = []
            
            if category:
                conditions.append("category = ?")
                params.append(category)
            
            if search:
                conditions.append("(name LIKE ? OR description LIKE ?)")
                params.extend([f"%{search}%", f"%{search}%"])
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY popularity_score DESC LIMIT ?"
            params.append(limit)
            
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
            
            products = [db.parse_json_fields(dict(row)) for row in rows]
            
            return ProductResponse(
                products=products,
                total=len(products)
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories")
async def get_categories():
    """Get all product categories"""
    try:
        db = get_db_manager()
        
        with db.get_connection() as conn:
            cursor = conn.execute("SELECT DISTINCT category FROM products ORDER BY category")
            categories = [row[0] for row in cursor.fetchall()]
            
            return {"categories": categories, "total": len(categories)}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
