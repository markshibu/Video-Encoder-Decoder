class macroblock:
	def __init__(self,i,j,redgreenblue):
		self.rgb = 		[[redgreenblue[(j * 16 + y) * 720 + i * 16 + x] for y in range(16)] for x in range(16)]
		self.red = 		[[self.rgb[x][y][0] for y in range(16)] for x in range(16)]
		self.green = 	[[self.rgb[x][y][1] for y in range(16)] for x in range(16)]
		self.blue = 	[[self.rgb[x][y][2] for y in range(16)] for x in range(16)]

	def print_value(self,x,y):
		print self.rgb[x][y]

	def get_value(self,x,y):
		return self.rgb[x][y]

	def get_red(self,x,y):
		return self.red[x][y]

	def get_green(self,x,y):
		return self.green[x][y]

	def get_blue(self,x,y):
		return self.blue[x][y]
