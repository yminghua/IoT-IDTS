import requests

def email_warning(img_file):
    url = "your-email-api-url-(e.g. mailgun)"
    with open(img_file, "rb") as f:
        file_content = f.read()
        
    return requests.post(
        url,
        auth=("api", "your-own-api"),
        files=[("attachment", ("image.jpg", file_content))],
        data={"from": "IoT-IDTS@xxx.com",
            "to": ["your-own-email"],
            "subject": "Somebody Unknown is in your House!",
            "html": "<h3>Detect somebody unknown in your house.</h3>"})
