#!/usr/bin/env python3
"""
Test script to verify Google Sheets access
"""

import gspread
from google.oauth2.service_account import Credentials

def test_sheets_access():
    print("\n" + "="*70)
    print("  GOOGLE SHEETS ACCESS TEST")
    print("="*70 + "\n")
    
    # 1. Load credentials
    print("1. Loading credentials...")
    try:
        creds = Credentials.from_service_account_file(
            'credentials.json',
            scopes=[
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
        )
        print(f"   ✓ Credentials loaded")
        print(f"   Service Account: {creds.service_account_email}")
    except Exception as e:
        print(f"   ✗ Error loading credentials: {e}")
        return
    
    # 2. Authorize client
    print("\n2. Authorizing client...")
    try:
        client = gspread.authorize(creds)
        print("   ✓ Client authorized")
    except Exception as e:
        print(f"   ✗ Error authorizing: {e}")
        return
    
    # 3. List all accessible sheets
    print("\n3. Listing all accessible sheets...")
    try:
        sheets = client.openall()
        if sheets:
            print(f"   ✓ Found {len(sheets)} accessible sheet(s):")
            for sheet in sheets:
                print(f"      - {sheet.title}")
                print(f"        URL: {sheet.url}")
        else:
            print("   ⚠️  No sheets accessible to this service account")
            print("\n" + "="*70)
            print("  TROUBLESHOOTING STEPS:")
            print("="*70)
            print("\n1. Go to your Google Sheet: 'EA Job Outreach Pipeline'")
            print("\n2. Click the 'Share' button (top right)")
            print("\n3. Add this email as Editor:")
            print(f"   {creds.service_account_email}")
            print("\n4. Make sure to:")
            print("   - Grant 'Editor' permissions")
            print("   - Click 'Send' or 'Done'")
            print("\n5. Run this script again to verify")
            print("="*70 + "\n")
    except Exception as e:
        print(f"   ✗ Error listing sheets: {e}")
        return
    
    # 4. Try to open specific sheet
    print("\n4. Trying to open 'EA Job Outreach Pipeline'...")
    try:
        sheet = client.open("EA Job Outreach Pipeline")
        print(f"   ✓ Successfully opened sheet!")
        print(f"   URL: {sheet.url}")
        
        # Try to read first row
        worksheet = sheet.sheet1
        headers = worksheet.row_values(1)
        if headers:
            print(f"   ✓ Headers: {headers}")
        else:
            print("   ⚠️  Sheet is empty (no headers)")
            
    except gspread.SpreadsheetNotFound:
        print("   ✗ Sheet not found or not shared with service account")
        print("\n   Please share the sheet with:")
        print(f"   {creds.service_account_email}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    test_sheets_access()
