class InvestmentFund:
    def __init__(self, fund_id, name, manager_name, description, nav, creation_date, performance, created_at=None, updated_at=None):    
        self.fund_id = fund_id
        self.name = name
        self.manager_name = manager_name
        self.description = description
        self.nav = nav
        self.creation_date = creation_date
        self.performance = performance
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "fund_id": self.fund_id,
            "name": self.name,
            "manager_name": self.manager_name,
            "description": self.description,
            "nav": self.nav,
            "creation_date": self.creation_date,
            "performance": self.performance,
        }