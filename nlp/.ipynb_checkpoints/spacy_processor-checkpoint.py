import spacy

def process_chat_message(message):
    # Mock response to simulate parsing for testing
    parsed_data = {
        "entities": [
            ("chicken", "FOOD"),
            ("200 grams", "QUANTITY"),
            ("grill", "METHOD")
        ],
        "tokens": message.split()  # Tokenize by splitting on spaces for simplicity
    }
    return parsed_data