import pymysql
import re
from baseObject import baseObject

class workoutPlanList(baseObject):
	def __init__(self):
		self.setupObject('WorkoutDetails')

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
		sql = 'SELECT `WorkoutID` FROM `' + self.tn +'` WHERE `WorkoutName` = %s'
		tokens = (name)
		self.connect()
		cur = self.conn.cursor(pymysql.cursors.DictCursor)
		cur.execute(sql,tokens)
		self.data = []
		rows = cur.fetchall()
		for row in rows:
			self.data.append(row)
			workoutID = row['WorkoutID']
			return workoutID


	def verifyNew(self,n=0):
		self.errList = []

		if len(self.data[n]['WorkoutName']) == 0:
			self.errList.append("Workout Name cannot be blank")

		if len(self.data[n]['WorkoutType']) == 0:
			self.errList.append("Workout Type cannot be blank")

		if len(self.data[n]['WorkoutTimeTotalHours']) == 0:
			self.errList.append("Workout Time Total Hours cannot be blank")

		if len(self.data[n]['NoOfDaysWorkout']) == 0:
			self.errList.append("No Of Days Workout cannot be blank")

		if len(self.errList) > 0:
			return False
		else:
			return True	

		#Add if statements for validation of other fields
		#Add Unit Test

	






