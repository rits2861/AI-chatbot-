# ============================================================
# AI Powered Chatbot for Automated ITSM Using NLP
# Student: Ritika Sharma
# Enrollment No: O24MCA111878
# Guide: Vikas Kumar Atray
# University: Chandigarh University
# ============================================================

import re
import random
from datetime import datetime

# ============================================================
# KNOWLEDGE BASE - Intent Patterns and Responses
# Based on Project Report Chapter 5
# ============================================================

intents = {
    "greeting": {
        "patterns": ["hello", "hi", "hey", "good morning", "good evening", "greetings"],
        "responses": [
            "Hello! I am your IT Support Assistant. How can I help you today?",
            "Hi there! Welcome to IT Support. What issue are you facing?",
            "Hey! I am here to help with your IT issues. What do you need?"
        ]
    },

    "password_reset": {
        "patterns": ["reset password", "forgot password", "change password", 
                     "cant login", "cannot login", "password expired", 
                     "locked out", "password not working", "reset my password"],
        "responses": [
            """I can help you reset your password! Here are the steps:
            
Step 1: Go to the company login portal
Step 2: Click on 'Forgot Password'
Step 3: Enter your registered email address
Step 4: Check your email for the reset link
Step 5: Click the link and set a new password

Requirements for new password:
- Minimum 8 characters
- At least one uppercase letter
- At least one number
- At least one special character

If you still face issues, a ticket has been raised for IT team assistance."""
        ]
    },

    "vpn_issue": {
        "patterns": ["vpn not working", "vpn issue", "cannot connect vpn", 
                     "vpn disconnects", "vpn problem", "vpn error",
                     "vpn keeps disconnecting", "vpn connection failed"],
        "responses": [
            """Let me help you fix your VPN issue! Please try these steps:

Step 1: Check your internet connection first
Step 2: Disconnect and reconnect the VPN
Step 3: Restart the VPN application
Step 4: Check if your VPN credentials are correct
Step 5: Try connecting to a different VPN server

If the problem persists:
- Restart your computer and try again
- Check if VPN software needs an update

A support ticket has been automatically created for your VPN issue."""
        ]
    },

    "slow_laptop": {
        "patterns": ["laptop slow", "computer slow", "system slow", 
                     "pc is slow", "laptop hanging", "system hanging",
                     "computer not responding", "laptop freezing"],
        "responses": [
            """Here are steps to fix your slow laptop:

Step 1: Restart your computer
Step 2: Close unnecessary applications
Step 3: Clear temporary files:
        - Press Windows + R
        - Type %temp% and press Enter
        - Delete all files
Step 4: Check disk space (should have at least 10% free)
Step 5: Run antivirus scan

If problem continues, a ticket has been raised for hardware check."""
        ]
    },

    "printer_issue": {
        "patterns": ["printer not working", "printer issue", "cannot print",
                     "printer offline", "printer error", "install printer",
                     "printer not printing", "printer problem"],
        "responses": [
            """Let me help with your printer issue!

Step 1: Check if printer is turned ON and connected
Step 2: Check printer cable or WiFi connection
Step 3: On your computer:
        - Go to Settings > Devices > Printers
        - Remove the printer
        - Add printer again
Step 4: Download latest printer driver from manufacturer website
Step 5: Restart both computer and printer

A ticket has been created for IT team to assist further."""
        ]
    },

    "software_install": {
        "patterns": ["install software", "need software", "software installation",
                     "install microsoft office", "install application",
                     "software request", "need application", "install app"],
        "responses": [
            """I have raised a software installation request for you!

Your request details:
- Request Type: Software Installation
- Status: Pending Approval
- Expected Time: 24-48 hours

Note: Software installation requires manager approval.
You will receive an email confirmation shortly.

Ticket Number: TKT-{ticket_number} has been created."""
        ]
    },

    "ticket_status": {
        "patterns": ["ticket status", "check ticket", "my ticket", 
                     "what is status", "ticket update", "check my request",
                     "status of my ticket", "ticket number"],
        "responses": [
            "Please provide your ticket number and I will check the status for you.",
            "To check ticket status, please share your ticket number starting with TKT-",
            "I can help check your ticket! Please provide the ticket number."
        ]
    },

    "network_issue": {
        "patterns": ["no internet", "internet not working", "network issue",
                     "wifi not working", "wifi problem", "network down",
                     "cannot connect internet", "internet slow"],
        "responses": [
            """Let me help with your network issue!

Step 1: Check if WiFi is turned ON on your device
Step 2: Disconnect and reconnect to WiFi
Step 3: Restart your router/modem
Step 4: Forget the network and reconnect:
        - Go to WiFi Settings
        - Click on network name
        - Select Forget
        - Reconnect with password
Step 5: Check if other devices have internet

If issue persists, a network ticket has been raised for IT team."""
        ]
    },

    "email_issue": {
        "patterns": ["email not working", "outlook issue", "cannot send email",
                     "email problem", "outlook not opening", "mail issue",
                     "cannot receive email", "email error"],
        "responses": [
            """Here are steps to fix your email issue:

Step 1: Check your internet connection
Step 2: Restart Outlook application
Step 3: Check if your password has expired
Step 4: Clear Outlook cache:
        - Close Outlook
        - Press Windows + R
        - Type %localappdata%\\Microsoft\\Outlook
        - Delete .ost files
Step 5: Reopen Outlook

A ticket has been created for email support team."""
        ]
    },

    "access_request": {
        "patterns": ["need access", "access request", "permission denied",
                     "cannot access folder", "access issue", "request access",
                     "need permission", "access denied"],
        "responses": [
            """I have logged an access request for you!

To process your request I need:
1. Which system/folder do you need access to?
2. Reason for access requirement
3. Your manager name for approval

Your request has been forwarded to:
- Your manager for approval
- IT Security team for verification

Expected processing time: 24-48 hours
Ticket Number: TKT-{ticket_number} created."""
        ]
    },

    "escalate": {
        "patterns": ["talk to human", "speak to agent", "human support",
                     "real person", "connect to agent", "escalate",
                     "need human help", "talk to someone"],
        "responses": [
            """I understand you need human assistance!

Connecting you to a live IT Support Agent...

Your conversation history has been shared with the agent.
Current Queue Position: 2
Estimated Wait Time: 5-10 minutes

You can also reach us at:
- Email: itsupport@company.com
- Phone: 1800-IT-HELP
- Teams: IT Support Channel"""
        ]
    },

    "goodbye": {
        "patterns": ["bye", "goodbye", "exit", "quit", "close", 
                     "thank you", "thanks", "that's all", "done"],
        "responses": [
            "Thank you for contacting IT Support! Have a great day!",
            "Goodbye! Feel free to reach out if you need more help!",
            "Thank you! Your issue has been logged. IT team will follow up if needed!"
        ]
    }
}

# ============================================================
# TICKET SYSTEM
# Based on Project Report Chapter 4 - ER Diagram
# ============================================================

ticket_counter = 1000
tickets = []

def generate_ticket():
    global ticket_counter
    ticket_counter += 1
    ticket_number = f"TKT-{ticket_counter}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return ticket_number, timestamp

def create_ticket(user_input, intent_name):
    ticket_number, timestamp = generate_ticket()
    ticket = {
        "ticket_number": ticket_number,
        "issue": user_input,
        "intent": intent_name,
        "status": "Open",
        "severity": "Medium",
        "created_at": timestamp
    }
    tickets.append(ticket)
    return ticket_number

# ============================================================
# NLP ENGINE - Intent Recognition
# Based on Project Report Chapter 3.1 and 5.2
# ============================================================

def preprocess_input(user_input):
    """
    Preprocessing step:
    - Convert to lowercase (normalization)
    - Remove special characters
    - Tokenization
    """
    user_input = user_input.lower()
    user_input = re.sub(r'[^\w\s]', '', user_input)
    return user_input

def recognize_intent(user_input):
    """
    Intent Recognition using pattern matching
    Based on NLP techniques from Chapter 3.1
    """
    processed_input = preprocess_input(user_input)
    
    matched_intent = None
    highest_match = 0
    
    for intent_name, intent_data in intents.items():
        for pattern in intent_data["patterns"]:
            pattern_words = pattern.lower().split()
            input_words = processed_input.split()
            
            matches = sum(1 for word in pattern_words if word in input_words)
            match_score = matches / len(pattern_words)
            
            if match_score > highest_match:
                highest_match = match_score
                matched_intent = intent_name
    
    # Confidence threshold - 0.5 as mentioned in report
    if highest_match >= 0.5:
        return matched_intent, highest_match
    else:
        return "unknown", 0

def generate_response(intent_name, user_input):
    """
    Response Generation
    Based on Project Report Chapter 5.2
    """
    if intent_name == "unknown":
        ticket_number = create_ticket(user_input, "Unknown Issue")
        return f"""I am sorry, I could not understand your query completely.

However, I have created a support ticket for you:
Ticket Number: {ticket_number}
Status: Open
An IT support agent will contact you within 2-4 hours.

You can also try rephrasing your issue or type 'talk to human' for immediate assistance."""

    intent_data = intents[intent_name]
    response = random.choice(intent_data["responses"])
    
    # Auto create ticket for technical issues
    technical_intents = ["password_reset", "vpn_issue", "slow_laptop", 
                         "printer_issue", "software_install", "network_issue",
                         "email_issue", "access_request"]
    
    if intent_name in technical_intents:
        ticket_number = create_ticket(user_input, intent_name)
        response = response.replace("{ticket_number}", str(ticket_number.split("-")[1]))
        if "{ticket_number}" not in response:
            response += f"\n\n📋 Ticket Created: {ticket_number}"
    
    return response

# ============================================================
# SENTIMENT ANALYSIS
# Basic implementation based on Chapter 3.1
# ============================================================

def analyze_sentiment(user_input):
    """
    Basic Sentiment Analysis
    Detects frustrated or urgent users
    """
    negative_words = ["urgent", "emergency", "not working", "broken", 
                      "frustrated", "angry", "immediately", "asap", 
                      "critical", "cannot", "failed", "error"]
    
    processed = user_input.lower()
    negative_count = sum(1 for word in negative_words if word in processed)
    
    if negative_count >= 2:
        return "negative"
    else:
        return "neutral"

# ============================================================
# MAIN CHATBOT ENGINE
# Based on Project Report Chapter 6.2 - Proposed System
# ============================================================

def chatbot():
    print("=" * 60)
    print("   AI POWERED ITSM CHATBOT USING NLP")
    print("   Chandigarh University - MCA Project")
    print("   Student: Ritika Sharma | O24MCA111878")
    print("=" * 60)
    print("\nBot: Hello! I am your IT Support Assistant.")
    print("Bot: I can help you with:")
    print("     - Password Reset")
    print("     - VPN Issues")
    print("     - Software Installation")
    print("     - Network Problems")
    print("     - Printer Issues")
    print("     - Email Problems")
    print("     - Access Requests")
    print("     - Ticket Status")
    print("\nBot: Type 'bye' to exit anytime.")
    print("-" * 60)
    
    conversation_history = []
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                print("Bot: Please type your issue so I can help you!")
                continue
            
            # Store conversation
            conversation_history.append({
                "role": "user",
                "message": user_input,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            
            # Sentiment Analysis
            sentiment = analyze_sentiment(user_input)
            
            # Intent Recognition
            intent, confidence = recognize_intent(user_input)
            
            # Generate Response
            response = generate_response(intent, user_input)
            
            # Add urgency message for negative sentiment
            if sentiment == "negative":
                print("\nBot: I understand this is urgent. Let me prioritize your issue!")
            
            print(f"\nBot: {response}")
            
            # Store bot response
            conversation_history.append({
                "role": "bot",
                "message": response,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            
            # Exit condition
            if intent == "goodbye":
                print("\n" + "=" * 60)
                print(f"Session Summary: {len(conversation_history)//2} interactions")
                if tickets:
                    print(f"Tickets Created: {len(tickets)}")
                    for ticket in tickets:
                        print(f"  - {ticket['ticket_number']}: {ticket['intent']} [{ticket['status']}]")
                print("=" * 60)
                break
                
        except KeyboardInterrupt:
            print("\n\nBot: Session ended. Thank you for using IT Support!")
            break

# ============================================================
# RUN THE CHATBOT
# ============================================================

if __name__ == "__main__":
    chatbot()
