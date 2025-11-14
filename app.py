import streamlit as st
from backend.fetcher import extract_article_from_url
from backend.cleaner import clean_text
from backend.summarizer import summarize_text
from dotenv import load_dotenv
load_dotenv()


st.set_page_config(page_title="AI News Summarizer", layout="centered")

st.title("📰 AI News Summarizer")
st.write("Paste a news article link and choose your summary style.")

url = st.text_input("Enter News Article URL:")

summary_type = st.selectbox(
    "Select Summary Type:",
    ["Layman (kid-friendly)", "Technical (professional)"]
)

if st.button("Generate Summary"):
    if not url:
        st.error("Please enter a valid URL.")
    else:
        with st.spinner("Fetching article..."):
            original_article = extract_article_from_url(url)

        if original_article is None or len(original_article.strip()) < 50:
            st.error("Could not extract valid article text. Try another link.")
        else:
            st.success("Article fetched!")

            with st.spinner("Cleaning article text..."):
                cleaned_article = clean_text(original_article)

            with st.spinner("Summarizing with LLaMA..."):
                summary = summarize_text(cleaned_article, summary_type)

            st.subheader("📝 Summary:")
            st.write(summary)
