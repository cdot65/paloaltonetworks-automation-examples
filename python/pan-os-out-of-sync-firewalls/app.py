"""Check the synchronization status of device groups and templates in Panorama and generate a PDF report.

This script connects to a Panorama appliance, retrieves lists of device groups and templates,
and generates a PDF report showing which ones are in sync (in green) and which are out of sync (in red).

(c) 2024 Your Name
"""

# standard library imports
import argparse
import logging
from pathlib import Path
from typing import Dict, List

# third party library imports
import requests
import urllib3
import xmltodict
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from config import settings

# Suppress InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ----------------------------------------------------------------------------
# Configure logging settings
# ----------------------------------------------------------------------------
logger = logging.getLogger(__name__)


def configure_logging(debug: bool = False) -> None:
    """Configure logging settings."""
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("panorama_sync_check.log"), logging.StreamHandler()],
    )


# ----------------------------------------------------------------------------
# Panorama API interaction
# ----------------------------------------------------------------------------
def get_panorama_data(cmd: str) -> Dict:
    """Retrieve data from Panorama."""
    url = f"https://{settings.hostname}/api/?type=op&cmd={cmd}"
    headers = {
        'X-PAN-KEY': settings.api_key
    }

    logger.info(f"Retrieving data from {settings.hostname}")
    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        logger.debug("Data retrieved successfully")
        return xmltodict.parse(response.text)
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve data: {e}")
        raise


def parse_sync_status(data: Dict, key: str) -> List[Dict]:
    """Parse the sync status data for device groups or templates."""
    items = []
    entries = data['response']['result'][key]['entry']

    if not isinstance(entries, list):
        entries = [entries]

    for entry in entries:
        name = entry['@name']
        is_synced = True
        devices = entry.get('devices', {}).get('entry', [])
        if not isinstance(devices, list):
            devices = [devices]

        for device in devices:
            if device.get('template-status', 'In Sync').lower() != 'in sync':
                is_synced = False
                break

        items.append({
            'name': name,
            'is_synced': is_synced
        })

    return items


# ----------------------------------------------------------------------------
# PDF Report Generation
# ----------------------------------------------------------------------------
def generate_pdf_report(device_groups: List[Dict], templates: List[Dict], output_file: str):
    """Generate a PDF report of the sync status."""
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("Panorama Sync Status Report", styles['Title']))
    elements.append(Spacer(1, 0.25 * inch))

    # Device Groups
    elements.append(Paragraph("Device Groups", styles['Heading2']))
    elements.append(Spacer(1, 0.1 * inch))
    dg_data = [["Device Group", "Status"]]
    for dg in device_groups:
        status = "In Sync" if dg['is_synced'] else "Out of Sync"
        color = colors.green if dg['is_synced'] else colors.red
        dg_data.append([dg['name'], status])

    dg_table = Table(dg_data, colWidths=[4 * inch, 2 * inch])
    dg_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (1, 1), (1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    for i, row in enumerate(dg_data[1:], start=1):
        color = colors.green if row[1] == "In Sync" else colors.red
        dg_table.setStyle(TableStyle([('TEXTCOLOR', (1, i), (1, i), color)]))

    elements.append(dg_table)
    elements.append(Spacer(1, 0.25 * inch))

    # Templates
    elements.append(Paragraph("Templates", styles['Heading2']))
    elements.append(Spacer(1, 0.1 * inch))
    template_data = [["Template", "Status"]]
    for template in templates:
        status = "In Sync" if template['is_synced'] else "Out of Sync"
        color = colors.green if template['is_synced'] else colors.red
        template_data.append([template['name'], status])

    template_table = Table(template_data, colWidths=[4 * inch, 2 * inch])
    template_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (1, 1), (1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    for i, row in enumerate(template_data[1:], start=1):
        color = colors.green if row[1] == "In Sync" else colors.red
        template_table.setStyle(TableStyle([('TEXTCOLOR', (1, i), (1, i), color)]))

    elements.append(template_table)

    # Build the PDF
    doc.build(elements)


# ----------------------------------------------------------------------------
# Main execution of our script
# ----------------------------------------------------------------------------
def main():
    """Main execution of the script."""
    parser = argparse.ArgumentParser(
        description="Check the synchronization status of device groups and templates in Panorama and generate a PDF "
                    "report."
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable debug logging"
    )
    parser.add_argument(
        "-o", "--output", type=str, default="panorama_sync_report.pdf", help="Output PDF file name"
    )
    args = parser.parse_args()

    configure_logging(args.debug)
    logger.info("Script execution started.")

    try:
        # Get and parse device groups
        device_groups_data = get_panorama_data("<show><devicegroups></devicegroups></show>")
        device_groups = parse_sync_status(device_groups_data, 'devicegroups')

        # Get and parse templates
        templates_data = get_panorama_data("<show><templates></templates></show>")
        templates = parse_sync_status(templates_data, 'templates')

        # Generate PDF report
        output_file = Path(args.output)
        generate_pdf_report(device_groups, templates, str(output_file))
        logger.info(f"PDF report generated: {output_file.resolve()}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

    logger.info("Script execution completed.")


# ----------------------------------------------------------------------------
# Execute main function
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
