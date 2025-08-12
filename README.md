# Excel Import Django Project

This is a Django web application that allows users to upload an Excel file (`exam.xlsx`) and import its data into a SQLite database. The application processes multiple sheets, including user details, loan information, guarantees, and cheque statuses, while handling data integrity issues such as `NaN` values in ID fields. It provides a simple web interface for uploading files and a management command for direct imports.

## Features
- Upload Excel files via a web interface at `/upload/`.
- Process multiple sheets: `Users Tables`, `Lines`, `Guarantees`, `Loans`, `Collaterals Types`, `Cheque`, and `Cheque Status`.
- Handle `NaN` values in `ID` columns to prevent errors like `Field 'id' expected a number but got nan`.
- Store data in a SQLite database with proper relationships (e.g., ForeignKeys for users, guarantees, and collaterals).
- Management command (`import_excel`) for importing Excel files from the command line.
- Redirects from root URL (`/`) to the upload page.

## Prerequisites
- Python 3.8+
- Django 4.2+
- pandas 2.0+
- openpyxl 3.0+
- Git

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/excel-import-django.git
   cd excel-import-django
