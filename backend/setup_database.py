import sqlite3
import pandas as pd

import os

def create_database():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'janmitra_schemes.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Drop and recreate table with richer schema
    cursor.execute('DROP TABLE IF EXISTS schemes')
    cursor.execute('''
    CREATE TABLE schemes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scheme_name TEXT NOT NULL,
        hindi_name TEXT,
        ministry TEXT,
        category TEXT,
        sub_category TEXT,
        launch_year INTEGER,
        scheme_type TEXT,
        beneficiary_type TEXT,
        age_min INTEGER,
        age_max INTEGER,
        age_note TEXT,
        income_limit TEXT,
        income_annual_max INTEGER,
        gender TEXT,
        caste_category TEXT,
        state_applicability TEXT,
        benefits TEXT,
        benefit_amount TEXT,
        documents_required TEXT,
        application_mode TEXT,
        portal_url TEXT,
        helpline TEXT,
        process TEXT,
        status TEXT DEFAULT 'Active'
    )
    ''')

    schemes_data = [
        # Agriculture
        (
            "PM-Kisan Samman Nidhi", "प्रधानमंत्री किसान सम्मान निधि", "Ministry of Agriculture & Farmers Welfare",
            "Agriculture", "Income Support", 2019, "Central", "Small & Marginal Farmers",
            18, 70, "No upper age limit for farmers", "Land holding up to 2 hectares", None,
            "All", "All categories", "All States & UTs",
            "Direct income support of Rs.6,000/year in 3 equal installments of Rs.2,000 directly to bank account",
            "Rs.6,000 per year", "Aadhaar Card, Bank Passbook, Land Records (Khatoni/Khatauni), Self-declaration",
            "Online (pmkisan.gov.in) / CSC / Local Lekhpal", "https://pmkisan.gov.in", "155261",
            "Register at pmkisan.gov.in or visit your village Lekhpal / Patwari. Link Aadhaar with bank account. After verification by state, funds are directly transferred.",
            "Active"
        ),
        (
            "PM Fasal Bima Yojana (PMFBY)", "प्रधानमंत्री फसल बीमा योजना", "Ministry of Agriculture & Farmers Welfare",
            "Agriculture", "Crop Insurance", 2016, "Central", "Farmers growing notified crops",
            18, 999, "No upper age limit", "No income limit for enrolled farmers", None,
            "All", "All", "All States & UTs",
            "Crop insurance coverage against natural calamities, pests, and diseases. Farmers pay very low premium (2% Kharif, 1.5% Rabi, 5% Horticulture).",
            "Full sum insured (varies by crop/district)", "Aadhaar, Bank account, Land records, Sowing certificate",
            "Online (pmfby.gov.in) / Nearest bank / CSC", "https://pmfby.gov.in", "14447",
            "Contact your nearest bank branch or insurance company before the crop season deadline. Get Kisan Credit Card if not already enrolled.",
            "Active"
        ),
        (
            "Kisan Credit Card (KCC)", "किसान क्रेडिट कार्ड", "Ministry of Agriculture & Farmers Welfare",
            "Agriculture", "Credit & Loans", 1998, "Central", "Farmers, Fishermen, Animal Husbandry",
            18, 75, "Maximum 75 years with co-borrower", "Based on crop area and production costs", None,
            "All", "All", "All States & UTs",
            "Short-term crop loan at subsidized interest rate (4% effective after subvention). Credit limit up to Rs.3 lakh without collateral.",
            "Up to Rs.3 Lakh (collateral-free)", "Aadhaar, PAN, Land records, Passport photo, Bank account",
            "Nearest bank / Cooperative bank / RRB", "https://agricoop.gov.in", "0120-6025109",
            "Visit nearest bank. Fill KCC application form with land records. Bank sanctions limit based on crop area. Card issued within 14 days.",
            "Active"
        ),
        # Health
        (
            "Ayushman Bharat PM-JAY", "आयुष्मान भारत प्रधानमंत्री जन आरोग्य योजना", "Ministry of Health & Family Welfare",
            "Health", "Health Insurance", 2018, "Central", "Economically Weaker Sections (SECC 2011)",
            0, 999, "No age limit - entire family covered", "SECC 2011 database / State BPL list", None,
            "All", "SC/ST/OBC priority; All eligible", "All States (except some)",
            "Cashless health insurance up to Rs.5 Lakh per family per year. Covers 1,929+ medical packages including surgeries, chemotherapy, ICU care at empanelled hospitals.",
            "Rs.5 Lakh per family per year", "Aadhaar, Ration Card, Mobile number",
            "Nearest empanelled hospital / Ayushman Mitra / PMJAY portal", "https://pmjay.gov.in", "14555",
            "Check eligibility at pmjay.gov.in or call 14555. Visit nearest empanelled hospital / Ayushman Mitra kiosk. Show Aadhaar to get Ayushman Card. Treatment is 100% cashless.",
            "Active"
        ),
        (
            "Pradhan Mantri Suraksha Bima Yojana (PMSBY)", "प्रधानमंत्री सुरक्षा बीमा योजना", "Ministry of Finance",
            "Health", "Accident Insurance", 2015, "Central", "Bank account holders",
            18, 70, "Between 18 and 70 years", "No income limit", None,
            "All", "All", "All States & UTs",
            "Accidental death and disability insurance. Rs.2 Lakh on accidental death/full disability. Rs.1 Lakh on partial disability. Annual premium only Rs.20.",
            "Rs.2 Lakh (death/full disability), Rs.1 Lakh (partial disability)", "Aadhaar, Bank account linked to Aadhaar",
            "Bank / Post Office / Online", "https://jansuraksha.gov.in", "1800-180-1111",
            "Visit your bank branch or net banking and enroll in PMSBY. Just Rs.20 auto-debited annually from your account. Nomination must be provided.",
            "Active"
        ),
        (
            "Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY)", "प्रधानमंत्री जीवन ज्योति बीमा योजना", "Ministry of Finance",
            "Health", "Life Insurance", 2015, "Central", "Bank account holders",
            18, 50, "Between 18 and 50 years (renewable till 55)", "No income limit", None,
            "All", "All", "All States & UTs",
            "Life insurance cover of Rs.2 Lakh for death due to any reason. Annual premium only Rs.436.",
            "Rs.2 Lakh on death (any cause)", "Aadhaar, Bank account",
            "Bank / Post Office / Online banking", "https://jansuraksha.gov.in", "1800-180-1111",
            "Enroll through your bank (net banking or branch). Rs.436 per year auto-debited. Covers death from any cause including illness.",
            "Active"
        ),
        # Housing
        (
            "PM Awas Yojana - Urban (PMAY-U)", "प्रधानमंत्री आवास योजना (शहरी)", "Ministry of Housing & Urban Affairs",
            "Housing", "Home Loan Subsidy", 2015, "Central", "Urban Poor - EWS, LIG, MIG",
            21, 999, "Adult earning member", "EWS: Up to Rs.3 Lakh/yr; LIG: Rs.3-6 Lakh/yr; MIG-I: Rs.6-12 Lakh/yr; MIG-II: Rs.12-18 Lakh/yr", None,
            "All", "All (SC/ST/Minority/Women priority)", "Urban areas (all cities)",
            "Interest subsidy on home loans (CLSS). EWS: 6.5% subsidy (up to Rs.6 Lakh loan). LIG: 6.5%. MIG-I: 4% (up to Rs.9 Lakh). Beneficiary must not own a pucca house.",
            "Subsidy: Rs.2.20 Lakh (EWS/LIG) to Rs.2.35 Lakh (MIG-I)", "Aadhaar, Income proof, Property documents, Bank account, Passport photo",
            "Online (pmaymis.gov.in) / Banks / HFCs / CSC", "https://pmaymis.gov.in", "1800-11-6163",
            "Apply online at pmaymis.gov.in or through your home loan bank. First check you do not own a pucca house anywhere in India. Submit income proof and Aadhaar.",
            "Active"
        ),
        (
            "PM Awas Yojana - Gramin (PMAY-G)", "प्रधानमंत्री आवास योजना (ग्रामीण)", "Ministry of Rural Development",
            "Housing", "House Construction Grant", 2016, "Central", "Houseless / Kutcha house - BPL Rural",
            18, 999, "Adult member of BPL household", "BPL / SECC 2011 listed households", None,
            "All", "SC/ST/Minorities/Women priority", "Rural areas only",
            "Financial assistance of Rs.1.20 Lakh (plains) or Rs.1.30 Lakh (hilly/NE states) to construct a pucca house with toilet. Additional support from MGNREGS (90-95 days wages).",
            "Rs.1.20-1.30 Lakh + MGNREGS wages", "Aadhaar, BPL / SECC listing, Bank account, Land ownership proof",
            "Gram Panchayat / Block Development Office / AwaasSoft portal", "https://pmayg.nic.in", "1800-11-6446",
            "Contact your Gram Panchayat Pradhan or Block Development Officer. Get name included in SECC list. Funds transferred directly to bank account in installments.",
            "Active"
        ),
        # Pension
        (
            "Atal Pension Yojana (APY)", "अटल पेंशन योजना", "Ministry of Finance / PFRDA",
            "Pension", "Retirement Pension", 2015, "Central", "Unorganized sector workers",
            18, 40, "Must join between 18 and 40 years", "No income limit; for unorganized/informal sector", None,
            "All", "All", "All States & UTs",
            "Guaranteed monthly pension of Rs.1,000 to Rs.5,000 after age 60. Monthly contribution depends on age at joining and pension amount chosen. On death, spouse gets pension; nominee gets corpus.",
            "Rs.1,000-5,000/month pension after 60 years", "Aadhaar, Bank/Post Office savings account, Mobile number",
            "Bank / Post Office / Mobile banking app", "https://www.npscra.nsdl.co.in", "1800-110-069",
            "Visit your bank/post office and fill APY form. Choose your monthly pension amount (Rs.1k-Rs.5k). Monthly contribution auto-debited. Government contributes 50% or Rs.1,000 (whichever is lower) for eligible subscribers.",
            "Active"
        ),
        (
            "PM Shram Yogi Maandhan (PM-SYM)", "प्रधानमंत्री श्रम योगी मान-धन", "Ministry of Labour & Employment",
            "Pension", "Pension for Informal Workers", 2019, "Central", "Informal/Unorganized sector workers",
            18, 40, "Between 18 and 40 years", "Monthly income <= Rs.15,000", None,
            "All", "All", "All States & UTs",
            "Monthly pension of Rs.3,000 after age 60. Both subscriber and government contribute equal monthly premium (ranges Rs.55-Rs.200 based on age at enrollment).",
            "Rs.3,000/month after 60 years", "Aadhaar, Savings bank account / Jan Dhan account, Mobile number",
            "CSC (Common Service Centre) / Mobile app", "https://maandhan.in", "14434",
            "Visit nearest CSC with Aadhaar and bank passbook. Biometric authentication done. Contribution auto-deducted monthly. Cannot be EPFO/NPS/ESIC member.",
            "Active"
        ),
        (
            "National Social Assistance Programme (NSAP)", "राष्ट्रीय सामाजिक सहायता कार्यक्रम", "Ministry of Rural Development",
            "Pension", "Social Pension for Destitute", 1995, "Central",
            "Elderly, Widows, Disabled - BPL",
            60, 999, "60+ years (old age); Widow any age; Disabled any age",
            "BPL / Destitute", None,
            "All", "All", "All States & UTs",
            "Indira Gandhi National Old Age Pension: Rs.300-500/month. Widow Pension: Rs.300-500/month. Disability Pension: Rs.300/month.",
            "Rs.300-500/month (state may top up)", "Aadhaar, BPL Ration Card, Age proof, Bank account",
            "Gram Panchayat / Block Office / State portal", "https://nsap.nic.in", "1800-111-555",
            "Apply through your Gram Panchayat or BDO office. State verifies BPL status. Amount transferred directly to bank account monthly.",
            "Active"
        ),
        # Women & Child
        (
            "Sukanya Samriddhi Yojana (SSY)", "सुकन्या समृद्धि योजना", "Ministry of Finance",
            "Women & Child", "Girl Child Savings", 2015, "Central", "Parents/Guardians of girl child",
            0, 10, "Girl child must be below 10 years at account opening", "No income limit", None,
            "Female", "All", "All States & UTs",
            "High-interest savings scheme for girl education and marriage. Interest rate ~8.2% p.a. (revised quarterly). Tax-free returns. Account matures after 21 years or on marriage after 18.",
            "~8.2% p.a. interest; Tax-free maturity; Partial withdrawal at 18 for education",
            "Birth certificate of girl child, Aadhaar of parent/guardian, Address proof",
            "Post Office / Authorized bank branches", "https://www.india.gov.in/sukanya-samriddhi-yojna", "1800-266-6868",
            "Visit nearest post office or bank. Open account in the name of girl child. Minimum deposit Rs.250/year. Maximum Rs.1.5 Lakh/year. Only 2 accounts allowed (1 per girl child, up to 2 girls).",
            "Active"
        ),
        (
            "PM Ujjwala Yojana 2.0 (PMUY)", "प्रधानमंत्री उज्ज्वला योजना", "Ministry of Petroleum & Natural Gas",
            "Women & Child", "LPG Connection", 2016, "Central", "Adult women from BPL/poor households",
            18, 999, "Adult woman (18+) of the household", "BPL / PM-Kisan / Ration card holder", None,
            "Female", "SC/ST/PM-Kisan/PMAY/Ration Card beneficiaries", "All States & UTs",
            "Free LPG connection (14.2 kg cylinder with regulator, hose). First refill and stove cost covered. Migrant families can get connection without address proof.",
            "Free connection + first refill + stove (subsidized)", "Aadhaar, Self-declaration of BPL, Bank account",
            "Nearest LPG distributor / Online (mylpg.in)", "https://www.pmujjwalayojana.com", "1906",
            "Visit LPG distributor (HP/Bharat/Indian Gas) with Aadhaar. Fill Form 7 for Ujjwala. BPL verification done. Connection and first refill are free.",
            "Active"
        ),
        (
            "Beti Bachao Beti Padhao", "बेटी बचाओ बेटी पढ़ाओ", "Ministry of Women & Child Development",
            "Women & Child", "Girl Child Education & Welfare", 2015, "Central", "Girls & families in target districts",
            0, 18, "For girl children 0-18 years", "No income limit", None,
            "Female", "All", "Focused districts (612 districts)",
            "Awareness campaigns plus incentives to prevent sex-selective abortion, ensure girl child enrollment in school, prevent dropout. District-level grants for implementing departments.",
            "Incentive grants to districts; awareness programs", "Varies by state component",
            "Anganwadi / School / District Administration", "https://wcd.nic.in", "1098",
            "No direct application - benefits through Anganwadi workers and schools. Campaign for girl child registration at birth, enrollment at school, and retention till class 12.",
            "Active"
        ),
        # Business & Loans
        (
            "PM Mudra Yojana (PMMY)", "प्रधानमंत्री मुद्रा योजना", "Ministry of Finance / SIDBI",
            "Business & Loans", "Micro-Enterprise Loans", 2015, "Central", "Non-farm micro/small enterprises",
            18, 65, "Adult entrepreneur 18-65 years", "No income limit; for non-corporate, non-farm enterprises", None,
            "All", "All (women, SC/ST prioritized)", "All States & UTs",
            "Collateral-free loans: Shishu (up to Rs.50,000), Kishore (Rs.50,001-Rs.5 Lakh), Tarun (Rs.5-Rs.10 Lakh). Covers manufacturing, trade, services, agriculture allied activities.",
            "Up to Rs.10 Lakh (no collateral)", "Aadhaar, PAN, Business proof, Bank statement, Passport photo",
            "Scheduled Commercial Banks / RRBs / MFIs / Online via Udyamimitra", "https://www.mudra.org.in", "1800-180-1111",
            "Identify your loan category (Shishu/Kishore/Tarun). Prepare a simple business plan. Apply at nearest bank or through udyamimitra.in online. No processing fee for Shishu loans.",
            "Active"
        ),
        (
            "PM SVANidhi - Street Vendor Loan", "पीएम स्वनिधि", "Ministry of Housing & Urban Affairs",
            "Business & Loans", "Working Capital Loan for Vendors", 2020, "Central", "Urban street vendors",
            18, 999, "Registered street vendor", "Street vendors with identity certificate", None,
            "All", "All", "Urban Local Body areas",
            "First loan: Rs.10,000. On timely repayment: Rs.20,000 then Rs.50,000. Digital payment incentive: up to Rs.1,200 cashback annually. No collateral. No guarantor.",
            "Rs.10,000 to Rs.50,000 (escalating)", "Vendor identity certificate / Letter of recommendation from Town Vending Committee / Aadhaar",
            "Urban Local Body / Microfinance institutions / Banks / Online (pmsvanidhi.mohua.gov.in)", "https://pmsvanidhi.mohua.gov.in", "1800-11-1979",
            "Get Vendor Certificate from your city Urban Local Body. Apply online on SVANidhi portal or visit nearby lending institution. Use UPI/digital payments for cashback incentive.",
            "Active"
        ),
        (
            "Stand-Up India Scheme", "स्टैंड-अप इंडिया", "Ministry of Finance / SIDBI",
            "Business & Loans", "Entrepreneurship Loans", 2016, "Central", "SC/ST and Women entrepreneurs",
            18, 999, "Adult entrepreneur", "Greenfield enterprise (first time)", None,
            "All", "SC / ST / Women ONLY", "All States & UTs",
            "Bank loans between Rs.10 Lakh and Rs.1 Crore to set up greenfield enterprise (manufacturing, services, or trading). At least one SC/ST and one woman borrower per bank branch.",
            "Rs.10 Lakh to Rs.1 Crore", "Aadhaar, PAN, Caste certificate (for SC/ST), Project report, Business proof",
            "Scheduled Commercial Banks / Online via Standupmitra.in", "https://www.standupmitra.in", "1800-180-1111",
            "Apply online at standupmitra.in or visit your bank. Submit project report. Bank sanctions loan in 4-5 weeks. Includes credit guarantee and hand-holding support.",
            "Active"
        ),
        # Financial Inclusion
        (
            "Pradhan Mantri Jan Dhan Yojana (PMJDY)", "प्रधानमंत्री जन-धन योजना", "Ministry of Finance",
            "Financial Inclusion", "Basic Banking", 2014, "Central", "Unbanked citizens",
            10, 999, "Minimum 10 years; minor account opened by guardian", "No income limit; focus on unbanked poor", None,
            "All", "All", "All States & UTs",
            "Zero-balance savings account with RuPay debit card. Free accident insurance of Rs.2 Lakh (via PMSBY). Overdraft facility up to Rs.10,000 after 6 months. No minimum balance.",
            "Zero-balance account + Rs.2 Lakh accident insurance + Rs.10,000 OD",
            "Aadhaar or any one officially valid document (OVD)",
            "Nearest bank branch / Business Correspondent / Bank Mitra", "https://pmjdy.gov.in", "1800-11-0001",
            "Visit any nationalized bank with Aadhaar. Fill Form A (account opening). Get zero-balance account + RuPay card same day or within 10 days. Link mobile number for DBT benefits.",
            "Active"
        ),
        # Education
        (
            "National Scholarship Portal (NSP)", "राष्ट्रीय छात्रवृत्ति पोर्टल", "Ministry of Electronics & IT",
            "Education", "Scholarships", 2015, "Central", "Students (Pre-Matric to Post-Matric)",
            5, 30, "Depends on scholarship scheme", "Varies: typically family income < Rs.2.5 Lakh/year", None,
            "All", "SC/ST/OBC/Minorities/Disabled/General (separate schemes)", "All States & UTs",
            "Multiple scholarships on single portal: Pre-Matric (class 1-10), Post-Matric (class 11-PhD), Merit-cum-Means (minority). Covers tuition, maintenance, books.",
            "Rs.1,000-20,000+ per year (scheme-specific)", "Aadhaar, Income certificate, Caste certificate, School/College enrollment proof, Bank account, Marksheets",
            "Online only (scholarships.gov.in)", "https://scholarships.gov.in", "0120-6619540",
            "Register on scholarships.gov.in using Aadhaar. Select your applicable scholarship scheme. Upload documents. Institution verifies application. Scholarship transferred to bank account directly.",
            "Active"
        ),
        # Disability
        (
            "Indira Gandhi National Disability Pension (IGNDPS)", "इंदिरा गांधी राष्ट्रीय विकलांगता पेंशन", "Ministry of Rural Development",
            "Disability", "Disability Pension", 2009, "Central", "Persons with severe disability - BPL",
            18, 79, "Between 18 and 79 years", "BPL household", None,
            "All", "All", "All States & UTs",
            "Monthly pension of Rs.300 (Centre); State government may top up. For persons with 80%+ disability.",
            "Rs.300/month (Centre) + state top-up", "Aadhaar, Disability certificate (80%+), BPL ration card, Bank account",
            "Gram Panchayat / Block Office / District Social Welfare Officer", "https://nsap.nic.in", "1800-111-555",
            "Apply at Gram Panchayat with disability certificate (from Government hospital). BPL verification by state. Pension transferred monthly to bank account.",
            "Active"
        ),
        # Skill & Employment
        (
            "PM Kaushal Vikas Yojana (PMKVY) 4.0", "प्रधानमंत्री कौशल विकास योजना", "Ministry of Skill Development & Entrepreneurship",
            "Skill & Employment", "Free Skill Training", 2015, "Central", "Youth 15-45 years",
            15, 45, "15-45 years (varies by sector)", "Family income < Rs.3 Lakh/year preferred", None,
            "All", "All (priority to dropout youth, women, rural)", "All States & UTs",
            "Free short-term skill training (150-300 hours) in 30+ sectors (IT, Electronics, Construction, Hospitality, etc.). Certificate recognized by industry. Reward: Rs.8,000 on completion. Placement support.",
            "Free training + Rs.8,000 reward + placement", "Aadhaar, Educational certificates, Passport photo, Bank account",
            "PMKVY Training Centre / Online registration (pmkvyofficial.org)", "https://www.pmkvyofficial.org", "1800-123-9626",
            "Find nearest PMKVY training centre at pmkvyofficial.org. Register online or walk in. 3-month to 1-year courses. Assessment by SSC. Certificate issued. Placement support at job fairs.",
            "Active"
        ),
        (
            "Mahatma Gandhi NREGS (MGNREGA)", "महात्मा गांधी राष्ट्रीय ग्रामीण रोजगार गारंटी", "Ministry of Rural Development",
            "Skill & Employment", "Rural Employment Guarantee", 2005, "Central", "Rural adult households (any BPL/APL)",
            18, 999, "Any adult (18+ years) of a rural household", "No income limit; for rural households", None,
            "All", "All rural households", "Rural areas only",
            "Guaranteed 100 days of wage employment per year to each rural household. Wages paid at statutory minimum rate (Rs.204-357/day based on state). Work within 5 km of village.",
            "100 days/year @ Rs.204-357/day (state-wise)", "Job Card (from Gram Panchayat), Aadhaar, Bank account",
            "Gram Panchayat (apply in person)", "https://nregs.nic.in", "1800-111-555",
            "Register at your Gram Panchayat to get a MGNREGA Job Card. Apply for work at GP office when needed. Work assigned within 15 days or unemployment allowance paid.",
            "Active"
        ),
    ]

    cursor.executemany('''
    INSERT INTO schemes (
        scheme_name, hindi_name, ministry, category, sub_category, launch_year, scheme_type,
        beneficiary_type, age_min, age_max, age_note, income_limit, income_annual_max,
        gender, caste_category, state_applicability, benefits, benefit_amount,
        documents_required, application_mode, portal_url, helpline, process, status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', schemes_data)

    conn.commit()

    # Export to CSV
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'janmitra_schemes.csv')
    df = pd.read_sql_query("SELECT * FROM schemes", conn)
    df.to_csv(csv_path, index=False)

    # Also create an Excel file for supervisor review
    excel_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'janmitra_schemes_supervisor.xlsx')
    try:
        df.to_excel(excel_path, index=False, sheet_name='Government Schemes')
        print(f"Excel file '{excel_path}' created.")
    except Exception as e:
        print(f"Excel export skipped (openpyxl not installed): {e}")

    total = cursor.execute("SELECT COUNT(*) FROM schemes").fetchone()[0]
    print(f"\nDatabase 'janmitra_schemes.db' created with {total} schemes.")

    cats = cursor.execute("SELECT category, COUNT(*) FROM schemes GROUP BY category ORDER BY COUNT(*) DESC").fetchall()
    for cat, count in cats:
        print(f"  - {cat}: {count} scheme(s)")

    conn.close()

if __name__ == '__main__':
    create_database()
