import spacy

# Load your custom NLP model
nlp = spacy.load("C:/Users/Rimantas/Desktop/architektura/nlp/foodstuffs")

def process_chat_message(message):
    # Process the input message with spaCy to identify entities
    doc = nlp(message)
    
    # Extract entities and store only relevant tags
    parsed_data = {
        "entities": [(ent.text, ent.label_) for ent in doc.ents if ent.label_ in ["COOKING_TIME", "SERVING_SIZE", "INGREDIENT", "METHOD", "FLAVOR_PROFILE", "MEAL_TYPE", "DIETARY", "QUANTITY", "TEMPERATURE"]]
    }
    print(parsed_data)
    return parsed_data