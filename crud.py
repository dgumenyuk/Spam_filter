import json


class CRUD:
    """
    Class for realising CRUD functionality.
    """

    def __init__(self):
        self.users_file = "users.json"
        self.groups_file = "groups.json"

    ##*************CREATE**************

    def add_new_user(self, user_email, date):
        # adds a new user to the 'users.json' file
        users = self.read_users_file()
        user_num = len(users) + 1
        users[str(user_num)] = {}
        fields = {}
        fields["name"] = user_email
        fields["Trust"] = 50
        fields["SpamN"] = 0
        fields["HamN"] = 0
        fields["Date_of_first_seen_message"] = date
        fields["Date_of_last_seen_message"] = date
        fields["Groups"] = ["default"]
        users[str(user_num)].update(fields)
        groups = self.update_groups(
            self.get_group_id("default"), "List_of_members", user_email
        )
        self.modify_users_file(users)
        self.modify_groups_file(groups)
        #print("User ", user_email, " added...")
        return users

    def add_new_group(self, name, trust, members_list):
        # adds a new group o the 'groups.json'
        groups = self.read_groups_file()
        group_num = len(groups) + 1
        groups[str(group_num)] = {}
        fields = {}
        fields["name"] = name
        fields["Trust"] = trust
        fields["List_of_members"] = members_list
        groups[str(group_num)].update(fields)
        self.modify_groups_file(groups)
        #print("Group ", name, " added...")
        return groups

    ###***********READ****************
    def read_users_file(self):
        # reads the contents of 'users.json' and returns the dictionary
        with open(self.users_file) as users_file:
            return json.load(users_file)

    def read_groups_file(self):
        # reads the contents of 'groups.json' and returns the dictionary
        with open(self.groups_file) as group_file:
            return json.load(group_file)

    def get_user_data(self, user_id, field):
        # gets user data for the given key from 'users.json'
        users = self.read_users_file()
        return users.get(user_id)[field]

    def get_group_data(self, group_id, field):
        # gets group data for the given key from 'users.json'
        groups = self.read_groups_file()
        return groups.get(group_id)[field]

    def get_user_id(self, name):
        # returns user id given the user e-mail
        users = self.read_users_file()
        for user in users:
            if users.get(user)["name"] == name:
                return user
        return 1

    def get_group_id(self, name):
        # returns group id given the group id
        groups = self.read_groups_file()
        for group in groups:
            if groups.get(group)["name"] == name:
                return group
        return 1

    ##*******UPDATE******************

    def modify_users_file(self, data):
        # writes data in 'users.json' file
        with open(self.users_file, "w") as outfile:
            json.dump(data, outfile)
            return 0

    def modify_groups_file(self, data):
        # writes data in 'groups.json' file
        with open(self.groups_file, "w") as outfile:
            json.dump(data, outfile)
            return 0

    def update_users(self, user_id, field, data):
        # updates 'users.json' file
        users = self.read_users_file()
        # print(users)
        if field == "Groups":
            users[user_id]["Groups"].append(data)
        else:
            users[user_id][field] = data
        self.modify_users_file(users)
        return users

    def update_groups(self, group_id, field, data):
        # updates 'groups.json' file
        groups = self.read_groups_file()
        # print(groups)
        if field == "List_of_members":
            groups[group_id]["List_of_members"].append(data)
            #print("User", data, "added to group with id", group_id)
        else:
            groups[group_id][field] = data
        self.modify_groups_file(groups)
        return groups

    ##***********DELETE***********************

    def remove_user(self, user_id, remove_user_group=0, group_name=""):
        # removes a user from 'users.json'
        users = self.read_users_file()
        if remove_user_group:
            users[user_id]["Groups"].remove(group_name)
        else:
            del users[user_id]
        self.modify_users_file(users)
        #print("User ", user_id, " removed...")
        return users

    def remove_group(self, group_id, remove_group_member=0, member_name=""):
        # removes a group from 'groups.json'
        groups = self.read_groups_file()
        if remove_group_member:
            groups[group_id]["List_of_members"].remove(member_name)
        else:
            del groups[group_id]
        self.modify_groups_file(groups)
        #print("Group ", group_id, " removed...")
        return groups
