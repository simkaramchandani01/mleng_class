#!/usr/bin/env python
# coding: utf-8

# #### Importing Libraries

# In[1]:


import sys
import os
import joblib
import datetime
from sentence_transformers import SentenceTransformer


# #### Check Validity of Input

# In[2]:


def validate_input():
    if len(sys.argv) != 3:
        print("Invalid number of inputs. Usage: python score_headlines.py <HEADLINE_FILE> <SOURCE_NAME>")
        sys.exit(1)

    headline_file = sys.argv[1]
    source_name = sys.argv[2]

    if not os.path.exists(headline_file):
        print(f"Error: Unable to find '{headline_file}'.")
        sys.exit(1)

    if not headline_file.endswith('.txt'):
        print(f"Error:'{headline_file}' is not a text file.")
        sys.exit(1)

    return headline_file, source_name


# #### Analyze Headline 

# In[3]:


def analyze_headline_sentiment(headlines, transformer_model, sentiment_classifier):
    print("Generating embeddings for headlines...")
    embeddings = transformer_model.encode(headlines)  

    print("Predicting sentiment...")
    predictions = sentiment_classifier.predict(embeddings)  

    label_mapping = {0: "neutral", 1: "positive", -1: "negative"}
    readable_predictions = [label_mapping[pred] for pred in predictions]

    results = list(zip(readable_predictions, headlines))

    return results


# #### Save File

# In[4]:


def save_file(results, source):
    today = datetime.today().strftime("%Y_%m_%d")
    final_file = f"headline_scores_{source}_{today}.txt"

    try:
        with open(final_file, "w", encoding="utf-8") as file:
            for label, headline in results:
                file.write(f"{label}, {headline}\n")
        print(f"Final File: {final_file}")
    except Exception as e:
        print(f"Error while saving final file: {e}")
        sys.exit(1)


# #### Main Function

# In[6]:


def main():
    headlines, source = validate_input()

    print("Loading models...")
    transformer_model = SentenceTransformer('all-MiniLM-L6-v2')  
    sentiment_classifier = joblib.load("svm.joblib")  

    print("Analyzing headline sentiment...")
    results = analyze_headline_sentiment(headlines, transformer_model, sentiment_classifier)

    save_file(results, source)


# In[7]:


if __name__ == "__main__":
    main()

