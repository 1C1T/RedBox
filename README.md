# RedBox
项目简介：使普通鼠标拥有类似罗技鼠标的宏编程功能，兼容罗技宏文件lua脚本，直接导入即可使用

免责声明：非盈利项目，仅供学习交流使用

QQ群1：928286446

QQ群2（备用）：519619515

![测试鼠标按键](https://github.com/1C1T/RedBox/assets/142925722/b48ac4a5-ccf1-4b93-8795-2f14b960e98d)


-------- API函数示例 --------

-- 休眠

Sleep(1000)-- 休眠1000毫秒


-- 将输出日志消息至脚本编辑器的控制台操作窗中

OutputLogMessage("Hello World!\n")--打印 Hello World!


-- 返回以毫秒为单位的执行脚本总时间

endTime = GetRunningTime()


-- 获取已格式化的当前时间

nowDate = GetDate()


-- 清空脚本编辑器控制台中的输出内容

ClearLog()


-- 按下键盘按键

PressKey("a")-- 按下键盘上的"a"


-- 释放键盘按键

ReleaseKey("a")-- 释放键盘上的"a"


-- 按下并释放键盘按键

PressAndReleaseKey("a")-- 按下并释放键盘上的"a"


-- 方法可用于确定某修饰键是否被按下

IsModifierPressed("lctrl")-- 判断左侧Ctrl键是否按下，是则返回true，否则返回false


-- 模拟鼠标左键、中键或右键被按下

PressMouseButton(1)-- 按下鼠标左键

PressMouseButton(2)-- 按下鼠标中键

PressMouseButton(3)-- 按下鼠标右键


-- 模拟鼠标左键、中键或右键被按下

ReleaseMouseButton(1)-- 释放鼠标左键

ReleaseMouseButton(2)-- 释放鼠标中键

ReleaseMouseButton(3)-- 释放鼠标右键


-- 模拟鼠标左键、中键或右键按下并释放

PressAndReleaseMouseButton(1)-- 按下并释放鼠标左键

PressAndReleaseMouseButton(2)-- 按下并释放鼠标中键

PressAndReleaseMouseButton(3)-- 按下并释放鼠标右键


-- 可用于确定某鼠标按键是否被按下

IsMouseButtonPressed(1)-- 判断鼠标左键是否按下，是则返回true，否则返回false

IsMouseButtonPressed(2)-- 判断鼠标中键是否按下，是则返回true，否则返回false

IsMouseButtonPressed(3)-- 判断鼠标右键是否按下，是则返回true，否则返回false

IsMouseButtonPressed(4)-- 判断鼠标侧键X1是否按下，是则返回true，否则返回false

IsMouseButtonPressed(5)-- 判断鼠标侧键X2是否按下，是则返回true，否则返回false


-- 移动鼠标指针至屏幕的绝对坐标，参数范围在 0 到 65535 之间

MoveMouseTo(0, 0)-- 移动鼠标至屏幕左上角

MoveMouseTo(32767, 32767)-- 移动鼠标至屏幕中央

MoveMouseTo(65535, 65535)-- 移动鼠标至屏幕右下角


-- 移动鼠标指针至相对坐标（相对当前鼠标指针）

MoveMouseRelative(-10, 0)-- 鼠标向左移动10个单位

MoveMouseRelative(10, 0)-- 鼠标向右移动10个单位

MoveMouseRelative(0, -10)-- 鼠标向上移动10个单位

MoveMouseRelative(0, 10)-- 鼠标向下移动10个单位


-- 获取鼠标指针当前相对标准坐标

x, y = GetMousePosition()-- 返回x坐标和y坐标


-- 用于确定锁定键是否处于启用状态

IsKeyLockOn("capslock")-- 判断 大小写锁定键 是否按下，是则返回true，否则返回false

IsKeyLockOn("numlock")-- 判断 数字锁定键 是否按下，是则返回true，否则返回false

IsKeyLockOn("scrolllock")-- 判断 滚动锁定键 是否按下，是则返回true，否则返回false


-- 启用或禁用鼠标左键事件报告 默认禁用

EnablePrimaryMouseButtonEvents(true)-- 启用鼠标左键事件报告

EnablePrimaryMouseButtonEvents(false)-- 禁用鼠标左键事件报告


--查询鼠标加速度是否启用

mouseAcc = GetMouseAcceleration()-- 是则返回true，否则返回false


--设置启用或关闭鼠标加速度

SetMouseAcceleration(true)-- 启用鼠标加速度

SetMouseAcceleration(false)-- 关闭鼠标加速度


--查询鼠标灵敏度

mouseSpeed = GetMouseSpeed()


--设置鼠标灵敏度，参数范围在 1 到 20 之间

SetMouseSpeed(10)-- 设置鼠标灵敏度为10档


-- 判断当前活动窗口是否指定进程 参数："xxx.exe"

IsActiveWindows("红盒.exe")-- 判断当前活动窗口是否"红盒.exe", 是则返回true，否则返回false


-------- 快捷键 --------

-- 暂停或继续脚本运行：		pause 键

-- 加载上一个文件：		Ctrl + P

-- 新建文件：				Ctrl + N

-- 打开文件：				Ctrl + O

-- 保存：				Ctrl + S

-- 另存为：				Ctrl + Shift + S

-- 隐藏行号：				Ctrl + Shift + L

-- 关闭语法高亮：			Ctrl + Shift + H

-- 文字放大：				Ctrl + 鼠标滚轮向上

-- 文字缩小：				Ctrl + 鼠标滚轮向下

-- 注释代码：				Ctrl + E

-- 取消注释：				Ctrl + Q

-- 增加缩进：				Tab 键

-- 减小缩进：				Shift + Tab

-- 查询与替换：			Ctrl + F

-- 显示文件树：			Ctrl + T

-- 打开颜色选择器：		Ctrl + M

