import pymysql
import re
from baseObject import baseObject

class subscriptionList(baseObject):
	def __init__(self):
		self.setupObject('SubscriptionDetails')

	def tryLogin(self,email,password):
		sql = 'SELECT * FROM `' + self.tn +'` WHERE `email` = %s AND `password` = %s;'
		tokens = (email,password)
		self.connect()
		cur = self.conn.cursor(pymysql.cursors.DictCursor)
		cur.execute(sql,tokens)
		self.data = []
		n = 0
		for row in cur:
			self.data.append(row)
			n+=1
		if n>0:
			return True
		else:
			return False

	def verifyNew(self,n=0):
		self.errList = []

		if len(self.data[n]['SubscriptionName']) == 0:
			self.errList.append("Subscription Name cannot be blank")

		if len(self.data[n]['SubscriptionPrice']) == 0:
			self.errList.append("Subscription Price cannot be blank")

		if len(self.data[n]['SubscriptionType']) == 0:
			self.errList.append("Subscription Type cannot be blank")

		if len(self.data[n]['NoOfDaysSubscription']) == 0:
			self.errList.append("No Of Days Subscription cannot be blank")

		if len(self.errList) > 0:
			return False
		else:
			return True	

		#Add if statements for validation of other fields
		#Add Unit Test

	






