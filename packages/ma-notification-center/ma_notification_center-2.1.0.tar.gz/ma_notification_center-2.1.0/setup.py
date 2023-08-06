import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ma_notification_center",
    version="2.1.0",
    author="Fatima Medlij",
    author_email="medlijfatima@gmail.com",
    description="MobileArts Notification Center Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires  = ['boto3', 'email_validator'], 
    license = 'MIT'
)
