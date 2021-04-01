import json
import os
from text_cleaner import TextCleaning


class VocabularyCreator:
    """Class for creating vocabulary of spam and non-spam messages"""

    def __init__(self):
        self.train_set = "train700.json"
        # self.train_set = "1000-mailsV1.json"
        self.cleaning = TextCleaning()
        self.vocabulary = "vocabulary.json"

    def create_vocab(self):
        # function that creates the vocabulary of words that apper in spam and ham
        if os.path.exists(self.vocabulary):
            print("Vocabulary is already created...")
            return 0

        print("Creating vocabulary...")

        vocab = {"spam_sub": {}, "total_spam_sub": {}, "ham_sub": {}, "total_ham_sub": {}, 
                 "spam_body": {}, "total_spam_body": {}, "ham_body": {}, "total_ham_body": {}}

        total_spam_sub = 0
        total_spam_body = 0
        total_ham_sub = 0
        total_ham_body = 0

        with open(self.train_set) as json_data:
            data_dict = json.load(json_data)
        for item in data_dict["dataset"]:
            email = item["mail"]
            subject = self.cleaning.clean_text(email["Subject"])
            body = self.cleaning.clean_text(email["Body"])

            #print(body)
            if email["Spam"] == "true":
                for word in subject:
                    if word in vocab["spam_sub"]:
                        vocab["spam_sub"][word] += 1
                        total_spam_sub += 1
                    else:
                        vocab["spam_sub"][word] = 1
                        total_spam_sub += 1
                for word in body:
                    if word in vocab["spam_body"]:
                        vocab["spam_body"][word] += 1
                        total_spam_body += 1
                    else:
                        vocab["spam_body"][word] = 1
                        total_spam_body += 1
            if email["Spam"] == "false":
                for word in subject:
                    if word in vocab["ham_sub"]:
                        vocab["ham_sub"][word] += 1
                        total_ham_sub += 1
                    else:
                        vocab["ham_sub"][word] = 1
                        total_ham_sub += 1
                for word in body:
                    #print(word)
                    if word in vocab["ham_body"]:
                        vocab["ham_body"][word] += 1
                        total_ham_body += 1
                    else:
                        vocab["ham_body"][word] = 1
                        total_ham_body += 1


        for word in dict(vocab["spam_sub"]):
            vocab["spam_sub"][word] = vocab["spam_sub"][word] / total_spam_sub
        vocab["total_spam_sub"] = total_spam_sub
        for word in dict(vocab["spam_body"]):
            vocab["spam_body"][word] = vocab["spam_body"][word] / total_spam_body
        vocab["total_spam_body"] = total_spam_body
        for word in dict(vocab["ham_sub"]):
            vocab["ham_sub"][word] = vocab["ham_sub"][word] / total_ham_sub
        vocab["total_ham_sub"] = total_ham_sub
        for word in dict(vocab["ham_body"]):
            vocab["ham_body"][word] = vocab["ham_body"][word] / total_ham_body
        vocab["total_ham_body"] = total_ham_body
        #for category in vocab:
         #   for word in dict(vocab[category]):
         #       vocab[category][word] = vocab[category][word] / len(vocab[category])

        with open(self.vocabulary, "w") as outfile:
            json.dump(vocab, outfile)
            print("Vocabulary created....")

        return vocab
