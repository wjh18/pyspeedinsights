import xlsxwriter


class ExcelWorkbook:
    
    def __init__(self, audit_results, metrics_results=None):
        self.workbook = None
        self.worksheet = None
        self.audit_results = audit_results
        self.metrics_results = metrics_results
    
    def _create_workbook(self):
        self.workbook = xlsxwriter.Workbook('psi-results.xlsx')
        
    def _write_results(self):
        row = 0
        col = 1
        if self.audit_results is not None:            
            # Write audit results to Excel workbook            
            for k, v in self.audit_results.items():
                score = v[0]
                value = v[1]
                self.worksheet.write(row, col, k)
                self.worksheet.write(row + 1, col, v[0])
                col += 1
        if self.metrics_results is not None:
            # Write metrics results to Excel workbook
            for k, v in self.metrics_results.items():
                self.worksheet.write(row, col, k)
                self.worksheet.write(row + 1, col, v)
                col += 1
        
    def setup_worksheet(self):
        self._create_workbook()
        self.worksheet = self.workbook.add_worksheet()
        self.worksheet.write(0, 0, 'Page')
        self.worksheet.write(1, 0, 'https://www.example.com')
        
    def write_to_worksheet(self):
        if self.worksheet is not None:
            self._write_results()
            self.workbook.close()