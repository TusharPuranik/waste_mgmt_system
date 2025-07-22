def classify_waste(description):
    """
    Simple rule-based classification.
    Returns one of: 'Organic', 'Recyclable', 'Hazardous', or 'Mixed'.
    """
    text = description.lower()
    organic_keywords = ['fruit', 'vegetable', 'food', 'organic', 'leaf']
    recyclable_keywords = ['plastic', 'paper', 'glass', 'metal', 'cardboard']
    hazardous_keywords = ['battery', 'chemical', 'paint', 'hazard']

    for kw in organic_keywords:
        if kw in text:
            return 'Organic'
    for kw in recyclable_keywords:
        if kw in text:
            return 'Recyclable'
    for kw in hazardous_keywords:
        if kw in text:
            return 'Hazardous'
    # Default if no keywords match
    return 'Mixed'
