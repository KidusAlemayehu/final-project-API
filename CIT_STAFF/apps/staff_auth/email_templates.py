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
    
    ACCOUNT_CREATED_EMAIL_SUBJECT_TEXT = "Welcome to {}"
    """
    ACCOUNT_CREATED_EMAIL_SUBJECT_TEXT
    Template for a simple text email subject.
    Only one format parameter: the name of the site the account is created on.
    """
    
    ACCOUNT_CREATED_EMAIL_MESSAGE_TEXT = """Hello {},
    \n
    Your account at {} has been created within the office {} and the role of `{}`. Please click on the following link and reset your password to
    start using your account. {}.
    \n
    Thank you,
    {}"""
    """
    ACCOUNT_CREATED_EMAIL_MESSAGE_TEXT
    Template for a simple text email message that doesn't contain html components. Good for testing.
    Format parameters in order are: \n
        1. First name\n
        2. Website name or url the account is created at\n
        3. Role of user on the system\n
        4. URL to follow for the created account\n
        5. Signature (sender name)\n
    """
