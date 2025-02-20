#!/usr/bin/env python
# coding: utf-8

# ## Assignment 2 | Simran Karamchandani

# ### Import Libraries

# In[1]:


import logging


# In[2]:


from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from transformers import pipeline


# ### Logging

# In[3]:


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ### Transformer Model

# In[4]:


logger.info("Loading sentiment analysis model...")
sentiment_analyzer = pipeline("sentiment-analysis")
logger.info("Model loaded successfully.")


# ### Create FastAPI

# In[5]:


app = FastAPI()


# ### Defining Base Model

# In[6]:


class HeadlinesRequest(BaseModel):
    headlines: List[str]


# ### Classification

# In[8]:


def classify_headline(headline: str) -> str:
    try:
        result = sentiment_analyzer(headline)[0]
        logger.debug(f"Headline: {headline} | Sentiment: {result}")
        if result["label"] == "POSITIVE":
            return "Optimistic"
        elif result["label"] == "NEGATIVE":
            return "Pessimistic"
        else:
            return "Neutral"
    except Exception as e:
        logger.error(f"Error processing headline: {headline}. Exception: {e}")
        return "Neutral"


# ### Status

# In[9]:


@app.get("/status")
def status():
    logger.info("Status check request received.")
    return {"status": "OK"}


# ### Score Headlines

# In[10]:


@app.post("/score_headlines")
def score_headlines(request: HeadlinesRequest):
    logger.info(f"Scoring request received with {len(request.headlines)} headlines.")
    labels = [classify_headline(headline) for headline in request.headlines]
    return {"labels": labels}

