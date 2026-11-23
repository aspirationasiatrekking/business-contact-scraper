
from pathlib import Path
from dataclasses import asdict
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter


def export_to_excel(companies):

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    file_path = output_dir / "global_business_leads.xlsx"

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Business Leads"

    headers = [
        "Business Name",
        "Website",
        "Email Addresses",
        "Phone Numbers",
        "Extraction Status"
    ]

    worksheet.append(headers)

    # Header styling
    for cell in worksheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(
            start_color="1F4E78",
            end_color="1F4E78",
            fill_type="solid"
        )
        cell.alignment = Alignment(horizontal="center")

    # Add business records
    for company in companies:

        company_data = asdict(company)

        worksheet.append([
            company_data.get("name", ""),
            company_data.get("website", ""),
            ", ".join(company_data.get("emails", [])),
            ", ".join(company_data.get("phone_numbers", [])),
            company_data.get("extraction_status", "")
        ])

        # Make website clickable
        website_cell = worksheet.cell(
            row=worksheet.max_row,
            column=2
        )

        if website_cell.value:
            website_cell.hyperlink = website_cell.value
            website_cell.style = "Hyperlink"

    # Column widths
    column_widths = {
        "A": 45,
        "B": 45,
        "C": 40,
        "D": 45,
        "E": 25
}   

    for column, width in column_widths.items():
        worksheet.column_dimensions[column].width = width

    # Improve readability
    for row in worksheet.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(
                vertical="top",
                wrap_text=True
            )

    worksheet.freeze_panes = "A2"
    worksheet.auto_filter.ref = worksheet.dimensions

    workbook.save(file_path)

    print(f"\nExcel file saved: {file_path}")
    print(f"Total businesses exported: {len(companies)}")
