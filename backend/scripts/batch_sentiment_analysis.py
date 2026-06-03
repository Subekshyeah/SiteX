"""
Batch Sentiment Analysis Script

Processes all reviews in POIs and Restaurants databases:
1. Fetches reviews with null sentiment scores
2. Analyzes sentiment for each review using VADER
3. Stores results back to database
4. Provides progress tracking and summary statistics
"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Dict
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_backend_path():
    """Add backend to path so we can import our modules."""
    script_dir = Path(__file__).resolve().parent
    backend_dir = script_dir.parent
    if str(backend_dir) not in sys.path:
        sys.path.insert(0, str(backend_dir))


def import_sentiment_analyzer():
    """Dynamically import sentiment analyzer."""
    setup_backend_path()
    try:
        from app.services.sentiment_analyzer import get_analyzer
        return get_analyzer("vader")
    except ImportError as e:
        logger.error(f"Failed to import sentiment analyzer: {e}")
        raise


class ReviewSentimentProcessor:
    """Processes reviews and computes sentiment scores."""
    
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.processed_count = 0
        self.skipped_count = 0
        self.error_count = 0
    
    def process_reviews_batch(
        self,
        db_path: str,
        batch_size: int = 100,
        limit: int = None
    ) -> Dict[str, int]:
        """
        Process reviews in a database in batches.
        
        Args:
            db_path: Path to SQLite database
            batch_size: Number of reviews to process before committing
            limit: Maximum number of reviews to process (None = all)
            
        Returns:
            Dictionary with processing statistics
        """
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Fetch total count
            cursor.execute(
                "SELECT COUNT(*) FROM reviews WHERE Description IS NOT NULL AND Description != ''"
            )
            total = cursor.fetchone()[0]
            
            if limit:
                total = min(total, limit)
            
            logger.info(f"\nProcessing {total} reviews from {Path(db_path).name}")
            
            # Fetch reviews that haven't been analyzed yet (use rowid for unique identification)
            query = """
                SELECT rowid, Description, place_id, Rating 
                FROM reviews 
                WHERE Description IS NOT NULL 
                  AND Description != ''
                  AND (sentiment_score IS NULL OR sentiment_score = '')
                ORDER BY rowid ASC
            """
            
            if limit:
                query += f" LIMIT {limit}"
            
            cursor.execute(query)
            reviews = cursor.fetchall()
            
            if not reviews:
                logger.info("No reviews to process.")
                conn.close()
                return {
                    "total": 0,
                    "processed": 0,
                    "skipped": 0,
                    "errors": 0
                }
            
            # Process in batches
            batch = []
            for i, review in enumerate(reviews, 1):
                rowid = review[0]
                description = review[1]
                place_id = review[2]
                rating = review[3]
                
                try:
                    # Analyze sentiment
                    sentiment = self.analyzer.analyze(description)
                    score = sentiment.get("normalized_score", 50.0)
                    label = self.analyzer.get_sentiment_label(score)
                    
                    batch.append({
                        "rowid": rowid,
                        "score": score,
                        "label": label,
                        "place_id": place_id,
                        "rating": rating,
                        "timestamp": datetime.now().isoformat(),
                        "method": "vader"
                    })
                    
                    self.processed_count += 1
                    
                except Exception as e:
                    logger.error(f"Error analyzing review at rowid {rowid}: {e}")
                    self.error_count += 1
                
                # Commit batch
                if len(batch) >= batch_size or i == len(reviews):
                    self._save_batch(conn, batch)
                    batch = []
                    
                    # Progress logging
                    if i % (batch_size * 10) == 0 or i == len(reviews):
                        logger.info(
                            f"Progress: {i}/{len(reviews)} "
                            f"({100*i/len(reviews):.1f}%) - "
                            f"Processed: {self.processed_count}, "
                            f"Errors: {self.error_count}"
                        )
            
            conn.close()
            
            logger.info(f"\n✓ Completed processing from {Path(db_path).name}")
            
        except Exception as e:
            logger.error(f"Error processing database {db_path}: {e}")
            raise
        
        return {
            "total": len(reviews),
            "processed": self.processed_count,
            "skipped": self.skipped_count,
            "errors": self.error_count
        }
    
    def _save_batch(self, conn: sqlite3.Connection, batch: List[Dict]):
        """Save a batch of sentiment scores to database using rowid."""
        if not batch:
            return
        
        cursor = conn.cursor()
        
        try:
            for item in batch:
                cursor.execute("""
                    UPDATE reviews 
                    SET sentiment_score = ?,
                        sentiment_label = ?,
                        sentiment_method = ?,
                        analyzed_at = ?
                    WHERE rowid = ?
                """, (
                    item["score"],
                    item["label"],
                    item["method"],
                    item["timestamp"],
                    item["rowid"]
                ))
            
            conn.commit()
            
        except Exception as e:
            logger.error(f"Error saving batch: {e}")
            conn.rollback()


def main():
    """Main entry point."""
    try:
        # Import sentiment analyzer
        analyzer = import_sentiment_analyzer()
        logger.info("✓ Sentiment analyzer initialized (VADER)")
        
        # Initialize processor
        processor = ReviewSentimentProcessor(analyzer)
        
        # Define databases to process
        script_dir = Path(__file__).resolve().parent
        backend_dir = script_dir.parent
        databases = [
            backend_dir / "data" / "ktm_pois.db",
            backend_dir / "data" / "ktm_restaurants.db",
        ]
        
        total_stats = {
            "total": 0,
            "processed": 0,
            "errors": 0
        }
        
        # Process each database
        for db_path in databases:
            if db_path.exists():
                logger.info(f"\n{'='*60}")
                logger.info(f"Processing: {db_path.name}")
                logger.info(f"{'='*60}")
                
                stats = processor.process_reviews_batch(str(db_path), batch_size=100)
                
                for key in total_stats:
                    total_stats[key] += stats.get(key, 0)
            else:
                logger.warning(f"Database not found: {db_path}")
        
        # Summary
        logger.info(f"\n{'='*60}")
        logger.info("SUMMARY")
        logger.info(f"{'='*60}")
        logger.info(f"Total reviews processed: {total_stats['processed']}")
        logger.info(f"Total errors: {total_stats['errors']}")
        logger.info("✓ Batch sentiment analysis complete!")
        
        return 0
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
