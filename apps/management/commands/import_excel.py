import pandas as pd
import numpy as np
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from ...models import User, Line, Guarantee, Loan, CollateralType, Cheque, ChequeStatus


def import_excel_to_db(file_path):
    try:
        xls = pd.ExcelFile(file_path)

        def clean_df(df):
            df = df.dropna(how='all')  # Drop entirely blank rows
            df = df.replace({np.nan: None})  # Replace NaN with None for Django
            return df

        # Import Users Tables
        if 'Users Tables' in xls.sheet_names:
            df_users = pd.read_excel(xls, sheet_name='Users Tables')
            df_users = clean_df(df_users)
            df_users = df_users[df_users['ID'].notna()]
            df_users['ID'] = pd.to_numeric(df_users['ID'], errors='coerce').astype('Int64')
            for _, row in df_users.iterrows():
                try:
                    User.objects.update_or_create(
                        id=row['ID'],
                        defaults={
                            'name': row['Name'],
                            'last_name': row['Last Name'],
                            'national_id': row['National ID'],
                            'birth_date': row['Birth Date'],
                            'phone_number': row['phone Number'],
                        }
                    )
                except ValidationError as e:
                    print(f"User row {row['ID']}: {e}")
                    continue

        # Import Collaterals Types
        if 'Collaterals Types' in xls.sheet_names:
            df_coll = pd.read_excel(xls, sheet_name='Collaterals Types')
            df_coll = clean_df(df_coll)
            df_coll = df_coll[df_coll['ID'].notna()]
            df_coll['ID'] = pd.to_numeric(df_coll['ID'], errors='coerce').astype('Int64')
            for _, row in df_coll.iterrows():
                try:
                    CollateralType.objects.update_or_create(
                        id=row['ID'],
                        defaults={
                            'collateral_type': row['Collateral Type'],
                            'collateral_info': row['Collateral Info'],
                        }
                    )
                except ValidationError as e:
                    print(f"CollateralType row {row['ID']}: {e}")
                    continue

        # Import Lines
        if 'Lines' in xls.sheet_names:
            df_lines = pd.read_excel(xls, sheet_name='Lines')
            df_lines = clean_df(df_lines)
            df_lines = df_lines[df_lines['ID'].notna()]
            df_lines['ID'] = pd.to_numeric(df_lines['ID'], errors='coerce').astype('Int64')
            for _, row in df_lines.iterrows():
                try:
                    coll1 = CollateralType.objects.filter(id=row['Collateral_Type1']).first() if row[
                        'Collateral_Type1'] else None
                    coll2 = CollateralType.objects.filter(id=row['Collateral_Type2']).first() if row[
                        'Collateral_Type2'] else None
                    coll3 = CollateralType.objects.filter(id=row['Collateral_Type3']).first() if row[
                        'Collateral_Type3'] else None
                    Line.objects.update_or_create(
                        id=row['ID'],
                        defaults={
                            'line_name': row['Line Name'],
                            'beneficiary': row['Beneficiary'],
                            'interest_rate': row['Interest_Rate'],
                            'installment_count': row['Installment_Count'],
                            'comission_fee': row['Comission Fee'],
                            'deposite_rate': row['Deposite_Rate'],
                            'collateral_type1': coll1,
                            'collateral_type2': coll2,
                            'collateral_type3': coll3,
                            'leeway': row['Leeway'],
                            'action1': row.get('action1'),
                            'action2': row.get('action2'),
                            'action3': row.get('action3'),
                            'action4': row.get('action4'),
                            'action5': row.get('action5'),
                            'action6': row.get('action6'),
                            'action7': row.get('action7'),
                            'action8': row.get('action8'),
                            'action9': row.get('action9'),
                            'action10': row.get('action10'),
                        }
                    )
                except ValidationError as e:
                    print(f"Line row {row['ID']}: {e}")
                    continue

        # Import Guarantees
        if 'Guarantees' in xls.sheet_names:
            df_guar = pd.read_excel(xls, sheet_name='Guarantees')
            df_guar = clean_df(df_guar)
            df_guar = df_guar[df_guar['ID'].notna()]
            df_guar['ID'] = pd.to_numeric(df_guar['ID'], errors='coerce').astype('Int64')
            for _, row in df_guar.iterrows():
                try:
                    line = Line.objects.filter(id=row['Line']).first()
                    if line:
                        Guarantee.objects.update_or_create(
                            id=row['ID'],
                            defaults={
                                'guarantee_number': row['Guarantee Number'],
                                'issue_gregorian_date': row['Issue Gregorian  Date'],
                                'issue_shamsi_date': row['Issue Shamsi Date'],
                                'line': line,
                            }
                        )
                except ValidationError as e:
                    print(f"Guarantee row {row['ID']}: {e}")
                    continue

        # Import Loans
        if 'Loans' in xls.sheet_names:
            df_loans = pd.read_excel(xls, sheet_name='Loans')
            df_loans = clean_df(df_loans)
            df_loans = df_loans[df_loans['ID'].notna()]
            df_loans['ID'] = pd.to_numeric(df_loans['ID'], errors='coerce').astype('Int64')
            for _, row in df_loans.iterrows():
                try:
                    guarantee = Guarantee.objects.filter(id=row['Guarantee_ID']).first()
                    user1 = User.objects.filter(id=row['User_ID']).first()
                    user2 = User.objects.filter(id=row['User_ID2']).first() if row['User_ID2'] else None
                    user3 = User.objects.filter(id=row['User_ID3']).first() if row['User_ID3'] else None
                    coll1 = Cheque.objects.filter(id=row['Collateral_ID']).first() if row['Collateral_ID'] else None
                    coll2 = Cheque.objects.filter(id=row['Collateral_ID2']).first() if row['Collateral_ID2'] else None
                    coll3 = Cheque.objects.filter(id=row['Collateral_ID3']).first() if row['Collateral_ID3'] else None
                    if guarantee and user1:
                        Loan.objects.update_or_create(
                            id=row['ID'],
                            defaults={
                                'guarantee': guarantee,
                                'loan_number': row['Loan Number'],
                                'loan_amount': row['Loan Amount'],
                                'issue_date': row['Issue Date'],
                                'comission_amount': row['Comission_Amount'],
                                'deposite_amount': row['Deposite_Amount'],
                                'user': user1,
                                'user2': user2,
                                'user3': user3,
                                'collateral': coll1,
                                'collateral2': coll2,
                                'collateral3': coll3,
                            }
                        )
                except ValidationError as e:
                    print(f"Loan row {row['ID']}: {e}")
                    continue

        # Import Cheque
        if 'Cheque' in xls.sheet_names:
            df_cheque = pd.read_excel(xls, sheet_name='Cheque')
            df_cheque = clean_df(df_cheque)
            df_cheque = df_cheque[df_cheque['ID'].notna()]
            df_cheque['ID'] = pd.to_numeric(df_cheque['ID'], errors='coerce').astype('Int64')
            for _, row in df_cheque.iterrows():
                try:
                    user = User.objects.filter(id=row['User ID']).first()
                    loan = Loan.objects.filter(id=row['Loan ID']).first()
                    if user and loan:
                        Cheque.objects.update_or_create(
                            id=row['ID'],
                            defaults={
                                'user': user,
                                'loan': loan,
                                'sayadi_id': row['Sayadi ID'],
                                'cheque_date': row['Cheque Date'],
                                'cheque_amount': row['Cheque amount'],
                                'holder': row['Holder'],
                                'transfer_date': row['Transfer Date'],
                                'sayad_transfer': row['Sayad Transfer?'],
                            }
                        )
                except ValidationError as e:
                    print(f"Cheque row {row['ID']}: {e}")
                    continue

        # Import Cheque Status
        if 'Cheque Status' in xls.sheet_names:
            df_status = pd.read_excel(xls, sheet_name='Cheque Status')
            df_status = clean_df(df_status)
            df_status = df_status[df_status['ID'].notna()]
            df_status['ID'] = pd.to_numeric(df_status['ID'], errors='coerce').astype('Int64')
            for _, row in df_status.iterrows():
                try:
                    cheque = Cheque.objects.filter(id=row['Cheque ID']).first()
                    if cheque:
                        ChequeStatus.objects.update_or_create(
                            id=row['ID'],
                            defaults={
                                'cheque': cheque,
                                'cheque_status': row['Cheque Status'],
                                'inquiry_date': row['Inquiry date'],
                            }
                        )
                except ValidationError as e:
                    print(f"ChequeStatus row {row['ID']}: {e}")
                    continue

        return "Import successful! Data loaded into database."

    except Exception as e:
        return f"Error during import: {str(e)}"


class Command(BaseCommand):
    help = 'Imports data from an Excel file into the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        result = import_excel_to_db(file_path)
        self.stdout.write(self.style.SUCCESS(result))