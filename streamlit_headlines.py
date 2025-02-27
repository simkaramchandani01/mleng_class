#!/usr/bin/env python
# coding: utf-8

# ### Import Libraries

# In[1]:


import streamlit as st
import requests


# ### Headline Input

# In[3]:


def send_to_web_service(headlines):
    url = "http://104.248.15.218:9087/score_headlines_api_2.py"  
    response = requests.post(url, json={"headlines": headlines})
    return response.json() if response.status_code == 200 else {"error": "Service unavailable"}

st.title("Score Headlines App")

st.write("Enter your headlines below. You can edit or delete them before final submission.")


# In[4]:


if "headlines" not in st.session_state:
    st.session_state.headlines = [""]


# ### Addition of Headline

# In[5]:


if st.button("Add Headline"):
    st.session_state.headlines.append("")


# ### Update Headlines

# In[6]:


updated_headlines = []
for i, headline in enumerate(st.session_state.headlines):
    col1, col2 = st.columns([4, 1])
    updated_text = col1.text_input(f"Headline {i+1}", value=headline, key=f"headline_{i}")
    delete = col2.button("X", key=f"delete_{i}")
    if not delete:
        updated_headlines.append(updated_text)

st.session_state.headlines = updated_headlines


# ### Final Result

# In[7]:


if st.button("Submit Headlines"):
    result = send_to_web_service(st.session_state.headlines)
    st.write("Result:")
    st.json(result)

