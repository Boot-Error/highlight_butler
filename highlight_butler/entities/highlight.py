from dataclasses import dataclass
from typing import List, Optional

@dataclass
class HighlightLocation:
    locationIdentifier: str
    value: str

@dataclass
class Highlight:
    text: str
    annotation: str
    location: Optional[HighlightLocation]
    tags: Optional[List[str]]
    
@dataclass
class HighlightDocument:
    author: str
    category: str
    tags: str
    created: str
    url: str
    title: str
    highlights: List[Highlight]

