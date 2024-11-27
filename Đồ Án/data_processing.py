import pandas as pd
import os

class DataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)

    def add_data(self, new_row):
        self.data = pd.concat([self.data, pd.DataFrame([new_row], columns=self.data.columns)], ignore_index=True)

    def delete_data(self, indexes):
        self.data = self.data.drop(indexes).reset_index(drop=True)

    def filter_data(self, column, value):
        return self.data[self.data[column].astype(str).str.contains(value, case=False, na=False)]

    def update_data(self, index, updated_row):
        self.data.iloc[index] = updated_row
        
    def save_to_csv(self):
        self.data.to_csv(self.file_path, index=False)
