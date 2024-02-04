import os
from openai import OpenAI

oclient = OpenAI(api_key='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')#os.environ.get("OPENAI_API_KEY"))

class OpenAIClient:
    def __init__(self):
        print("\nopenai key is" + oclient.api_key )

    def complete(self, prompt):
        response = oclient.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
        )

        print("response form openai is :\n" + str(response) + "\n")
        return response.choices[0].message.content

# class OpenAIClient:
#     def __init__(self):
#         pass
#         #print("\nopenai key is" + client.api_key )

#     def complete(self, prompt):
#         response = client.chat.completions.create(
#             messages=[
#                 {
#                     "role": "user",
#                     "content": prompt,
#                 }
#             ],
#             model="gpt-3.5-turbo",
            
#         prompt=prompt,
#         temperature=0.0,
#         max_tokens=256,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0
#         )

#         print("response form openai is :\n" + str(response) + "\n")
#         return response.choices[0].message.content
# class OpenAIClient:
#     def __init__(self):
#         pass
#         # sprint ("\nopenai key is" + openai.api_key + " and its type is " + openai.api_type)

#     def complete(self, prompt):
#         response = client.completions.create(model="text-davinci-003",
#         prompt=prompt,
#         temperature=0.0,
#         max_tokens=256,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0)

#         print ("response form openai is :\n" + str(response) + "\n")
#         return response.choices[0].text

if __name__ == "__main__":
    client = OpenAIClient()
    response = client.complete("how are you")
    print (response)
    