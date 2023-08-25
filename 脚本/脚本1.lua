function OnEvent(event, arg)
	if event == "MOUSE_BUTTON_PRESSED" then
		if arg == 1 then
			OutputLogMessage("按下了鼠标左键\n")
		elseif arg == 2 then
			OutputLogMessage("按下了鼠标右键\n")
		elseif arg == 3 then
			OutputLogMessage("按下了鼠标中键\n")
		elseif arg == 4 then
			OutputLogMessage("按下了鼠标侧键\n")
		end
	end
	
end


EnablePrimaryMouseButtonEvents(true)
