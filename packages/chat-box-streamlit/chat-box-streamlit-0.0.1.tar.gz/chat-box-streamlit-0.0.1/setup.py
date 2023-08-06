import setuptools

setuptools.setup(
    name="chat-box-streamlit",
    version="0.0.1",
    author="SSK-14",
    author_email="sanjaykumar1481999@gmail.com",
    description="Seamlessly visualize engaging conversations in a sleek ChatBox.",
    long_description="ChatBox is a powerful Streamlit component designed to effortlessly display and showcase interactive chat conversations between users. With its seamless integration with Streamlit, ChatBox offers a sleek and intuitive interface for visualizing dynamic dialogues, making it an ideal solution for chatbots, virtual assistants, and interactive conversational applications.",
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        "streamlit >= 0.63",
    ],
)
