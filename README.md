# Spam_filter
Naive Bayes Spam Filter used in the lab works for "Software testing and validation" course in Polytechnique Montreal, where I was a TA.
More information about the system can be found in the pdf file, which lab1 description.
Here's a brief overview:
Each module of the system is implemented in the separate python file. The main ones
System modules are:
- `crud.py`: module to achieve the functionality
CRUD (Create Read Update Delete) for users and groups. User
is represented by his e-mail address and the information he receives
associated. Group is a collection of users.
- `text_cleaner.py`: module for cleaning and tokenization of the text.
- Vocabulary creation: module to create vocabulary with frequency
words found in spam and ham messages.
- `renege.py`: module for processing new emails. Executed
the logic of adding / updating information about users and
groups.
- `email_analyzer.py`: module to calculate the probability that
e-mail is spam or ham.
- `main.py`: main module to manage the system. Understand
a spam detection accuracy evaluation function.
