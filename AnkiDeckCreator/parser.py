"""
Parses an Excel file into lists of words for the deck creator.
"""

from openpyxl import load_workbook

class Parser:
    def __init__(self, filename):
        self.filename = filename
        self.data = {}

        self.parse_file()
    
    def parse_file(self):
        wb = load_workbook(filename=self.filename)
        cols = tuple(wb.active.columns)
        for col in cols:
            title = col[0].value
            self.data[title] = []
            for i in range(1, len(col)):
                self.data[title].append(col[i].value)
                
    def get_titles(self):
        return self.data.keys()
