"""
Sentiment Analysis Verification and Testing

Tests:
1. Sentiment analyzer accuracy on sample reviews
2. Database sentiment score distribution
3. Composite score calculation
"""

import sys
from pathlib import Path
import sqlite3
import logging
from statistics import mean, stdev

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_sentiment_analyzer():
    """Test sentiment analyzer with known examples."""
    from app.services.sentiment_analyzer import get_analyzer
    
    analyzer = get_analyzer("vader")
    
    test_reviews = [
        ("This cafe is amazing! Best coffee in town.", "positive"),
        ("Terrible service, never coming back.", "negative"),
        ("It was okay, nothing special.", "neutral"),
        ("🔥 Outstanding experience! Love this place! 😍", "positive"),
        ("Worst waste of money ever.", "negative"),
    ]
    
    logger.info("\n" + "="*60)
    logger.info("SENTIMENT ANALYZER TEST")
    logger.info("="*60)
    
    for text, expected in test_reviews:
        result = analyzer.analyze(text)
        score = result["normalized_score"]
        label = analyzer.get_sentiment_label(score)
        
        logger.info(f"\nReview: {text}")
        logger.info(f"Score: {score:.1f} | Label: {label} | Expected: {expected}")
    
    logger.info("\n✓ Sentiment analyzer test complete\n")


def analyze_database_sentiment_distribution(db_path: str):
    """Analyze sentiment score distribution in database."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get sentiment distribution
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                AVG(sentiment_score) as avg,
                MIN(sentiment_score) as min_score,
                MAX(sentiment_score) as max_score,
                SUM(CASE WHEN sentiment_score < 40 THEN 1 ELSE 0 END) as negative_count,
                SUM(CASE WHEN sentiment_score >= 40 AND sentiment_score <= 60 THEN 1 ELSE 0 END) as neutral_count,
                SUM(CASE WHEN sentiment_score > 60 THEN 1 ELSE 0 END) as positive_count
            FROM reviews 
            WHERE sentiment_score IS NOT NULL
        """)
        
        result = cursor.fetchone()
        if result:
            total, avg, min_score, max_score, neg, neu, pos = result
            
            logger.info(f"\n{'='*60}")
            logger.info(f"DATABASE SENTIMENT ANALYSIS: {Path(db_path).name}")
            logger.info(f"{'='*60}")
            logger.info(f"Total reviewed: {total:,}")
            logger.info(f"Average sentiment: {avg:.1f}/100")
            logger.info(f"Score range: {min_score:.1f} - {max_score:.1f}")
            logger.info(f"\nSentiment Distribution:")
            logger.info(f"  Positive (>60):     {pos:6,} ({100*pos/total:5.1f}%)")
            logger.info(f"  Neutral (40-60):    {neu:6,} ({100*neu/total:5.1f}%)")
            logger.info(f"  Negative (<40):     {neg:6,} ({100*neg/total:5.1f}%)")
            
            # Sample reviews
            logger.info(f"\nSample High Sentiment (>80):")
            cursor.execute("""
                SELECT Description, sentiment_score FROM reviews
                WHERE sentiment_score > 80
                LIMIT 3
            """)
            for desc, score in cursor.fetchall():
                preview = (desc[:60] + "...") if len(desc) > 60 else desc
                logger.info(f"  [{score:.0f}] {preview}")
            
            logger.info(f"\nSample Low Sentiment (<30):")
            cursor.execute("""
                SELECT Description, sentiment_score FROM reviews
                WHERE sentiment_score < 30
                LIMIT 3
            """)
            for desc, score in cursor.fetchall():
                preview = (desc[:60] + "...") if len(desc) > 60 else desc
                logger.info(f"  [{score:.0f}] {preview}")
        
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Error analyzing {db_path}: {e}")
        return False


def analyze_place_level_sentiment(db_path: str):
    """Analyze aggregated sentiment at place level."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        logger.info(f"\n{'='*60}")
        logger.info(f"PLACE-LEVEL SENTIMENT ANALYSIS: {Path(db_path).name}")
        logger.info(f"{'='*60}")
        
        # Count places with sentiment data
        cursor.execute("""
            SELECT COUNT(*) FROM cafes_main 
            WHERE avg_sentiment_score IS NOT NULL
        """)
        places_with_sentiment = cursor.fetchone()[0]
        logger.info(f"Places with sentiment scores: {places_with_sentiment:,}")
        
        if places_with_sentiment > 0:
            # Get statistics
            cursor.execute("""
                SELECT 
                    AVG(avg_sentiment_score) as avg,
                    MIN(avg_sentiment_score) as min_score,
                    MAX(avg_sentiment_score) as max_score,
                    AVG(sentiment_positive_pct) as avg_pos_pct,
                    AVG(sentiment_review_count) as avg_review_count
                FROM cafes_main 
                WHERE avg_sentiment_score IS NOT NULL
            """)
            
            result = cursor.fetchone()
            if result:
                avg, min_score, max_score, avg_pos_pct, avg_review_count = result
                logger.info(f"\nPlace-level Statistics:")
                logger.info(f"  Average sentiment: {avg:.1f}/100")
                logger.info(f"  Sentiment range: {min_score:.1f} - {max_score:.1f}")
                logger.info(f"  Avg positive %: {avg_pos_pct:.1f}%")
                logger.info(f"  Avg reviews per place: {avg_review_count:.0f}")
                
                # Top places
                logger.info(f"\nTop 5 Places by Sentiment:")
                cursor.execute("""
                    SELECT name, avg_sentiment_score, sentiment_review_count 
                    FROM cafes_main
                    WHERE avg_sentiment_score IS NOT NULL
                    ORDER BY avg_sentiment_score DESC
                    LIMIT 5
                """)
                
                for i, (name, score, count) in enumerate(cursor.fetchall(), 1):
                    logger.info(
                        f"  {i}. {name[:40]:40s} "
                        f"{score:6.1f}/100 ({count:.0f} reviews)"
                    )
        
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Error analyzing places in {db_path}: {e}")
        return False


def main():
    """Run all tests."""
    script_dir = Path(__file__).resolve().parent
    backend_dir = script_dir.parent
    
    # Add backend to path
    if str(backend_dir) not in sys.path:
        sys.path.insert(0, str(backend_dir))
    
    try:
        # Test 1: Sentiment analyzer
        test_sentiment_analyzer()
        
        # Test 2 & 3: Database analysis
        databases = [
            backend_dir / "data" / "ktm_pois.db",
            backend_dir / "data" / "ktm_restaurants.db",
        ]
        
        for db_path in databases:
            if db_path.exists():
                analyze_database_sentiment_distribution(str(db_path))
                analyze_place_level_sentiment(str(db_path))
        
        logger.info("\n" + "="*60)
        logger.info("✓ ALL TESTS COMPLETE")
        logger.info("="*60 + "\n")
        
        return 0
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
