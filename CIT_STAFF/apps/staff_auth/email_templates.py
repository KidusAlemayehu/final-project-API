class EmailTemplates:
    
    PASSWORD_RESET_EMAIL_SUBJECT_TEXT = "{} Password Reset"
    """
    PASSWORD_RESET_EMAIL_SUBJECT_TEXT
    Template for a simple text email subject.
    Only one format parameter: the name of the site the account is created on.
    """

    PASSWORD_RESET_EMAIL_MESSAGE_TEXT = """Hello {},
    \n
    Someone requested for a passowrd reset link on CIT Staff Management System. If you initiated the request, please follow the following link to reset your passowrd:\n
    \n
    {}

    If you did not request for this link, please ignore this email. 
    
    \n
    Thank you,
    {}"""
    """
    PASSWORD_RESET_EMAIL_MESSAGE_TEXT
    Template for a simple text email message that doesn't contain html components. Good for testing.
    Format parameters in order are: \n
        1. First name\n
        2. Pasword reset link\n
        3. Signature (sender name)\n
    """