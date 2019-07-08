import openpyxl

def create(rows):
    filepath = "test101.xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active

    row_number = 1
    for row in rows:
        i = 1
        for k in row:
            ws.cell(row=row_number, column=i, value=str(row[k]))
           
            i += 1
        row_number += 1
        
        
    wb.save(filepath)
    return filepath