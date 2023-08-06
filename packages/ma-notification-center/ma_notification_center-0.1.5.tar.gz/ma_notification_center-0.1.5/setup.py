import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ma_notification_center",
    version="0.1.5",
    author="Fatima Medlij",
    author_email="medlijfatima@gmail.com",
    description="MobileArts Notification Center Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires  = ['boto3','json','uuid', 'email_validator','urllib'], 
    license = 'MIT'
)
