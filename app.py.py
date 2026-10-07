from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Simple keyword-based response logic for a Restaurant Management Chatbot
def get_bot_response(user_input):
    text = user_input.lower()
    
    if any(word in text for word in ["menu", "food", "eat", "dishes", "card"]):
        return "Our menu features Starters (Garlic Bread, Wings), Main Courses (Grilled Salmon, Margherita Pizza, Cheeseburgers), and Desserts (Tiramisu, Lava Cake). Type 'price' for details!"
    elif any(word in text for word in ["price", "cost", "rate", "how much"]):
        return "Here are some popular prices: Margherita Pizza ($14), Cheeseburger ($12), Grilled Salmon ($18), and Tiramisu ($7)."
    elif any(word in text for word in ["reserve", "book", "table", "reservation"]):
        return "To book a table, please let us know your preferred date, time, and party size (e.g., 'Table for 4 tonight at 8 PM')."
    elif any(word in text for word in ["hour", "timing", "open", "close", "time"]):
        return "We are open Monday to Sunday from 11:00 AM to 10:00 PM."
    elif any(word in text for word in ["deliver", "delivery", "order", "takeout", "take away"]):
        return "Yes, we offer home delivery and takeout! You can place an order online through our website or call us directly."
    elif any(word in text for word in ["location", "address", "where", "map"]):
        return "We are located at 456 Culinary Avenue, Downtown City."
    elif any(word in text for word in ["hi", "hello", "hey", "greetings"]):
        return "Hello and welcome to Bistro Delights! How can I assist you with your dining or reservation needs today?"
    elif any(word in text for word in ["bye", "exit", "quit", "thank"]):
        return "Thank you for chatting with Bistro Delights! Have a wonderful day and hope to see you soon!"
    else:
        return "I'm not quite sure about that. You can ask me about our menu, prices, opening hours, table reservations, or delivery options!"

# Single-page HTML template with embedded CSS and JavaScript
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Restaurant Assistant - Bistro Delights</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #fcf8f2; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .chat-container { width: 420px; background: white; border-radius: 12px; box-shadow: 0 6px 15px rgba(0,0,0,0.1); display: flex; flex-direction: column; overflow: hidden; border: 1px solid #e7d7c9; }
        .chat-header { background: #8b0000; color: white; padding: 18px; text-align: center; font-size: 19px; font-weight: bold; letter-spacing: 0.5px; }
        .chat-box { flex: 1; padding: 15px; overflow-y: auto; height: 360px; display: flex; flex-direction: column; gap: 12px; background: #fffaf5; }
        .message { padding: 10px 14px; border-radius: 14px; max-width: 75%; font-size: 14px; line-height: 1.4; }
        .user-message { background: #8b0000; color: white; align-self: flex-end; border-bottom-right-radius: 2px; }
        .bot-message { background: #f0e6dc; color: #333; align-self: flex-start; border-bottom-left-radius: 2px; }
        .chat-input-area { display: flex; border-top: 1px solid #e7d7c9; padding: 12px; background: #fff; }
        .chat-input-area input { flex: 1; padding: 10px; border: 1px solid #dcdcdc; border-radius: 6px; outline: none; font-size: 14px; }
        .chat-input-area input:focus { border-color: #8b0000; }
        .chat-input-area button { background: #8b0000; color: white; border: none; padding: 10px 16px; margin-left: 8px; border-radius: 6px; cursor: pointer; font-weight: bold; }
        .chat-input-area button:hover { background: #a30000; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">🍽️ Bistro Delights Assistant</div>
        <div class="chat-box" id="chatBox">
            <div class="message bot-message">Hello and welcome to Bistro Delights! How can I assist you with your dining or reservation needs today?</div>
        </div>
        <div class="chat-input-area">
            <input type="text" id="userInput" placeholder="Ask about menu, reservations..." onkeypress="handleKey(event)">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const inputField = document.getElementById("userInput");
            const chatBox = document.getElementById("chatBox");
            const text = inputField.value.trim();
            
            if (!text) return;

            // Append user message
            chatBox.innerHTML += `<div class="message user-message">${escapeHtml(text)}</div>`;
            inputField.value = "";
            chatBox.scrollTop = chatBox.scrollHeight;

            // Send to Flask backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            const data = await response.json();

            // Append bot response
            chatBox.innerHTML += `<div class="message bot-message">${escapeHtml(data.response)}</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function handleKey(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        function escapeHtml(text) {
            return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/chat", methods=["POST"])
def chat():
    user_data = request.get_json()
    user_message = user_data.get("message", "")
    bot_reply = get_bot_response(user_message)
    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)