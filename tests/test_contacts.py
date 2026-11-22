from extractors.contacts import extract_emails

sample_text = """
Contact us:
info@example.com
sales@example.org
"""

emails = extract_emails(sample_text)

print("Extracted emails:", emails)