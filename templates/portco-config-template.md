# Portco Configuration Template
# Copy this to portcos/[company-slug]/config.md and fill in values

PORTCO_NAME: "[Company Name]"
PORTCO_SLUG: "[company-slug]"         # kebab-case, used in artifact keys
INDUSTRY: "[industry]"                 # e.g. B2B SaaS, Healthcare Services

# Systems
ERP_SYSTEM: NetSuite                   # NetSuite | QuickBooks | Sage | SAP | other
HRIS_SYSTEM: Rippling                  # Rippling | ADP | Gusto | Bullhorn | other
CRM_SYSTEM: Salesforce                 # Salesforce | HubSpot | Bullhorn | other

# Reporting
REPORTING_CADENCE: monthly             # monthly | quarterly
FISCAL_YEAR_END: December              # Month name
BOARD_MEETING_DAY: 15                  # Day of month after close
CLOSE_TARGET_DAYS: 10                  # Business days after month end
CURRENCY: USD
ROUNDING: thousands                    # thousands | millions

# KPI Definitions
KPI_REVENUE: "Net revenue excluding contra-revenue"
KPI_EBITDA: "Operating income + D&A + stock-based comp + one-time items"
KPI_NRR: "Net revenue retention (SaaS portcos only — delete if not applicable)"

# Covenant Thresholds (from credit agreement — update at each amendment)
COVENANT_MAX_LEVERAGE: 4.5             # Total debt / LTM EBITDA
COVENANT_MIN_COVERAGE: 1.25            # LTM EBITDA / LTM cash interest
COVENANT_TESTING_FREQUENCY: quarterly  # quarterly | semi-annual | annual
COVENANT_NEXT_TEST_DATE: YYYY-MM-DD

# Cash Management
PORTCO_MIN_CASH: 500000                # Minimum cash balance before escalation ($)
REVOLVER_AVAILABILITY: 0               # Available revolver capacity ($, 0 if none)

# Key Contacts
CFO_NAME: ""
CFO_EMAIL: ""
CONTROLLER_NAME: ""
CONTROLLER_EMAIL: ""
PE_DEAL_LEAD: ""
PE_OPERATING_PARTNER: ""

# Acquisition Context
ACQUISITION_DATE: YYYY-MM-DD
ENTRY_EV: 0                            # Entry enterprise value ($M)
ENTRY_EBITDA: 0                        # LTM EBITDA at acquisition ($M)
ENTRY_MULTIPLE: 0.0                    # EV / EBITDA at entry
HOLD_PERIOD_TARGET: 5                  # Years
