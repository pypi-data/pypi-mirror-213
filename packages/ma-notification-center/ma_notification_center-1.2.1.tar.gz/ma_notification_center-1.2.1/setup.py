from setuptools import setup, find_packages

setup(
    name='ma_notification_center',
    version='1.2.1',
    description='Python package for sending notifications via SMS, email, and Telegram',
    author='Fatima Medlij',
    author_email='medlijfatima@gmail.com',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'email-validator'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
