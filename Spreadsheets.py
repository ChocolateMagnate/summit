"""Architecting spreadsheets. Further ideas for improvemnt:\n
1. [DONE] Support using different datatypes as entiries including custom items;\n
2. Support various standard operations on the table;\n
3. Create a derived Database class to handle SQl with one item;\n
4. [IN PROGRESS] Improve the printing outlook and performance;\n
5. Support merged areas and draw the boundaries between them accordinagly and evently.."""
#Going to use those imports later, so I'm going to comment them out.
#import numpy as np
#import timeit as tm
#import matplotlib.pyplot as plt
#-----------------------------------------------------------------------------------
#THE CURRENT PROBLEMS: write the algorithm that finds the biggest item in a column.
#-----------------------------------------------------------------------------------
from tabulate import tabulate


def arranged(item, cls: str) -> bool:
    """Checks if the item belongs to the specified type."""
    return type(item).__name__ == cls

class Sheet:
    """Cells of spreadsheets."""
    def __init__(self, content, address: tuple, length: int or tuple) -> None:
        if len(address) != 2 or not isinstance(address[0], int) or not isinstance(address[1], int):
            raise ValueError(f"The address must be a tuple of two integers, {address} given.")
        #The Sheet constructor converts a list of item into a list of seperate sheets.
        self.content = content
        self.address = address #(row, column)
        self.stratch = length
        self.type = type(content).__name__
        self.length = len(str(content))

        #if isinstance(content, list):
        #    content = list(content)
        #if header:
        #    self.text = "~" * len(str(content)) + "\n" + " " + "!" + str(content) + "!" + "\n" + "~" * len(str(content))
        #else:
        #    self.text = str(index) + "|" + str(content) + "|" + "\n" + "-" * len(str(content))
        #self.text = self.text.replace("[", "").replace("]", "").replace(",", " |")
    def __str__(self) -> str:
        return str(self.content)

class Spreadsheet:
    """Basic class for representing data in memory as spreadsheets easily consumable for
    machines. It is built as a two-dimensional layout of sheets."""
    def __init__(self, header: list[str], dtypes: list[str], depth: int or None):
        self.contents = header #Represents the values within the spreadsheet.
        self.grid = [x[0] for x in enumerate(header)] #Represents the 2D layout.
        self.index = self.columns = len(header) #Represents the number of columns in the table.
        self.depth = depth #Represents the maximum number of rows in the table.
        self.dtypes = dtypes #Represents the data types of each column.
        self.rows = 0 #Represents the number of rows in the table.
        self.length = [] #Represents the longest entriest.

    def __getitem__(self, iposition: tuple or int):
        return self.contents[self.grid[iposition] if isinstance(iposition, tuple) else (0, iposition)]

    def __setitem__(self, iposition: tuple or int, value):
        self.contents[self.grid[iposition] if isinstance(iposition, tuple) else (0, iposition)] = value

    def __repr__(self):
        """Returns a string representation of the spreadsheet."""
        return tabulate(self.contents, headers="keys", tablefmt="grid")

        #return str(Sheet(self.contents[0], index = None, header=True)) + "\n" + "\n".join(
        #    str(row) for row in self.contents[1:])

    def log(self, row: list):
        """Logs a row to the spreadsheet."""
        if self.depth is not None and self.rows + 1 >= self.depth:
            raise IndexError(f"Exceeded maximum size of {self.depth} rows.")
        for column in enumerate(row):
            if not arranged(row[column[0]], self.dtypes[column[0]]):
                t = f"Spreadsheet doesn't support {type(row[column])} on the column {column}. "
                t += f"Use {self.dtypes[column]} instead."
                raise TypeError(t)
        self.rows += 1
        self.contents += row
        self.grid.append([item for item in enumerate(row, self.index)])
        self.index += len(self.contents)
        #for column in enumerate(self.contents-1):
        #    for item in self.contents[column]:
        #        if len(item) > self.length[column]:
        #            self.length[column] = item
        #    print(self.length[column])

    def viewRow(self, row: int):
        """Returns a string representation of a row."""
        return str(self.contents[row])

    def viewColumn(self, column: int):
        """Returns a string representation of a column."""
        return self.contents[0][column]

    def describe(self) -> dict:
        """Returns basic statistics about the spreadsheets."""
        return {"Rows": self.rows, "Columns": self.columns, "Depth": self.depth}

    def remove(self, value: list):
        """Removes all matched rows from the spreadsheet."""
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
    table = Spreadsheet(["Name", "Age", "Job", "Salary"],
                        ["str", "int", "str", "int"], 5)
    table.log(["John", 25, "Programmer", 100000])
    table.log(["Antony", 34, "Pilot", 349078])
    table.log(["Jane", 23, "Doctor", 120000])
    table.log(["Mary", 22, "Nurse", 90000])
    #table.log(["Mark", 67, "Writer", 450000]) IndexError successfully raised.
    #table.log([56, "g", 5, "100000"]) TypeError successfully raised.
    print(table)

if __name__=="__main__":
    main()
