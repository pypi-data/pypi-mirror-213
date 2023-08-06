# Streamlit Chat Box 📨

Streamlit Chat Box is a custom chat component built for Streamlit using React, TypeScript, and Styled Components. This project allows you to easily integrate a chat box into your Streamlit applications, enabling interactive and engaging user experiences.

## Features 🌟
- Real-time chat functionality
- Customizable UI with styled components
- Easy integration with Streamlit applications
- Supports sending and receiving messages
- Loading indicator for real-time feedback [Work in Progress...]

## Installation ⚙️
To use the Streamlit Chat Box in your Streamlit application, you need to follow these steps:

1. Install the necessary dependencies by running the following command:
```
pip install chat-box-streamlit
```

2. Import the ChatBox component in your Streamlit application:
```
from chat-box-streamlit import display_chat
```

## How to use 

1. Input Box
![Input Box](./assets/Input-Box.png)
To display an input box where users can enter their messages, use the following code:
```python
response = display_chat(component="input", placeholder="This is the input component", rows=1)
st.write(response)
```

2. Left and Right Messages
![Left and Right Messages](./assets/Message.png)
You can display messages on the left or right side of the chatbox using the message component. Set isLeft parameter to True for a left message and False for a right message.
```
display_chat(component="message", isLeft=True, message="Hi, I am the left message component")
display_chat(component="message", isLeft=False, message="Hello, I am the right message component")
```

3. Complete Chat Component
![Complete Chat Component](./assets/Complete-Chat.png)
For a complete chat component with multiple messages and scrollable content, use the following code:
```python
response = display_chat(
    message=["What is your name?", "I am the chat component", "How are you different from others?", "I am a complete chat box with scroll"],
    placeholder="Enter your input",
    height=600
)
st.write(response)
```

## Enjoy Conversational UI! 🗣️💬
Feel free to experiment with different messages, components, and settings to create your unique chatbox experience. Happy coding! 💻🎉

## Contributing 🤝
Contributions to the Streamlit Chat Box project are welcome! If you encounter any issues, have suggestions for improvements, or would like to contribute new features, please open an issue or submit a pull request on the GitHub repository.


## How to Contribute 👨‍💻

Thank you for your interest in contributing to our project! We welcome contributions from the community and are grateful for any time and effort you are willing to put in.

1. Fork the repository by clicking the "Fork" button in the top right corner of the page. This will create a copy of the repository in your own GitHub account.
2. Clone the repository to your local machine using `git clone https://github.com/YOUR_USERNAME/Streamlit-Chatbox.git`.
3. Make the changes you would like to contribute. Be sure to follow the project's code style guidelines and ensure that your code is properly tested.
4. Commit your changes and push them to your forked repository using `git commit -am "YOUR_NAME: Commit message"` and `git push`.
5. Go back to the original repository and create a pull request by clicking the "New pull request" button.
6. In the pull request, make sure to describe the changes you made and why you made them.
7. Submit the pull request and wait for it to be reviewed by the project maintainers.

Thank you again for your interest in contributing to our project! We look forward to reviewing your pull request.

## Code of Conduct 🛠️

We ask that all contributors follow our code of conduct, which can be found in the [Code of Conduct](https://github.com/SSK-14/Streamlit-Chatbox/blob/main/CODE_OF_CONDUCT.md) file in the root of the repository.

## License 📄

By contributing to this project, you agree that your contributions will be licensed under the [MIT License](https://github.com/SSK-14/Streamlit-Chatbox/blob/main/LICENSE). Please make sure you understand the implications of this before making a contribution.
