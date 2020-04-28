import pymysql
import re
from baseObject import baseObject

class trainerList(baseObject):
	def __init__(self):
		self.setupObject('TrainerDetails')

	def tryLogin(self,email,password):
		sql = 'SELECT * FROM `' + self.tn +'` WHERE `TrainerEmail` = %s AND `TrainerPassword` = %s;'
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

	def getCurrentID(self,email,password):
		sql = 'SELECT `TrainerID` FROM `' + self.tn +'` WHERE `TrainerEmail` = %s AND `TrainerPassword` = %s;'
		tokens = (email,password)
		self.connect()
		cur = self.conn.cursor(pymysql.cursors.DictCursor)
		cur.execute(sql,tokens)
		self.data = []
		rows = cur.fetchall()
		for row in rows:
			self.data.append(row)
			trainerID = row['TrainerID']
			return trainerID

	def getCurrentFieldName(self,id):
		sql = 'SELECT `TrainerName` FROM `' + self.tn +'` WHERE `TrainerID` = %s;'
		tokens = (id)
		self.connect()
		cur = self.conn.cursor(pymysql.cursors.DictCursor)
		cur.execute(sql,tokens)
		self.data = []
		rows = cur.fetchall()
		for row in rows:
			self.data.append(row)
			trainerName = row['TrainerName']
			return trainerName

	def getFieldID(self,name):
		sql = 'SELECT `TrainerID` FROM `' + self.tn +'` WHERE `TrainerName` = %s'
		tokens = (name)
		self.connect()
		cur = self.conn.cursor(pymysql.cursors.DictCursor)
		cur.execute(sql,tokens)
		self.data = []
		rows = cur.fetchall()
		for row in rows:
			self.data.append(row)
			trainerID = row['TrainerID']
			return trainerID

	def verifyNew(self,n=0):
		self.errList = []

		if len(self.data[n]['TrainerName']) == 0:
			self.errList.append("Trainer Name cannot be blank")

		if len(self.data[n]['TrainerEmail']) == 0:
			self.errList.append("Trainer Email cannot be blank")

		elif not(bool(re.search(self.regex,self.data[n]['TrainerEmail']))):
			self.errList.append("Enter Valid Email with . and @")

		if len(self.data[n]['TrainerPassword']) == 0:
			self.errList.append("Trainer Password cannot be blank")

		elif len(self.data[n]['TrainerPassword']) <= 4:
			self.errList.append("Password must be longer than 4 characters")

		if len(self.data[n]['TrainerYrsOfExperience']) == 0:
			self.errList.append("Trainer Years Of Experience cannot be blank")

		if len(self.data[n]['TrainerGender']) == 0:
			self.errList.append("Trainer Gender cannot be blank")

		if len(self.errList) > 0:
			return False
		else:
			return True	

		#Add if statements for validation of other fields
		#Add Unit Test

	






