import streamlit as st
import spacy
from collections import Counter

# Load spaCy's small English model
@st.cache_resource
def load_nlp():
    return spacy.load("en_core_web_sm")

nlp = load_nlp()

# Streamlit App UI Setup
st.set_page_config(page_title="AI Entity & Keyword Extractor", page_icon="🔍")
st.title("🔍 Smart Keyword & Entity Extractor")
st.write("Paste your text below to extract key entities and top keywords instantly.")

# Text Input Area
text_input = st.text_area("Enter Text Here:", height=200, placeholder="Type or paste an article, resume, or paragraph...")

if st.button("Extract Info"):
    if text_input.strip() == "":
        st.warning("Please enter some text first!")
    else:
        # Process the text with spaCy
        doc = nlp(text_input)
        
        # 1. Extract Named Entities
        st.subheader("📌 Named Entities Found")
        
        # Define the types of entities we want to display nicely
        target_labels = {"PERSON": "👤 People", "ORG": "🏢 Organizations", "GPE": "📍 Locations", "DATE": "📅 Dates"}
        
        # Group entities by their category
        entities_found = {val: [] for val in target_labels.values()}
        for ent in doc.ents:
            if ent.label_ in target_labels:
                category = target_labels[ent.label_]
                if ent.text not in entities_found[category]: # Avoid duplicates
                    entities_found[category].append(ent.text)
        
        # Display entities in organized columns
        cols = st.columns(len(target_labels))
        for col, (category, items) in zip(cols, entities_found.items()):
            with col:
                st.markdown(f"**{category}**")
                if items:
                    for item in items:
                        st.markdown(f"- {item}")
                else:
                    st.caption("None detected")
                    
        st.markdown("---")
        
        # 2. Extract Top Keywords (Nouns and Verbs, excluding common stopwords)
        st.subheader("🔑 Top Keywords")
        keywords = [
            token.text.lower() for token in doc 
            if token.pos_ in ["NOUN", "PROPN", "VERB"] and not token.is_stop and not token.is_punct
        ]
        
        # Get the 10 most common words
        most_common_keywords = Counter(keywords).most_common(10)
        
        if most_common_keywords:
            # Display keywords as clickable tags or a neat list
            keyword_strings = [f"{word} ({count})" for word, count in most_common_keywords]
            st.info(", ".join(keyword_strings))
        else:
            st.caption("No significant keywords found.")