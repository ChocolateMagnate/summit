"""Architecting spreadsheets. Further ideas for improvemnt:
1. Support using different datatypes as entirs including custom objects;
2. Support various standard operations on the table;
3. Create a derived Database class to handle SQl with one object;
4. Improve the printing outlook and performance."""
#Going to use those imports later, so I'm going to comment them out.
#import numpy as np
#import timeit as tm
#import matplotlib.pyplot as plt

class Spreadsheet:
    """Basic class for representing data in memory as spreadsheets easily consumable for
    machines. Might be useful for ML algorithms and data processing."""
    def __init__(self, header: list(str), columns: int):
        self.contents = [header]
        self.columns = columns
        self.counter = 0

    def __getitem__(self, iposition: tuple):
        return self.contents[iposition]

    def __setitem__(self, position: tuple, value: list(str)):
        self.contents[position] = value

    def log(self, row: list(str)):
        """Logs a row to the spreadsheet."""
        if self.counter > self.columns + 1:
            raise IndexError("Too many rows")
        self.contents.append(row)
        self.counter += 1

    def remove(self, row: list(str)):
        """Removes a row from the spreadsheet."""
        self.contents.remove(row)
        self.counter -= 1

    def pop(self, row: list(str)):
        """Removes a row from the spreadsheet and returns it."""
        result = self.contents.pop(row)
        self.counter -= 1
        return result

    def __str__(self):
        """Returns a string representation of the spreadsheet."""
        return str(self.contents)

    def viewRow(self, row: list(str)):
        """Returns a string representation of a row."""
        return str(row)

    def viewColumn(self, column: list(str)):
        """Returns a string representation of a column."""
        return str(column)
    def describe(self):
        """Returns basic statistics about the spreadsheets."""
        print("Number of rows:", self.counter)
        print("Number of columns:", self.columns)

def main():
    """Main function for testing."""
    table = Spreadsheet(["Name", "Age", "Job", "Salary"], 10)
    table.log(["John", "25", "Programmer", "100000"])
    table.log(["Antony", "34", "Pilot", "349078"])
    table.log(["Jane", "23", "Doctor", "120000"])
    table.log(["Mary", "22", "Nurse", "90000"])


if __name__=="__main__":
    main()
