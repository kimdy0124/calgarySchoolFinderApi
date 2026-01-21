import os
import math
from typing import List, Dict, Any, Optional

from fastapi import APIRouter

router = APIRouter(prefix="/schools", tags=["schools"])

DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() in ("1", "true", "yes", "y")

DEMO_SCHOOLS: List[Dict[str, Any]] = [
    {
        "school_id": 1,
        "name": "Demo - Crescent Heights High School",
        "address_line": "1015 1 St NW, Calgary, AB",
        "postal_code": "T2M 2R2",
        "phone": "403-000-0001",
        "email": "info@demo-public.ca",
        "latitude": 51.0667,
        "longitude": -114.0746,
        "district": {"name": "Calgary Board of Education", "type": "Public"},
    },
    {
        "school_id": 2,
        "name": "Demo - St. Mary's High School",
        "address_line": "111 18 Ave SW, Calgary, AB",
        "postal_code": "T2S 0B3",
        "phone": "403-000-0002",
        "email": "info@demo-catholic.ca",
        "latitude": 51.0376,
        "longitude": -114.0719,
        "district": {"name": "Calgary Catholic School District", "type": "Catholic"},
    },
    {
        "school_id": 3,
        "name": "Demo - Western Canada High School",
        "address_line": "641 17 Ave SW, Calgary, AB",
        "postal_code": "T2S 0B5",
        "phone": "403-000-0003",
        "email": "info@demo-public2.ca",
        "latitude": 51.0373,
        "longitude": -114.0785,
        "district": {"name": "Calgary Board of Education", "type": "Public"},
    },
    {
        "school_id": 4,
        "name": "Demo - Father Lacombe High School",
        "address_line": "332 35 Ave SE, Calgary, AB",
        "postal_code": "T2G 1W1",
        "phone": "403-000-0004",
        "email": "info@demo-catholic2.ca",
        "latitude": 51.0215,
        "longitude": -114.0576,
        "district": {"name": "Calgary Catholic School District", "type": "Catholic"},
    },
    {
        "school_id": 5,
        "name": "Demo - Sir Winston Churchill High School",
        "address_line": "5220 Northland Dr NW, Calgary, AB",
        "postal_code": "T2L 2J6",
        "phone": "403-000-0005",
        "email": "info@demo-public3.ca",
        "latitude": 51.0912,
        "longitude": -114.1330,
        "district": {"name": "Calgary Board of Education", "type": "Public"},
    },
]

def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@router.get("/nearby")
def nearby(
    lat: float,
    lng: float,
    radius_km: float = 10,
    district_type: Optional[str] = None,
    limit: int = 50,
):
    if DEMO_MODE:
        results = []
        for s in DEMO_SCHOOLS:
            d = _haversine_km(lat, lng, s["latitude"], s["longitude"])
            if d <= radius_km:
                item = dict(s)
                item["distance_km"] = d
                results.append(item)

        if district_type:
            results = [
                r for r in results
                if (r.get("district") or {}).get("type") == district_type
            ]

        results.sort(key=lambda x: x.get("distance_km", 999999))
        return results[:limit]

    return []
