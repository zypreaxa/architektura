document.addEventListener("DOMContentLoaded", function () {
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");
    const messageBox = document.getElementById("message-box");
    const API_URL = "/nlp/process_chat/";

    // Trigger sendMessage when the button is clicked
    sendButton.onclick = sendMessage;

    // Trigger sendMessage when the Enter key is pressed
    messageInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") { //padaryti serverside patikrinima del tusciu inputu
            event.preventDefault(); // Prevent default form submission
            sendMessage();
        }
    });

    function sendMessage() {
        const userMessage = messageInput.value.trim();
        if (userMessage.length > 0) {
            // Add user's message to the chat
            addMessageToChat(userMessage, userImage, "message");
            messageInput.value = ""; // Clear input field

            const responsePlaceholder = addMessageToChat("...", chatbotImage, "response");

            // Send message to the server
            fetch(API_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken  // Ensure CSRF token is passed in headers
                },
                body: JSON.stringify({ message: userMessage })
            })
            .then(response => response.json())
            .then(data => {
                // Update the response placeholder with the actual response
                updateChatBotResponse(responsePlaceholder, data);
            })
            .catch(error => {
                updateChatBotResponse(responsePlaceholder, "Oops! An error occurred. Please try again.");
                console.error("Error:", error);
            });
        }
    }

    function addMessageToChat(text, imgSrc, className) {
        const messageElement = document.createElement("div");
        messageElement.className = `chat ${className}`;

        const imageElement = document.createElement("img");
        imageElement.src = imgSrc;
        messageElement.appendChild(imageElement);

        const textElement = document.createElement("span");
        textElement.innerHTML = text;
        messageElement.appendChild(textElement);

        messageBox.appendChild(messageElement);
        messageBox.scrollTop = messageBox.scrollHeight;

        return textElement;
    }

    function updateChatBotResponse(element, data) {
        if (typeof data === "string") {
            element.innerHTML = data;
        } else if (data.recipes && data.recipes.length > 0) {
            element.innerHTML = data.recipes.map(recipe => recipe.name).join(", ");
        } else {
            element.innerHTML = "No matching recipes found.";
        }
    }
});
