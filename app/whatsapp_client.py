import os
import requests
import json
import logging


# from dotenv import load_dotenv
# load_dotenv()

class WhatsAppClient:
    API_URL = "https://graph.facebook.com/v18.0/"
    WHATSAPP_API_TOKEN = os.environ.get("WHATSAPP_API_TOKEN")
    WHATSAPP_CLOUD_NUMBER_ID = os.environ.get("WHATSAPP_CLOUD_NUMBER_ID")

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {self.WHATSAPP_API_TOKEN}",
            "Content-Type": "application/json",
        }
        self.API_URL = self.API_URL + self.WHATSAPP_CLOUD_NUMBER_ID

    def send_template_message(self, template_name, language_code, phone_number):

        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                }
            }
        }

        response = requests.post(f"{self.API_URL}/messages", json=payload, headers=self.headers)

        assert response.status_code == 200, "Error sending message"

        return response.status_code

    def send_text_message(self, body_mess, phone_number):

        try:
            # Maximum length allowed fop a single message.
            MAX_MESSAGE_LENGTH = 550
            # Split the message into chunks.
            lines = body_mess.split('\n')
            chunks = []
            current_chunk = ""
            # Iterate over each line in the message.
            for line in lines:
                words = line.split()
                for word in words:
                    #	If adding another word exceeds the max length, save the current chunk
                    if len(current_chunk) + len(word) + 1 > MAX_MESSAGE_LENGTH:
                        chunks.append(current_chunk.strip())
                        current_chunk = ""
                    current_chunk += word + " "
                # Add a newline character at the end of each line.
                current_chunk += "\n"
            if current_chunk:
                chunks.append(current_chunk.strip())

            total_chunks = len(chunks)
            # Send each chunk as a separate message.
            for i, chunk in enumerate(chunks):
                # Adding a part number to each message chunk for better readability.
                part_number = f"[{i + 1}/{total_chunks}]"
                final_chunk = f"{chunk} {part_number if total_chunks > 1 else ''}"
                payload = {
                    "messaging_product": 'whatsapp',
                    "to": phone_number,
                    "type": "text",
                    "text": {
                        "preview_url": False,
                        "body": final_chunk
                    }
                }
                response = requests.post(f"{self.API_URL}/messages", json=payload, headers=self.headers)
                print(response.status_code)
                print(response.text)
                assert response.status_code != 200, "Error sending message"
                return response.status_code
        except Exception as e:

            logging.error(f"Failed to send message. Error: {str(e)}")

    def process_notification(self, data):
        entries = data["entry"]
        for entry in entries:
            for change in entry["changes"]:
                value = change["value"]
                if value:
                    if "messages" in value:
                        for message in value["messages"]:
                            if message["type"] == "text":
                                from_no = message["from"]
                                message_body = message["text"]["body"]
                                prompt = message_body
                                print(f"Ack from FastAPI-WtsApp Webhook: {message_body}")
                                return {
                                    "statusCode": 200,
                                    "body": prompt,
                                    "from_no": from_no,
                                    "isBase64Encoded": False
                                }

        return {
            "statusCode": 403,
            "body": json.dumps("Unsupported method"),
            "isBase64Encoded": False
        }


if __name__ == "__main__":
    client = WhatsAppClient()
    # send a template message
    client.send_template_message("hello_world", "en_US", "201012345678")

    def process_notification(self, data):
        print(str(data))
        entries = data["entry"]
        for entry in entries:
            for change in entry["changes"]:
                value = change["value"]
                if value:
                    if "messages" in value:
                        for message in value["messages"]:
                            if message["type"] == "text":
                                from_no = message["from"]
                                message_body = message["text"]["body"]
                                prompt = message_body
                                print(f"Ack from FastAPI-WtsApp Webhook: {message_body}")
                                return {
                                    "statusCode": 200,
                                    "body": prompt,
                                    "from_no": from_no,
                                    "isBase64Encoded": False
                                }

        return {
            "statusCode": 403,
            "body": json.dumps("Unsupported method"),
            "isBase64Encoded": False
        }



if __name__ == "__main__":
    client = WhatsAppClient()
    # send a template message
    client.send_template_message("hello_world", "en_US", "201012345678")
    
    
    
