import pymysql
import re
from baseObject import baseObject

class memberList(baseObject):
	def __init__(self):
		self.setupObject('MemberDetails')

	def tryLogin(self,email,password):
		sql = 'SELECT * FROM `' + self.tn +'` WHERE `MemberEmail` = %s AND `MemberPassword` = %s;'
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
		sql = 'SELECT `MemberID` FROM `' + self.tn +'` WHERE `MemberEmail` = %s AND `MemberPassword` = %s;'
		tokens = (email,password)
		self.connect()
		cur = self.conn.cursor(pymysql.cursors.DictCursor)
		cur.execute(sql,tokens)
		self.data = []
		rows = cur.fetchall()
		for row in rows:
			self.data.append(row)
			memberID = row['MemberID']
			return memberID

	def getCurrentFieldName(self,id):
		sql = 'SELECT `MemberName` FROM `' + self.tn +'` WHERE `MemberID` = %s;'
		tokens = (id)
		self.connect()
		cur = self.conn.cursor(pymysql.cursors.DictCursor)
		cur.execute(sql,tokens)
		self.data = []
		rows = cur.fetchall()
		for row in rows:
			self.data.append(row)
			memberName = row['MemberName']
			return memberName

	def getFieldID(self,name):
		sql = 'SELECT `MemberID` FROM `' + self.tn +'` WHERE `MemberName` = %s'
		tokens = (name)
		self.connect()
		cur = self.conn.cursor(pymysql.cursors.DictCursor)
		cur.execute(sql,tokens)
		self.data = []
		rows = cur.fetchall()
		for row in rows:
			self.data.append(row)
			memberID = row['MemberID']
			return memberID

	def verifyNew(self,n=0):
		self.errList = []

		m = memberList()
		m.getByField('MemberEmail',self.data[n]['MemberEmail'])

		if len(self.data[n]['MemberName']) == 0:
			self.errList.append("Member Name cannot be blank")

		if len(self.data[n]['MemberEmail']) == 0:
			self.errList.append("Member Email cannot be blank")

		elif not(bool(re.search(self.regex,self.data[n]['MemberEmail']))):
			self.errList.append("Enter Valid Email with . and @")

		if len(self.data[n]['MemberPassword']) == 0:
			self.errList.append("Member Password cannot be blank")

		elif len(self.data[n]['MemberPassword']) <= 4:
			self.errList.append("Password must be longer than 4 characters")

		if len(str(self.data[n]['MemberAddress'])) == 0:
			self.errList.append("Member Address cannot be blank")

		if len(self.errList) > 0:
			return False
		else:
			return True	

		#Add if statements for validation of other fields
		#Add Unit Test

	






