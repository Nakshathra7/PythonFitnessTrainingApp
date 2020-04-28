import pymysql
import re

class baseObject:

	def setupObject(self,tn):
		self.data = []
		self.tempdata = {}
		self.tn = tn
		self.fn1 = []
		#self.fn1 = ['fname', 'lname', 'email', 'password', 'subscribed']
		self.errList = []
		self.conn = None
		self.regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
		self.pk = ''
		self.getFields()

	def connect(self):
		#return pymysql.connect(host='',port=3306,user='',password='',db='',autocommit=True)
		import config
		self.conn = pymysql.connect(host=config.DB['host'],port=config.DB['port'],user=config.DB['user'],password=config.DB['password'],db=config.DB['db'],autocommit=True)
		#self.conn = pymysql.connect(host='',port=3306,user='',password='',db='',autocommit=True)

	def getFields(self):
		sql = 'DESCRIBE `' + self.tn +'`;'
		self.connect()
		cur = self.conn.cursor(pymysql.cursors.DictCursor)
		cur.execute(sql)
		self.fn1 = []
		for row in cur:
			#self.data.append(row)
			#if row["Key"] != "PRI":
			self.fn1.append(row['Field'])
			if row['Extra'] == 'auto_increment' and row['Key'] == 'PRI':
				self.pk = row['Field']
			#else:
				#self.pk = row["Field"]

		#print(row)

	def add(self):
		#if len(self.tempdata) == len(self.fn1):
		self.data.append(self.tempdata)
	def set(self,fn, val):
		if fn in self.fn1:
			self.tempdata[fn] = val
		else:
			print('Invalid Field: ' + str(fn))
	def update(self,n,fn,val):
		if len(self.data) >= (n + 1) and fn in self.fn1:
			self.data[n][fn] = val
		else:
			print("Could not set value at row ",str(n),' col ', str(fn))

	'''		
	def insert(self, n=0):
		
		cols = '`,`'.join(self.fn1)
		cols = '`'+cols+'`'
		vals = ('%s,'*len(self.fn1))[:-1]
		#cols = ''
		#vals = ''
		tokens = []
		for fieldname in self.fn1:
			#if fieldname in self.data[n].keys():
				tokens.append(self.data[n][fieldname])
				#vals += '%s,'
				#cols += '`'+fieldname+'`,'
		#vals = vals[:-1]
		#cols = cols[:-1]
		#print(cols)
		sql='INSERT INTO `' + self.tn + '` (' +cols+ ') VALUES (' + vals +');'
		#conn = self.connect()
		self.connect()
		#cur = conn.cursor(pymysql.cursors.DictCursor)
		cur = self.conn.cursor(pymysql.cursors.DictCursor)
		print(sql)
		print(tokens)
		cur.execute(sql,tokens)
		self.data[n][self.pk] = cur.lastrowid
	'''

	def insert(self,n=0):
		cols = ''
		vals = ''
		tokens = []
		for fieldname in self.fn1:
			if fieldname in self.data[n].keys():
				tokens.append(self.data[n][fieldname])
				vals += '%s,'
				cols += '`'+fieldname+'`,'
		vals = vals[:-1]
		cols = cols[:-1]
		sql = 'INSERT INTO `' + self.tn +'` (' +cols + ') VALUES (' + vals+');'
		self.connect()
		cur = self.conn.cursor(pymysql.cursors.DictCursor)
		#print(sql)
		#print(tokens)
		#self.log(sql,tokens)
		cur.execute(sql,tokens)
		self.data[n][self.pk] = cur.lastrowid


	def delete(self,n=0):
		item = self.data.pop(n)
		self.deleteByID(item[self.pk])

	def deleteByID(self,id):
		sql = 'DELETE FROM `' + self.tn +'` WHERE `'+self.pk+'` = %s;' 
		tokens = (id)
		self.connect()
		cur = self.conn.cursor(pymysql.cursors.DictCursor)
		cur.execute(sql,tokens)

	def getByID(self,id):
		sql = 'SELECT * FROM `' + self.tn +'` WHERE `'+self.pk+'` = %s;' 
		tokens = (id)
		self.connect()
		cur = self.conn.cursor(pymysql.cursors.DictCursor)
		cur.execute(sql,tokens)
		self.data = []
		for row in cur:
			self.data.append(row)

	def getAll(self,order=None):
		sql = 'SELECT * FROM `' + self.tn +'`'
		if order != None:
			sql += ' ORDER BY `'+order+'`'
		self.connect()
		cur = self.conn.cursor(pymysql.cursors.DictCursor)
		cur.execute(sql)
		self.data = []
		for row in cur:
			self.data.append(row)

	def update(self, n=0):
		
		tokens = []
		setstring = ''
		for fieldname in self.data[n].keys():
			if fieldname != self.pk:
				setstring += ' `'+fieldname+'` = %s,'
				tokens.append(self.data[n][fieldname])

		setstring = setstring[:-1]

		sql='UPDATE `' + self.tn + '` SET ' + setstring + ' WHERE `' + self.pk + '`=%s'
		print("tokenpd",self.data[n][self.pk])
		tokens.append(self.data[n][self.pk])
		#conn = self.connect()
		self.connect()
		print(sql)
		#cur = conn.cursor(pymysql.cursors.DictCursor)
		cur = self.conn.cursor(pymysql.cursors.DictCursor)
		cur.execute(sql,tokens)
		#self.data[n][self.pk] = cur.lastrowid

	def getByField(self,field,value):
		sql = 'SELECT * FROM `' + self.tn +'` WHERE `'+field+'` = %s;' 
		tokens = (value)
		self.connect()
		cur = self.conn.cursor(pymysql.cursors.DictCursor)
		cur.execute(sql,tokens)
		self.data = []
		for row in cur:
			self.data.append(row)

	def getLikeField(self,field,value):
		sql = 'SELECT * FROM `' + self.tn +'` WHERE `'+field+'` LIKE %s;' 
		tokens = ('%' + value + '%')
		self.connect()
		cur = self.conn.cursor(pymysql.cursors.DictCursor)
		cur.execute(sql,tokens)
		self.data = []
		for row in cur:
			self.data.append(row)

	def getByFieldName(self,field):
		sql = 'SELECT `'+field+'` FROM `' + self.tn +'`' 
		#tokens = (value)
		self.connect()
		cur = self.conn.cursor(pymysql.cursors.DictCursor)
		cur.execute(sql)
		self.data = []
		for row in cur:
			self.data.append(row)