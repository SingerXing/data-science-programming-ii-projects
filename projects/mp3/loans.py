# Add additional imports if needed

import json
from csv import DictReader
import csv
from io import TextIOWrapper
from zipfile import ZipFile

race_lookup = {
    "1": "American Indian or Alaska Native",
    "2": "Asian",
    "21": "Asian Indian",
    "22": "Chinese",
    "23": "Filipino",
    "24": "Japanese",
    "25": "Korean",
    "26": "Vietnamese",
    "27": "Other Asian",
    "3": "Black or African American",
    "4": "Native Hawaiian or Other Pacific Islander",
    "41": "Native Hawaiian",
    "42": "Guamanian or Chamorro",
    "43": "Samoan",
    "44": "Other Pacific Islander",
    "5": "White",
}
with open('banks.json') as f:
    banks = json.load(f)
class Applicant:
    def __init__(self, age, race):
        self.age = age
        self.race = set()

        # TODO: add each race to self.race using race_lookup
        for r in race:
            if r not in race_lookup:
                continue
            self.race.add(race_lookup[r])



    def lower_age(self):
        # TODO: return the lower bound of the applicant’s age range as an int
        s = self.age.replace("<", "").replace(">", "")
        if '-' not in self.age:
            age = int(s)
        else:
            age = int(self.age.split('-')[0])
        return age

    def __lt__(self, other):
        # TODO: return True if this applicant is younger than the other
        if self.lower_age() < other.lower_age():
            return True
        else:
            return False
    
    def __repr__(self):
        # TODO: return a string like Applicant('25-34', ['White', 'Asian'])
        races = sorted(self.race)
        return f"Applicant({self.age!r}, {races})"

    def __str__(self):
        return self.__repr__()


class Loan:
    def __init__(self, values):
        # TODO: use float_extract to set loan_amount, property_value, and interest_rate
        self.loan_amount = self.float_extract(values, "loan_amount")
        self.property_value = self.float_extract(values,'property_value')
        self.interest_rate = self.float_extract(values,'interest_rate')

        # TODO: create a list of Applicant objects for applicant and co-applicant
        self.applicants = []
        applicant_races = []
        for i in range(1,6):
            applicant_races.append(values[f"applicant_race-{i}"])
        self.applicants.append(Applicant(values['applicant_age'],applicant_races))
        if values["co-applicant_age"] != "9999":
            co_applicant_races = []
            for i in range(1, 6):
                co_applicant_races.append(values.get(f"co-applicant_race-{i}", ""))
            self.applicants.append(Applicant(values["co-applicant_age"], co_applicant_races))
        

    def float_extract(self, values, attr):
        val = values.get(attr, "NA")
        if val in ("NA", "Exempt", "", None):
            return -1.0
        try:
            return float(val)
        except ValueError:
            return -1.0

    def yearly_amounts(self, yearly_payment):
        assert self.interest_rate > 0
        assert self.loan_amount > 0

        amt = self.loan_amount

        while amt > 0: 
            yield amt
            # TODO: yield amt
            amt *= (self.interest_rate/100 + 1)
            amt -= yearly_payment
            # TODO: add interest rate multiplied by amt to amt
            # TODO: subtract yearly payment from amt
            # remove this line once you implement this function

    def __str__(self):
        # TODO: return a summary string like "<Loan: 4.5% on $200000 with 2 applicant(s)>"
        return f"<Loan: {self.interest_rate}% on ${self.loan_amount} with {len(self.applicants)} applicant(s)>"

    def __repr__(self):
        return self.__str__()


class Bank:
    def __init__(self, name):
        self.name = name
        self.lei = None
        self.loans = []
        self.loan_list = self.loans
        # TODO: look up bank’s LEI in banks.json using `banks`
        for row in banks:
            if name == row['name']:
                self.lei = row['lei']
        # TODO: read wi.zip/wi.csv and load Loan objects belonging to this bank
        with ZipFile('wi.zip') as zf:
            with zf.open('wi.csv') as raw:
                wi = DictReader(TextIOWrapper(raw, encoding="utf-8"))
                for row in wi:
                    if row['lei'] == self.lei:
                        self.loans.append(Loan(row))
                        
        
    def __len__(self):
        # TODO: return the number of loans
        return len(self.loan_list)

    def __getitem__(self, idx):
        # TODO: return loan at index idx
        return self.loan_list[idx]