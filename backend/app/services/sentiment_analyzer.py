"""
Sentiment Analysis Service for Reviews

Provides functionality to analyze sentiment of review texts and compute
sentiment scores that will be integrated into the composite suitability score.

Supports multiple sentiment analysis methods:
1. VADER (Valence Aware Dictionary and sEntiment Reasoner) - from NLTK
   - Fast, optimized for social media reviews
   - Works well with short, informal text
   - Returns compound score: -1 (most negative) to +1 (most positive)

2. TextBlob - simpler, alternative approach
   - Uses pattern-based sentiment analysis
   - Polarity: -1 (negative) to +1 (positive)
   - Subjectivity: 0 (objective) to 1 (subjective)
"""

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from typing import Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Analyzes sentiment of review text."""
    
    def __init__(self, method: str = "vader"):
        """
        Initialize sentiment analyzer.
        
        Args:
            method: "vader" (default) or "textblob"
        """
        self.method = method.lower()
        
        if self.method == "vader":
            # Download vader lexicon if not already present
            try:
                nltk.data.find('sentiment/vader_lexicon')
            except LookupError:
                nltk.download('vader_lexicon')
            self.sia = SentimentIntensityAnalyzer()
        elif self.method != "textblob":
            raise ValueError(f"Unknown sentiment method: {method}")
    
    def analyze_vader(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment using VADER.
        
        Args:
            text: Review text to analyze
            
        Returns:
            Dictionary with keys:
            - compound: overall sentiment score (-1 to +1)
            - positive: positive sentiment intensity (0 to 1)
            - neutral: neutral sentiment intensity (0 to 1)
            - negative: negative sentiment intensity (0 to 1)
            - normalized_score: 0-100 scale suitable for composite score
        """
        if not text or not isinstance(text, str) or len(text.strip()) == 0:
            return {
                "compound": 0.0,
                "positive": 0.0,
                "neutral": 1.0,
                "negative": 0.0,
                "normalized_score": 50.0,
            }
        
        scores = self.sia.polarity_scores(text)
        
        # Convert compound score (-1 to +1) to normalized score (0 to 100)
        # -1 → 0, 0 → 50, +1 → 100
        normalized = ((scores["compound"] + 1) / 2) * 100
        
        return {
            "compound": scores["compound"],
            "positive": scores["pos"],
            "neutral": scores["neu"],
            "negative": scores["neg"],
            "normalized_score": normalized,
        }
    
    def analyze_textblob(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment using TextBlob.
        
        Args:
            text: Review text to analyze
            
        Returns:
            Dictionary with keys:
            - polarity: sentiment polarity (-1 to +1)
            - subjectivity: how subjective the text is (0 to 1)
            - normalized_score: 0-100 scale suitable for composite score
        """
        if not text or not isinstance(text, str) or len(text.strip()) == 0:
            return {
                "polarity": 0.0,
                "subjectivity": 0.5,
                "normalized_score": 50.0,
            }
        
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        # Convert polarity (-1 to +1) to normalized score (0 to 100)
        # -1 → 0, 0 → 50, +1 → 100
        normalized = ((polarity + 1) / 2) * 100
        
        return {
            "polarity": polarity,
            "subjectivity": blob.sentiment.subjectivity,
            "normalized_score": normalized,
        }
    
    def analyze(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of review text.
        
        Args:
            text: Review text to analyze
            
        Returns:
            Dictionary with sentiment scores and normalized_score (0-100)
        """
        if self.method == "vader":
            return self.analyze_vader(text)
        elif self.method == "textblob":
            return self.analyze_textblob(text)
        else:
            raise ValueError(f"Unknown sentiment method: {self.method}")
    
    def get_sentiment_label(self, normalized_score: float) -> str:
        """
        Get human-readable sentiment label.
        
        Args:
            normalized_score: Sentiment score on 0-100 scale
            
        Returns:
            Label: "Very Negative", "Negative", "Neutral", "Positive", "Very Positive"
        """
        if normalized_score < 20:
            return "Very Negative"
        elif normalized_score < 40:
            return "Negative"
        elif normalized_score < 60:
            return "Neutral"
        elif normalized_score < 80:
            return "Positive"
        else:
            return "Very Positive"


# Singleton instance for efficient reuse
_analyzer = None


def get_analyzer(method: str = "vader") -> SentimentAnalyzer:
    """Get or create singleton sentiment analyzer instance."""
    global _analyzer
    if _analyzer is None:
        _analyzer = SentimentAnalyzer(method=method)
    return _analyzer


def analyze_sentiment(text: str, method: str = "vader") -> Dict[str, float]:
    """
    Convenience function to analyze sentiment of a single review.
    
    Args:
        text: Review text
        method: Sentiment analysis method ("vader" or "textblob")
        
    Returns:
        Dictionary with sentiment scores and normalized_score
    """
    analyzer = get_analyzer(method)
    return analyzer.analyze(text)


def get_sentiment_scores_batch(texts: list, method: str = "vader") -> list:
    """
    Analyze sentiment for a batch of reviews.
    
    Args:
        texts: List of review texts
        method: Sentiment analysis method
        
    Returns:
        List of sentiment score dictionaries
    """
    analyzer = get_analyzer(method)
    return [analyzer.analyze(text) for text in texts]
