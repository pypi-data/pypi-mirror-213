# notification-center-ma
## Functions

- send_email()
- send_telegram()
- send_sms()
- send_telegram_photo()
- send_telegram_document()

## Installation
Install the dependencies.
```sh
pip install notification-center-ma
pip install -r requirements.txt
```

## Usage
After installation add requirement to your code
```sh
import notification_center
```


For Email (up to 2GB messages)
```sh
notification_center.send_email(to_emails,cc_emails,bcc_emails,subject,text_body,text_html)
```


For Telegram
```sh
notification_center.send_telegram(chat_ids,text)
```


For Telegram Photos
```sh
notification_center.send_telegram_photo(chat_ids, imageurl, caption)
```


For Telegram Documents
```sh
notification_center.send_telegram_document(chat_ids, documenturl, caption)
```


For SMS
```sh
notification_center.send_sms(source, phonenumbers, text)
```
