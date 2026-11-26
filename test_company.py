
from backend.database.operations import (
    add_company,
    get_all_companies
)

company_data = {
    "company_name": "TCS",
    "industry": "Information Technology",
    "website": "https://www.tcs.com",
    "location": "Mohali",
    "contact_person": "HR Department",
    "contact_email": "hr@example.com",
    "contact_phone": "9876543210",
    "company_description": "IT services and consulting company.",
    "created_by": 1
}

try:
    company_id = add_company(company_data)

    print("Company added successfully!")
    print("Company ID:", company_id)

    companies = get_all_companies()

    print("\nCompany Records:")
    print(companies)

except Exception as e:
    print("Error:", e)
