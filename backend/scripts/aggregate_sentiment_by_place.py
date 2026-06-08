"""
Aggregated Sentiment Analysis by Place

Aggregates individual review sentiment scores to compute:
- Average sentiment score per place
- Sentiment distribution (% positive, neutral, negative)
- Review volume weighted sentiment
"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PlaceSentimentAggregator:
    """Aggregates sentiment scores by place."""
    
    def __init__(self):
        self.places_updated = 0
        self.places_with_reviews = 0
    
    def aggregate_sentiment_by_place(self, db_path: str) -> Dict:
        """
        Aggregate sentiment scores by place_id.
        
        Computes for each place:
        - avg_sentiment_score: Average of all review sentiment scores
        - sentiment_positive_pct: % of reviews with score > 60
        - sentiment_neutral_pct: % of reviews with 40 <= score <= 60
        - sentiment_negative_pct: % of reviews with score < 40
        - sentiment_review_count: Number of reviews analyzed
        - sentiment_last_updated: When aggregation was done
        
        Args:
            db_path: Path to SQLite database
            
        Returns:
            Dictionary with aggregation statistics
        """
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            logger.info(f"\nAggregating sentiment scores from {Path(db_path).name}")
            
            # First, ensure the columns exist in cafes_main
            cursor.execute("PRAGMA table_info(cafes_main)")
            columns = {row[1] for row in cursor.fetchall()}
            
            new_columns = []
            if "avg_sentiment_score" not in columns:
                cursor.execute('ALTER TABLE cafes_main ADD COLUMN avg_sentiment_score REAL DEFAULT NULL')
                new_columns.append("avg_sentiment_score")
            
            if "sentiment_positive_pct" not in columns:
                cursor.execute('ALTER TABLE cafes_main ADD COLUMN sentiment_positive_pct REAL DEFAULT NULL')
                new_columns.append("sentiment_positive_pct")
            
            if "sentiment_neutral_pct" not in columns:
                cursor.execute('ALTER TABLE cafes_main ADD COLUMN sentiment_neutral_pct REAL DEFAULT NULL')
                new_columns.append("sentiment_neutral_pct")
            
            if "sentiment_negative_pct" not in columns:
                cursor.execute('ALTER TABLE cafes_main ADD COLUMN sentiment_negative_pct REAL DEFAULT NULL')
                new_columns.append("sentiment_negative_pct")
            
            if "sentiment_review_count" not in columns:
                cursor.execute('ALTER TABLE cafes_main ADD COLUMN sentiment_review_count INTEGER DEFAULT NULL')
                new_columns.append("sentiment_review_count")
            
            if "sentiment_last_updated" not in columns:
                cursor.execute('ALTER TABLE cafes_main ADD COLUMN sentiment_last_updated TIMESTAMP DEFAULT NULL')
                new_columns.append("sentiment_last_updated")
            
            if new_columns:
                conn.commit()
                logger.info(f"Added columns: {', '.join(new_columns)}")
            
            # Get all unique places that have reviews with sentiment scores
            cursor.execute("""
                SELECT DISTINCT place_id 
                FROM reviews 
                WHERE sentiment_score IS NOT NULL 
                  AND sentiment_score != ''
                ORDER BY place_id
            """)
            
            places = [row[0] for row in cursor.fetchall()]
            self.places_with_reviews = len(places)
            
            logger.info(f"Found {self.places_with_reviews} places with analyzed reviews")
            
            # Aggregate sentiment for each place
            updated_count = 0
            for i, place_id in enumerate(places, 1):
                try:
                    # Calculate aggregates
                    cursor.execute("""
                        SELECT 
                            AVG(sentiment_score) as avg_score,
                            SUM(CASE WHEN sentiment_score > 60 THEN 1 ELSE 0 END) as positive_count,
                            SUM(CASE WHEN sentiment_score >= 40 AND sentiment_score <= 60 THEN 1 ELSE 0 END) as neutral_count,
                            SUM(CASE WHEN sentiment_score < 40 THEN 1 ELSE 0 END) as negative_count,
                            COUNT(*) as total_count
                        FROM reviews
                        WHERE place_id = ? AND sentiment_score IS NOT NULL
                    """, (place_id,))
                    
                    result = cursor.fetchone()
                    if result:
                        avg_score, pos_count, neu_count, neg_count, total = result
                        
                        # Calculate percentages
                        pos_pct = (pos_count / total * 100) if total > 0 else 0
                        neu_pct = (neu_count / total * 100) if total > 0 else 0
                        neg_pct = (neg_count / total * 100) if total > 0 else 0
                        
                        # Update cafes_main table
                        cursor.execute("""
                            UPDATE cafes_main
                            SET avg_sentiment_score = ?,
                                sentiment_positive_pct = ?,
                                sentiment_neutral_pct = ?,
                                sentiment_negative_pct = ?,
                                sentiment_review_count = ?,
                                sentiment_last_updated = ?
                            WHERE place_id = ?
                        """, (
                            avg_score,
                            pos_pct,
                            neu_pct,
                            neg_pct,
                            total,
                            datetime.now().isoformat(),
                            place_id
                        ))
                        
                        updated_count += 1
                        
                        # Progress logging
                        if (i % 100 == 0) or (i == len(places)):
                            logger.info(
                                f"Progress: {i}/{len(places)} "
                                f"({100*i/len(places):.1f}%) - "
                                f"Updated: {updated_count}"
                            )
                
                except Exception as e:
                    logger.error(f"Error aggregating sentiment for place {place_id}: {e}")
            
            conn.commit()
            conn.close()
            
            self.places_updated = updated_count
            logger.info(f"✓ Aggregation complete: {updated_count} places updated")
            
            return {
                "places_with_reviews": self.places_with_reviews,
                "places_updated": self.places_updated
            }
            
        except Exception as e:
            logger.error(f"Error aggregating sentiment for {db_path}: {e}")
            raise


def main():
    """Main entry point."""
    try:
        aggregator = PlaceSentimentAggregator()
        
        script_dir = Path(__file__).resolve().parent
        backend_dir = script_dir.parent
        databases = [
            backend_dir / "data" / "ktm_pois.db",
            backend_dir / "data" / "ktm_restaurants.db",
        ]
        
        total_stats = {
            "places_with_reviews": 0,
            "places_updated": 0
        }
        
        for db_path in databases:
            if db_path.exists():
                logger.info(f"\n{'='*60}")
                logger.info(f"Aggregating: {db_path.name}")
                logger.info(f"{'='*60}")
                
                stats = aggregator.aggregate_sentiment_by_place(str(db_path))
                
                for key in total_stats:
                    total_stats[key] += stats.get(key, 0)
            else:
                logger.warning(f"Database not found: {db_path}")
        
        logger.info(f"\n{'='*60}")
        logger.info("SUMMARY")
        logger.info(f"{'='*60}")
        logger.info(f"Total places with reviewed: {total_stats['places_with_reviews']}")
        logger.info(f"Total places updated: {total_stats['places_updated']}")
        logger.info("✓ Aggregation complete!")
        
        return 0
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
