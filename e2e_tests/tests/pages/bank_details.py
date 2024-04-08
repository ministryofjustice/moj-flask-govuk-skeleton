class BankDetails:
	def __init__(self, page):
		self.page = page

	def navigate(self):
		self.page.goto("http://localhost:8000/forms/bank-details")

