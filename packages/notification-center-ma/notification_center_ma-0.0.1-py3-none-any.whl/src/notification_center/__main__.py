# __main__.py
import notification_center


def main():
    notification_center.send_email(["fatima.medlij@mobileartsme.com"], [], [], 'Test from PyPI', '', '<h1>HELLO</h1>')


if __name__ == "__main__":
    main()
