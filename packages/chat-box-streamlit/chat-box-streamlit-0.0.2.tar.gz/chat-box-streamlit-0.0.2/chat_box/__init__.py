import os
import pandas as pd
import numpy as np

import streamlit as st
import streamlit.components.v1 as components


_RELEASE = False

if not _RELEASE:
    _chat_box = components.declare_component(
        "chat_box_streamlit",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _chat_box = components.declare_component("chat_box_streamlit", path=build_dir)


def display_chat(component="", isLeft=True, message="", placeholder="Enter your input",height=500, rows=1):
    return _chat_box(component=component, isLeft=isLeft, message=message, placeholder=placeholder, rows=rows, height=height)


if not _RELEASE:
    st.set_page_config(page_title="ChatBox Demo", page_icon=":speech_balloon:")
    st.markdown("## Streamlit ChatBox Demo 💬")
    st.markdown("### Input Box")
    response = display_chat(component="input", placeholder="This is input component", rows=1)
    st.write(response)
    st.markdown("### Left message")
    display_chat(component="message", isLeft=True, message="Hi, i am left message component")
    st.markdown("### Right message")
    display_chat(component="message", isLeft=False, message="Hello, i am right message component")
    st.markdown("### Complete Chat Component")
    response = display_chat(message=["What is your name?", "I am chat component", "How are you different from others ?", "I am a complete chat box with scroll"], placeholder="Enter you input", height=600)
    st.write(response)
