
from pathlib import Path
from dataclasses import asdict

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment


def export_to_excel(companies):

    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    file_path = output_dir / "global_business_leads.xlsx"

    # Create workbook
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Business Leads"

    # Column headings
    headers = [
        "Business Name",
        "Category",
        "Website",
        "Email Addresses",
        "Phone Numbers",
        "Address",
        "City",
        "State / Province",
        "Country",
        "Address Source",
        "City Source",
        "Country Source",
        "Source URL",
        "Contact Page URLs",
        "Extraction Status"
    ]

    worksheet.append(headers)

    # Header styling
    for cell in worksheet[1]:

        cell.font = Font(
            bold=True,
            color="FFFFFF"
        )

        cell.fill = PatternFill(
            start_color="1F4E78",
            end_color="1F4E78",
            fill_type="solid"
        )

        cell.alignment = Alignment(
            horizontal="center",
            vertical="center",
            wrap_text=True
        )

    # Add business records
    for company in companies:

        company_data = asdict(company)

        worksheet.append([
            company_data.get("name", ""),
            company_data.get("category", ""),
            company_data.get("website", ""),
            ", ".join(company_data.get("emails", [])),
            ", ".join(company_data.get("phone_numbers", [])),
            company_data.get("address", ""),
            company_data.get("city", ""),
            company_data.get("state_province", ""),
            company_data.get("country", ""),
            company_data.get("address_source", ""),
            company_data.get("city_source", ""),
            company_data.get("country_source", ""),
            company_data.get("source_url", ""),
            ", ".join(company_data.get("contact_page_urls", [])),
            company_data.get("extraction_status", "")
        ])

        # Make website clickable (Column C)
        website_cell = worksheet.cell(
            row=worksheet.max_row,
            column=3
        )

        if website_cell.value:

            website_cell.hyperlink = website_cell.value
            website_cell.style = "Hyperlink"

    # Column widths
    column_widths = {
        "A": 40,
        "B": 22,
        "C": 40,
        "D": 35,
        "E": 35,
        "F": 50,
        "G": 20,
        "H": 22,
        "I": 18,
        "J": 18,
        "K": 18,
        "L": 18,
        "M": 40,
        "N": 45,
        "O": 22
    }

    for column, width in column_widths.items():

        worksheet.column_dimensions[column].width = width

    # Improve data readability
    for row in worksheet.iter_rows(min_row=2):

        for cell in row:

            cell.alignment = Alignment(
                vertical="top",
                wrap_text=True
            )

    # Adjust row heights
    worksheet.row_dimensions[1].height = 35

    # Freeze header row
    worksheet.freeze_panes = "A2"

    # Enable filters
    worksheet.auto_filter.ref = worksheet.dimensions

    # Save workbook
    workbook.save(file_path)

    print(f"\nExcel file saved: {file_path}")
    print(f"Total businesses exported: {len(companies)}")
