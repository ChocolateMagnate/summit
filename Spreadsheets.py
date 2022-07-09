"""Architecting spreadsheets. Further ideas for improvemnt:\n
1. [DONE] Support using different datatypes as entiries including custom items;\n
2. Support various standard operations on the table;\n
3. Create a derived Database class to handle SQl with one item;\n
4. [DONE] Improve the printing outlook and performance;\n"""
#Going to use those imports later, so I'm going to comment them out.
#import timeit as tm
#import matplotlib.pyplot as plt
from math import *
import numpy as np
from tabulate import tabulate


def arranged(item, cls: str) -> bool:
    """Checks if the item belongs to the specified type."""
    return type(item).__name__ == cls

class Spreadsheet:
    """Basic class for representing data in memory as spreadsheets easily consumable for
    machines. It is built as a two-dimensional layout of sheets."""
    def __init__(self, header: list[str], dtypes: list[str], depth: int or None):
        self.contents = header #Represents the values within the spreadsheet.
        self.grid = [[x[0] for x in enumerate(header)]] #Represents the 2D layout.
        self.index = self.columns = len(header) #Represents the number of columns in the table.
        self.depth = depth #Represents the maximum number of papers in the table.
        self.dtypes = dtypes #Represents the data types of each column.
        self.rows = 0 #Represents the number of papers in the table.
        self.length = [] #Represents the longest entriest.

    def __getitem__(self, iposition: tuple or int):
        return self.contents[self.grid[iposition] if isinstance(iposition, tuple) else (0, iposition)]

    def __setitem__(self, iposition: tuple or int, value):
        self.contents[self.grid[iposition] if isinstance(iposition, tuple) else (0, iposition)] = value

    def __repr__(self):
        """Returns a string representation of the spreadsheet."""
        papers, start = [], self.columns
        for column in range(0, self.columns):
            papers.append(self.contents[start:start+self.columns])
            start += self.columns
        return tabulate(papers, headers=self.contents[:self.columns], tablefmt="grid")

    def log(self, row: list):
        """Logs a row to the spreadsheet."""
        if self.depth is not None and self.rows + 1 >= self.depth:
            raise IndexError(f"Exceeded maximum size of {self.depth} papers.")
        for column in enumerate(row):
            try:
                if not arranged(row[column[0]], self.dtypes[column[0]]):
                    t = f"Spreadsheet doesn't support {type(row[column])} on the column {column}. "
                    t += f"Use {self.dtypes[column]} instead."
                    raise TypeError(t)
            except IndexError:
                raise IndexError(f"Column {column[0]+1} is out of range.")

        self.rows += 1
        self.contents += row
        self.grid.append([item[0] for item in enumerate(row, self.index)])
        self.index += len(row)

    def viewRow(self, row: int):
        """Returns a string representation of a row."""
        return str(self.contents[row])

    def viewColumn(self, column: int):
        """Returns a string representation of a column."""
        return self.contents[0][column]

    def describe(self) -> dict:
        """Returns basic statistics about the spreadsheets."""
        return {"Rows": self.rows, "Columns": self.columns, "Depth": self.depth}

    def sumif(self, column: int, condition: str, value: int, message: str or None = None):
        """Returns the sum of all entries in a column that match a condition."""
        result = sum([self.contents[row][column] for row in range(1, self.rows) if eval(condition)])
        self.contents += result
        self.grid.append([item[0] for item in enumerate(result, self.index)])
        self.index += len(result)
        return result
    
    def sumifs(self, column: int, conditions: list[str]):
        """Returns the sum of all entries in a column that match a condition."""
        return sum([self.contents[row][column] for row in range(1, self.rows) if eval(conditions[row])])


    def remove(self, value: list):
        """Removes all matched papers from the spreadsheet."""
        self.contents.remove(value)
        self.rows -= 1

    def delete(self, index: int):
        """Deletes a row from the spreadsheet."""
        self.contents.pop(index)
        self.rows -= 1

    def pop(self, row: list):
        """Removes a row from the spreadsheet and returns it."""
        result = self.contents.pop(row)
        self.rows -= 1
        return result

    def clear(self, header: list[str] or None, dtypes: list[str] or None, depth: int or None):
        """Clears the contents of the spreadsheet."""
        self.contents = [header]
        self.columns = len(self.contents[0])
        self.dtypes = dtypes
        self.depth = depth
        self.rows = 0
        self.length = 0

def main():
    """Main function for testing."""
    table = Spreadsheet(["Name", "Age", "Job", "Salary", "City"],
                        ["str", "int", "str", "int", "str"], 5)
    table.log(["John", 25, "Programmer", 100000, "New York"])
    table.log(["Antony", 34, "Pilot", 349078, "London"])
    table.log(["Jane", 23, "Doctor", 120000, "London"])
    table.log(["Mary", 22, "Nurse", 90000, "Los Angeles"])
    #table.log(["Susan", 25, "Teacher", 100000, "Paris", 7]) IndexError for column raised.
    #table.log(["Mark", 67, "Writer", 450000, "Kyiv"]) IndexError for row successfully raised.
    #table.log([56, "g", 5, "100000", 90]) TypeError successfully raised.
    print(table)
    table.sumif(3, "Salary > 100000", 100000, "Salary of John is greater than 100000.")

if __name__=="__main__":
    main()
