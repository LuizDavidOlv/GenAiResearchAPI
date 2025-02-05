# ResearchAPI
- This API was based in this langchain repo: https://github.com/langchain-ai/report-mAIstro



## Overview

The **Research API** is a FastAPI-based application designed to facilitate research and essay generation using AI models. The system enables users to submit research topics, which are processed to generate structured reports or essays based on web searches and AI-generated insights.

## Features

- **Research Topic Generation**: Submits a research request and receives a summarized document.
- **Essay Writing**: Generates structured essays based on user-provided topics.
- **Configurable Search Queries**: Utilizes web searches for enhanced context generation.
- **AI-driven Report Structuring**: Automatically organizes reports into logical sections.
- **Error Handling**: Provides structured API responses with error messages.

## API Endpoints

### **Health Check**
**Endpoint**: `GET /health`

Checks the health of the API.

### **Research Topic**
**Endpoint**: `POST /research/research-topic`

#### Request Body:
```json
{
  "input_text": "Quantum Computing in Cryptography",
  "chat_model": "gpt-4o-mini",
  "temp": 1
}
```

#### Response Body:
```json
{
  "data": "Generated summary of the research topic",
  "errors": null,
  "meta": null,
  "success": true,
  "message": "Document Summarized"
}
```
