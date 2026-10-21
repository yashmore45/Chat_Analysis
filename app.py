import re
from collections import Counter

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Intelligent Chat Analysis",
    page_icon="💬",
    layout="wide",
)

st.title("💬 Intelligent Chat Analysis")
st.caption("Intent Detection • Emotion Recognition • Message Classification • Conversation Summary")


INTENT_KEYWORDS = {
    "Refund Request": ["refund", "money back", "reimburse", "return my money"],
    "Order Tracking": ["where is my order", "track my order", "delivery", "shipped", "tracking", "late order", "hasn't arrived", "not arrived"],
    "Technical Support": ["not working", "error", "bug", "crash", "issue", "problem", "can't log in", "cannot log in", "reset password", "technical"],
    "Billing / Payment": ["charged", "payment", "billing", "invoice", "wrong amount", "subscription", "paid twice"],
    "Cancellation": ["cancel", "cancellation", "close my account", "stop my subscription"],
    "Product Inquiry": ["features", "details", "how does", "information", "available", "price", "cost", "specifications"],
    "Complaint": ["complaint", "unacceptable", "terrible", "very bad", "disappointed", "poor service", "frustrated", "angry"],
    "Appreciation": ["thank you", "thanks", "great service", "excellent", "awesome", "appreciate"],
    "General Inquiry": ["what", "when", "where", "why", "how", "can you", "could you", "please help"],
}

EMOTION_KEYWORDS = {
    "Frustration": ["frustrated", "angry", "annoyed", "unacceptable", "ridiculous", "fed up", "terrible", "worst", "disappointed", "still waiting"],
    "Satisfaction": ["satisfied", "resolved", "that helps", "problem solved", "works now", "happy with", "thank you", "thanks", "great service"],
    "Happiness": ["happy", "excited", "awesome", "excellent", "love it", "amazing", "wonderful", "great"],
    "Sadness": ["sad", "upset", "unfortunate", "disappointed", "sorry to hear", "unhappy"],
    "Confusion": ["confused", "don't understand", "do not understand", "unclear", "what do you mean", "not sure"],
}

CATEGORY_KEYWORDS = {
    "Complaint": ["complaint", "unacceptable", "terrible", "frustrated", "angry", "disappointed", "poor service", "worst"],
    "Request": ["please", "can you", "could you", "i need", "i want", "help me", "would like"],
    "Inquiry": ["what", "when", "where", "why", "how", "details", "information", "is it", "does it"],
    "Feedback": ["suggest", "feedback", "recommend", "improve", "opinion"],
    "Appreciation": ["thank you", "thanks", "appreciate", "excellent", "great service", "awesome"],
}


def keyword_score(text, keywords):
    text = text.lower()
    return sum(1 for keyword in keywords if keyword in text)


def detect_intent(text):
    scores = {intent: keyword_score(text, words) for intent, words in INTENT_KEYWORDS.items()}
    best_intent = max(scores, key=scores.get)
    if scores[best_intent] == 0:
        return "Other / Unclear"
    return best_intent


def detect_emotion(text):
    scores = {emotion: keyword_score(text, words) for emotion, words in EMOTION_KEYWORDS.items()}
    best_emotion = max(scores, key=scores.get)
    if scores[best_emotion] == 0:
        return "Neutral"
    return best_emotion


def classify_message(text):
    scores = {category: keyword_score(text, words) for category, words in CATEGORY_KEYWORDS.items()}
    best_category = max(scores, key=scores.get)
    if scores[best_category] == 0:
        return "General"
    return best_category


def clean_text(text):
    text = str(text).replace("\n", " ").strip()
    return re.sub(r"\s+", " ", text)


def make_summary(messages, results):
    if not messages:
        return "No messages were provided."
    intents = Counter(results["Intent"])
    emotions = Counter(results["Emotion"])
    categories = Counter(results["Category"])
    common_intent = intents.most_common(1)[0][0]
    common_emotion = emotions.most_common(1)[0][0]
    common_category = categories.most_common(1)[0][0]
    customer_msgs = len(messages)
    preview = " ".join(messages[:3])
    if len(preview) > 350:
        preview = preview[:347] + "..."
    return (
        f"The conversation contains {customer_msgs} analyzed message(s). "
        f"The most common detected intent is **{common_intent}**, the most common "
        f"emotion label is **{common_emotion}**, and the most common message category "
        f"is **{common_category}**. Key conversation text: “{preview}” "
        "These labels are generated using keyword-based heuristics and should be reviewed "
        "in context rather than treated as definitive judgments."
    )


def analyze_messages(messages):
    rows = []
    for i, message in enumerate(messages, start=1):
        message = clean_text(message)
        if not message:
            continue
        rows.append({
            "Message No.": i,
            "Message": message,
            "Intent": detect_intent(message),
            "Emotion": detect_emotion(message),
            "Category": classify_message(message),
            "Word Count": len(message.split()),
        })
    return pd.DataFrame(rows)


with st.sidebar:
    st.header("How to use")
    st.write("1. Paste a chat or upload a file.")
    st.write("2. Click **Analyze Conversation**.")
    st.write("3. Review labels, charts and summary.")
    st.divider()
    st.caption("Prototype note: this version uses keyword-based NLP heuristics, not a trained deep-learning model.")


tab_paste, tab_upload, tab_demo = st.tabs(["Paste chat", "Upload file", "Try sample"])

messages = []
input_source = ""

with tab_paste:
    pasted_chat = st.text_area(
        "Paste one message per line",
        height=220,
        placeholder="Customer: My order hasn't arrived yet.\nCustomer: I'm really frustrated. Can someone help me?\nAgent: I'm sorry for the delay. Your order will arrive tomorrow.",
    )
    if st.button("Analyze pasted chat", type="primary", key="analyze_paste"):
        messages = [line.strip() for line in pasted_chat.splitlines() if line.strip()]
        input_source = "pasted chat"
        if not messages:
            st.warning("Please paste at least one message.")
        else:
            st.session_state["messages_to_analyze"] = messages
            st.session_state["input_source"] = input_source

with tab_upload:
    uploaded_file = st.file_uploader("Upload a TXT or CSV file", type=["txt", "csv"])
    csv_column = None
    if uploaded_file is not None:
        if uploaded_file.name.lower().endswith(".txt"):
            file_text = uploaded_file.getvalue().decode("utf-8", errors="replace")
            st.text_area("File preview", file_text[:1500], height=120, disabled=True)
            if st.button("Analyze TXT file", type="primary"):
                messages = [line.strip() for line in file_text.splitlines() if line.strip()]
                if messages:
                    st.session_state["messages_to_analyze"] = messages
                    st.session_state["input_source"] = uploaded_file.name
                else:
                    st.warning("The TXT file contains no messages.")
        else:
            try:
                uploaded_df = pd.read_csv(uploaded_file)
                st.write("CSV preview", uploaded_df.head())
                csv_column = st.selectbox("Choose the column containing chat messages", uploaded_df.columns)
                if st.button("Analyze CSV file", type="primary"):
                    messages = uploaded_df[csv_column].dropna().astype(str).tolist()
                    if messages:
                        st.session_state["messages_to_analyze"] = messages
                        st.session_state["input_source"] = uploaded_file.name
                    else:
                        st.warning("The selected column contains no messages.")
            except Exception as exc:
                st.error(f"Could not read the CSV file: {exc}")

with tab_demo:
    st.write("Use this sample conversation to test the dashboard.")
    sample = [
        "Customer: My order hasn't arrived yet. I've been waiting for five days!",
        "Customer: I'm really frustrated. Can someone help me?",
        "Agent: I'm sorry for the delay. Your order will arrive tomorrow.",
        "Customer: Thank you for checking. I appreciate your help.",
    ]
    st.code("\n".join(sample))
    if st.button("Analyze sample conversation", type="primary"):
        st.session_state["messages_to_analyze"] = sample
        st.session_state["input_source"] = "sample conversation"


if "messages_to_analyze" in st.session_state:
    messages = st.session_state["messages_to_analyze"]
    results = analyze_messages(messages)

    st.divider()
    st.header("Analysis dashboard")
    st.caption(f"Source: {st.session_state.get('input_source', 'chat')}")

    if results.empty:
        st.warning("No valid messages were found.")
    else:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Messages analyzed", len(results))
        col2.metric("Unique intents", results["Intent"].nunique())
        col3.metric("Most common emotion", results["Emotion"].mode().iloc[0])
        col4.metric("Average words/message", round(results["Word Count"].mean(), 1))

        st.subheader("Conversation summary")
        st.markdown(make_summary(results["Message"].tolist(), results))

        left, right = st.columns(2)
        with left:
            intent_counts = results["Intent"].value_counts().rename_axis("Intent").reset_index(name="Count")
            fig_intent = px.bar(intent_counts, x="Intent", y="Count", title="Intent distribution", text="Count")
            fig_intent.update_layout(xaxis_tickangle=-25)
            st.plotly_chart(fig_intent, use_container_width=True)
        with right:
            emotion_counts = results["Emotion"].value_counts().rename_axis("Emotion").reset_index(name="Count")
            fig_emotion = px.pie(emotion_counts, names="Emotion", values="Count", title="Emotion distribution", hole=0.35)
            st.plotly_chart(fig_emotion, use_container_width=True)

        st.subheader("Message-by-message analysis")
        st.dataframe(results, use_container_width=True, hide_index=True)

        csv_data = results.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download analysis as CSV",
            data=csv_data,
            file_name="chat_analysis_results.csv",
            mime="text/csv",
        )

        st.info(
            "Interpretation caution: this starter version uses keyword matching. "
            "It can miss sarcasm, context, negation, mixed emotions, and indirect intent. "
            "Use it as a demonstration prototype, not as a definitive assessment of a person."
        )
