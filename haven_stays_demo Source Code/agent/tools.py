# Custom tools for the Haven Stays concierge agent.
#
# Readable copy of the CUSTOM_TOOLS source that is embedded (as a JSON string)
# in the agent config and sent to POST /v1/agents. The AdaL runtime writes this
# to .adal/tools.py in the session worker and auto-discovers the CUSTOM_TOOLS list.
#
# Design: the property catalog is an in-memory dict and pricing is pure logic,
# so every tool call succeeds live (no external API to fail mid-demo). Rates and
# discounts live in build_quote — never in the prompt — so the agent cannot
# hallucinate a price.

# In-memory luxury property catalog. property_id -> details.
_CATALOG = {
    "HVN-MAUI-01": {
        "name": "Cliffside Oasis, Maui",
        "location": "Maui, Hawaii",
        "region": "hawaii",
        "price_per_night": 1200,
        "bedrooms": 3,
        "bathrooms": 3,
        "max_guests": 6,
        "amenities": ["pool", "oceanfront", "wifi", "ac", "kitchen", "hot_tub", "parking"],
        "tags": ["beach", "romantic", "luxury"],
        "rating": 4.9,
        "reviews": 312,
    },
    "HVN-BIGSUR-02": {
        "name": "Glass House, Big Sur",
        "location": "Big Sur, California",
        "region": "california",
        "price_per_night": 950,
        "bedrooms": 2,
        "bathrooms": 2,
        "max_guests": 4,
        "amenities": ["wifi", "ac", "kitchen", "fireplace", "parking", "workspace"],
        "tags": ["nature", "design", "luxury"],
        "rating": 4.8,
        "reviews": 198,
    },
    "HVN-ASPEN-03": {
        "name": "Alpine Chalet, Aspen",
        "location": "Aspen, Colorado",
        "region": "colorado",
        "price_per_night": 1450,
        "bedrooms": 4,
        "bathrooms": 4,
        "max_guests": 8,
        "amenities": ["pool", "hot_tub", "wifi", "ac", "kitchen", "fireplace", "parking", "ski_in_out"],
        "tags": ["mountain", "family", "luxury", "ski"],
        "rating": 4.9,
        "reviews": 421,
    },
    "HVN-TUSC-04": {
        "name": "Villa Bellavista, Tuscany",
        "location": "Tuscany, Italy",
        "region": "italy",
        "price_per_night": 1100,
        "bedrooms": 5,
        "bathrooms": 4,
        "max_guests": 10,
        "amenities": ["pool", "wifi", "kitchen", "fireplace", "parking", "vineyard"],
        "tags": ["countryside", "family", "luxury", "wine"],
        "rating": 4.9,
        "reviews": 287,
    },
    "HVN-TULUM-05": {
        "name": "Jungle Retreat, Tulum",
        "location": "Tulum, Mexico",
        "region": "mexico",
        "price_per_night": 680,
        "bedrooms": 2,
        "bathrooms": 2,
        "max_guests": 4,
        "amenities": ["pool", "wifi", "ac", "kitchen", "parking", "pet_friendly"],
        "tags": ["beach", "jungle", "boutique"],
        "rating": 4.7,
        "reviews": 156,
    },
    "HVN-KYOTO-06": {
        "name": "Machiya Garden House, Kyoto",
        "location": "Kyoto, Japan",
        "region": "japan",
        "price_per_night": 820,
        "bedrooms": 3,
        "bathrooms": 2,
        "max_guests": 6,
        "amenities": ["wifi", "ac", "kitchen", "garden", "workspace", "parking"],
        "tags": ["city", "design", "cultural"],
        "rating": 4.8,
        "reviews": 203,
    },
    "HVN-SANTO-07": {
        "name": "Cycladic Escape, Santorini",
        "location": "Santorini, Greece",
        "region": "greece",
        "price_per_night": 1380,
        "bedrooms": 2,
        "bathrooms": 2,
        "max_guests": 4,
        "amenities": ["pool", "oceanfront", "wifi", "ac", "kitchen", "hot_tub"],
        "tags": ["beach", "romantic", "luxury"],
        "rating": 5.0,
        "reviews": 178,
    },
    "HVN-PARIS-08": {
        "name": "Le Marais Penthouse, Paris",
        "location": "Paris, France",
        "region": "france",
        "price_per_night": 990,
        "bedrooms": 2,
        "bathrooms": 2,
        "max_guests": 4,
        "amenities": ["wifi", "ac", "kitchen", "workspace", "balcony"],
        "tags": ["city", "design", "luxury"],
        "rating": 4.8,
        "reviews": 245,
    },
}


def _find(property_id):
    """Case-insensitive catalog lookup. Returns (canonical_id, details) or (None, None)."""
    key = str(property_id).strip().upper()
    for k, v in _CATALOG.items():
        if k.upper() == key:
            return k, v
    return None, None


def _match_amenities(have, want):
    """True if every wanted amenity is present in the home's amenity list."""
    if not want:
        return True
    have_set = {a.lower() for a in have}
    return all(w.lower() in have_set for w in want)


def search_properties(location: str = "", budget: int = 0, amenities: list = None) -> list:
    """Search the Haven Stays luxury property catalog.

    Call this FIRST whenever the traveler asks about homes, recommendations,
    availability, or prices. Filter by location (region or destination name),
    max nightly budget, and required amenities.

    Args:
        location: Region or destination — e.g. "hawaii", "italy", "maui", "paris".
                  Case-insensitive; matches against the property's region and location.
        budget: Maximum nightly rate in USD. 0 or omitted = no budget cap.
        amenities: Required amenities — e.g. ["pool", "oceanfront", "pet_friendly"].
                   The home must have ALL listed amenities to match.

    Returns a list of matching homes: property_id, name, location, price_per_night,
    bedrooms, bathrooms, max_guests, amenities, rating, reviews.
    """
    loc = str(location or "").strip().lower()
    amenities = amenities or []
    results = []
    for pid, p in _CATALOG.items():
        if loc and loc not in p["region"].lower() and loc not in p["location"].lower():
            continue
        if budget and p["price_per_night"] > budget:
            continue
        if not _match_amenities(p["amenities"], amenities):
            continue
        results.append({
            "property_id": pid,
            "name": p["name"],
            "location": p["location"],
            "price_per_night": p["price_per_night"],
            "bedrooms": p["bedrooms"],
            "bathrooms": p["bathrooms"],
            "max_guests": p["max_guests"],
            "amenities": p["amenities"],
            "rating": p["rating"],
            "reviews": p["reviews"],
        })
    # Sort by rating (desc) then price (asc) so the best rises to the top.
    results.sort(key=lambda r: (-r["rating"], r["price_per_night"]))
    return results


def check_availability(property_id: str, dates: str = "") -> dict:
    """Check availability for a Haven Stays property on given dates.

    Always call this before promising specific dates to a traveler. Returns
    whether the home is available and the next available check-in date.

    Args:
        property_id: The property ID from search_properties (e.g. "HVN-MAUI-01").
        dates: Human-readable date range (e.g. "2026-07-15 to 2026-07-22").
               Parsed loosely; if empty, returns general availability.
    """
    canonical, p = _find(property_id)
    if not p:
        return {"error": f"Property '{property_id}' not found."}
    # Deterministic mock: homes are "available" — this is a self-contained demo.
    return {
        "property_id": canonical,
        "name": p["name"],
        "location": p["location"],
        "requested_dates": dates or "not specified",
        "available": True,
        "next_check_in": "2026-07-15",
        "min_nights": 2,
        "note": "Available for your dates. Reserve with capture_lead to hold it.",
    }


def build_quote(property_id: str, nights: int = 1, loyalty_member: bool = False) -> dict:
    """Build a price quote for a Haven Stays property.

    Applies a 10% weekly discount for stays of 7+ nights, and an extra 5%
    loyalty discount for Haven Stays loyalty members. Returns the nightly rate,
    line items, discounts, the final total, and total savings.

    Args:
        property_id: The property ID from search_properties.
        nights: Number of nights for the stay.
        loyalty_member: True if the traveler is a Haven Stays loyalty member.
    """
    canonical, p = _find(property_id)
    if not p:
        return {"error": f"Property '{property_id}' not found."}
    nights = max(1, int(nights))
    nightly = p["price_per_night"]
    subtotal = nightly * nights
    weekly = round(subtotal * 0.10, 2) if nights >= 7 else 0.0
    loyalty = round((subtotal - weekly) * 0.05, 2) if loyalty_member else 0.0
    total = round(subtotal - weekly - loyalty, 2)
    return {
        "property_id": canonical,
        "name": p["name"],
        "location": p["location"],
        "nights": nights,
        "nightly_rate": nightly,
        "subtotal": subtotal,
        "weekly_discount": weekly,
        "loyalty_discount": loyalty,
        "total": total,
        "you_save": round(subtotal - total, 2),
        "loyalty_member": loyalty_member,
    }


def capture_lead(name: str, email: str, property_id: str = "") -> dict:
    """Save a traveler's contact details and place a hold on a property.

    Call this ONLY when the traveler shows booking intent — they ask to reserve,
    request a hold, or share their contact details. Never capture a lead for
    casual browsing.

    Args:
        name: Traveler's full name.
        email: Traveler's email address.
        property_id: The property ID to place on hold.
    """
    canonical, p = _find(property_id)
    return {
        "status": "held",
        "name": name,
        "email": email,
        "property_id": canonical,
        "property_name": p["name"] if p else None,
        "next_step": "A Haven Stays specialist will email you within 1 hour to confirm your reservation and send a secure payment link.",
    }


CUSTOM_TOOLS = [search_properties, check_availability, build_quote, capture_lead]
