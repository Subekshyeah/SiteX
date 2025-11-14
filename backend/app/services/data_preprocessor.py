# app/services/data_preprocessor.py
from typing import Dict, Any

def flatten_additional_info(info_dict: Dict, key: str) -> Dict:
    """Helper function to flatten lists like 'Crowd' or 'Parking' into booleans."""
    # ... (implementation from previous response) ...
    if key not in info_dict or not isinstance(info_dict[key], list):
        return {}
    flat_dict = {}
    for item in info_dict[key]:
        for sub_key, sub_val in item.items():
            clean_sub_key = sub_key.lower().replace(' ', '_').replace('+', '_plus').replace("'", "")
            flat_dict[f"{key.lower()}_{clean_sub_key}"] = sub_val
    return flat_dict


def process_single_cafe(cafe: Dict[str, Any]) -> Dict[str, Any]:
    """Processes a single cafe JSON object into a flat dictionary."""
    # ... (implementation from previous response) ...
    flat_data = {
        'category': cafe.get('categoryName'),
        'neighborhood': cafe.get('neighborhood'),
        # ... other fields
        'latitude': cafe.get('location', {}).get('lat'),
        'longitude': cafe.get('location', {}).get('lng'),
        'is_permanently_closed': cafe.get('permanentlyClosed', False)
    }
    additional_info = cafe.get('additionalInfo', {})
    if additional_info:
        flat_data.update(flatten_additional_info(additional_info, 'Crowd'))
        flat_data.update(flatten_additional_info(additional_info, 'Parking'))
    return flat_data