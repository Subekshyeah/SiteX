# app/services/data_preprocessor.py
import json
from typing import Dict, Any, List, Optional

def _extract_boolean_flag(info_list: Optional[List[Dict]], target_key: str) -> bool:
    """
    Safely checks a list of dictionaries (like 'Crowd' or 'Offerings')
    for a specific key and returns True if its value is true.
    """
    if not isinstance(info_list, list):
        return False
    for item in info_list:
        if isinstance(item, dict) and item.get(target_key):
            return True
    return False

def process_single_cafe(cafe: Dict[str, Any]) -> Dict[str, Any]:
    """
    Processes a single raw cafe JSON object and flattens it into a rich,
    comprehensive set of fields that precisely matches the required schema.
    """
    additional_info = cafe.get('additionalInfo') or {}

    # Safely get specific lists from additionalInfo
    service_options = additional_info.get('Service options')
    offerings = additional_info.get('Offerings')
    dining_options = additional_info.get('Dining options')
    amenities = additional_info.get('Amenities')
    atmosphere = additional_info.get('Atmosphere')
    crowd = additional_info.get('Crowd')
    planning = additional_info.get('Planning')
    payments = additional_info.get('Payments')
    
    # Logic for wifi (can be under two different keys)
    has_wifi = _extract_boolean_flag(amenities, 'Wi-Fi') or _extract_boolean_flag(amenities, 'Free Wi-Fi')
    
    # Logic for cash_only (inferring from the absence of electronic payments)
    has_credit_card = _extract_boolean_flag(payments, 'Credit cards')
    has_debit_card = _extract_boolean_flag(payments, 'Debit cards')
    has_nfc = _extract_boolean_flag(payments, 'NFC mobile payments')
    is_cash_only = not (has_credit_card or has_debit_card or has_nfc)

    # Build the final flattened dictionary, matching the image fields exactly
    flat_data = {
        # ---- Core Business Information ----
        'name': cafe.get('title'),
        'main_category': cafe.get('categoryName'),
        'category': json.dumps(cafe.get('categories')) if cafe.get('categories') else None,
        'address': cafe.get('address'),
        'city': cafe.get('city'),
        'postal': cafe.get('postalCode'),
        'country': cafe.get('countryCode'),
        'phone': cafe.get('phone'),
        'place_id': cafe.get('placeId'),
        'cid': cafe.get('cid'),
        'url': cafe.get('url'),
        
        # ---- Search and Performance Metrics ----
        'search_term': cafe.get('searchString'),
        'rating': cafe.get('totalScore'),
        'reviews_count': cafe.get('reviewsCount'),
        
        # ---- Location ----
        'lat': cafe.get('location', {}).get('lat'),
        'lng': cafe.get('location', {}).get('lng'),
        
        # ---- Hours ----
        'weekly_hours': json.dumps(cafe.get('openingHours')) if cafe.get('openingHours') else None,
        
        # ---- Service Boolean Flags ----
        'dine_in': _extract_boolean_flag(service_options, 'Dine-in'),
        'takeout': _extract_boolean_flag(service_options, 'Takeout'),
        
        # ---- Offering Boolean Flags ----
        'vegetarian': _extract_boolean_flag(offerings, 'Vegetarian options'),
        'alcohol': _extract_boolean_flag(offerings, 'Alcohol'),
        'beer': _extract_boolean_flag(offerings, 'Beer'),
        'coffee': _extract_boolean_flag(offerings, 'Coffee'),
        
        # ---- Dining Occasion Boolean Flags ----
        'breakfast': _extract_boolean_flag(dining_options, 'Breakfast'),
        'lunch': _extract_boolean_flag(dining_options, 'Lunch'),
        'dinner': _extract_boolean_flag(dining_options, 'Dinner'),
        
        # ---- Amenity Boolean Flags ----
        'wifi': has_wifi,
        'restroom': _extract_boolean_flag(amenities, 'Restroom'),
        
        # ---- Atmosphere & Crowd Boolean Flags ----
        'casual': _extract_boolean_flag(atmosphere, 'Casual'),
        'family_friendly': _extract_boolean_flag(crowd, 'Family-friendly'),
        'tourists': _extract_boolean_flag(crowd, 'Tourists'),
        
        # ---- Planning & Payment Boolean Flags ----
        'reservations': _extract_boolean_flag(planning, 'Accepts reservations'),
        'cash_only': is_cash_only if payments else None
    }
    
    return flat_data