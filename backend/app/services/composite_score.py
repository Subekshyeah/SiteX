"""
Sentiment Analysis Integration - Composite Score Module

Computes composite suitability scores incorporating:
1. Review sentiment (user_reviews text → sentiment_score)
2. Review volume (review_count → volume signal)  
3. Star distribution (review_rating → quality signal)
4. Popularity patterns (popular_times → foot traffic proxy)

Reference: Phase 1 diagram in project documentation
"""

from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class CompositeScoreCalculator:
    """
    Computes composite suitability scores by combining multiple signals.
    
    Weights (configurable):
    - Sentiment Score: 30% (user satisfaction from review text analysis)
    - Rating Distribution: 25% (star rating aggregation)
    - Review Volume: 20% (popularity signal)
    - Popular Times: 15% (foot traffic proxy)
    - Other POI factors: 10% (location features)
    """
    
    # Default weights for composite score
    DEFAULT_WEIGHTS = {
        "sentiment": 0.30,       # Review sentiment from text analysis
        "rating": 0.25,          # Star distribution
        "volume": 0.20,          # Review count (popularity signal)
        "foot_traffic": 0.15,    # Popular times pattern
        "poi_context": 0.10,     # POI proximity, centrality, etc.
    }
    
    def __init__(self, weights: Optional[Dict[str, float]] = None):
        """
        Initialize composite score calculator.
        
        Args:
            weights: Optional custom weights. Must sum to 1.0.
                    If not provided, uses DEFAULT_WEIGHTS.
        """
        self.weights = weights or self.DEFAULT_WEIGHTS.copy()
        
        # Verify weights sum to ~1.0
        weight_sum = sum(self.weights.values())
        if abs(weight_sum - 1.0) > 0.01:
            logger.warning(
                f"Weights sum to {weight_sum}, not 1.0. "
                f"Scores will be scaled accordingly."
            )
    
    def normalize_score(
        self, 
        value: Optional[float], 
        min_val: float = 0.0,
        max_val: float = 100.0
    ) -> float:
        """
        Normalize a score to 0-100 range.
        
        Args:
            value: Score to normalize
            min_val: Minimum expected value
            max_val: Maximum expected value
            
        Returns:
            Normalized score (0-100), or 50 if value is None
        """
        if value is None:
            return 50.0  # Neutral score
        
        if max_val == min_val:
            return 50.0
        
        normalized = ((value - min_val) / (max_val - min_val)) * 100
        return max(0.0, min(100.0, normalized))
    
    def calculate_rating_score(
        self,
        avg_rating: Optional[float],
        positive_pct: Optional[float],
        neutral_pct: Optional[float],
        negative_pct: Optional[float]
    ) -> float:
        """
        Calculate rating quality score from star distribution.
        
        Args:
            avg_rating: Average star rating (0-5)
            positive_pct: % of 4-5 star reviews
            neutral_pct: % of 3 star reviews
            negative_pct: % of 1-2 star reviews
            
        Returns:
            Normalized rating score (0-100)
        """
        if avg_rating is None:
            return 50.0
        
        # Primary: average rating (0-5 → 0-100)
        base_score = (avg_rating / 5.0) * 100
        
        # Adjust for distribution if available
        if positive_pct is not None:
            # Prefer concentrated positive reviews
            distribution_score = positive_pct * 1.0 - negative_pct * 0.5 if negative_pct else positive_pct
            base_score = base_score * 0.7 + (distribution_score) * 0.3
        
        return max(0.0, min(100.0, base_score))
    
    def calculate_volume_score(
        self,
        review_count: Optional[int],
        min_threshold: int = 5,
        max_threshold: int = 100
    ) -> float:
        """
        Calculate popularity score from review volume.
        
        More reviews = more established, popular place.
        Uses logarithmic scaling to avoid outliers dominating.
        
        Args:
            review_count: Number of reviews
            min_threshold: Reviews below this → score 0
            max_threshold: Reviews above this → score 100
            
        Returns:
            Normalized volume score (0-100)
        """
        if review_count is None or review_count < min_threshold:
            return 20.0  # Low score for little data
        
        import math
        
        # Logarithmic scaling
        log_min = math.log(min_threshold)
        log_max = math.log(max_threshold)
        log_count = math.log(min(review_count, max_threshold))
        
        normalized = ((log_count - log_min) / (log_max - log_min)) * 100
        return max(0.0, min(100.0, normalized))
    
    def calculate_sentiment_score(
        self,
        avg_sentiment: Optional[float],
        positive_pct: Optional[float]
    ) -> float:
        """
        Calculate sentiment score from review text analysis.
        
        Args:
            avg_sentiment: Average sentiment (0-100 scale)
            positive_pct: % of reviews with positive sentiment
            
        Returns:
            Normalized sentiment score (0-100)
        """
        if avg_sentiment is None:
            return 50.0
        
        # Primary: average sentiment
        base_score = avg_sentiment  # Already 0-100
        
        # Adjust for consensus
        if positive_pct is not None:
            # Prefer strong consensus
            consensus_bonus = (positive_pct - 50) * 0.5 if positive_pct > 50 else 0
            base_score = min(100.0, base_score + consensus_bonus * 0.2)
        
        return max(0.0, min(100.0, base_score))
    
    def calculate_composite_score(
        self,
        sentiment_score: float,
        rating_score: float,
        volume_score: float,
        foot_traffic_score: Optional[float] = None,
        poi_context_score: Optional[float] = None
    ) -> Tuple[float, Dict]:
        """
        Calculate final composite suitability score.
        
        Combines all signals with configured weights.
        
        Args:
            sentiment_score: User review sentiment (0-100)
            rating_score: Star rating quality (0-100)
            volume_score: Review popularity (0-100)
            foot_traffic_score: Popular times score (0-100), optional
            poi_context_score: POI context score (0-100), optional
            
        Returns:
            Tuple of (composite_score, components_dict)
            composite_score: Final suitability score (0-100)
            components_dict: Breakdown of each component
        """
        components = {
            "sentiment": sentiment_score * self.weights["sentiment"],
            "rating": rating_score * self.weights["rating"],
            "volume": volume_score * self.weights["volume"],
        }
        
        # Optional components
        if foot_traffic_score is not None:
            components["foot_traffic"] = (
                foot_traffic_score * self.weights["foot_traffic"]
            )
        else:
            # Distribute weight if not provided
            other_weights = self.weights["sentiment"] + self.weights["rating"]
            components["sentiment"] += foot_traffic_score * 0.075 if foot_traffic_score else 0
        
        if poi_context_score is not None:
            components["poi_context"] = (
                poi_context_score * self.weights["poi_context"]
            )
        
        composite = sum(components.values())
        
        return max(0.0, min(100.0, composite)), components
    
    def get_suitability_label(self, score: float) -> str:
        """Get human-readable suitability label."""
        if score < 20:
            return "Poor"
        elif score < 40:
            return "Fair"
        elif score < 60:
            return "Moderate"
        elif score < 80:
            return "Good"
        else:
            return "Excellent"


def compute_place_composite_score(
    place_data: Dict,
    weights: Optional[Dict[str, float]] = None
) -> Tuple[float, Dict, str]:
    """
    Convenience function to compute composite score for a place.
    
    Expected place_data keys:
    - avg_sentiment_score: 0-100
    - sentiment_positive_pct: 0-100
    - rating (avg): 0-5
    - reviews_count: integer
    - [optional] popular_times_score: 0-100
    
    Returns:
        (score, components, label)
    """
    calculator = CompositeScoreCalculator(weights)
    
    # Extract and normalize components
    sentiment_score = calculator.calculate_sentiment_score(
        place_data.get("avg_sentiment_score"),
        place_data.get("sentiment_positive_pct")
    )
    
    rating_score = calculator.calculate_rating_score(
        place_data.get("rating"),
        place_data.get("positive_pct"),
        place_data.get("neutral_pct"),
        place_data.get("negative_pct")
    )
    
    volume_score = calculator.calculate_volume_score(
        place_data.get("reviews_count")
    )
    
    foot_traffic_score = place_data.get("popular_times_score")
    poi_context_score = place_data.get("poi_context_score")
    
    # Compute composite
    composite, components = calculator.calculate_composite_score(
        sentiment_score=sentiment_score,
        rating_score=rating_score,
        volume_score=volume_score,
        foot_traffic_score=foot_traffic_score,
        poi_context_score=poi_context_score
    )
    
    label = calculator.get_suitability_label(composite)
    
    return composite, components, label


# Example usage
if __name__ == "__main__":
    # Mock place data
    mock_place = {
        "avg_sentiment_score": 72.5,
        "sentiment_positive_pct": 68.0,
        "rating": 4.2,
        "reviews_count": 87,
        "popular_times_score": 65.0,
    }
    
    score, components, label = compute_place_composite_score(mock_place)
    
    print(f"Composite Score: {score:.1f}")
    print(f"Suitability: {label}")
    print(f"\nComponent Breakdown:")
    for key, value in components.items():
        print(f"  {key:20s}: {value:6.2f}")
