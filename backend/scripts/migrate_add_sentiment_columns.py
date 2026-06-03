"""
Database Migration: Add Sentiment Analysis Columns to Reviews Table

This script adds sentiment analysis columns to both POIs and Restaurants databases:
- sentiment_score: normalized 0-100 sentiment score
- sentiment_label: human-readable sentiment label
- sentiment_method: which method was used (vader, textblob)
- analyzed_at: timestamp when sentiment was analyzed
"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_sentiment_columns(db_path: str) -> bool:
    """
    Add sentiment analysis columns to reviews table.
    
    Args:
        db_path: Path to SQLite database
        
    Returns:
        True if successful, False otherwise
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if sentiment columns already exist
        cursor.execute("PRAGMA table_info(reviews)")
        columns = {row[1] for row in cursor.fetchall()}
        
        alterations = []
        
        if "sentiment_score" not in columns:
            cursor.execute(
                'ALTER TABLE reviews ADD COLUMN sentiment_score REAL DEFAULT NULL'
            )
            alterations.append("sentiment_score")
        
        if "sentiment_label" not in columns:
            cursor.execute(
                'ALTER TABLE reviews ADD COLUMN sentiment_label TEXT DEFAULT NULL'
            )
            alterations.append("sentiment_label")
        
        if "sentiment_method" not in columns:
            cursor.execute(
                'ALTER TABLE reviews ADD COLUMN sentiment_method TEXT DEFAULT NULL'
            )
            alterations.append("sentiment_method")
        
        if "analyzed_at" not in columns:
            cursor.execute(
                'ALTER TABLE reviews ADD COLUMN analyzed_at TIMESTAMP DEFAULT NULL'
            )
            alterations.append("analyzed_at")
        
        conn.commit()
        
        if alterations:
            logger.info(f"Added columns to {db_path}: {', '.join(alterations)}")
        else:
            logger.info(f"Sentiment columns already exist in {db_path}")
        
        # Verify columns were added
        cursor.execute("PRAGMA table_info(reviews)")
        columns = [row[1] for row in cursor.fetchall()]
        logger.info(f"Table reviews now has columns: {columns}")
        
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Error adding sentiment columns to {db_path}: {e}")
        return False


def main():
    """Run migrations on both POIs and Restaurants databases."""
    # Get backend directory correctly
    script_dir = Path(__file__).resolve().parent  # scripts directory
    backend_dir = script_dir.parent  # backend directory
    
    databases = [
        backend_dir / "data" / "ktm_pois.db",
        backend_dir / "data" / "ktm_restaurants.db",
    ]
    
    all_success = True
    for db_path in databases:
        if db_path.exists():
            logger.info(f"\nProcessing {db_path.name}...")
            if not add_sentiment_columns(str(db_path)):
                all_success = False
        else:
            logger.warning(f"Database not found: {db_path}")
    
    if all_success:
        logger.info("\n✓ All migrations completed successfully!")
        return 0
    else:
        logger.error("\n✗ Some migrations failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
