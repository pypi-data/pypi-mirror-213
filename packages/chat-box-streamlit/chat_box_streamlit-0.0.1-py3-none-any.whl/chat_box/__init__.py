import os

import streamlit as st
import streamlit.components.v1 as components


_RELEASE = False

if not _RELEASE:
    _chat_box = components.declare_component(
        "chat_box",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _chat_box = components.declare_component("chat_box", path=build_dir)


def custom_chat_box(left_message, right_message, height=500):
    return _chat_box(leftMessage=left_message, rightMessage=right_message, height=height)


if not _RELEASE:
    custom_chat_box(
        left_message=["What is your name?", "How old are you?", "Thank you"],
        right_message=["My name is John", "I am 25 years old", "You are welcome"],
        height=500,
    )
