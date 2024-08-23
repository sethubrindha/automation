import requests

def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")

# Example usage
bot_token = 'your_bot_token_here'
chat_id = 'your_chat_id_here'
message = 'Hello from Python!'

# send_telegram_message(bot_token, chat_id, message)



def get_telegram_messages(bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        updates = response.json()
        if 'result' in updates:
            for update in updates['result']:
                if 'message' in update:
                    chat_id = update['message']['chat']['id']
                    user = update['message']['from']['first_name']
                    message_text = update['message']['text']
                    print(f"Message from {user} (chat_id: {chat_id}): {message_text}")
        else:
            print("No messages found.")
    else:
        print(f"Failed to get updates. Status code: {response.status_code}")

# Example usage
bot_token = 'your_bot_token_here'

# get_telegram_messages(bot_token)
