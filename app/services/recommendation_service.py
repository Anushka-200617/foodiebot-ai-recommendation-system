"""
Advanced Recommendation Engine - Complete Implementation
Multiple algorithms as required by assignment
"""

from typing import Dict, List, Optional, Tuple
import json
import random
from app.models.database import get_db_manager

class RecommendationEngine:
    def __init__(self):
        self.recommendation_cache = {}
        self.user_interaction_history = {}
    
    def get_smart_recommendations(self, preferences: Dict, session_id: str, 
                                interest_score: float, limit: int = 5) -> List[Dict]:
        """
        Main recommendation engine combining all algorithms
        """
        try:
            db = get_db_manager()
            
            # Algorithm 1: Preference Matching
            preference_matches = self._preference_matching(preferences, db, limit * 2)
            
            # Algorithm 2: Mood-Based Filtering  
            mood_matches = self._mood_based_filtering(preferences, db, limit * 2)
            
            # Algorithm 3: Budget Optimization
            budget_matches = self._budget_optimization(preferences, db, limit * 2)
            
            # Algorithm 4: Dietary Intelligence
            dietary_matches = self._dietary_intelligence(preferences, db, limit * 2)
            
            # Algorithm 5: Collaborative Filtering (simplified)
            collaborative_matches = self._collaborative_filtering(session_id, db, limit)
            
            # Combine and rank all recommendations
            all_recommendations = self._combine_recommendations(
                preference_matches, mood_matches, budget_matches, 
                dietary_matches, collaborative_matches, interest_score
            )
            
            # Remove duplicates and limit results
            final_recommendations = self._deduplicate_and_rank(all_recommendations, limit)
            
            # Store recommendation history
            self._store_recommendation_history(session_id, final_recommendations, preferences)
            
            return final_recommendations
            
        except Exception as e:
            print(f"Recommendation engine error: {e}")
            return self._fallback_recommendations(limit)
    
    def _preference_matching(self, preferences: Dict, db, limit: int) -> List[Tuple[Dict, float]]:
        """Algorithm 1: Match conversation keywords to product tags"""
        recommendations = []
        
        with db.get_connection() as conn:
            # Build dynamic query based on preferences
            query = "SELECT * FROM products WHERE 1=1"
            params = []
            score_multiplier = 1.0
            
            # Category matching
            if 'categories' in preferences:
                category_conditions = []
                for category in preferences['categories']:
                    category_conditions.append("category = ?")
                    params.append(category)
                if category_conditions:
                    query += " AND (" + " OR ".join(category_conditions) + ")"
                    score_multiplier += 0.3
            
            # Mood tag matching
            if 'mood' in preferences:
                for mood in preferences['mood']:
                    query += " AND (mood_tags LIKE ? OR dietary_tags LIKE ?)"
                    params.extend([f"%{mood}%", f"%{mood}%"])
                    score_multiplier += 0.2
            
            # Dietary tag matching
            if 'dietary' in preferences:
                for diet in preferences['dietary']:
                    query += " AND (dietary_tags LIKE ? OR mood_tags LIKE ?)"
                    params.extend([f"%{diet}%", f"%{diet}%"])
                    score_multiplier += 0.2
            
            query += " ORDER BY popularity_score DESC LIMIT ?"
            params.append(limit)
            
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
            
            for row in rows:
                product = db.parse_json_fields(dict(row))
                match_score = self._calculate_preference_match_score(product, preferences) * score_multiplier
                recommendations.append((product, match_score))
        
        return recommendations
    
    def _mood_based_filtering(self, preferences: Dict, db, limit: int) -> List[Tuple[Dict, float]]:
        """Algorithm 2: Map customer emotions to product mood_tags"""
        recommendations = []
        
        if 'mood' not in preferences:
            return recommendations
        
        with db.get_connection() as conn:
            mood_conditions = []
            params = []
            
            for mood in preferences['mood']:
                mood_conditions.append("mood_tags LIKE ?")
                params.append(f"%{mood}%")
            
            if mood_conditions:
                query = f"""
                SELECT * FROM products 
                WHERE ({' OR '.join(mood_conditions)}) 
                ORDER BY popularity_score DESC 
                LIMIT ?
                """
                params.append(limit)
                
                cursor = conn.execute(query, params)
                rows = cursor.fetchall()
                
                for row in rows:
                    product = db.parse_json_fields(dict(row))
                    mood_score = self._calculate_mood_match_score(product, preferences['mood'])
                    recommendations.append((product, mood_score))
        
        return recommendations
    
    def _budget_optimization(self, preferences: Dict, db, limit: int) -> List[Tuple[Dict, float]]:
        """Algorithm 3: Find best value within price range"""
        recommendations = []
        
        max_budget = preferences.get('max_budget', 50)  # Default max budget
        
        with db.get_connection() as conn:
            # Find products within budget, optimized for value
            query = """
            SELECT *, 
                   (popularity_score / price) as value_score
            FROM products 
            WHERE price <= ? 
            ORDER BY value_score DESC, popularity_score DESC 
            LIMIT ?
            """
            
            cursor = conn.execute(query, (max_budget, limit))
            rows = cursor.fetchall()
            
            for row in rows:
                product = db.parse_json_fields(dict(row))
                # Calculate value score (popularity per dollar)
                value_score = (product['popularity_score'] / max(product['price'], 1)) * 10
                recommendations.append((product, value_score))
        
        return recommendations
    
    def _dietary_intelligence(self, preferences: Dict, db, limit: int) -> List[Tuple[Dict, float]]:
        """Algorithm 4: Strict filtering for restrictions/allergens"""
        recommendations = []
        
        if 'dietary' not in preferences:
            return recommendations
        
        with db.get_connection() as conn:
            for dietary_pref in preferences['dietary']:
                # Positive matching for dietary preferences
                query = """
                SELECT * FROM products 
                WHERE dietary_tags LIKE ? 
                ORDER BY popularity_score DESC 
                LIMIT ?
                """
                
                cursor = conn.execute(query, (f"%{dietary_pref}%", limit))
                rows = cursor.fetchall()
                
                for row in rows:
                    product = db.parse_json_fields(dict(row))
                    
                    # Check allergen compatibility
                    if self._check_allergen_compatibility(product, preferences):
                        dietary_score = 95.0  # High score for dietary matches
                        recommendations.append((product, dietary_score))
        
        return recommendations
    
    def _collaborative_filtering(self, session_id: str, db, limit: int) -> List[Tuple[Dict, float]]:
        """Algorithm 5: 'Customers who liked X also liked Y' (simplified)"""
        recommendations = []
        
        # Get user's interaction history
        user_history = self.user_interaction_history.get(session_id, [])
        
        if not user_history:
            # New user - recommend popular items
            with db.get_connection() as conn:
                cursor = conn.execute("""
                SELECT * FROM products 
                ORDER BY popularity_score DESC 
                LIMIT ?
                """, (limit,))
                rows = cursor.fetchall()
                
                for row in rows:
                    product = db.parse_json_fields(dict(row))
                    popularity_score = product['popularity_score'] / 100.0 * 80  # Scale to 80 max
                    recommendations.append((product, popularity_score))
        else:
            # Existing user - find similar products
            with db.get_connection() as conn:
                # Find products in same categories as previously liked items
                liked_categories = [item['category'] for item in user_history if item.get('liked')]
                
                if liked_categories:
                    category_conditions = []
                    params = []
                    for category in set(liked_categories):
                        category_conditions.append("category = ?")
                        params.append(category)
                    
                    query = f"""
                    SELECT * FROM products 
                    WHERE ({' OR '.join(category_conditions)})
                    ORDER BY popularity_score DESC 
                    LIMIT ?
                    """
                    params.append(limit)
                    
                    cursor = conn.execute(query, params)
                    rows = cursor.fetchall()
                    
                    for row in rows:
                        product = db.parse_json_fields(dict(row))
                        similarity_score = 70.0  # Base collaborative score
                        recommendations.append((product, similarity_score))
        
        return recommendations
    
    def _combine_recommendations(self, *recommendation_lists, interest_score: float) -> List[Tuple[Dict, float]]:
        """Combine recommendations from different algorithms"""
        combined = []
        
        # Weight algorithms based on interest score
        weights = self._get_algorithm_weights(interest_score)
        
        for i, rec_list in enumerate(recommendation_lists):
            weight = weights[i] if i < len(weights) else 0.5
            for product, score in rec_list:
                weighted_score = score * weight
                combined.append((product, weighted_score, f"algo_{i+1}"))
        
        return combined
    
    def _get_algorithm_weights(self, interest_score: float) -> List[float]:
        """Get algorithm weights based on interest score"""
        if interest_score >= 80:
            # High interest - prioritize order-focused algorithms
            return [1.2, 1.0, 0.8, 1.1, 0.9]  # Preference, Mood, Budget, Dietary, Collaborative
        elif interest_score >= 60:
            # Medium-high interest - balanced approach
            return [1.0, 1.1, 1.0, 1.0, 0.8]
        elif interest_score >= 40:
            # Medium interest - focus on discovery
            return [0.9, 1.2, 1.1, 0.9, 1.0]
        else:
            # Low interest - popular items and budget
            return [0.8, 0.9, 1.3, 0.8, 1.2]
    
    def _deduplicate_and_rank(self, recommendations: List[Tuple], limit: int) -> List[Dict]:
        """Remove duplicates and return top recommendations"""
        seen_products = set()
        unique_recommendations = []
        
        # Sort by weighted score
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        for product, score, source in recommendations:
            product_id = product['product_id']
            if product_id not in seen_products:
                seen_products.add(product_id)
                product['recommendation_score'] = round(score, 1)
                product['recommendation_source'] = source
                unique_recommendations.append(product)
                
                if len(unique_recommendations) >= limit:
                    break
        
        return unique_recommendations
    
    def _calculate_preference_match_score(self, product: Dict, preferences: Dict) -> float:
        """Calculate how well a product matches user preferences"""
        score = 50.0  # Base score
        
        # Category match
        if 'categories' in preferences:
            if product['category'] in preferences['categories']:
                score += 20.0
        
        # Mood tag matches
        if 'mood' in preferences:
            product_moods = product.get('mood_tags', [])
            for mood in preferences['mood']:
                if any(mood.lower() in str(tag).lower() for tag in product_moods):
                    score += 15.0
        
        # Dietary matches
        if 'dietary' in preferences:
            product_dietary = product.get('dietary_tags', [])
            for diet in preferences['dietary']:
                if any(diet.lower() in str(tag).lower() for tag in product_dietary):
                    score += 15.0
        
        # Price consideration
        if 'max_budget' in preferences:
            if product['price'] <= preferences['max_budget']:
                score += 10.0
            else:
                score -= 20.0  # Penalize over-budget items
        
        # Popularity boost
        score += (product['popularity_score'] / 100.0) * 10
        
        return min(score, 100.0)
    
    def _calculate_mood_match_score(self, product: Dict, user_moods: List[str]) -> float:
        """Calculate mood matching score"""
        score = 40.0
        product_moods = product.get('mood_tags', [])
        
        matches = 0
        for user_mood in user_moods:
            if any(user_mood.lower() in str(tag).lower() for tag in product_moods):
                matches += 1
        
        # Boost score based on matches
        score += matches * 20.0
        
        # Add popularity factor
        score += (product['popularity_score'] / 100.0) * 15
        
        return min(score, 100.0)
    
    def _check_allergen_compatibility(self, product: Dict, preferences: Dict) -> bool:
        """Check if product is safe for user's dietary restrictions"""
        # Simplified allergen checking
        product_allergens = product.get('allergens', [])
        
        # Check for obvious conflicts
        if 'dietary' in preferences:
            if 'vegan' in preferences['dietary']:
                conflict_ingredients = ['dairy', 'eggs', 'honey']
                if any(allergen in conflict_ingredients for allergen in product_allergens):
                    return False
            
            if 'vegetarian' in preferences['dietary']:
                product_ingredients = product.get('ingredients', [])
                meat_words = ['beef', 'chicken', 'pork', 'fish', 'meat']
                if any(meat in str(product_ingredients).lower() for meat in meat_words):
                    return False
        
        return True
    
    def _store_recommendation_history(self, session_id: str, recommendations: List[Dict], preferences: Dict):
        """Store recommendation history for learning"""
        if session_id not in self.user_interaction_history:
            self.user_interaction_history[session_id] = []
        
        for rec in recommendations:
            self.user_interaction_history[session_id].append({
                'product_id': rec['product_id'],
                'category': rec['category'],
                'preferences_when_recommended': preferences.copy(),
                'recommendation_score': rec.get('recommendation_score', 0),
                'timestamp': 'now'
            })
        
        # Keep only last 50 interactions per session
        self.user_interaction_history[session_id] = self.user_interaction_history[session_id][-50:]
    
    def _fallback_recommendations(self, limit: int) -> List[Dict]:
        """Fallback recommendations when main engine fails"""
        try:
            db = get_db_manager()
            with db.get_connection() as conn:
                cursor = conn.execute("""
                SELECT * FROM products 
                ORDER BY popularity_score DESC 
                LIMIT ?
                """, (limit,))
                rows = cursor.fetchall()
                return [db.parse_json_fields(dict(row)) for row in rows]
        except:
            return []
    
    def get_recommendation_analytics(self) -> Dict:
        """Get analytics about recommendation performance"""
        total_sessions = len(self.user_interaction_history)
        total_recommendations = sum(len(history) for history in self.user_interaction_history.values())
        
        # Category analysis
        category_counts = {}
        for history in self.user_interaction_history.values():
            for item in history:
                category = item.get('category', 'Unknown')
                category_counts[category] = category_counts.get(category, 0) + 1
        
        return {
            'total_sessions_with_recommendations': total_sessions,
            'total_recommendations_made': total_recommendations,
            'avg_recommendations_per_session': total_recommendations / max(total_sessions, 1),
            'top_recommended_categories': sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        }

# Global recommendation engine
recommendation_engine = RecommendationEngine()
