# SiteX Composite Score Methodology

The **Composite Score** is a comprehensive metric ranging from 0 to 100 that evaluates a place's overall quality and suitability by mathematically combining up to five distinct data signals. 

To ensure every place in the database receives a score—even if it lacks textual reviews for sentiment analysis—the system dynamically adjusts its weighting strategy based on data availability.

---

## 1. The Two Scoring Models

The algorithm first checks if a place has **Sentiment Data** (meaning it has at least one review with textual description that could be processed by VADER sentiment analysis). Based on this, it routes to one of two weighting models:

### Model A: With Sentiment Data (5 Signals)
For places that have textual reviews, the score relies heavily on the sentiment of those reviews.

| Signal | Weight | Source |
|---|---|---|
| **Sentiment** | **35%** | NLP analysis of review text |
| **Rating** | **25%** | Average star rating |
| **Volume** | **20%** | Total number of reviews |
| **Foot Traffic** | **12%** | Google Popular Times |
| **Open Hours** | **8%** | Total weekly operating hours |

### Model B: Without Sentiment Data (4 Signals)
For places missing textual reviews (e.g., they only have star ratings but no text), the algorithm redistributes the weight to the remaining signals, placing higher emphasis on the raw star rating and volume.

| Signal | Weight | Source |
|---|---|---|
| **Rating** | **40%** | Average star rating |
| **Volume** | **30%** | Total number of reviews |
| **Foot Traffic** | **20%** | Google Popular Times |
| **Open Hours** | **10%** | Total weekly operating hours |

---

## 2. Component Calculations

Every signal is normalized to a strict **0 to 100** scale before weights are applied.

### 2.1 Sentiment Score (0 - 100)
- **Base:** The raw average VADER sentiment score of all text reviews.
- **Bonus:** Up to +10 bonus points are awarded based on the percentage of positive reviews. For example, if 80% of a place's reviews are categorized as "Positive", it receives a +8 point bonus.
- **Cap:** The final score is strictly capped at 100.
- *Default if missing:* N/A (Triggers Model B).

### 2.2 Rating Score (0 - 100)
- **Calculation:** `(Average Star Rating / 5.0) * 100`
- Example: A 4.5 star rating becomes a 90.
- *Default if missing:* 50.0

### 2.3 Volume Score (0 - 100)
Review volume follows a **logarithmic curve** because the difference between 5 and 50 reviews is statistically much more significant than the difference between 500 and 550 reviews.
- **≥ 100 reviews:** 100 score
- **5 to 99 reviews:** Logarithmic scale between 50 and 100 points.
- **1 to 4 reviews:** 25 flat score (low statistical confidence).
- **0 reviews:** 0 score.

### 2.4 Foot Traffic Score (0 - 100)
- **Calculation:** Uses the `popularity` metric directly from the Google Popular Times dataset, averaged across all hours the place is open.
- *Default if missing:* 50.0 (Neutral).

### 2.5 Open Hours Score (0 - 100)
- **Calculation:** Evaluates the total number of hours a business is open per week against a benchmark of 98 hours (equivalent to 14 hours a day, 7 days a week).
- `(Total Weekly Hours / 98) * 100`
- **Cap:** Capped at 100 (places open 24/7 don't receive extra bonus past the benchmark).
- *Default if missing:* 50.0 (Neutral).

---

## 3. The Final Composite

The normalized components are multiplied by their respective weights (from Model A or Model B) and summed up to create the final `composite_score`.

Finally, the score is mapped to a human-readable `composite_label`:

| Score Range | Label |
|-------------|-------|
| 80 – 100 | **Excellent** |
| 70 – 79.9 | **Good** |
| 60 – 69.9 | **Moderate** |
| 50 – 59.9 | **Fair** |
| 0 – 49.9 | **Poor** |

---

## 4. Database Schema Impact

When exported to `ktm_all.db`, the algorithm populates the following columns in the `place` table:
- `composite_score` (REAL)
- `composite_label` (TEXT)
- `has_sentiment` (INTEGER: 1 or 0)
- `rating_score_component` (REAL)
- `volume_score_component` (REAL)
- `foot_traffic_score_component` (REAL)
- `open_hours_score_component` (REAL)
- `sentiment_score_component` (REAL or NULL)
