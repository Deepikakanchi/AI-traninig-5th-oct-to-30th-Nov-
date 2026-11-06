import re


MAX_INPUT_LENGTH = 1000

_RESTAURANT_KEYWORDS = {
    "restaurant",
    "restaurants",
    "food",
    "eat",
    "dine",
    "dining",
    "cuisine",
    "menu",
    "dish",
    "meal",
    "lunch",
    "dinner",
    "breakfast",
    "price",
    "cost",
    "guest",
    "guests",
    "people",
    "seat",
    "seats",
    "table",
    "italian",
    "chinese",
    "indian",
    "mexican",
    "japanese",
    "thai",
    "french",
    "american",
    "mediterranean",
    "pizza",
    "sushi",
}

_FOLLOW_UPS = {
    "yes",
    "yes please",
    "yeah",
    "yep",
    "no",
    "no thanks",
    "no thank you",
    "nope",
}

_GUEST_COUNT_FOLLOW_UP = re.compile(
    r"(?:(?:what about|for)\s+)?\d{1,2}(?:\s+(?:people|guests|persons?))?[?.!]?",
    re.IGNORECASE,
)

_EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
_PHONE = re.compile(
    r"(?<!\w)(?:\+\d{1,3}[\s.-]?)?(?:\(\d{2,4}\)|\d{3,4})"
    r"[\s.-]?\d{3,4}[\s.-]?\d{3,4}(?!\w)"
)


def validate_input(text: str) -> tuple[bool, str]:
    """Reject blank and excessively long user messages."""
    if not text or not text.strip():
        return False, "Please enter a question."
    if len(text) > MAX_INPUT_LENGTH:
        return False, f"Please keep your question under {MAX_INPUT_LENGTH} characters."
    return True, ""


def is_restaurant_related(text: str, has_context: bool = False) -> bool:
    """Allow restaurant topics and concise replies in an active conversation."""
    normalized = text.lower().strip().strip(" .!?")
    if has_context and (
        normalized in _FOLLOW_UPS or _GUEST_COUNT_FOLLOW_UP.fullmatch(normalized)
    ):
        return True

    words = set(re.findall(r"[a-z]+", normalized))
    return bool(words & _RESTAURANT_KEYWORDS)


def redact_pii(text: str) -> str:
    """Mask email addresses and phone numbers in text shown to the user."""
    text = _EMAIL.sub("[REDACTED EMAIL]", text)
    return _PHONE.sub("[REDACTED PHONE]", text)
