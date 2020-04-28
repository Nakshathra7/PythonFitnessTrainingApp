import pymysql
import re
from baseObject import baseObject

class memberHealthList(baseObject):
	def __init__(self):
		self.setupObject('MemberHealthRecords')

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

	def getParentID(self,childID):
		sql = 'SELECT `MemberID` FROM `' + self.tn +'` WHERE `MemberHealthRecordID` = %s;'
		tokens = (childID)
		self.connect()
		cur = self.conn.cursor(pymysql.cursors.DictCursor)
		cur.execute(sql,tokens)
		self.data = []
		rows = cur.fetchall()
		for row in rows:
			self.data.append(row)
			memberID = row['MemberID']
			return memberID

	def getReferntialID(self,id):
		sql = 'SELECT `MealPlanID`,`WorkoutID` FROM `' + self.tn +'` WHERE `MemberID` = %s;'
		tokens = (id)
		self.connect()
		cur = self.conn.cursor(pymysql.cursors.DictCursor)
		cur.execute(sql,tokens)
		self.data = []
		for row in cur:
			self.data.append(row)

	def updateSpecificField(self, mealPlanID,workoutID,memberID):
		
		sql='UPDATE `' + self.tn + '` SET `MealPlanID` =%s, `WorkoutID` =%s WHERE `MemberID` = %s;'
		tokens = (mealPlanID,workoutID,memberID)
		#conn = self.connect()
		self.connect()
		print(sql)
		#cur = conn.cursor(pymysql.cursors.DictCursor)
		cur = self.conn.cursor(pymysql.cursors.DictCursor)
		cur.execute(sql,tokens)
		#self.data[n][self.pk] = cur.lastrowid

	def updateReferenceField(self, subscribeID,memberID):
		
		sql='UPDATE `' + self.tn + '` SET `SubscriptionID` =%s WHERE `MemberID` = %s;'
		tokens = (subscribeID,memberID)
		#conn = self.connect()
		self.connect()
		print(sql)
		#cur = conn.cursor(pymysql.cursors.DictCursor)
		cur = self.conn.cursor(pymysql.cursors.DictCursor)
		cur.execute(sql,tokens)
		#self.data[n][self.pk] = cur.lastrowid

	def verifyNew(self,n=0):
		self.errList = []

		if len(self.data[n]['MemberAge']) == 0:
			self.errList.append("Member Age cannot be blank")

		if len(self.data[n]['MemberGender']) == 0:
			self.errList.append("Member Gender cannot be blank")

		if len(self.data[n]['MemberHeight']) == 0:
			self.errList.append("Member Height cannot be blank")

		if len(self.data[n]['MemberWeight']) == 0:
			self.errList.append("Member Weight cannot be blank")

		if len(str(self.data[n]['MemberBMI'])) == 0:
			self.errList.append("Member BMI cannot be blank")

		if len(str(self.data[n]['MemberProfession'])) == 0:
			self.errList.append("Member Profession cannot be blank")

		if len(str(self.data[n]['MemberMedicalAilments'])) == 0:
			self.errList.append("Member Medical Ailments cannot be blank")

		if len(self.errList) > 0:
			return False
		else:
			return True	

		#Add if statements for validation of other fields
		#Add Unit Test

	






