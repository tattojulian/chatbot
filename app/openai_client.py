import os
from openai import OpenAI
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage
oclient = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

#db = TinyDB(db_location='tmp', in_memory=False)
db = TinyDB(storage=MemoryStorage)

class OpenAIClient:
    def __init__(self):
        print("\nopenai key is" + oclient.api_key)

    def complete(self, prompt, phone_number):
        # Retrieve the last 10 interactions from the database for the given phone number.
        previous_conversation=None
        try:
            all_conversations = db.read_list_record("conversations", phone_number, default=[])
            last_5_conversations = all_conversations[-10:]
            # Format the previous conversations to provide context to the GPT model.
            previous_conversation = "\n".join(
            [f'User: {conv["user_message"]}\nAssistant: {conv["gpt_response"]}' for conv in last_5_conversations])
        except:
            pass
        # System message providing guidelines and context to the GPT model.
        system_message = """Eres un asistente virtual de un estudio de tatuajes en la ciudad de Zaragoza españa. se llama tattoojulian studio, en dicho studio tatuan Julian, cuyo estilo es realista, chechu que su estilo es old school, tu vas a atender los mensajes que recibamos desde whatsapp, te agregare contexto de acuerdo a las conversaciones que hayas tenido con el usuario. Tus objetivos como agente, son que el usuario aparte una cita con uno de nuestros tatuadores, y, que cuando detectes que el usuario quiere una cita, retornes al final del texto de tu respuesta quiere cita "#{%QUIERE_CITA%}. debes obtener el nombre del tatuador, cuando sea asi escribir al final el texto {%TATUADOR <nombre_tatuador>%}, que se quiere tatuar, en que parte del cuerpo{%ZONA <zona_cuerpo> %} y concretar una cita{%CITA <fecha> <hora> %}. inmediatamente tengas esos datos, escribes como la plantilla indica, al final de tu respuesta"""

        messages = [
            {"role": "system", "content": system_message}]

        # Append the previous conversation to the system  message for context,
        if previous_conversation:
            messages.append({"content":f"\n\nHere are the five previous user messages and chatbot responses for context:\n\n{previous_conversation}"})
        messages.append({
            "role": "user",
            "content": prompt})
        print(messages)
        response = oclient.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": messages,
                }
            ],
            model="gpt-3.5-turbo",
        )
        print(response)
        generated_response = response.choices[0].message.content

        new_conversation = {
            "user_message": prompt,
            "gpt_response": generated_response}
        groups = db.table('conversations')
        db.insert({ 'phone_number': phone_number, 'text':new_conversation})
        print("response form openai is :\n" + str(response) + "\n")
        return generated_response


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
    print(response)
    
