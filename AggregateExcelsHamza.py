import pandas as pd
import glob

#Inputs
basepath = 'D:\World Bank\Romania'
file_names_list = glob.glob(basepath+'\Migratia ZM'+'\*.xlsx')
final_file = pd.ExcelWriter(basepath+'\AGGREGATES\Migratia ZM.xlsx')

#We will now set the names of the sheets in the final spreadsheet
example = pd.ExcelFile(basepath+'\Migratia ZM'+'\Migratia ZM Alba Iulia.xlsx')


sheets_ex = []
replaceitems = {"Migratia ZM ":"", "migratie ":"", "mig ZM ":""}

for x in example.sheet_names:
    # if x contains the word Sheet
    if 'Sheet' in x:
        pass
    else:
        y = x.split(' ')
        y.pop()
        y.pop()
        y = ' '.join(y)
        sheets_ex.append(y)

#function calls
def replace_all(text, replaceitems):
    # items instead of iteritems in Python 3
    for i, j in replaceitems.items():
        text = text.replace(i,j)
    return text

#Creation of dictionary: For each file, we create a file_ID
file_IDs = {}
for fil in file_names_list:
    #identify location
    file_ID = fil.split('\\')
    file_ID = file_ID.pop()
    file_ID = file_ID.split('.')
    file_ID = file_ID[0]
    file_ID = replace_all(file_ID,replaceitems)
    file_IDs[fil] = file_ID

for sheet in sheets_ex:
    
    list_df = []
    
    for file in file_names_list:
        to_add = pd.read_excel(file, header=None, sheetname=sheet+' '+file_IDs[file])
        to_add['File_ID'] = file_IDs[file]
        list_df.append(to_add)
        print(sheet+" in "+file+" has been appended")
        
    newsheet = pd.concat(list_df)
    newsheet = newsheet.drop_duplicates(newsheet.columns.difference(['File_ID']))
    newsheet.to_excel(final_file, sheet_name=sheet, header=False, index=False)
    print(sheet+" has been added to final file")

#SAVE!
final_file.save()
