benefits = [
    "401K",
    "401K Match",
    "Childcare",
    "Concierge Services",
    "Donation Matching Program",
    "Employee Events",
    "Employee Referral Program",
    "Flexible Schedule",
    "Flexible Spending Accounts",
    "Free Food and Drinks",
    "Game Rooms",
    "Gym Membership",
    "Health Care on Site",
    "Life Insurance",
    "Medical, Dental, Vision",
    "Merchandise Discounts",
    "Military Leave",
    "Mobile Phone",
    "On Site Cafeteria",
    "Paid Sick Days",
    "Paid Time-Off",
    "Parental Paid Leave",
    "Parking",
    "Performance Bonus",
    "Prescription Drug Coverage",
    "Professional Development",
    "Relocation Assistance",
    "Retirement / Pension Plans",
    "Stock Options",
    "Subsidized Commuting",
    "Transportation Allowance",
    "Tuition Reimbursement",
    "Vehicle Allowance",
    "Work From Home",
]

# Skills should be bucketed by the associated job title
skills = {
    "1": "HR",
    "2": "Benefits",
    "3": "Recruiting",
    "4": "Front Desk",
    "5": "Reception",
    "6": "Marketing",
    "7": "Graphic Design",
    "8": "Payroll",
    "9": "Mortgage Loans",
    "10": "Administrative Assitant",
}


class StaticDataRepository:
    def get_user_skills(self):
        return skills

    def get_company_benefits(self):
        return benefits
