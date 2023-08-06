import boto3
import json
from uuid import uuid4
from email_validator import validate_email, EmailNotValidError
from urllib.parse import urlparse

arn = "https://sqs.eu-central-1.amazonaws.com/059256371462/notifications-"

sqs_client = boto3.client("sqs", region_name="eu-central-1")
s3_client = boto3.client("s3", region_name="eu-central-1")
bucket_name = "lambda-testing-fatima-de-serverlessdeploymentbuck-g76sanrcmrse"
bucket_path = "notifications-email"


class Notifications:
    def send_sms(source: str, phonenumbers: list, text: str):
        url = arn + "sms"
        if all(validate_phone_number(number) for number in phonenumbers) and validate_text(text):
            sms_params = {
                "source": source,
                "phonenumbers": phonenumbers,
                "text": text
            }
            return push_to_sqs(sms_params, url)
        else:
            return "SMS not sent"

    def send_email(to_emails: list, cc_emails: list, bcc_emails: list, subject: str, body_text: str, body_html: str):
        url = arn + "email"
        if not validate_email_params(to_emails, cc_emails, bcc_emails, subject, body_text, body_html):
            return "Email not sent"
        else:
            email_params = dict(to_emails=to_emails, cc_emails=cc_emails, bcc_emails=bcc_emails, message={
                "subject": subject,
                "body_text": body_text,
                "body_html": body_html
            })
            return push_to_sqs(email_params, url)

    def send_telegram(chat_ids: list, text: str):
        url = arn + "telegram"
        if validate_telegram_params(chat_ids, text):
            telegram_params = {
                "chat_ids": chat_ids,
                "text": text
            }
            return push_to_sqs(telegram_params, url)
        else:
            return "Telegram message not sent"

    def send_telegram_photo(chat_ids: list, image_url: str, caption: str):
        url = arn + "photo-telegram"
        if validate_telegram_media_params(chat_ids, image_url, caption):
            telegram_params = {
                "chat_ids": chat_ids,
                "imageurl": image_url,
                "caption": caption
            }
            return push_to_sqs(telegram_params, url)
        else:
            return "Telegram message not sent"

    def send_telegram_document(chat_ids: list, document_url: str, caption: str):
        url = arn + "document-telegram"
        if validate_telegram_media_params(chat_ids, document_url, caption):
            telegram_params = {
                "chat_ids": chat_ids,
                "documenturl": document_url,
                "caption": caption
            }
            return push_to_sqs(telegram_params, url)
        else:
            return "Telegram message not sent"

def push_to_sqs(data: dict, sqs_url: str):
    send_to_s3 = False
    sqs_params = {
        "MessageBody": json.dumps(data),
        "QueueUrl": sqs_url,
        "DelaySeconds": 3
    }

    rough_obj_size = len(json.dumps(data))
    if rough_obj_size > 200000:
        send_to_s3 = True
        object_key = str(uuid4())
        sqs_params["MessageBody"] = f"s3://{bucket_name}/{bucket_path}/{object_key}"

    sqs_response = sqs_client.send_message(**sqs_params)

    if send_to_s3:
        s3_params = {
            "Bucket": bucket_name,
            "Key": f"{bucket_path}/{object_key}",
            "Body": json.dumps(data)
        }
        s3_client.put_object(**s3_params)

    if sqs_response.get("MessageId"):
        print("Notification Sent")



def validate_phone_number(number: int):
    return 6 < len(str(number)) <= 15


def validate_text(text: str):
    return isinstance(text, str) and len(text) >= 3


def validate_email_address(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False


def validate_email_params(to_emails: list, cc_emails: list, bcc_emails: list, subject: str, body_text: str,
                          body_html: str) -> bool:
    for email in to_emails + cc_emails + bcc_emails:
        if not validate_email_address(email):
            print("Invalid email address:", email)
            return False

    if not subject:
        print("Subject cannot be empty")
        return False

    if not body_text and not body_html:
        print("Body of email cannot be empty")
        return False

    return True


def validate_chat_id(chat_id):
    return 6 < len(str(chat_id)) <= 15


def validate_caption(caption: str):
    return isinstance(caption, str) and (len(caption) >= 3)


def validate_url(url: str):
    parsed_url = urlparse(url)
    return parsed_url.scheme in ["http", "https"]


def validate_telegram_params(chat_ids: list, text: str):
    for chat_id in chat_ids:
        if not validate_chat_id(chat_id):
            print("Not a valid chat ID:", chat_id)
            return False

    if not validate_text(text):
        print("Text is too short or invalid")
        return False

    return True


def validate_telegram_media_params(chat_ids: list, media_url: str, caption: str):
    for chat_id in chat_ids:
        if not validate_chat_id(chat_id):
            print("Not a valid chat ID:", chat_id)
            return False

    if not validate_caption(caption):
        print("Caption is too short or invalid")
        return False

    if not validate_url(media_url):
        print("Not a valid URL")
        return False

    return True