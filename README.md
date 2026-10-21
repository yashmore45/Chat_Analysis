# Intelligent Chat Analysis Dashboard

A Python-based web application that analyzes customer-support conversations and classifies individual messages based on their intent, emotional tone, and communication category. The application also provides a conversation overview, visual analytics, detailed results, and CSV export functionality through an interactive Streamlit dashboard.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B)
![Status](https://img.shields.io/badge/Project-Prototype-orange)

## Overview

Customer-support conversations contain valuable information about customer needs, concerns, and experiences. This project provides a simple way to organize and analyze chat messages using a keyword-based text analysis approach.

Users can submit conversations directly, import text or CSV files, or explore the application using sample data. The results are presented in a dashboard for easier interpretation.

## Key Features

- **Multiple Input Methods:** Analyze text entered manually, upload TXT or CSV files, or use the included sample conversation.
- **Intent Classification:** Identify common topics such as refunds, order tracking, technical issues, billing, cancellations, product questions, complaints, appreciation, and general inquiries.
- **Emotion Analysis:** Categorize messages into frustration, satisfaction, happiness, sadness, confusion, or neutral emotion.
- **Message Type Detection:** Group messages into complaints, requests, inquiries, feedback, appreciation, or general communication.
- **Conversation Insights:** Generate an overview of the conversation based on the most frequently detected labels.
- **Visual Analytics:** Explore intent distribution and emotional patterns through interactive charts.
- **Message-Level Results:** View the predicted labels and word count for each message in a structured table.
- **Export Results:** Download the analyzed messages and their classifications as a CSV file.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web interface and dashboard |
| Pandas | Data processing and tabular results |
| Keyword-based text analysis | Message classification |
| Plotly or Streamlit charts, as implemented | Data visualization |

*The visualization library should match the one used in your actual source code.*

## Analysis Workflow

The application follows a straightforward text-processing pipeline:

1. **Collect input:** Accept pasted conversations, uploaded files, or sample messages.
2. **Prepare text:** Normalize whitespace and convert text to lowercase for consistent matching.
3. **Analyze content:** Compare message text against predefined keyword lists for each classification group.
4. **Assign labels:** Select the category with the highest keyword score, using a default label when no keywords match.
5. **Present insights:** Display summary information, charts, message classifications, and word counts.
6. **Export data:** Allow users to download the analysis results in CSV format.

### Classification Approach

Each category contains a predefined collection of relevant words and phrases. The application checks which terms appear in a message and calculates a score for each category. The category with the highest score becomes the predicted label.

This method is lightweight and easy to understand, making it suitable for demonstrating the basic concepts of text classification and customer conversation analytics.

## Installation and Setup

### Prerequisites

- Python 3.9 or later
- Git
- pip package manager

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_REPOSITORY_FOLDER
```

Replace the repository URL and folder name with your own GitHub repository details.

### 2. Create a Virtual Environment (Optional)

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On macOS or Linux:

```bash
source venv/bin/activate
```

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

### 4. Launch the Application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, usually `http://localhost:8501`.

## Sample Conversation

Try analyzing the following customer-support messages:

```text
Customer: Can you tell me the status of my order?
Customer: My delivery is late, and I need an update.
Customer: I am disappointed with this delay.
Agent: I apologize for the inconvenience. Please share your order ID.
Customer: Thank you for helping me resolve this issue.
```

The application will classify each message and display the resulting labels, conversation statistics, and visual summaries.

## Repository Structure

```text
intelligent-chat-analysis/
├── app.py
├── requirements.txt
├── sample_data/
│   └── sample_chat.csv
├── README.md
└── LICENSE
```

- `app.py` — Contains the Streamlit interface and analysis functionality.
- `requirements.txt` — Lists the Python packages needed to run the project.
- `sample_data/sample_chat.csv` — Provides example conversation data for testing.
- `README.md` — Documents the project and its setup instructions.
- `LICENSE` — Specifies the terms under which the project may be used.

## Current Limitations

The application uses predefined keywords rather than a trained natural language processing model. Therefore, some predictions may not accurately represent the meaning of a message.

Current limitations include:

- Difficulty recognizing sarcasm and understanding negation.
- Limited support for spelling variations, slang, emojis, and regional languages.
- Inability to represent multiple intents or emotions with a single predicted label.
- No distinction between customer and support-agent messages during classification.
- Possible incorrect matches when keywords appear in unrelated contexts.
- No formal accuracy evaluation against a labelled benchmark dataset.

The application is intended for learning and demonstration purposes. Its predictions should not be treated as definitive assessments of customer sentiment or intent.

## Future Enhancements

Potential improvements include:

- Integrating machine learning models such as Naive Bayes and Support Vector Machines.
- Exploring transformer-based models for contextual text understanding.
- Improving keyword matching through lemmatization and negation handling.
- Separating customer and agent messages for more meaningful analysis.
- Adding conversation timelines and emotion-trend visualizations.
- Supporting Hindi, Marathi, and mixed-language conversations.
- Generating more informative summaries using NLP or large language models.
- Evaluating classification performance using accuracy, precision, recall, F1-score, and confusion matrices.
- Connecting the dashboard to customer-support platforms for automated analysis.

## Author

**Yash More**

GitHub: [Add Your GitHub Profile URL](https://github.com/)

