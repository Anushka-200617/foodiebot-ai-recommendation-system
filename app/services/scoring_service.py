"""
Fixed Interest Scoring Service with Robust Error Handling
"""

import re
from typing import Dict, List
from datetime import datetime

# Import with error handling
try:
    from app.services.sentiment_service import sentiment_analyzer
    SENTIMENT_AVAILABLE = True
except ImportError:
    SENTIMENT_AVAILABLE = False
    print("⚠️ Sentiment service not available, using basic scoring")

class RobustInterestScoringService:
    def __init__(self):
        # Exact scoring factors from assignment
        self.ENGAGEMENT_FACTORS = {
            'specific_preferences': 15,
            'dietary_restrictions': 10,
            'budget_mention': 5,
            'mood_indication': 20,
            'question_asking': 10,
            'enthusiasm_words': 8,
            'price_inquiry': 25,
            'order_intent': 30,
        }
        
        self.NEGATIVE_FACTORS = {
            'hesitation': -10,
            'budget_concern': -15,
            'dietary_conflict': -20,
            'rejection': -25,
            'delay_response': -5,
        }
        
        self.session_scores = {}
        self.conversation_history = {}
    
    def calculate_interest_score(self, user_message: str, session_id: str, 
                               previous_recommendations: List[Dict] = None) -> float:
        """
        Calculate interest score with robust error handling
        """
        try:
            message_lower = user_message.lower()
            current_score = self.session_scores.get(session_id, 30.0)
            
            # Calculate base score using assignment factors
            score_changes = []
            
            # Positive factors
            if self._has_specific_preferences(message_lower):
                score_changes.append(self.ENGAGEMENT_FACTORS['specific_preferences'])
            
            if self._mentions_dietary_restrictions(message_lower):
                score_changes.append(self.ENGAGEMENT_FACTORS['dietary_restrictions'])
            
            if self._mentions_budget(message_lower):
                score_changes.append(self.ENGAGEMENT_FACTORS['budget_mention'])
            
            if self._indicates_mood(message_lower):
                score_changes.append(self.ENGAGEMENT_FACTORS['mood_indication'])
            
            if self._asks_questions(message_lower):
                score_changes.append(self.ENGAGEMENT_FACTORS['question_asking'])
            
            if self._shows_enthusiasm(message_lower):
                score_changes.append(self.ENGAGEMENT_FACTORS['enthusiasm_words'])
            
            if self._inquires_about_price(message_lower):
                score_changes.append(self.ENGAGEMENT_FACTORS['price_inquiry'])
            
            if self._shows_order_intent(message_lower):
                score_changes.append(self.ENGAGEMENT_FACTORS['order_intent'])
            
            # Negative factors
            if self._shows_hesitation(message_lower):
                score_changes.append(self.NEGATIVE_FACTORS['hesitation'])
            
            if self._shows_budget_concern(message_lower):
                score_changes.append(self.NEGATIVE_FACTORS['budget_concern'])
            
            if self._shows_rejection(message_lower):
                score_changes.append(self.NEGATIVE_FACTORS['rejection'])
            
            # Calculate new score
            score_delta = sum(score_changes)
            new_score = current_score + score_delta
            
            # Apply NLP enhancements if available
            if SENTIMENT_AVAILABLE:
                try:
                    new_score = self._apply_nlp_enhancements(new_score, user_message, session_id)
                except Exception as e:
                    print(f"NLP enhancement error: {e}")
                    # Continue with base score
            
            # Apply conversation context
            final_score = self._apply_conversation_context(new_score, session_id)
            
            # Normalize to 0-100
            final_score = max(0, min(100, final_score))
            
            # Store score
            self.session_scores[session_id] = final_score
            
            # Store conversation history
            if session_id not in self.conversation_history:
                self.conversation_history[session_id] = []
            
            self.conversation_history[session_id].append({
                'message': user_message,
                'score': final_score,
                'score_changes': score_changes,
                'timestamp': datetime.now().isoformat()
            })
            
            # Keep only last 10 entries
            self.conversation_history[session_id] = self.conversation_history[session_id][-10:]
            
            return round(final_score, 1)
            
        except Exception as e:
            print(f"Interest scoring error: {e}")
            # Return a safe default score
            return 40.0
    
    def _apply_nlp_enhancements(self, base_score: float, message: str, session_id: str) -> float:
        """Apply NLP sentiment analysis enhancements"""
        try:
            sentiment_result = sentiment_analyzer.analyze_comprehensive_sentiment(message, 'food')
            
            enhanced_score = base_score
            
            # Sentiment multiplier
            if sentiment_result.overall_sentiment == 'positive':
                enhanced_score *= 1.15
            elif sentiment_result.overall_sentiment == 'negative':
                enhanced_score *= 0.85
            
            # Confidence boost
            if sentiment_result.confidence_score > 0.7:
                enhanced_score += 5
            
            # Emotion intensity
            enhanced_score += sentiment_result.emotion_intensity * 10
            
            # Specific emotions
            emotions = sentiment_result.specific_emotions
            if emotions.get('excitement', 0) > 0.5:
                enhanced_score += 8
            if emotions.get('enthusiasm', 0) > 0.5:
                enhanced_score += 6
            if emotions.get('frustration', 0) > 0.5:
                enhanced_score -= 10
            
            # Urgency
            if sentiment_result.urgency_level == 'high':
                enhanced_score += 10
            elif sentiment_result.urgency_level == 'medium':
                enhanced_score += 4
            
            # Food-specific sentiment
            if sentiment_result.food_specific_sentiment == 'positive':
                enhanced_score += 5
            elif sentiment_result.food_specific_sentiment == 'negative':
                enhanced_score -= 8
            
            return enhanced_score
            
        except Exception as e:
            print(f"NLP enhancement error: {e}")
            return base_score
    
    def _apply_conversation_context(self, score: float, session_id: str) -> float:
        """Apply conversation context"""
        history = self.conversation_history.get(session_id, [])
        
        if len(history) > 1:
            # Recent trend analysis
            recent_scores = [h['score'] for h in history[-3:]]
            if len(recent_scores) >= 2:
                if recent_scores[-1] > recent_scores[-2]:
                    score += 3  # Positive trend
                elif recent_scores[-1] < recent_scores[-2]:
                    score -= 2  # Negative trend
        
        return score
    
    def get_score_analysis(self, session_id: str) -> Dict:
        """Get score analysis for session"""
        current_score = self.session_scores.get(session_id, 0)
        history = self.conversation_history.get(session_id, [])
        
        analysis = {
            "current_score": current_score,
            "conversation_length": len(history),
            "engagement_level": self._get_engagement_level(current_score),
            "score_trend": "stable"
        }
        
        if len(history) >= 2:
            recent_scores = [h['score'] for h in history[-3:]]
            if recent_scores[-1] > recent_scores[0]:
                analysis["score_trend"] = "improving"
            elif recent_scores[-1] < recent_scores[0]:
                analysis["score_trend"] = "declining"
        
        # Add NLP analysis if available
        if SENTIMENT_AVAILABLE:
            try:
                sentiment_analysis = sentiment_analyzer.analyze_comprehensive_sentiment(
                    history[-1]['message'] if history else "No messages yet", 'food'
                )
                analysis["sentiment"] = {
                    "overall": sentiment_analysis.overall_sentiment,
                    "confidence": sentiment_analysis.confidence_score,
                    "emotions": sentiment_analysis.specific_emotions
                }
            except:
                analysis["sentiment"] = {"status": "unavailable"}
        
        return analysis
    
    def _get_engagement_level(self, score: float) -> str:
        """Get engagement level description"""
        if score >= 80:
            return "Very High - Ready to Order"
        elif score >= 60:
            return "High - Strong Interest"
        elif score >= 40:
            return "Medium - Considering Options"
        elif score >= 20:
            return "Low - Browsing"
        else:
            return "Very Low - Disengaged"
    
    # Original detection methods (robust versions)
    def _has_specific_preferences(self, message: str) -> bool:
        keywords = ['love', 'like', 'favorite', 'prefer', 'want', 'craving', 'enjoy', 'spicy', 'sweet']
        return any(keyword in message for keyword in keywords)
    
    def _mentions_dietary_restrictions(self, message: str) -> bool:
        keywords = ['vegetarian', 'vegan', 'gluten-free', 'keto', 'allergic', 'dairy-free']
        return any(keyword in message for keyword in keywords)
    
    def _mentions_budget(self, message: str) -> bool:
        return bool(re.search(r'under \$?\d+|budget|cheap|affordable|inexpensive', message))
    
    def _indicates_mood(self, message: str) -> bool:
        keywords = ['feeling', 'mood', 'adventurous', 'comfort', 'healthy', 'hungry', 'starving']
        return any(keyword in message for keyword in keywords)
    
    def _asks_questions(self, message: str) -> bool:
        return '?' in message or any(word in message for word in ['what', 'how', 'when', 'where'])
    
    def _shows_enthusiasm(self, message: str) -> bool:
        keywords = ['amazing', 'awesome', 'perfect', 'great', 'love it', 'fantastic', 'excellent']
        return any(keyword in message for keyword in keywords) or '!' in message
    
    def _inquires_about_price(self, message: str) -> bool:
        keywords = ['cost', 'price', 'how much', 'expensive', 'worth']
        return any(keyword in message for keyword in keywords)
    
    def _shows_order_intent(self, message: str) -> bool:
        keywords = ['order', 'buy', 'get', 'take', "i'll have", 'purchase', 'add to cart']
        return any(keyword in message for keyword in keywords)
    
    def _shows_hesitation(self, message: str) -> bool:
        keywords = ['maybe', 'not sure', 'uncertain', "i don't know", 'possibly']
        return any(word in message for word in keywords)
    
    def _shows_budget_concern(self, message: str) -> bool:
        keywords = ['too expensive', "can't afford", 'too much', 'pricey', 'costly']
        return any(word in message for word in keywords)
    
    def _shows_rejection(self, message: str) -> bool:
        keywords = ["don't like", 'hate', 'dislike', 'not interested', 'no thanks']
        return any(word in message for word in keywords)

# Global scoring service
scoring_service = RobustInterestScoringService()
