import logging
from livekit.agents import function_tool, RunContext
import requests
from langchain_community.tools import DuckDuckGoSearchRun
from typing import Optional
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib




# Retrieve real time weather using Weather Report API
@function_tool
async def get_weather(context: RunContext, city: str) -> str:

    try:
        response = requests.get(f"http://wttr.in/{city}?format=3")
        if response.status_code == 200:
            response_weather = f"Weather for {city} is {response.text.strip()}"
            logging.info(response_weather)

        else:
            response_weather = f"Failed to provide weather from {city}"
            logging.error(response_weather)

    except Exception as e:
        response_weather = f"Error retrieving weather for {city}: {e}"
        logging.error(response_weather)

    return response_weather


# Retrieve web search using Duck Duck go langchain
@function_tool
async def search_web(context: RunContext, query: str) -> str:
    try:
        results = DuckDuckGoSearchRun().run(tool_input=query)
        logging.info(f"Search result of {query}: {results}")
        return results

    except Exception as e:
        logging.error(f"Error for retrieving the web for query {query}: {e}")
        return f"An error for searching query {query}"


@function_tool
async def send_email(
    context: RunContext, to_email: str, subject: str, message: str, cc_email: Optional[str] = None
):
    try:
        # Gmail SMTP configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Initiate email credential
        gmail_address = os.getenv("GMAIL_ADDRESS")
        gmail_app_password = os.getenv("GMAIL_APP_PASSWORD")

        if not gmail_address or not gmail_app_password:
            logging.error("Could not found gmail credential from environment variables")
            return "Email sending failed: Gmail credentials not configured."

        # Create message
        else:
            msg = MIMEMultipart()
            msg["From"] = gmail_address
            msg["To"] = to_email
            msg["Subject"] = subject
            msg["Message"] = message

            # Add CC if needed
            receipents = [to_email]
            if cc_email:
                msg["Cc"] = cc_email
                receipents.append(cc_email)

            # Attach message body
            msg.attach(MIMEText(message, "plain"))

            # Connect to GMAIL SMTP Server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Enable TLS encryption
            server.login(gmail_address, gmail_app_password)

            # Send email
            text = msg.as_string()
            server.sendmail(gmail_address, receipents, text)
            server.quit()

            logging.info(f"Email sent successfully to {to_email}")
            return f"Email sent successfully to {to_email}"

    except smtplib.SMTPAuthenticationError:
        logging.error("Gmail authentication failed")
        return f"Email authentication error. Please check your Gmail credentials."

    except smtplib.SMTPException as e:
        logging.error(f"SMTP error occured: {e} ")
        return f"Email sending failed: SMTP Error - {str(e)}"

    except Exception as e:
        logging.error(f"Error while sending email: {e}")
        return f"An error while sending email: {e}"
