import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import pyautogui
from pynput import keyboard
import time
keyinput = keyboard.Controller()

class MousePositionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Position Tracker")
        
        # 显示鼠标当前位置的标签
        self.label = tk.Label(root, text="Move the mouse to see the position", font=("Helvetica", 16))
        self.label.pack(padx=20, pady=10)
        
        # 创建一个文本框，用于记录鼠标位置
        self.textbox = ScrolledText(root, width=50, height=4, font=("Helvetica", 12))
        self.textbox.pack(padx=10, pady=10)

        self.textbox1 = ScrolledText(root, width=50, height=2, font=("Helvetica", 12))
        self.textbox1.pack(padx=10, pady=20)

        self.textbox2 = ScrolledText(root, width=50, height=2, font=("Helvetica", 12))
        self.textbox2.pack(padx=10, pady=30)

        self.positions = []  # 记录所有坐标
        
        # 添加开始和结束检测按钮
        self.start_button = tk.Button(root, text="开始检测", command=self.start_detection, font=("Helvetica", 14))
        self.start_button.pack(pady=5)
        
        self.stop_button = tk.Button(root, text="结束检测", command=self.stop_detection, font=("Helvetica", 14))
        self.stop_button.pack(pady=5)
        # 添加执行自定义动作的按钮
        self.action_button = tk.Button(root, text="执行自定义动作", command=self.execute_action, font=("Helvetica", 14))
        self.action_button.pack(pady=5)
        self.running = False  # 标志位，表示是否正在检测

    def start_detection(self):
        if not self.running:
            self.running = True
            self.update_mouse_position()
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()
            
    def stop_detection(self):
        if self.running:
            self.running = False
            if hasattr(self, "listener"):
                self.listener.stop()
        
    def update_mouse_position(self):
        if self.running:
            x, y = pyautogui.position()
            self.label.config(text=f"当前鼠标位置: (X: {x}, Y: {y})")
            self.label.update()
            self.root.after(100, self.update_mouse_position)
            
    def on_press(self, key):
        if self.running:
            try:
                if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                    x, y = pyautogui.position()
                    position = f"({x}, {y}, 5)"
                    self.positions.append(position)
                    self.textbox.insert(tk.END, f"{position}; ")
                    self.textbox.yview(tk.END)  # 滚动到最后一行
                else:
                    position = f"({key}, -1, 1)"  # 记录按键，y填-1，等待1s
                    self.positions.append(position)
                    self.textbox.insert(tk.END, f"{position}; ")
                    self.textbox.yview(tk.END)  # 滚动到最后一行
            except AttributeError:
                pass

    def execute_action(self):
        if self.running:
            self.stop_detection()
        #执行自定义动作
        #把 textbox 中的内容取出来, 并以string 的形式保存在变量 mouse_position_list 中
        mouse_position_list = self.textbox.get("1.0", tk.END)
        #去掉mouse_position_list 中的换行符
        mouse_position_list = mouse_position_list.replace("\n", "")
        print(mouse_position_list)
        coordinates_array = []
        for coord in mouse_position_list.split('; '):
            print(coord)
            if coord.strip('(); '):
                x, y, z = coord.strip('(); ').split(', ')
                x_str, y_str, z_str = map(str, (x, y, z))
                coordinates_array.append((x_str, y_str, z_str))
        print(coordinates_array)
        
        
        def press_key(key):
            if isinstance(key, str):
                # 如果key是字符串，则尝试获取对应的键名属性
                key_name = key.split('.')[1] if '.' in key else key
                keyinput.press(getattr(keyboard.Key, key_name))
                keyinput.release(getattr(keyboard.Key, key_name))
            else:
                # 如果key不是字符串，则直接将其作为按键传递给keyboard.press()
                keyinput.press(key)
                keyinput.release(key)
       
        def move_mouse_and_click(coordinates):
            for coordinate in coordinates:
                x, y, z = coordinate
                if y != '-1':
                    pyautogui.moveTo(int(x), int(y))
                    pyautogui.click()
                    time.sleep(int(z))
                else:
                    press_key(x)
                    time.sleep(int(z))

        move_mouse_and_click(coordinates_array)

    def on_close(self):
        self.stop_detection()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = MousePositionApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)  # 确保安全关闭监听器
    root.mainloop()
    
if __name__ == "__main__":
    main()
