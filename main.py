import json
from vocabulary_creator2 import VocabularyCreator
from renege import RENEGE
from email_analyzer import EmailAnalyzer
from text_cleaner import TextCleaning


def evaluate():
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    total = 0
    analyzer = EmailAnalyzer()
    with open("test300.json") as email_file:
        new_emails = json.load(email_file)

    for e_mail in new_emails["dataset"]:
        new_email = e_mail["mail"]
        subject = new_email["Subject"]
        body = new_email["Body"]
        spam = new_email["Spam"]

        is_spam = analyzer.is_spam(subject, body)
        if (is_spam) and (spam == "true"):
            tp += 1
        if (not (is_spam)) and (spam == "false"):
            tn += 1
        if ((is_spam)) and (spam == "false"):
            fp += 1
        if (not (is_spam)) and (spam == "true"):
            fn += 1
        total += 1
    print("Accuracy: ", (tp + tn) / (tp + tn + fp + fn))
    print("********************************************")
   # print("Accuracy: ", (tp + tn) / (total))
    #print("Precision: ", tp / (tp + fp))
    #print("Recall: ", tp / (tp + fn))


if __name__ == "__main__":

    vocab = VocabularyCreator()
    vocab.create_vocab()


    renege = RENEGE()
    renege.classify_emails()
    

    evaluate()
