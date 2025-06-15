from email import policy
from email.parser import BytesParser
import os
from datetime import datetime
import email.utils

def parse_eml(file_path):
    """Parse .eml file and extract email data"""
    try:
        with open(file_path, 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)

        # Parse date with better handling
        date_str = msg['date']
        parsed_date = None
        if date_str:
            try:
                # Parse the date string
                date_tuple = email.utils.parsedate_tz(date_str)
                if date_tuple:
                    # Convert to datetime object
                    timestamp = email.utils.mktime_tz(date_tuple)
                    parsed_date = datetime.fromtimestamp(timestamp)
                else:
                    parsed_date = datetime.now()  # Fallback to current time
            except:
                parsed_date = datetime.now()  # Fallback to current time
        else:
            parsed_date = datetime.now()  # Fallback to current time

        email_data = {
            'subject': msg.get('subject', 'No Subject'),
            'sender': msg.get('from', 'Unknown Sender'),
            'recipient': msg.get('to', 'Unknown Recipient'),
            'date': parsed_date,
            'body': get_email_body(msg),
            'attachments': get_attachments(msg)
        }

        return email_data
    except Exception as e:
        raise Exception(f"Failed to parse email file: {str(e)}")

def get_email_body(msg):
    """Extract email body text"""
    body = ""
    
    if msg.is_multipart():
        for part in msg.iter_parts():
            content_type = part.get_content_type()
            content_disposition = part.get_content_disposition()
            
            # Skip attachments
            if content_disposition == 'attachment':
                continue
                
            if content_type == 'text/plain':
                try:
                    charset = part.get_content_charset() or 'utf-8'
                    body = part.get_payload(decode=True).decode(charset, errors='ignore')
                    break  # Use first plain text part
                except:
                    continue
            elif content_type == 'text/html' and not body:
                try:
                    charset = part.get_content_charset() or 'utf-8'
                    html_body = part.get_payload(decode=True).decode(charset, errors='ignore')
                    # Simple HTML to text conversion (remove tags)
                    import re
                    body = re.sub('<[^<]+?>', '', html_body)
                except:
                    continue
    else:
        # Single part message
        content_type = msg.get_content_type()
        if content_type == 'text/plain':
            try:
                charset = msg.get_content_charset() or 'utf-8'
                body = msg.get_payload(decode=True).decode(charset, errors='ignore')
            except:
                body = str(msg.get_payload())
        elif content_type == 'text/html':
            try:
                charset = msg.get_content_charset() or 'utf-8'
                html_body = msg.get_payload(decode=True).decode(charset, errors='ignore')
                import re
                body = re.sub('<[^<]+?>', '', html_body)
            except:
                body = str(msg.get_payload())

    return body.strip() if body else ""

def get_attachments(msg):
    """Extract attachment information"""
    attachments = []
    if msg.is_multipart():
        for part in msg.iter_parts():
            if part.get_content_disposition() == 'attachment':
                filename = part.get_filename()
                if filename:
                    attachments.append({
                        'filename': filename,
                        'content_type': part.get_content_type(),
                        'size': len(part.get_payload(decode=True)) if part.get_payload(decode=True) else 0
                    })
    return attachments

def extract_eml_files(directory):
    """Extract all .eml files from a directory"""
    eml_files = []
    try:
        for filename in os.listdir(directory):
            if filename.endswith('.eml'):
                eml_files.append(os.path.join(directory, filename))
    except Exception as e:
        print(f"Error reading directory {directory}: {str(e)}")
    return eml_files