from openai import OpenAI

client = OpenAI(api_key="sk-proj-fXyZ7Kt7BHfuQJuZUK08T3BlbkFJPrQVldQY9Wld5JdoQkb4")

# stream = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[{"role": "user", "content": "Say this is a test"}],
#     stream=True,
# )
# for chunk in stream:
#     if chunk.choices[0].delta.content is not None:
        # print(chunk.choices[0].delta.content, end="")

chatHistory = []

chatHistory.append({"role": "system", "content": "Say this is a test"})

while True:
    user_input = input("\nUser: ")
    chatHistory.append({"role": "user", "content": user_input})
    if user_input.lower() == "stop":
        break
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chatHistory,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
            chatHistory.append({"role": "system", "content": chunk.choices[0].delta.content})
