# 🎈 IEC 61499 AI Assistant

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://ubiquitous-waddle-vpw54647w79hjx5.github.dev/)


## Overview of the IEC 61499 AI Assistant 

This application showcases a growing collection of LLM powered IEC 61499 control systems.

Current examples include:

- IEC 61499 AI Assistant
- IEC 61499 Solution Q&A
- IEC 61499 SQL Chatbot
- IEC 61499 ML Agent
- IEC 61499 FB Genereator Assistant
- IEC 61499 Graph DB Chatbot
- IEC 61499 AI Skill Executer

## Demo App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://iec61499.streamlit.app/)

### Get an OpenAI API key

You can get your own OpenAI API key by following the following instructions:

1. Go to https://platform.openai.com/account/api-keys.
2. Click on the `+ Create new secret key` button.
3. Next, enter an identifier name (optional) and click on the `Create secret key` button.

### Enter the OpenAI API key in Streamlit Community Cloud

To set the OpenAI API key as an environment variable in Streamlit apps, do the following:

1. At the lower right corner, click on `< Manage app` then click on the vertical "..." followed by clicking on `Settings`.
2. This brings the **App settings**, next click on the `Secrets` tab and paste the API key into the text box as follows:

```sh
OPENAI_API_KEY='xxxxxxxxxx'
```

## Run it locally

```sh
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run Chatbot.py
```
