import pandas as pd
import json
import os
from pathlib import Path

DATA_FILE = Path("contacts.json")

class Storage:
    def __init__(self):
        self.load_data()

    def load_data(self):
        """Load data from JSON file into a pandas DataFrame."""
        if DATA_FILE.exists():
            try:
                with open(DATA_FILE, "r") as f:
                    data = json.load(f)
                self.df = pd.DataFrame(data)
            except Exception as e:
                print(f"Error loading JSON: {e}")
                self.df = pd.DataFrame(columns=["Name", "Phone", "Email", "Information"])
        else:
            self.df = pd.DataFrame(columns=["Name", "Phone", "Email", "Information"])

    def save_data(self):
        """Save the current DataFrame to a JSON file."""
        self.df.to_json(DATA_FILE, orient="records", indent=4)

    def add_contact(self, name, phone, email, info):
        """Add a new contact to the DataFrame."""
        new_row = pd.DataFrame([{
            "Name": name,
            "Phone": phone,
            "Email": email,
            "Information": info
        }])
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        self.save_data()

    def get_all_contacts(self):
        """Return all contacts."""
        return self.df

    def search_contacts(self, query):
        """Search contacts by name or information context."""
        if self.df.empty:
            return self.df
        
        mask = (
            self.df["Name"].str.contains(query, case=False, na=False) |
            self.df["Information"].str.contains(query, case=False, na=False)
        )
        return self.df[mask]

    def delete_contact(self, index):
        """Delete a contact by index."""
        if 0 <= index < len(self.df):
            self.df = self.df.drop(index).reset_index(drop=True)
            self.save_data()
            return True
        return False
