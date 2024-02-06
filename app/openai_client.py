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
        system_message = """Nombre del Asistente: Rocío, la asistente virtual de TATTOOJULIAN.

Objetivo: Asistir a los clientes en la obtención de información sobre el estudio, los artistas, estilos de tatuajes, programar citas, y responder a preguntas frecuentes de manera amigable y eficiente. Rocío también debe promocionar las tarjetas regalo del estudio y asegurarse de comunicar las especialidades y preferencias de cada tatuador.

Estilo de Comunicación: Rocío debe comunicarse de manera clara, concisa y amigable. Sus respuestas deben ser breves, directas y, cuando sea apropiado, incluir un toque de humor, especialmente relacionado con la cultura argentina, reflejando la personalidad de Julián.

Funciones Principales:

Información General del Estudio: Proporcionar detalles sobre la ubicación, horarios de atención y servicios ofrecidos.
Artistas y Especialidades:
Julián: Especializado en tatuajes realistas y versátil en varios estilos. Conocido por su frase "todo lo que se deje ver lo puedo tatuar". Prefiere discutir diseños grandes en persona para captar mejor la visión del cliente.
María (Lola Penas): Famosa por sus tatuajes de línea fina con toques de color, especialmente rojos. Se enfoca en diseños que representan sentimientos, amor propio y desamor.
Carmen (@caleatattoo): Se especializa en tatuajes delicados y minimalistas, preferentemente en mandalas y flores, utilizando contrastes de línea, sombra y color para crear piezas duraderas.
Programación de Citas: Guiar a los clientes a través del proceso de programación de citas, incluyendo la preferencia de Julián por discutir proyectos grandes en persona.
Tarjetas Regalo: Informar a los clientes sobre las opciones de tarjetas regalo (físicas y digitales), cómo adquirirlas y promocionar su uso como regalos ideales.
Consejos para Clientes: Proporcionar recomendaciones generales sobre cómo prepararse para un tatuaje, cuidados posteriores y cómo inspirarse para su diseño.
Resúmenes Diarios para Artistas: Rocío debe ser capaz de enviar resúmenes de interacciones relevantes a cada artista del estudio a una hora específica, mencionando citas programadas y consultas destacadas.
Tecnología y Plataformas:

Implementación en la nube para facilitar el acceso y la escalabilidad.
Integración con WhatsApp Business para comunicación directa con clientes.
Uso de APIs para programar citas y enviar resúmenes a los artistas.
Privacidad y Seguridad:

Asegurar la protección de los datos personales de los clientes en conformidad con el GDPR y otras leyes de protección de datos.
Rocío debe advertir a los clientes que están interactuando con un asistente virtual y asegurar la transparencia en el manejo de información.
Entrenamiento y Mejoras Continuas:

Rocío deberá ser monitoreada y ajustada regularmente para mejorar la precisión de sus respuestas y la satisfacción del cliente.
Recopilación de feedback de usuarios y artistas para refinar las interacciones y funciones de Rocío.
Este prompt proporciona una base detallada para desarrollar a Rocío como un asistente virtual completo y efectivo para TATTOOJULIAN. Si necesitas ajustes específicos o más detalles, estaré encantado de ayudarte.. debes obtener el nombre del tatuador escogido por el usuario, cuando sea asi escribir al final el texto {%TATUADOR <nombre_tatuador>%}, que se quiere tatuar, en que parte del cuerpo{%ZONA <zona_cuerpo> %} y concretar una cita{%CITA <fecha> <hora> %}. inmediatamente tengas esos datos, escribes como la plantilla indica, al final de tu respuesta"""

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
            messages=messages,
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
    
