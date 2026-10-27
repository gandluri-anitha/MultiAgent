
import json
import streamlit as st

from src.pipelines.pipeline import run_research_pipeline

# ---------------- Page configuration ----------------
st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- Custom styling ----------------
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    .hero {
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(128,128,128,0.3);
        margin-bottom: 1.5rem;
    }
    .subtle {
        color: #777;
        font-size: 0.95rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- Helper ----------------
def to_text(value):
    """Convert strings, LangChain messages, or dictionaries to displayable text."""
    if value is None:
        return "No content returned."

    if hasattr(value, "content"):
        value = value.content

    if isinstance(value, (dict, list)):
        return json.dumps(value, indent=2, ensure_ascii=False, default=str)

    return str(value)


# ---------------- Sidebar ----------------
with st.sidebar:
    st.title("🔬 Research Studio")
    st.caption("Powered by your multi-agent pipeline")
    st.divider()

    st.markdown("### Pipeline")
    st.markdown("1. 🔎 Search Agent")
    st.markdown("2. 📖 Reader Agent")
    st.markdown("3. ✍️ Writer Chain")
    st.markdown("4. ✅ Critic Chain")

    st.divider()
    st.caption("Tip: Use a specific topic to get more focused research.")


# ---------------- Main page ----------------
st.markdown(
    """
    <div class="hero">
        <h1>AI Research Agent</h1>
        <p class="subtle">
            Discover information, inspect sources, draft a report,
            and review the final output using four AI stages.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("What would you like to research?")

with st.form("research_form"):
    topic = st.text_area(
        "Research topic",
        placeholder=(
            "Example: Recent breakthroughs in Generative AI "
            "and their business applications"
        ),
        height=100,
    )

    submitted = st.form_submit_button(
        "🚀 Run Research",
        type="primary",
        use_container_width=True,
    )


# ---------------- Execute pipeline ----------------
if submitted:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        try:
            with st.status(
                "Running your research pipeline...",
                expanded=True,
            ) as status:
                st.write("🔎 Searching for relevant information...")
                st.write("📖 Reading and extracting source content...")
                st.write("✍️ Drafting the research report...")
                st.write("✅ Reviewing the report...")

                result = run_research_pipeline(topic.strip())

                status.update(
                    label="Research pipeline completed!",
                    state="complete",
                    expanded=False,
                )

            # Keep results available after the script reruns.
            st.session_state["research_result"] = result
            st.session_state["research_topic"] = topic.strip()

        except Exception as exc:
            st.error(f"Research failed: {exc}")
            st.exception(exc)


# ---------------- Display results ----------------
if "research_result" in st.session_state:
    result = st.session_state["research_result"]
    saved_topic = st.session_state["research_topic"]

    st.divider()
    st.subheader("📊 Research Results")
    st.caption(f"Topic: {saved_topic}")

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Pipeline stages", "4")

    with col2:
        st.metric(
            "Search results",
            "Available" if result.get("search_results") else "Empty",
        )

    with col3:
        st.metric(
            "Scraped content",
            "Available" if result.get("scraped_content") else "Empty",
        )

    with col4:
        st.metric(
            "Critic review",
            "Available" if result.get("feedback") else "Empty",
        )

    search_tab, reader_tab, report_tab, critic_tab = st.tabs(
        [
            "🔎 Search Results",
            "📖 Source Content",
            "📝 Final Report",
            "✅ Critic Review",
        ]
    )

    with search_tab:
        st.subheader("Search Agent Output")
        st.markdown(to_text(result.get("search_results")))

    with reader_tab:
        st.subheader("Reader Agent Output")
        st.markdown(to_text(result.get("scraped_content")))

    with report_tab:
        st.subheader("Research Report")
        report_text = to_text(result.get("report"))
        st.markdown(report_text)

        st.download_button(
            label="⬇️ Download Report",
            data=report_text,
            file_name="research_report.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with critic_tab:
        st.subheader("Critic Feedback")
        st.markdown(to_text(result.get("feedback")))

    st.divider()
    st.success("Your research report is ready.")
