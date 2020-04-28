import pymysql
import re
from baseObject import baseObject

class mealPlanList(baseObject):
	def __init__(self):
		self.setupObject('MealPlanDetails')

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

	def getFieldID(self,name):
		sql = 'SELECT `MealPlanID` FROM `' + self.tn +'` WHERE `MealPlanName` = %s'
		tokens = (name)
		self.connect()
		cur = self.conn.cursor(pymysql.cursors.DictCursor)
		cur.execute(sql,tokens)
		self.data = []
		rows = cur.fetchall()
		for row in rows:
			self.data.append(row)
			mealPlanID = row['MealPlanID']
			return mealPlanID

	def verifyNew(self,n=0):
		self.errList = []

		if len(self.data[n]['MealPlanName']) == 0:
			self.errList.append("Meal Plan Name cannot be blank")

		if len(self.data[n]['MealPlanDescription']) == 0:
			self.errList.append("Meal Plan Description cannot be blank")

		if len(self.data[n]['NoOfDaysMealPlan']) == 0:
			self.errList.append("No Of Days Meal Plan cannot be blank")

		if len(self.errList) > 0:
			return False
		else:
			return True	

		#Add if statements for validation of other fields
		#Add Unit Test

	






