import json

from crud import CRUD
from email_analyzer import EmailAnalyzer


class RENEGE:

    """Class for performing spam filtering; using vocabular.json file as
    well as CRUD and EmalAnalyze classes"""

    def __init__(self):
        self.email_file = "train700.json"
        self.crud = CRUD()
        self.e_mail = EmailAnalyzer()

    def classify_emails(self):
        # function that performs e-mail classification and automatiocally updates users and groups
        self.process_email(self.get_email())
        return 0

    def process_email(self, new_emails):
        # processes a new e-mail: adds a new user if a new e-mail address is detected, updates number of spam/ham messages, trust level
        for email_ in new_emails:
            user_list = self.get_user_email_list()
            new_user_email = new_emails.get(email_)["From"]
            new_user_date = new_emails.get(email_)["Date"]
            #print("Email from ", new_user_email, "sent on ", new_user_date)
            new_email_spam = self.e_mail.is_spam(
                new_emails.get(email_)["Subject"], new_emails.get(email_)["Body"]
            )
            if new_user_email in user_list:
                #print("User", new_user_email, " is already in the list...")
                #print("Updating info...")
                self.update_user_info(new_user_email, new_user_date, new_email_spam)
                self.update_group_info(
                    self.crud.get_user_data(
                        self.crud.get_user_id(new_user_email), "Groups"
                    )
                )
                # self.crud.update_users(self.crud.get_user_id(new_user_email), 'Date_of_last_seen_message', new_user_date)
            else:
                self.crud.add_new_user(new_user_email, new_user_date)
                self.update_user_info(new_user_email, new_user_date, new_email_spam)
                self.update_group_info(
                    self.crud.get_user_data(
                        self.crud.get_user_id(new_user_email), "Groups"
                    )
                )
        return 0

    def update_user_info(self, new_user_email, new_user_date, new_email_spam):
        # callucates new values to update for the users after a new e-mail arrivces
        self.crud.update_users(
            self.crud.get_user_id(new_user_email),
            "Date_of_last_seen_message",
            new_user_date,
        )
        if new_email_spam:
            SpamN = int(
                self.crud.get_user_data(self.crud.get_user_id(new_user_email), "SpamN")
            )
            #print("Detected spam from user", new_user_email)
            self.crud.update_users(
                self.crud.get_user_id(new_user_email), "SpamN", SpamN + 1
            )
        else:
            HamN = int(
                self.crud.get_user_data(self.crud.get_user_id(new_user_email), "HamN")
            )
            #print("Detected ham from user", new_user_email)
            self.crud.update_users(
                self.crud.get_user_id(new_user_email), "HamN", HamN + 1
            )

        SpamN = int(
            self.crud.get_user_data(self.crud.get_user_id(new_user_email), "SpamN")
        )
        HamN = int(
            self.crud.get_user_data(self.crud.get_user_id(new_user_email), "HamN")
        )
        trust_level = 100 * HamN / (SpamN + HamN)
        self.crud.update_users(
            self.crud.get_user_id(new_user_email), "Trust", trust_level
        )
        #print("Trust level set to", trust_level, "for ", new_user_email)
        return 0

    def update_group_info(self, group_list):
        # callucates new values to update for the groups after a new e-mail arrivces
        for group in group_list:
            members = self.crud.get_group_data(
                self.crud.get_group_id(group), "List_of_members"
            )
            memeber_trust_level_list = []
            for member in members:
                trust_level = int(
                    self.crud.get_user_data(self.crud.get_user_id(member), "Trust")
                )
                memeber_trust_level_list.append(trust_level)
            group_trust_level = sum(memeber_trust_level_list) / len(
                memeber_trust_level_list
            )  # average turst level of each user
            self.crud.update_groups(
                self.crud.get_group_id(group), "Trust", group_trust_level
            )
            #print("Trust level for group", group, "updated to ", group_trust_level)
        return 0

    def get_last_email_date(self):
        data = self.crud.read_users_file()
        max_date = 0
        for line in data:
            date = self.crud.get_user_data(line, "Date_of_last_seen_message")
            if int(date) > max_date:
                max_date = date
        return max_date

    def get_user_email_list(self):
        user_email_list = []
        users = self.crud.read_users_file()
        for line in users:
            email_ = self.crud.get_user_data(line, "name")
            user_email_list.append(email_)
        return user_email_list

    def get_email(self):
        # reads all the e-mails and structures them in a dictionary
        with open(self.email_file) as email_file:
            new_emails = json.load(email_file)
        email_num = 0
        email_dict = {}
        for e_mail in new_emails["dataset"]:
            # print(e_mail)
            new_email = e_mail["mail"]
            print(new_email)

            email_dict[str(email_num)] = {}
            fields = {}
            fields["Subject"] = new_email["Subject"]
            fields["From"] = new_email["From"]
            fields["Body"] = new_email["Body"]
            fields["Date"] = 1596855166.0
            email_dict[str(email_num)].update(fields)
            email_num += 1

        return email_dict
