import streamlit as st
import pandas as pd

from vader import SentimentIntensityAnalyzer

st.title("VADER Playground")
text = st.text_input("Enter your text here")

if text:
    analyzer = SentimentIntensityAnalyzer()
    (score, analysis) = analyzer.polarity_scores(text)
    st.write(score)

    st.subheader("Detailed analysis")

    for name, content in analysis:
        if type(content) is list:
            st.markdown(f"**{name}**")
            df = pd.DataFrame(content, columns=["word", "score"])
            st.table(df.transpose())
        else:
            st.markdown(f"**{name}**: {content}")


# lan = st.selectbox("Select the language", ["English", "Portuguese"])
