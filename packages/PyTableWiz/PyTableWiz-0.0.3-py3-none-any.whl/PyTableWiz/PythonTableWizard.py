import csv
from timeit import default_timer as timer

""" Developer   : Pramu Programming Concept """
""" Description : This program has been created for represent (csv, json etc..) data file as a table. """
""" Date        : Thursday, 16 March 2023 """


class TableWizard:
    def __init__(self, file_path, dialect_mode="r", limit=100, justify='left',
                 align=None, acc_details=True, SelectedRows=None, DTE=None,
                 tl="┌", ti="┬", tr="┐", hdl="├", hdi="┼", hdr="┤", bl="└", bi="┴", br="┘", vl="│", hl="─"):

        self.file_path = file_path
        self.dialect_mode = dialect_mode
        self.limit = limit
        self.justify = justify
        self.align = align
        self.accessories_details = acc_details
        self.RowSelection = SelectedRows
        self.Derived_table = DTE

        self.top_left = tl
        self.top_interconnection = ti
        self.top_right = tr
        self.heading_left = hdl
        self.heading_interconnection = hdi
        self.heading_right = hdr
        self.bottom_left = bl
        self.bottom_interconnection = bi
        self.bottom_right = br
        self.vertical_line = vl
        self.horizontal_line = hl

        self.col_index = None
        self.row_count = 0

        self.temp_data_list = []
        self.data_list = []
        self.col_width = []

        self.start = timer()
        self.dataReader()
        self.column_width()
        self.draw_table()
        self.stop = timer()

        if self.accessories_details:
            self.reading_details()
        else:
            pass

    def dataReader(self):
        if self.file_path:
            try:
                if self.Derived_table is None:
                    with open(self.file_path, self.dialect_mode) as f:
                        csvDicRead = csv.DictReader(f)
                        self.data_list.append(csvDicRead.fieldnames)

                        if self.RowSelection:
                            for row in csvDicRead:
                                for ix, n in enumerate(self.RowSelection):
                                    # Grab specified rows from data (csv) file
                                    if row[n] in (list(self.RowSelection.values())[ix]):
                                        self.data_list.append(list(row.values()))
                        else:
                            for row in csvDicRead:
                                self.data_list.append([r for r in row.values()])

                        return self.data_list
                else:
                    self.data_list.append([i for i in self.Derived_table])
                    with open(self.file_path, self.dialect_mode) as f:
                        csvDicRead = csv.DictReader(f)
                        if self.RowSelection:
                            for row in csvDicRead:
                                for ix, n in enumerate(self.RowSelection):
                                    if row[n] in (list(self.RowSelection.values())[ix]):
                                        self.data_list.append(list(row[i] for i in self.Derived_table))
                        else:
                            for row in csvDicRead:
                                self.data_list.append(list(row[i] for i in self.Derived_table))

                        return self.data_list
            except Exception as e:
                print("[!] ", e)
                exit()
        else:
            print("[?] File Path Not Found !")
            exit()

    def column_width(self):
        for row in enumerate(self.data_list):
            if row[0] <= self.limit:
                for i in enumerate(row[1]):
                    if len(row[1]) <= len(self.col_width):
                        if len(i[1]) > self.col_width[i[0]]:
                            self.col_width[i[0]] = len(i[1])
                        else:
                            pass
                    else:
                        self.col_width.append(len(i[1]))
            else:
                break

        return self.col_width

    def draw_separators(self, start_symbol, Separate_symbol, end_symbol):
        print(start_symbol, end='')
        for cw in self.col_width:
            if self.col_width[-1] == cw:
                print(((self.horizontal_line * (cw + 3)) + self.horizontal_line), end=end_symbol)
            else:
                print(((self.horizontal_line * (cw + 3)) + self.horizontal_line), end=Separate_symbol)
        print()

    def fixed_length(self, text, length):
        if self.justify == 'left':
            text = (text + " " * length)[:length]
        elif self.justify == 'center':
            text = (" " * ((length // 2) - (len(text) // 2)) + text + " " * length)[:length]
        elif self.justify == 'right':
            text = (" " * (length - (len(text))) + text)[:length]
        return text

    def draw_table(self):
        reset_align = self.justify
        if self.align is None:
            pass
        else:
            try:
                self.align = {self.data_list[0].index(x): y for x, y in self.align.items() if x in self.data_list[0]}
            except ValueError as ve:
                print(f"[!] ValueError : {ve}\n Please check your 'alignment' argument")
                exit()
            except Exception as e:
                print(f'[!] Error : {e}')

        self.draw_separators(self.top_left, self.top_interconnection, self.top_right)
        print(f"{self.vertical_line} ", end=" ")

        for column in enumerate(self.data_list[0]):
            print(self.fixed_length(column[1], self.col_width[column[0]]), end=f"  {self.vertical_line}  ")
        print()
        self.draw_separators(self.heading_left, self.heading_interconnection, self.heading_right)

        self.data_list.pop(0)

        for row in enumerate(self.data_list):
            if self.row_count == self.limit:
                break
            else:
                print(f"{self.vertical_line} ", end=" ")
                for column in enumerate(row[1]):
                    if self.align is None:
                        pass
                    else:
                        if column[0] in self.align:
                            self.justify = self.align[column[0]]
                        else:
                            self.justify = reset_align

                    print(self.fixed_length(column[1], self.col_width[column[0]]), end=f"  {self.vertical_line}  ")
            self.row_count += 1
            print()

        self.draw_separators(self.bottom_left, self.bottom_interconnection, self.bottom_right)

    def reading_details(self):
        print(f"👉 Records    : {self.row_count}") if self.row_count > 1 else print(f"👉 Record     : {self.row_count}")
        print(f"👉 Attributes : {len(self.data_list[0])}") if len(self.data_list[0]) > 1 else \
            print(f"👉 Attribute  : {len(self.data_list[0])}")
        print(f"👉 File Name  : {self.file_path.split('/')[-1]}")

        time_duration = (self.stop - self.start)
        print(f"👉 TTE        : {time_duration:.4f} sec")
