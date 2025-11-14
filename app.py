import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from backend.fetcher import extract_article_from_url
from backend.cleaner import clean_text
from backend.summarizer import summarize_text

# Page configuration
st.set_page_config(
    page_title="AI News Summarizer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for improved UI - DARK SUMMARY CONTAINER
st.markdown("""
    <style>
    .main {
        padding-top: 0rem;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
    }
    .summary-container {
        background-color: #1a1a1a;
        color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        border: 2px solid #333333;
    }
    .summary-container h3 {
        color: #ffffff;
        margin-top: 0;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #1976d2;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("📰 AI News Summarizer")
st.markdown("---")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Settings")
    
    summary_length = st.radio(
        "📏 Summary Length:",
        options=["Concise (Bullet Points)", "Detailed (Full Text)"],
        help="Choose how you want your summary formatted"
    )
    
    summary_style = st.selectbox(
        "🎯 Summary Style:",
        options=["Simple (Layman)", "Technical (Professional)"],
        help="Select the complexity level and tone of the summary"
    )
    
    st.divider()
    st.markdown("""
    **ℹ️ How to use:**
    1. Paste a news article URL
    2. Select your preferred summary style
    3. Choose summary length
    4. Click "Generate Summary"
    """)

# Main content area
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### 🔗 Enter Article URL")
    url = st.text_input(
        "Paste the URL of the news article you want to summarize:",
        placeholder="https://example.com/news-article",
        label_visibility="collapsed"
    )

# Generate button
if st.button("✨ Generate Summary", use_container_width=True, type="primary"):
    if not url:
        st.error("❌ Please enter a valid URL before proceeding.")
    else:
        # Article extraction phase
        with st.spinner("🔄 Fetching article..."):
            original_text = extract_article_from_url(url)
        
        if not original_text:
            st.error("❌ Failed to extract text from the provided URL. Please try another article or check the URL.")
        else:
            st.success("✅ Article extracted successfully!")
            
            # Display article preview
            with st.expander("📖 Article Preview (First 300 characters)"):
                preview_text = original_text[:300] + "..." if len(original_text) > 300 else original_text
                st.write(preview_text)
            
            # Prepare summary parameters
            cleaned_text = clean_text(original_text)
            
            # Generate summary with selected options
            with st.spinner("🤖 Generating summary..."):
                summary = summarize_text(
                    original_text,
                    summary_style,
                    summary_length
                )
            
            # Display results
            st.divider()
            
            # Create summary container with styling - DARK BACKGROUND
            st.markdown("""
            <div class="summary-container">
            <h3>📝 Summary</h3>
            """, unsafe_allow_html=True)
            
            st.write(summary)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Additional actions
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📋 Copy to Clipboard", use_container_width=True):
                    st.info("💡 Tip: Use your browser's copy function to copy the summary above.")
            
            with col2:
                if st.button("🔄 Generate Another", use_container_width=True):
                    st.rerun()
            
            # Display metadata
            st.divider()
            with st.expander("📊 Summary Details"):
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Original Length", f"{len(original_text)} chars")
                with col_b:
                    st.metric("Summary Length", f"{len(summary)} chars")
                with col_c:
                    compression_ratio = round((1 - len(summary) / len(original_text)) * 100, 1)
                    st.metric("Compression", f"{compression_ratio}%")