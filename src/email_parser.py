from email import policy
from email.parser import BytesParser
import os

def parse_eml(file_path):
    with open(file_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)

    email_data = {
        'subject': msg['subject'],
        'sender': msg['from'],
        'recipient': msg['to'],
        'date': msg['date'],
        'body': get_email_body(msg),
        'attachments': get_attachments(msg)
    }

    return email_data

def get_email_body(msg):
    if msg.is_multipart():
        for part in msg.iter_parts():
            if part.get_content_type() == 'text/plain':
                return part.get_payload(decode=True).decode(part.get_content_charset())
    else:
        return msg.get_payload(decode=True).decode(msg.get_content_charset())

    return ""

def get_attachments(msg):
    attachments = []
    if msg.is_multipart():
        for part in msg.iter_parts():
            if part.get_content_disposition() == 'attachment':
                attachments.append({
                    'filename': part.get_filename(),
                    'content_type': part.get_content_type()
                })
    return attachments

def extract_eml_files(directory):
    eml_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.eml'):
            eml_files.append(os.path.join(directory, filename))
    return eml_files