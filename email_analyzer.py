import json
from text_cleaner import TextCleaning
import math


class EmailAnalyzer:
    """Class to classify e-mails as spam or non spam"""

    def __init__(self):
        self.vocab = "vocabulary.json"
        self.cleaning = TextCleaning()

    def is_spam(self, subject_orig, body_orig):
        # function that returns the probability of the message to be spam or ham
        if subject_orig:
            subject = self.cleaning.clean_text(subject_orig)
        else:
            subject = ""

        body = self.cleaning.clean_text(body_orig)

        body_is_spam, body_is_ham = self.spam_ham_body_prob(body)
        #print("Body spam ham 2",body_is_spam, body_is_ham)
        subject_is_spam, subject_is_ham = self.subject_spam_ham_prob(subject)
        #print("Subject spam ham 2", subject_is_spam, subject_is_ham)
        if (
            0.3 * subject_is_spam + 0.7 * body_is_spam
            > 0.3 * subject_is_ham + 0.7 * body_is_ham
        ):
            return True
        else:
            return False

    def spam_ham_body_prob(self, body):
        body_is_spam = 0
        body_is_ham = 0
        with open(self.vocab) as json_data:
            vocab = json.load(json_data)
        for word in body:
            if word in vocab["spam_body"]:
                body_is_spam += math.log(vocab["spam_body"][word])
            else:
                body_is_spam += math.log(1 / (vocab["total_spam_body"]+1))
            if word in vocab["ham_body"]:
                body_is_ham += math.log(vocab["ham_body"][word])
            else:
                body_is_ham += math.log(1 / (vocab["total_ham_body"]+1))
        #print("Body spam ham,", body_is_spam, body_is_ham)
        return body_is_spam, body_is_ham

    def subject_spam_ham_prob(self, subject):
        subject_is_spam = 0
        subject_is_ham = 0
        with open(self.vocab) as json_data:
            vocab = json.load(json_data)
        for word in subject:
            if word in vocab["spam_sub"]:
                subject_is_spam += math.log(vocab["spam_sub"][word])
            else:
                subject_is_spam += math.log(1 / (vocab["total_spam_sub"]+1))

            if word in vocab["ham_sub"]:
                subject_is_ham += math.log(vocab["ham_sub"][word])
            else:
                subject_is_ham += math.log(1 / (vocab["total_ham_sub"]+1))
        #print("Subject spam ham,", subject_is_spam, subject_is_ham)
        return subject_is_spam, subject_is_ham
