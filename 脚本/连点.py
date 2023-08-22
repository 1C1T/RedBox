# 如果 Shift键 和 鼠标左键 同时按下，则连续点击5次鼠标左键
while True:
	time.sleep(0.01)
	if isKeyHold("lshift") and isMouseHold(1):
		for i in range(4):# 加上实际按下鼠标左键1次等于5次
			mouseClick(1)
			time.sleep(0.01)
		clearLog()
		print("*"*10,"\t已完成5次连点\t", "*"*10, "\n")
