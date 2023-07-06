"""Excel workbook operations for writing PSI API results to Excel."""

import logging
from dataclasses import dataclass, field
from typing import Any, TypeAlias, Union, cast

from xlsxwriter import Workbook
from xlsxwriter.format import Format

AuditResults: TypeAlias = dict[str, tuple[Union[int, float]]]
MetricsResults: TypeAlias = Union[dict[str, Union[int, float]], None]

logger = logging.getLogger(__name__)


@dataclass
class ExcelWorkbook:
    """Class for creating an Excel Workbook and writing the PSI API results to it."""

    url: str
    metadata: dict[str, Any]
    audit_results: AuditResults
    metrics_results: MetricsResults = None
    workbook: Workbook = None
    worksheet: Workbook.worksheet_class = None
    cur_cell: list[int] = field(default_factory=list)
    category_scores: list[int] = field(default_factory=list)
    metrics_scores: list[int | float] = field(default_factory=list)

    def set_up_worksheet(self) -> None:
        """Creates the workbook, adds a worksheet, and sets up column headings."""
        self._create_workbook()
        self.worksheet = self.workbook.add_worksheet()
        logger.info("Excel worksheet created in workbook.")

        self.cur_cell = [0, 0]
        row, col = self.cur_cell  # First cell
        column_format = self._column_format()
        metadata_format = self._metadata_format()

        # Add metadata to the first cell of the Excel sheet.
        logger.info("Writing metadata to worksheet.")
        category = self.metadata["category"].upper()
        strategy = self.metadata["strategy"].upper()
        metadata_value = f"{strategy} {category}"
        self.worksheet.write(row, col, metadata_value, metadata_format)

        # Add the URL heading with a wider column of merged cells.
        row += 2
        # col += 1
        url_col_width = 4
        self.worksheet.set_column(col, col, 15)
        self.worksheet.merge_range(
            row, col, row, col + url_col_width, "URL", column_format
        )

        # Add a column heading to record each page's overall category score.
        col += url_col_width + 1
        self.worksheet.write(row, col, "OVR", column_format)
        self.cur_cell = [row, col]  # Set current cell for later use

    def write_to_worksheet(self, first_resp: bool) -> None:
        """Writes the URL, OVR page score, audit and metrics results to the sheet."""
        if self.worksheet is None:
            # Fallback if worksheet doesn't exist for some reason
            logger.warning("Worksheet not found. Creating.")
            self.set_up_worksheet()

        self._write_page_url()
        self._write_overall_category_score()
        self._write_metrics_results(first_resp)
        self._write_audit_results(first_resp)

        self.cur_cell[0] += 1  # Move down 1 row for next page's results
        self.cur_cell[1] = 5  # Reset to first results column

    def finalize_and_save(self) -> None:
        """Writes the average score to the worksheet and saves/closes it."""
        self._write_average_scores()
        self.workbook.close()
        logger.info("Workbook saved. Check your current directory!")

    def _create_workbook(self) -> None:
        """Creates an Excel workbook with a unique and descriptive name."""
        strategy = self.metadata["strategy"]
        category = self.metadata["category"]
        date = self.metadata["timestamp"]
        self.workbook = Workbook(f"psi-s-{strategy}-c-{category}-{date}.xlsx")
        logger.info("Excel workbook created.")

    def _write_page_url(self) -> None:
        """Writes the requested page URL being analyzed to the sheet."""
        logger.info("Writing page URL to worksheet.")
        url_format = self._url_format()
        row = self.cur_cell[0] + 2
        self.worksheet.merge_range(
            row, 0, row, self.cur_cell[1] - 1, self.url, url_format
        )

    def _write_overall_category_score(self) -> None:
        """Writes the OVR category score for the page to the sheet."""
        logger.info("Writing overall category score to worksheet.")
        category_score = self.metadata["category_score"] * 100
        cat_score_format = self._score_format(category_score)

        self.worksheet.write(
            self.cur_cell[0] + 2, self.cur_cell[1], category_score, cat_score_format
        )
        self.cur_cell[1] += 2
        # Add the score to a list so they can all be averaged at the end.
        self.category_scores.append(category_score)

    def _write_average_scores(self) -> None:
        """Writes the average scores next to the worksheet metadata."""
        logger.info("Writing average scores to worksheet.")
        format = self._metadata_format()

        # Audits avg
        cat_scores = self.category_scores
        cat_score = self._avg_and_round_scores(cat_scores)
        self.worksheet.write(0, 4, f"Cat. Score: {str(cat_score)}", format)

        # Metrics avg
        if self.metrics_scores:
            m_scores = self.metrics_scores
            avg_m_score = self._avg_and_round_scores(m_scores)
            self.worksheet.write(0, 7, f"Metrics Avg: {str(avg_m_score)}", format)

    def _write_audit_results(self, first_resp: bool) -> None:
        """Iterates through the audit results and writes them to the worksheet."""
        column_format = self._column_format()
        row, col = self.cur_cell

        logger.info("Writing audit results to worksheet.")
        for title, scores in self.audit_results.items():
            self.worksheet.set_column(col, col + 1, 15)
            # cast() is a mypy workaround for issue #1178
            score, value = cast(tuple[Any, Any], scores)
            score_format = self._score_format(score)
            if first_resp:
                logger.debug("Writing audit result headings to worksheet.")
                self._write_results_headings(
                    row, col, title, column_format, result_type="audit"
                )
            self.worksheet.write(row + 2, col, score, score_format)
            self.worksheet.write(row + 2, col + 1, value, score_format)
            col += 2

    def _write_metrics_results(self, first_resp: bool) -> None:
        """Iterates through the metrics results and writes them to the worksheet."""
        column_format = self._column_format()
        row, col = self.cur_cell

        if self.metrics_results is not None:
            logger.info("Writing metrics results to worksheet.")
            ovr_score = 0
            for title, score in self.metrics_results.items():
                self.worksheet.set_column(col, col, 10)
                if first_resp:
                    logger.debug("Writing metrics result headings to worksheet.")
                    self._write_results_headings(
                        row, col, title, column_format, result_type="metrics"
                    )
                score_format = self._score_format(score)
                self.worksheet.write(row + 2, col, score, score_format)
                ovr_score += score
                col += 1

            # For indiv. URL - will be averaged at the end
            ovr_score = ovr_score / len(self.metrics_results)
            ovr_score = round(ovr_score, 1)
            self.metrics_scores.append(ovr_score)

            self.cur_cell[1] = col + 2  # Don't overwrite metrics with audits

        elif self.metrics_scores:
            # No metrics results for this URL but previous URLs have written scores
            # Needed for formatting reasons (set column to align with audit scores)
            self.cur_cell[1] = 16

    def _write_results_headings(
        self, row: int, col: int, title: str, column_format: Format, result_type: str
    ) -> None:
        """Writes the headings for audit or metrics results to the worksheet."""
        if result_type == "audit":
            self.worksheet.merge_range(row, col, row, col + 1, title, column_format)
            self.worksheet.write(row + 1, col, "Score", column_format)
            self.worksheet.write(row + 1, col + 1, "Value", column_format)
        elif result_type == "metrics":
            self.worksheet.write(row, col, title, column_format)
            self.worksheet.write(row + 1, col, "Score", column_format)

    def _avg_and_round_scores(self, scores):
        """Helper for averaging and rounding scores."""
        scores = sum(scores) / len(scores)
        return round(scores, 1)

    def _column_format(self) -> Format:
        """Reusable formatting for column cells."""
        return self.workbook.add_format(
            {"font_size": 16, "bold": 1, "align": "center", "valign": "vcenter"}
        )

    def _data_format(self) -> Format:
        """Reusable formatting for cells with regular data."""
        return self.workbook.add_format(
            {"font_size": 14, "align": "center", "valign": "vcenter"}
        )

    def _url_format(self) -> Format:
        """Reusable formatting for cells with URLs."""
        return self.workbook.add_format(
            {"font_size": 14, "align": "left", "valign": "vcenter"}
        )

    def _metadata_format(self) -> Format:
        """Reusable formatting for cells with metadata."""
        return self.workbook.add_format(
            {"font_size": 20, "bold": 1, "align": "left", "valign": "vcenter"}
        )

    def _score_format(self, score: Union[int, float]) -> Format:
        """Reusable formatting and color coding for cells with scores."""

        def find_color_match(formats: dict[str, bool]) -> str:
            for color, in_range in formats.items():
                if in_range:
                    return color
            return "n/a"

        if score == "n/a":
            color = "white"
        else:
            score_formats = {
                "lime": score >= 90,
                "green": 90 > score >= 80,
                "yellow": 80 > score >= 70,
                "orange": 70 > score >= 60,
                "brown": 60 > score >= 50,
                "red": 50 > score,
            }
            color = find_color_match(score_formats)
        return self.workbook.add_format(
            {"bg_color": color, "font_size": 14, "align": "center", "valign": "vcenter"}
        )
