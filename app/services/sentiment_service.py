"""
Robust Sentiment Analysis Service with Fallbacks
Works even if NLP libraries are missing
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class SentimentResult:
    """Sentiment analysis result"""
    overall_sentiment: str
    confidence_score: float
    emotion_intensity: float
    specific_emotions: Dict[str, float]
    food_specific_sentiment: Optional[str]
    urgency_level: str
    sarcasm_detected: bool
    mixed_sentiment: bool

class RobustSentimentAnalyzer:
    def __init__(self):
        # Try to import NLP libraries
        self.nlp_available = False
        self.vader_analyzer = None
        
        try:
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            self.vader_analyzer = SentimentIntensityAnalyzer()
            self.nlp_available = True
            print("✅ NLP libraries loaded successfully")
        except ImportError:
            print("⚠️ NLP libraries not available, using enhanced rule-based analysis")
        
        # Enhanced food-related dictionaries
        self.food_sentiment_words = {
            'positive': {
                'love', 'amazing', 'delicious', 'fantastic', 'perfect', 'incredible', 
                'awesome', 'outstanding', 'excellent', 'wonderful', 'craving', 'hungry',
                'yum', 'yummy', 'tasty', 'flavorful', 'satisfying', 'mouth-watering',
                'divine', 'heavenly', 'scrumptious', 'appetizing', 'fresh', 'juicy',
                'crispy', 'tender', 'rich', 'creamy', 'spicy', 'savory', 'sweet'
            },
            'negative': {
                'hate', 'disgusting', 'terrible', 'awful', 'horrible', 'nasty', 'gross',
                'disappointing', 'bland', 'tasteless', 'stale', 'overcooked', 'undercooked',
                'soggy', 'dry', 'burnt', 'salty', 'bitter', 'sour', 'expired', 'rotten',
                'overpriced', 'expensive', 'cheap', 'bad'
            }
        }
        
        self.emotion_indicators = {
            'excitement': ['!', '!!', '!!!', 'excited', 'pumped', 'thrilled', 'stoked', 'ecstatic', 'amazing'],
            'frustration': ['frustrated', 'annoyed', 'irritated', 'fed up', 'angry', 'mad'],
            'curiosity': ['?', 'wondering', 'curious', 'interested', 'what about', 'tell me'],
            'satisfaction': ['satisfied', 'content', 'happy', 'pleased', 'glad', 'good'],
            'uncertainty': ['maybe', 'perhaps', 'not sure', 'uncertain', 'might', 'possibly'],
            'enthusiasm': ['absolutely', 'definitely', 'totally', 'completely', 'really', 'super']
        }
        
        self.urgency_words = {
            'high': ['asap', 'urgent', 'immediately', 'right now', 'hurry', 'rush', 'quick', 'fast', 'starving'],
            'medium': ['soon', 'quickly', 'when possible', 'hungry'],
            'low': ['whenever', 'no rush', 'take your time', 'eventually', 'later']
        }
    
    def analyze_comprehensive_sentiment(self, text: str, context: str = 'general') -> SentimentResult:
        """
        Analyze sentiment with robust error handling
        """
        try:
            if self.nlp_available and self.vader_analyzer:
                return self._advanced_nlp_analysis(text)
            else:
                return self._enhanced_rule_analysis(text)
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return self._basic_fallback_analysis(text)
    
    def _advanced_nlp_analysis(self, text: str) -> SentimentResult:
        """Advanced analysis using VADER"""
        try:
            # VADER analysis
            scores = self.vader_analyzer.polarity_scores(text)
            
            # Overall sentiment from compound score
            compound = scores['compound']
            if compound >= 0.05:
                overall_sentiment = 'positive'
            elif compound <= -0.05:
                overall_sentiment = 'negative'
            else:
                overall_sentiment = 'neutral'
            
            # Combine with rule-based analysis
            food_sentiment = self._analyze_food_words(text)
            emotions = self._detect_emotions(text)
            urgency = self._detect_urgency(text)
            
            return SentimentResult(
                overall_sentiment=overall_sentiment,
                confidence_score=abs(compound),
                emotion_intensity=abs(compound),
                specific_emotions=emotions,
                food_specific_sentiment=food_sentiment,
                urgency_level=urgency,
                sarcasm_detected=self._detect_sarcasm(text, overall_sentiment),
                mixed_sentiment=self._detect_mixed_sentiment(text)
            )
            
        except Exception as e:
            print(f"VADER analysis error: {e}")
            return self._enhanced_rule_analysis(text)
    
    def _enhanced_rule_analysis(self, text: str) -> SentimentResult:
        """Enhanced rule-based analysis"""
        text_lower = text.lower()
        
        # Count positive and negative words
        positive_count = sum(1 for word in self.food_sentiment_words['positive'] if word in text_lower)
        negative_count = sum(1 for word in self.food_sentiment_words['negative'] if word in text_lower)
        
        # Determine overall sentiment
        if positive_count > negative_count:
            overall_sentiment = 'positive'
            confidence = min(0.8, 0.5 + (positive_count - negative_count) * 0.1)
        elif negative_count > positive_count:
            overall_sentiment = 'negative'
            confidence = min(0.8, 0.5 + (negative_count - positive_count) * 0.1)
        else:
            overall_sentiment = 'neutral'
            confidence = 0.3
        
        # Enhanced emotion detection
        emotions = self._detect_emotions(text_lower)
        
        # Food-specific sentiment
        food_sentiment = self._analyze_food_words(text_lower)
        
        # Urgency detection
        urgency = self._detect_urgency(text_lower)
        
        # Emotion intensity based on punctuation and caps
        intensity = 0.5
        if '!' in text:
            intensity += 0.2
        if '!!!' in text:
            intensity += 0.3
        if any(word.isupper() for word in text.split()):
            intensity += 0.2
        
        intensity = min(1.0, intensity)
        
        return SentimentResult(
            overall_sentiment=overall_sentiment,
            confidence_score=confidence,
            emotion_intensity=intensity,
            specific_emotions=emotions,
            food_specific_sentiment=food_sentiment,
            urgency_level=urgency,
            sarcasm_detected=self._detect_sarcasm(text_lower, overall_sentiment),
            mixed_sentiment=positive_count > 0 and negative_count > 0
        )
    
    def _analyze_food_words(self, text: str) -> str:
        """Analyze food-specific sentiment"""
        positive_matches = sum(1 for word in self.food_sentiment_words['positive'] if word in text)
        negative_matches = sum(1 for word in self.food_sentiment_words['negative'] if word in text)
        
        if positive_matches > negative_matches:
            return 'positive'
        elif negative_matches > positive_matches:
            return 'negative'
        else:
            return 'neutral'
    
    def _detect_emotions(self, text: str) -> Dict[str, float]:
        """Detect specific emotions"""
        emotions = {}
        
        for emotion, indicators in self.emotion_indicators.items():
            score = 0.0
            for indicator in indicators:
                if indicator in text:
                    # Weight longer indicators more
                    weight = 0.3 if len(indicator) > 3 else 0.2
                    score += weight
            
            emotions[emotion] = min(score, 1.0)
        
        return emotions
    
    def _detect_urgency(self, text: str) -> str:
        """Detect urgency level"""
        for level, indicators in self.urgency_words.items():
            if any(indicator in text for indicator in indicators):
                return level
        
        # Check punctuation for urgency
        if '!' in text or any(word.isupper() for word in text.split()):
            return 'medium'
        
        return 'low'
    
    def _detect_sarcasm(self, text: str, sentiment: str) -> bool:
        """Basic sarcasm detection"""
        sarcasm_phrases = [
            'oh great', 'just wonderful', 'how nice', 'sure thing',
            'yeah right', 'absolutely not', 'just perfect'
        ]
        
        return any(phrase in text for phrase in sarcasm_phrases)
    
    def _detect_mixed_sentiment(self, text: str) -> bool:
        """Detect mixed sentiments"""
        positive_count = sum(1 for word in self.food_sentiment_words['positive'] if word in text.lower())
        negative_count = sum(1 for word in self.food_sentiment_words['negative'] if word in text.lower())
        
        return positive_count > 0 and negative_count > 0
    
    def _basic_fallback_analysis(self, text: str) -> SentimentResult:
        """Most basic analysis as final fallback"""
        text_lower = text.lower()
        
        # Very basic sentiment
        if any(word in text_lower for word in ['love', 'great', 'amazing', 'perfect', 'awesome']):
            sentiment = 'positive'
        elif any(word in text_lower for word in ['hate', 'bad', 'terrible', 'awful', 'horrible']):
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return SentimentResult(
            overall_sentiment=sentiment,
            confidence_score=0.5,
            emotion_intensity=0.5,
            specific_emotions={'general': 0.5},
            food_specific_sentiment=sentiment,
            urgency_level='medium',
            sarcasm_detected=False,
            mixed_sentiment=False
        )

# Global sentiment analyzer
sentiment_analyzer = RobustSentimentAnalyzer()
