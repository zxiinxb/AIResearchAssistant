import streamlit as st
from langgraph.types import Command
from main import app, config

st.set_page_config(page_title="AI Research Assistant", layout="wide")

st.title("📚 AI Research Assistant")

if "interrupt" not in st.session_state:
    st.session_state.interrupt = None

if "waiting" not in st.session_state:
    st.session_state.waiting = False

query = st.text_input("Enter your research query")

if st.button("Search Papers"):

    result = app.invoke(
        {
            "query": query,
            "topic": query
        },
        config=config
    )

    if "__interrupt__" in result:

        st.session_state.interrupt = result
        st.session_state.waiting = True

    else:

        st.error("Graph did not interrupt.")

if st.session_state.waiting:

    interrupt = st.session_state.interrupt["__interrupt__"][0]

    papers = interrupt.value["papers"]

    st.subheader("Select Papers")

    selected = []

    for paper in papers:

        if st.checkbox(
            f"{paper['index']}. {paper['title']}"
        ):
            selected.append(paper["index"])

    if st.button("Analyze Selected Papers"):

        result = app.invoke(
            Command(
                resume={
                    "selected_papers": selected
                }
            ),
            config=config
        )

        st.session_state.waiting = False

        st.success("Analysis Complete")

        st.header("Answer")
        st.write(result["answer"])

        st.header("Summary")
        st.write(result["summary"])

        st.header("Research Gaps")
        st.write(result["gaps"])

        st.header("Literature Review")
        st.write(result["review"])