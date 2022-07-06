"""Architecting spreadsheets. Further ideas for improvemnt:\n
1. [DONE] Support using different datatypes as entiries including custom items;\n
2. Support various standard operations on the table;\n
3. Create a derived Database class to handle SQl with one item;\n
4. [IN PROGRESS] Improve the printing outlook and performance."""
#Going to use those imports later, so I'm going to comment them out.
#import numpy as np
#import timeit as tm
#import matplotlib.pyplot as plt

def arranged(item, cls: list["str", "int", "float", "bool", "list", "dict", "tuple", "set", "None"]):
    """Checks if the item belongs to the specified type."""
    result = False
    match cls:
        case "str":
            result = isinstance(item, str)
        case "int":
            result = isinstance(item, int)
        case "float":
            result = isinstance(item, float)
        case "bool":
            result = isinstance(item, bool)
        case "list":
            result = isinstance(item, list)
        case "tuple":
            result = isinstance(item, tuple)
        case "dict":
            result = isinstance(item, dict)
        case "set":
            result = isinstance(item, set)
        case "None":
            result = item is None
    return result

class Sheet:
    """Node class for the Spreadsheet class."""
    def __init__(self, content, index: int or None, header: bool = False) -> None:
        if isinstance(content, list):
            content = list(content)
        if header:
            self.text = "~" * len(str(content)) + "\n" + " " + "!" + str(content) + "!" + "\n" + "~" * len(str(content))
        else:
            self.text = str(index) + "|" + str(content) + "|" + "\n" + "-" * len(str(content))
        self.text = self.text.replace("[", "").replace("]", "").replace(",", " |")
    def __str__(self) -> str:
        return self.text

class Spreadsheet:
    """Basic class for representing data in memory as spreadsheets easily consumable for
    machines. Might be useful for ML algorithms and data processing."""
    def __init__(self, header: list[str], dtypes: list[str], depth: int):
        self.contents = [header] #Represents the whole table as a two-dimensional list.
        self.columns = len(header) #Represents the number of columns in the table.
        self.depth = depth #Represents the maximum number of rows in the table.
        self.dtypes = dtypes #Represents the data types of each column.
        self.counter = 0 #Represents the number of rows in the table.
        self.length = 0 #Represents the longest entry.

    def __getitem__(self, iposition: tuple):
        return self.contents[iposition]

    def __setitem__(self, position: tuple, value: list[str]):
        self.contents[position] = value

    def __str__(self):
        """Returns a string representation of the spreadsheet."""
        return str(Sheet(self.contents[0], index = None, header=True)) + "\n" + "\n".join(
            str(row) for row in self.contents[1:])

    def log(self, row: list):
        """Logs a row to the spreadsheet."""
        if self.counter >= self.depth + 1:
            raise IndexError("Too many rows")
        for column in range(len(row)):
            if not arranged(row[column], self.dtypes[column]):
                raise TypeError("Wrong data type in {}".format(row[column]))
        self.counter += 1
        self.contents.append(Sheet(row, index = self.counter))
        if len("".join(str(row))) > self.length:
            self.length = len("".join(str(row)))

    def remove(self, row: list):
        """Removes a row from the spreadsheet."""
        self.contents.remove(row)
        self.counter -= 1

    def pop(self, row: list):
        """Removes a row from the spreadsheet and returns it."""
        result = self.contents.pop(row)
        self.counter -= 1
        return result

    def viewRow(self, row: int):
        """Returns a string representation of a row."""
        return str(self.contents[row])

    def viewColumn(self, column: int):
        """Returns a string representation of a column."""
        return self.contents[0][column]

    def describe(self):
        """Returns basic statistics about the spreadsheets."""
        return {"Rows": self.counter, "Columns": self.columns}

def main():
    """Main function for testing."""
    table = Spreadsheet(["Name", "Age", "Job", "Salary"],
                        ["str", "int", "str", "int"], 10)
    table.log(["John", 25, "Programmer", 100000])
    table.log(["Antony", 34, "Pilot", 349078])
    table.log(["Jane", 23, "Doctor", 120000])
    table.log(["Mary", 22, "Nurse", 90000])
    #table.log([56, "g", 5, "100000"]) Error successfully raised.
    print(table)

if __name__=="__main__":
    main()
