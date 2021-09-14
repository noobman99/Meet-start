# -*- coding: utf-8 -*-
"""
topic: display the links in table form
"""

from rich.table import Table
from rich.console import Console
from File import File


def print_table(*data,keys:list,header:list):  # table formatting of data 
    console=Console()
    table=Table(*header,title="Meetings")
    for i in data:
        table.add_row(*(map((lambda key:i[key]),keys)))
    console.print(table)
    
if __name__=="__main__":
    file=File("stor.txt")
    print_table(*(file.get_val()),keys=file.keys ,header=["start","Finish","Link"])
    input("Enter to exit.")