import setuptools
from pathlib import Path


setuptools.setup(
    name="chat-box-streamlit",
    version="0.0.3",
    author="SSK-14",
    author_email="sanjaykumar1481999@gmail.com",
    description="Seamlessly visualize engaging conversations in a sleek ChatBox.",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/SSK-14/Streamlit-Chatbox",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        "streamlit >= 0.63",
    ],
)
