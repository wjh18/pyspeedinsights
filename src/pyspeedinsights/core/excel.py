import xlsxwriter


class ExcelWorkbook:
    
    def __init__(self, audit_results, metrics_results=None):
        self.audit_results = audit_results
        self.metrics_results = metrics_results
        self.workbook = None
        self.worksheet = None        
        self.cur_cell = None
    
    def _create_workbook(self):
        self.workbook = xlsxwriter.Workbook('psi-results.xlsx')
        
    def _write_results(self, results, row=0, col=1):
        
        column_format = self._column_format()
        data_format = self._data_format()
        last_key = list(results.keys())[-1]
        for k, v in results.items():
            self.worksheet.set_column(col, col + 1, 15)
            
            if results == self.audit_results:
                score = v[0]
                value = v[1]
                
                self.worksheet.merge_range(row, col, row, col + 1, k, column_format)
                self.worksheet.write(row + 1, col, 'Score', column_format)
                self.worksheet.write(row + 1, col + 1, 'Value', column_format)
                self.worksheet.write(row + 2, col, score, data_format)                
                self.worksheet.write(row + 2, col + 1, value, data_format)
                if k == last_key:
                    col += 3
                else:
                    col += 2
                
            elif results == self.metrics_results:
                self.worksheet.write(row, col, k, column_format)
                self.worksheet.write(row + 1, col, 'Value', column_format)
                self.worksheet.write(row + 2, col, v, data_format)
                col += 1
        
        return [row, col]
    
    def _column_format(self):
        return self.workbook.add_format({
            'font_size': 16,
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter'})
    
    def _data_format(self):
        return self.workbook.add_format({
            'font_size': 14,
            'align': 'center',
            'valign': 'vcenter'})
    
    def _url_format(self):
        return self.workbook.add_format({
            'font_size': 14,
            'align': 'left',
            'valign': 'vcenter'})
        
    def setup_worksheet(self):
        self._create_workbook()
        self.worksheet = self.workbook.add_worksheet()
        
        column_format = self._column_format()
        url_format = self._url_format()
        row, col = 0, 0
        
        self.worksheet.set_column(col, col + 1, 15)
        self.worksheet.merge_range(row, col, row, col + 4, 'URL', column_format)
        self.worksheet.merge_range(row + 2, col, row + 2, col + 4, 'https://www.example.com', url_format)
        
        self.cur_cell = [0, 4]        
        
    def write_to_worksheet(self):
        if self.worksheet is not None:
            for results in [self.audit_results, self.metrics_results]:
                row, col = self.cur_cell[0], self.cur_cell[1] + 1
                new_pos = self._write_results(results, row=row, col=col)
                self.cur_cell = new_pos
        
        self.workbook.close()