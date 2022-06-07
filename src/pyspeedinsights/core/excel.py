from dataclasses import dataclass, field

import xlsxwriter


@dataclass
class ExcelWorkbook:
    """Class for creating an Excel Workbook and writing the PSI API results to it."""

    url: str
    metadata: dict
    audit_results: dict
    metrics_results: dict = None
    workbook: xlsxwriter.Workbook = None
    worksheet: xlsxwriter.Workbook.worksheet_class = None
    cur_cell: list[int] = None
    category_scores: list[int] = field(default_factory=list)

    def set_up_worksheet(self):
        """Create the workbook, add a worksheet, and set up column headings."""

        self._create_workbook()
        self.worksheet = self.workbook.add_worksheet()

        row, col = 0, 0  # First cell
        column_format = self._column_format()
        metadata_format = self._metadata_format()

        # Add metadata to the first cell of the Excel sheet.
        category = self.metadata["category"].upper()
        strategy = self.metadata["strategy"].upper()
        metadata_value = f"{strategy} {category} REPORT"
        self.worksheet.write(row, col, metadata_value, metadata_format)

        # Add the URL heading with a wider column of merged cells.
        row += 2
        col += 1
        self.worksheet.set_column(col, col, 15)
        self.worksheet.merge_range(row, col, row, col + 3, "URL", column_format)

        # Add a column heading for each page's overall category score.
        col += 4
        self.worksheet.write(row, col, "Ovr", column_format)

        # Set the current cell in [row, col] format for later use.
        self.cur_cell = [row, col]

    def write_to_worksheet(self, is_first):
        """Write the URL, overall page score, audit and metrics results to the sheet."""

        if self.worksheet is not None:
            # Write the results to the Excel sheet.
            self._write_page_url()
            self._write_overall_category_score()
            self._write_audit_results(self.audit_results, is_first)

            if self.metrics_results is not None:
                self._write_metrics_results(self.metrics_results, is_first)

            # Move one row down for the next page and reset the column.
            self.cur_cell[0] += 1
            self.cur_cell[1] = 5
        else:
            raise ValueError("The worksheet is not set up. ")

    def finalize_and_save(self):
        """Write the average score to the workbook and save/close it."""

        self._write_average_score()

        self.workbook.close()
        print("Workbook saved. Check your current directory!")

    def _create_workbook(self):
        """Create an Excel workbook with a unique and descriptive name."""

        strategy = self.metadata["strategy"]
        category = self.metadata["category"]
        date = self.metadata["timestamp"]

        self.workbook = xlsxwriter.Workbook(
            f"psi-s-{strategy}-c-{category}-{date}.xlsx"
        )

    def _write_overall_category_score(self):
        """Write the ovr category score for the page / URL to the sheet."""

        category_score = self.metadata["category_score"] * 100
        cat_score_format = self._score_format(category_score)

        self.worksheet.write(
            self.cur_cell[0] + 2, self.cur_cell[1], category_score, cat_score_format
        )

        self.cur_cell[1] += 2

        # Add the score to a list so they can all be averaged at the end.
        self.category_scores.append(category_score)

    def _write_average_score(self):
        """Write the average score next to the worksheet metadata."""

        scores = self.category_scores
        avg_score = sum(scores) / len(scores)
        avg_score = round(avg_score, 2)

        format = self._metadata_format()
        self.worksheet.write(0, 4, f"Avg Score: {avg_score}", format)

    def _write_page_url(self):
        """
        Write the requested page URL being analyzed to the sheet.

        self.cur_cell: Row 2, Col 5
        """
        url_format = self._url_format()

        row = self.cur_cell[0] + 2

        self.worksheet.merge_range(
            row, 0, row, self.cur_cell[1] - 1, self.url, url_format
        )

    def _write_audit_results(self, audit_results, is_first):
        """Iterate through the audit results and write them to the worksheet."""

        column_format = self._column_format()
        row, col = self.cur_cell[0], self.cur_cell[1]

        for k, v in audit_results.items():
            self.worksheet.set_column(col, col + 1, 15)

            score = v[0]
            value = v[1]
            score_format = self._score_format(score)

            if is_first:
                self._write_results_headings(
                    row, col, k, column_format, result_type="audit"
                )
            self.worksheet.write(row + 2, col, score, score_format)
            self.worksheet.write(row + 2, col + 1, value, score_format)

            col += 2

        self.cur_cell[1] = col + 2

    def _write_metrics_results(self, metrics_results, is_first):
        """Iterate through the metrics results and write them to the worksheet."""

        column_format = self._column_format()
        data_format = self._data_format()
        row, col = self.cur_cell[0], self.cur_cell[1]

        for k, v in metrics_results.items():
            self.worksheet.set_column(col, col, 30)

            if is_first:
                self._write_results_headings(
                    row, col, k, column_format, result_type="metrics"
                )
            self.worksheet.write(row + 2, col, v, data_format)
            col += 1

    def _write_results_headings(self, row, col, k, column_format, result_type):
        """Write the headings for audit or metrics results to the worksheet."""

        if result_type == "audit":
            self.worksheet.merge_range(row, col, row, col + 1, k, column_format)
            self.worksheet.write(row + 1, col, "Score", column_format)
            self.worksheet.write(row + 1, col + 1, "Value", column_format)
        elif result_type == "metrics":
            self.worksheet.write(row, col, k, column_format)
            self.worksheet.write(row + 1, col, "Value", column_format)

    def _column_format(self):
        """Reusable formatting for column cells."""

        return self.workbook.add_format(
            {"font_size": 16, "bold": 1, "align": "center", "valign": "vcenter"}
        )

    def _data_format(self):
        """Reusable formatting for cells with regular data."""

        return self.workbook.add_format(
            {"font_size": 14, "align": "center", "valign": "vcenter"}
        )

    def _url_format(self):
        """Reusable formatting for cells with URLs."""

        return self.workbook.add_format(
            {"font_size": 14, "align": "left", "valign": "vcenter"}
        )

    def _metadata_format(self):
        """Reusable formatting for cells with metadata."""

        return self.workbook.add_format(
            {"font_size": 20, "bold": 1, "align": "left", "valign": "vcenter"}
        )

    def _score_format(self, score):
        """Reusable formatting and color coding for cells with scores."""

        if score == "n/a":
            color = "white"
        elif score >= 90:
            color = "lime"
        elif 90 > score >= 80:
            color = "green"
        elif 80 > score >= 70:
            color = "yellow"
        elif 70 > score >= 60:
            color = "orange"
        elif 60 > score >= 50:
            color = "brown"
        elif 50 > score:
            color = "red"

        return self.workbook.add_format(
            {"bg_color": color, "font_size": 14, "align": "center", "valign": "vcenter"}
        )
