document.addEventListener("DOMContentLoaded", function () {
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");
    const messageBox = document.getElementById("message-box");
    const API_URL = "/nlp/process_chat/";

    // Get CSRF token from cookies
    const csrfToken = getCookie("csrftoken");

    // Trigger sendMessage when the button is clicked
    sendButton.onclick = sendMessage;

    // Trigger sendMessage when the Enter key is pressed
    messageInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Prevent default form submission
            sendMessage();
        }
    });

    function sendMessage() {
        // Sanitize input to prevent script injection
        const userMessage = messageInput.value.replace(/<[^>]*>?/gm, "").trim();

        if (userMessage.length > 0) {
            sendButton.disabled = true;  // Disable send button
            sendButton.innerHTML = "Sending...";  // Optional visual feedback

            // Add user's message to the chat
            addMessageToChat(userMessage, userImage, "message");
            messageInput.value = ""; // Clear input field

            const responsePlaceholder = addMessageToChat("...", chatbotImage, "response");

            // Send message to the server
            fetch(API_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({ message: userMessage })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Server error: " + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                updateChatBotResponse(responsePlaceholder, data);
            })
            .catch(error => {
                updateChatBotResponse(responsePlaceholder, "Oops! An error occurred. Please try again.");
                console.error("Error:", error);
            })
            .finally(() => {
                sendButton.disabled = false;  // Re-enable send button
                sendButton.innerHTML = "Send";  // Restore button text
            });
        } else {
            alert("Message cannot be empty.");  // Client-side validation for empty input
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

        const timestamp = document.createElement("span");
        timestamp.className = "timestamp";
        timestamp.textContent = new Date().toLocaleTimeString();
        messageElement.appendChild(timestamp);

        messageBox.appendChild(messageElement);
        messageBox.scrollTop = messageBox.scrollHeight;

        return textElement;
    }

    function updateChatBotResponse(element, data) {
        if (typeof data === "string") {
            element.innerHTML = data;
        } else if (data.recipes && data.recipes.length > 0) {
            // Display recipes
            element.innerHTML = "Recipes: " + data.recipes.map(recipe => recipe.name).join(", ");
            
            // Show created tags (if any)
            if (data.created_tags && data.created_tags.length > 0) {
                element.innerHTML += "<br><strong>Created Tags:</strong> " + data.created_tags.join(", ");
            }
        } else {
            element.innerHTML = "No matching recipes found.";
        }
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
