# Mini-Agent
Entry-level agent practice project

This is an Entry-level project for me to practice my skills of agent development. I am trying to learn how AI Agent work and the difference between traditional language models and AI Agents.
To make the project simple and easy, I avoid complex structure and unnecessary features. This project focuses on a single function, which gives accurate answer when users ask questions 
about an unfamiliar project. For example, user may ask about how to start the project and what functions does the project use when it is running, Then Mini-agent will search the project's directory,
 list directory contents and generate a final response. The agent decides which actions to take based on the available information.


Notice: Deepseek API has been used in this projecct. If you want to use other API, like open ai API or claude API, you can update API configuration in .env

A serious issue has to be mentioned: Deepseek can not support contextual understanding with single API key so we have to send history everytime.If use Responses sort format, we can add previous_response_id to avoid this issue. I provide non-history version in branch "test" and provide history-based version in branch "main".