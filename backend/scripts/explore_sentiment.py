#!/usr/bin/env python3
"""
Explore sentiment analysis results from the database.
Run: python scripts/explore_sentiment.py
"""

import sqlite3
from pathlib import Path
import json

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "ktm_pois.db"

def get_db_connection():
    """Create database connection."""
    return sqlite3.connect(str(DB_PATH))

def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def show_stats():
    """Show overall sentiment statistics."""
    print_section("OVERALL SENTIMENT STATISTICS")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Count stats
    cursor.execute("""
        SELECT 
            COUNT(*) as total_reviews,
            COUNT(CASE WHEN sentiment_score IS NOT NULL THEN 1 END) as analyzed,
            ROUND(AVG(sentiment_score), 1) as avg_sentiment
        FROM reviews
    """)
    total, analyzed, avg = cursor.fetchone()
    
    print(f"Total Reviews:        {total:,}")
    print(f"Analyzed Reviews:     {analyzed:,}")
    print(f"Average Sentiment:    {avg}/100")
    
    # Sentiment distribution
    print(f"\nSentiment Distribution:")
    cursor.execute("""
        SELECT 
            sentiment_label, 
            COUNT(*) as count,
            ROUND(100.0*COUNT(*)/(SELECT COUNT(*) FROM reviews WHERE sentiment_score IS NOT NULL),1) as pct
        FROM reviews 
        WHERE sentiment_score IS NOT NULL
        GROUP BY sentiment_label
        ORDER BY CASE 
            WHEN sentiment_label='Very Positive' THEN 1
            WHEN sentiment_label='Positive' THEN 2
            WHEN sentiment_label='Neutral' THEN 3
            WHEN sentiment_label='Negative' THEN 4
            ELSE 5 END
    """)
    
    for label, count, pct in cursor.fetchall():
        bar = "█" * int(pct / 2)
        print(f"  {label:15} {count:6,} ({pct:5.1f}%) {bar}")
    
    conn.close()

def show_top_cafes(limit=10):
    """Show top-rated cafes by sentiment (min 5 reviews)."""
    print_section(f"TOP {limit} CAFES BY SENTIMENT (min 5 reviews)")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            title,
            ROUND(avg_sentiment_score, 1) as sentiment,
            ROUND(sentiment_positive_pct, 0) as positive_pct,
            sentiment_review_count as reviews
        FROM cafes_main
        WHERE avg_sentiment_score IS NOT NULL 
            AND sentiment_review_count >= 5
        ORDER BY avg_sentiment_score DESC
        LIMIT ?
    """, (limit,))
    
    print(f"{'Cafe Name':<50} {'Sentiment':<10} {'Positive':<10} {'Reviews':<8}")
    print("-" * 78)
    
    for title, sentiment, pos_pct, reviews in cursor.fetchall():
        title_short = (title[:45] + "...") if len(title) > 48 else title
        print(f"{title_short:<50} {sentiment:>8.1f}  {pos_pct:>8.0f}%  {reviews:>7}")
    
    conn.close()

def show_worst_cafes(limit=10):
    """Show lowest-rated cafes by sentiment (min 5 reviews)."""
    print_section(f"LOWEST {limit} CAFES BY SENTIMENT (min 5 reviews)")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            title,
            ROUND(avg_sentiment_score, 1) as sentiment,
            ROUND(sentiment_positive_pct, 0) as positive_pct,
            sentiment_review_count as reviews
        FROM cafes_main
        WHERE avg_sentiment_score IS NOT NULL 
            AND sentiment_review_count >= 5
        ORDER BY avg_sentiment_score ASC
        LIMIT ?
    """, (limit,))
    
    print(f"{'Cafe Name':<50} {'Sentiment':<10} {'Positive':<10} {'Reviews':<8}")
    print("-" * 78)
    
    for title, sentiment, pos_pct, reviews in cursor.fetchall():
        title_short = (title[:45] + "...") if len(title) > 48 else title
        print(f"{title_short:<50} {sentiment:>8.1f}  {pos_pct:>8.0f}%  {reviews:>7}")
    
    conn.close()

def show_sample_reviews(sentiment_label=None, limit=15):
    """Show sample reviews with their sentiment scores."""
    if sentiment_label:
        print_section(f"SAMPLE {sentiment_label.upper()} REVIEWS")
    else:
        print_section(f"SAMPLE REVIEWS (RANDOM)")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if sentiment_label:
        cursor.execute("""
            SELECT 
                SUBSTR(Description, 1, 70) as review,
                ROUND(sentiment_score, 1) as sentiment,
                sentiment_label
            FROM reviews
            WHERE sentiment_score IS NOT NULL 
                AND sentiment_label = ?
                AND LENGTH(Description) > 20
            LIMIT ?
        """, (sentiment_label, limit))
    else:
        cursor.execute("""
            SELECT 
                SUBSTR(Description, 1, 70) as review,
                ROUND(sentiment_score, 1) as sentiment,
                sentiment_label
            FROM reviews
            WHERE sentiment_score IS NOT NULL 
                AND LENGTH(Description) > 20
            ORDER BY RANDOM()
            LIMIT ?
        """, (limit,))
    
    for i, (review, sentiment, label) in enumerate(cursor.fetchall(), 1):
        print(f"{i:2}. [{sentiment:>6.1f}] {label:15} | {review}")
    
    conn.close()

def show_cafe_details(cafe_name):
    """Show detailed sentiment breakdown for a specific cafe."""
    print_section(f"CAFE DETAILS: {cafe_name}")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get cafe info
    cursor.execute("""
        SELECT 
            title,
            ROUND(avg_sentiment_score, 1) as avg_sentiment,
            ROUND(sentiment_positive_pct, 1) as positive_pct,
            ROUND(sentiment_neutral_pct, 1) as neutral_pct,
            ROUND(sentiment_negative_pct, 1) as negative_pct,
            sentiment_review_count as total_reviews
        FROM cafes_main
        WHERE title LIKE ?
    """, (f"%{cafe_name}%",))
    
    result = cursor.fetchone()
    if not result:
        print(f"❌ Cafe '{cafe_name}' not found")
        conn.close()
        return
    
    title, avg_sent, pos_pct, neu_pct, neg_pct, total_reviews = result
    
    print(f"Cafe:              {title}")
    print(f"Average Sentiment: {avg_sent}/100")
    print(f"Total Reviews:     {total_reviews}")
    print(f"\nSentiment Breakdown:")
    print(f"  Positive:        {pos_pct:>6.1f}%")
    print(f"  Neutral:         {neu_pct:>6.1f}%")
    print(f"  Negative:        {neg_pct:>6.1f}%")
    
    # Get sample reviews
    print(f"\nRecent Reviews:")
    cursor.execute("""
        SELECT 
            SUBSTR(Description, 1, 60) as review,
            ROUND(sentiment_score, 1) as sentiment,
            sentiment_label,
            Rating
        FROM reviews
        WHERE place_id IN (
            SELECT place_id FROM cafes_main WHERE title LIKE ?
        )
        AND sentiment_score IS NOT NULL
        ORDER BY rowid DESC
        LIMIT 5
    """, (f"%{cafe_name}%",))
    
    for i, (review, sentiment, label, rating) in enumerate(cursor.fetchall(), 1):
        print(f"  {i}. [{rating}⭐] {sentiment:>6.1f} ({label:12}) | {review}")
    
    conn.close()

def main():
    """Main exploration menu."""
    print("\n🎯 SiteX Sentiment Analysis Explorer\n")
    
    while True:
        print("\nOptions:")
        print("  1. Overall statistics")
        print("  2. Top 10 cafes by sentiment")
        print("  3. Lowest 10 cafes by sentiment")
        print("  4. View positive reviews")
        print("  5. View negative reviews")
        print("  6. View random reviews")
        print("  7. Search cafe details")
        print("  0. Exit")
        
        choice = input("\nEnter choice (0-7): ").strip()
        
        if choice == "0":
            print("\n👋 Goodbye!\n")
            break
        elif choice == "1":
            show_stats()
        elif choice == "2":
            show_top_cafes(10)
        elif choice == "3":
            show_worst_cafes(10)
        elif choice == "4":
            show_sample_reviews("Very Positive", 10)
        elif choice == "5":
            show_sample_reviews("Very Negative", 10)
        elif choice == "6":
            show_sample_reviews(None, 15)
        elif choice == "7":
            cafe = input("\nEnter cafe name (partial): ").strip()
            if cafe:
                show_cafe_details(cafe)
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    if not DB_PATH.exists():
        print(f"❌ Database not found: {DB_PATH}")
        exit(1)
    
    main()
