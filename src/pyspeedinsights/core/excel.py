import xlsxwriter


class ExcelWorkbook:
    
    def __init__(self, url, metadata, audit_results, metrics_results=None):
        self.url = url
        self.metadata = metadata
        self.audit_results = audit_results
        self.metrics_results = metrics_results
        self.workbook = None
        self.worksheet = None        
        self.cur_cell = None
    
    def _create_workbook(self):
        self.workbook = xlsxwriter.Workbook('psi-results.xlsx')
        
    def _write_metadata(self):
        pass
        
    def _write_results(self, results, is_first, row=0, col=1):
        
        column_format = self._column_format()
        data_format = self._data_format()
                
        for k, v in results.items():
            self.worksheet.set_column(col, col + 1, 15)
            
            if results == self.audit_results:
                score = v[0]
                value = v[1]
                score_format = self._score_format(score)
                
                if is_first:
                    self.worksheet.merge_range(row, col, row, col + 1, k, column_format)
                    self.worksheet.write(row + 1, col, 'Score', column_format)
                    self.worksheet.write(row + 1, col + 1, 'Value', column_format)
                self.worksheet.write(row + 2, col, score, score_format)
                self.worksheet.write(row + 2, col + 1, value, score_format)
                
                if k == list(results.keys())[-1]:
                    col += 3
                else:
                    col += 2
                
            elif results == self.metrics_results:
                if is_first:
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
        
    def _metadata_format(self):
        return self.workbook.add_format({
            'font_size': 20,
            'bold': 1,
            'align': 'left',
            'valign': 'vcenter'})
        
    def _score_format(self, score):
        if score >= 90:
            color = 'lime'            
        elif 90 > score >= 80:
            color = 'green'
        elif 80 > score >= 70:
            color = 'yellow'
        elif 70 > score >= 60:
            color = 'orange'
        elif 60 > score >= 50:
            color = 'brown'
        elif 50 > score:
            color = 'red'
            
        return self.workbook.add_format({
            'bg_color': color,
            'font_size': 14,
            'align': 'center',
            'valign': 'vcenter'})
        
    def setup_worksheet(self):
        self._create_workbook()
        self.worksheet = self.workbook.add_worksheet()
        
        column_format = self._column_format()        
        metadata_format = self._metadata_format()
        
        # Add metadata to the first cell of the Excel sheet
        category = self.metadata['category'].upper()
        category_score = self.metadata['category_score'] * 100
        strategy = self.metadata['strategy'].upper()
        metadata_value = f"{strategy} {category} REPORT - SCORE: {str(category_score)}"        
        self.worksheet.write(0, 0, metadata_value, metadata_format)
        
        # Add header and data for the URL that was requested
        row, col = 2, 0
        self.worksheet.set_column(col, col + 1, 15)
        self.worksheet.merge_range(row, col, row, col + 4, 'URL', column_format)
        
        # Set the current cell in row-col format for use later
        self.cur_cell = [2, 4]
        
    def write_to_worksheet(self, is_first):
        if self.worksheet is not None:
            url_format = self._url_format()
            self.worksheet.merge_range(
                self.cur_cell[0] + 2, 0, self.cur_cell[0] + 2, self.cur_cell[1], self.url, url_format
            )
            
            for results in [self.audit_results, self.metrics_results]:
                row, col = self.cur_cell[0], self.cur_cell[1] + 1
                new_pos = self._write_results(results, is_first, row=row, col=col)
                self.cur_cell = new_pos
            self.cur_cell[0] += 1
            self.cur_cell[1] = 4