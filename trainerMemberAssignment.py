import pymysql
import re
from baseObject import baseObject

class trainerMemberAssignmentList(baseObject):
	def __init__(self):
		self.setupObject('TrainerMemberAssignment')

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

	def getAssignedID(self,trainerID):
		sql = 'SELECT `MemberID` FROM `' + self.tn +'` WHERE `TrainerID` = %s;'
		tokens = (trainerID)
		self.connect()
		cur = self.conn.cursor(pymysql.cursors.DictCursor)
		cur.execute(sql,tokens)
		self.data = []
		for row in cur:
			self.data.append(row)

	

	






