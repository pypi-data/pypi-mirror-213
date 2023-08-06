from email_validator import validate_email, EmailNotValidError
import sqs_services
from urllib.parse import urlparse
from botocore.exceptions import ParamValidationError

arn = "https://sqs.eu-central-1.amazonaws.com/059256371462/notifications-"


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


def send_sms(source: str, phonenumbers: list, text: str):
    url = arn + "sms"
    if all(validate_phone_number(number) for number in phonenumbers) and validate_text(text):
        sms_params = {
            "source": source,
            "phonenumbers": phonenumbers,
            "text": text
        }
        return sqs_services.push_to_sqs(sms_params, url)
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
        return sqs_services.push_to_sqs(email_params, url)


def send_telegram(chat_ids: list, text: str):
    url = arn + "telegram"
    if validate_telegram_params(chat_ids, text):
        telegram_params = {
            "chat_ids": chat_ids,
            "text": text
        }
        return sqs_services.push_to_sqs(telegram_params, url)
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
        return sqs_services.push_to_sqs(telegram_params, url)
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
        return sqs_services.push_to_sqs(telegram_params, url)
    else:
        return "Telegram message not sent"
