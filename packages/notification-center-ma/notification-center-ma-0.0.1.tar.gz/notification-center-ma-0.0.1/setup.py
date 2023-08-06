from setuptools import setup, find_namespace_packages

setup(
    name="notification-center-ma",
    version="0.0.1",
    description="A package for sending notifications internally for MobileArts",
    author="Fatima Medlij",
    author_email="medlijfatima@gmail.com",
    packages=find_namespace_packages(include=["src.*"]),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    keywords=["notification", "messaging", "communication"],
    install_requires=[
        "email_validator",
        "sqs_services",
        "boto3",
        "urllib3",
        "botocore",
        "python-dotenv",
    ],
)
