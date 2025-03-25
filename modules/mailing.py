import pandas as pd

class Mailing:
    def __init__(self):
        self.contacts = pd.DataFrame(columns=["name", "email", "phone", "tags"])

    def import_contacts(self, file_path):
        new_contacts = pd.read_csv(file_path)
        self.contacts = pd.concat([self.contacts, new_contacts], ignore_index=True)

    def export_contacts(self, file_path):
        self.contacts.to_csv(file_path, index=False)

    def get_contacts(self, filter_by=None):
        if filter_by:
            return self.contacts.query(filter_by)
        return self.contacts