import win32com.client as win32


class E611:
    def __init__(self, visible=False, filepath=None):
        self.eobj = win32.Dispatch('Excel.Application')
        self.eobj.Visible = visible
        if filepath:
            self.workbook = self.eobj.Workbooks.Open(filepath)
        else:
            self.workbook = self.eobj.Workbooks.Add()
        self.worksheet = self.workbook.ActiveSheet

    def sheet_names(self):
        return [ws.Name for ws in self.workbook .Worksheets]

    def active_sheet(self, sheet_name):
        self.worksheet = self.workbook.Worksheets(sheet_name)

    def max_row_column(self, index=None, letter=False):
        if index:
            if letter:
                return self.worksheet.Cells(self.worksheet.Rows.Count, index).End(win32.constants.xlUp).Row
            else:
                return self.worksheet.Cells(index, self.worksheet.Columns.Count).End(win32.constants.xlToLeft).Column
        else:
            return self.worksheet.UsedRange.Rows.Count, self.worksheet.UsedRange.Columns.Count

    def read_sheet(self, *args):
        return self.worksheet.Range(self.worksheet.Cells(args[0], args[1]), self.worksheet.Cells(args[2], args[3]))

    def write_sheet(self, *args):
        start_cell = self.worksheet.Cells(args[1], args[2])
        end_cell = self.worksheet.Cells(len(args[0]) + args[1] - 1, len(args[0][0]) + args[2] - 1)
        write_range = self.worksheet.Range(start_cell, end_cell)
        write_range.Value = args[0]