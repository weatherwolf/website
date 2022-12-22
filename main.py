# %%
from CheckFunc import MakeDatabase
import pandas as pd
import sys
import os

# %% 
def RunFile(inputFile):
    inputName = inputFile.split('.')[0]

    writer = pd.ExcelWriter(f"output/{inputName}_output.xlsx", engine='xlsxwriter')
    MakeDatabase(f'{inputFile}').to_excel(writer, sheet_name="Sheet1")
    writer.save()

print("Done")

# %%
if __name__ == '__main__':
    inputFile = input("give input file")
    RunFile(inputFile)
