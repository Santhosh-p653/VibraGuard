// Function to add a message to the chat
function addMessage(text, sender) {
    const chatBody = document.getElementById('chatbot-body');
    if (!chatBody) return;

    const messageDiv = document.createElement('div');
    messageDiv.classList.add('d-flex', 'mb-2');
    
    const bubbleDiv = document.createElement('div');
    bubbleDiv.classList.add('p-2', 'rounded', 'chat-bubble', sender);
    bubbleDiv.textContent = text;
    
    if (sender === 'user') {
        messageDiv.classList.add('justify-content-end');
    } else {
        messageDiv.classList.add('justify-content-start');
    }
    
    messageDiv.appendChild(bubbleDiv);
    chatBody.appendChild(messageDiv);
    
    // Scroll to the bottom of the chat
    chatBody.scrollTop = chatBody.scrollHeight;
}

// Function to handle sending the message
function handleSendMessage() {
    const chatInput = document.getElementById('chatbot-input');
    const userMessage = chatInput.value.trim().toLowerCase();
    if (userMessage === '') {
        return;
    }

    // Add user's message to the chat
    addMessage(userMessage, 'user');

    let botResponse = "";

    // Define different response options for each topic
    const responses = {
        greetings: [
            "Hello! I'm a chatbot designed by the NEURONINJAS team to help you.",
            "Hey! How can I help you today?",
            "I'm glad you're here. Can I help you find something?",
            "Are you stuck? I can help you with that."
        ],
        report: [
            "To view a report, open the menu on the left and select the specific report you need.",
            "You can access all reports from the main menu on the left. Just choose the one you want to view!",
            "Navigate to the main menu and click on the report you are looking for."
        ],
        download: [
            "To download a report, open the side menu and tap the 'Download Report' button. It will automatically download for you.",
            "Reports can be downloaded directly. Just go to the menu and click 'Download Report.'",
            "There's a 'Download Report' button in the side menu that will download a copy to your device."
        ],
        status: [
            "The system status is updated in real-time on the homepage. Please check the main dashboard to see if it's currently online.",
            "You can see the system's current status on the homepage. It will show if attendance tracking is live."
        ],
        login: [
            "This system does not require a user login. All reports and functions are accessible from the main menu.",
            "You don't need to log in to use this system. All features are publicly accessible from the menu."
        ],
        contact: [
            "You can find our contact information on the 'Reference and Contact' page in the main menu.",
            "For contact details, please visit the 'Reference and Contact' page from the main menu."
        ],
        who: [
            "I'm a virtual assistant designed by the NEURONINJAS team to help you navigate this attendance report system.",
            "I'm a chatbot designed to assist with questions about this system. I was created by the NEURONINJAS team."
        ],
        features: [
            "This system is designed to provide attendance reports for students, teachers, and classes, as well as general analytics.",
            "The main features are attendance reporting for individuals and classes, and a page for general attendance analytics."
        ],
        data: [
            "All attendance data is updated in real-time. The reports reflect the most current information available.",
            "The reports use live, real-time data to give you the most accurate information on attendance."
        ],
        bug: [
            "If you are experiencing a technical issue, please use the contact page to report the bug. We will address it as soon as possible.",
            "Please report any bugs or issues you encounter via the contact page. We appreciate your feedback!"
        ],
        default: [
            "I'm not sure I understand your question. Please try rephrasing it or ask about a specific report or feature.",
            "My apologies, I am a simple bot and can only answer questions related to the provided reports and navigation.",
            "I can't answer that. Could you ask about a different topic, like reports or system status?"
        ]
    };

    // Keyword-based response logic
    if (userMessage.includes('hi') || userMessage.includes('hello') || userMessage.includes('hey')) {
        botResponse = responses.greetings[Math.floor(Math.random() * responses.greetings.length)];
    } else if (userMessage.includes('report') || userMessage.includes('student') || userMessage.includes('class') || userMessage.includes('teacher') || userMessage.includes('analytics')) {
        botResponse = responses.report[Math.floor(Math.random() * responses.report.length)];
    } else if (userMessage.includes('download') || userMessage.includes('save') || userMessage.includes('get')) {
        botResponse = responses.download[Math.floor(Math.random() * responses.download.length)];
    } else if (userMessage.includes('status') || userMessage.includes('online') || userMessage.includes('working')) {
        botResponse = responses.status[Math.floor(Math.random() * responses.status.length)];
    } else if (userMessage.includes('login') || userMessage.includes('account') || userMessage.includes('password')) {
        botResponse = responses.login[Math.floor(Math.random() * responses.login.length)];
    } else if (userMessage.includes('contact') || userMessage.includes('help') || userMessage.includes('team')) {
        botResponse = responses.contact[Math.floor(Math.random() * responses.contact.length)];
    } else if (userMessage.includes('who') || userMessage.includes('what are')) {
        botResponse = responses.who[Math.floor(Math.random() * responses.who.length)];
    } else if (userMessage.includes('features') || userMessage.includes('functions') || userMessage.includes('purpose') || userMessage.includes('use')) {
        botResponse = responses.features[Math.floor(Math.random() * responses.features.length)];
    } else if (userMessage.includes('live') || userMessage.includes('updated') || userMessage.includes('real-time') || userMessage.includes('data')) {
        botResponse = responses.data[Math.floor(Math.random() * responses.data.length)];
    } else if (userMessage.includes('bug') || userMessage.includes('error') || userMessage.includes('issue') || userMessage.includes('problem') || userMessage.includes('broken')) {
        botResponse = responses.bug[Math.floor(Math.random() * responses.bug.length)];
    } else {
        botResponse = responses.default[Math.floor(Math.random() * responses.default.length)];
    }

    // Simulate a response from the AI after a slight delay
    setTimeout(() => {
        addMessage(botResponse, 'ai');
    }, 1000);

    // Clear the input field
    chatInput.value = '';
}

// Initialize the chatbot listeners
function initChatbot() {
    const chatInput = document.getElementById('chatbot-input');
    const chatSendBtn = document.getElementById('chatbot-send-btn');
    
    if (chatInput && chatSendBtn) {
        chatSendBtn.addEventListener('click', handleSendMessage);
        
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                handleSendMessage();
            }
        });
    }
}

export { initChatbot };
