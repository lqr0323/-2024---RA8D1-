import sensor, image, time
from pyb import UART, Timer

# 初始化传感器
sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # 设置为RGB模式
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
clock = time.clock()

uart = UART(1, 115200, timeout_char=1000)
i = 0
# 定义红色阈值
red_threshold = (10, 150, 15, 127, 15, 127)  # 根据具体情况调整阈值

# 标志，表示是否已经发送过中心坐标或发送't'
center_sent = False
last_x_center = 0  # 上次发送的x中心坐标
t_sent = False  # 标志表示是否已发送过't'

# 定时器中断处理函数
def send_uart(timer):
    global last_x_center
    print(f"Timer callback triggered. last_x_center = {last_x_center}")
    if last_x_center != 0:
        uart.write('X' + str(last_x_center) + '!@\n')
        print(f"Sending via UART: X{last_x_center}!@")

# 设置定时器，每隔0.5秒触发一次中断
tim = Timer(4, freq=2)  # freq=2 表示每0.5秒触发一次
tim.callback(send_uart)

# 主循环
while True:
    clock.tick()
    img = sensor.snapshot()

    # 在图像上绘制一个固定位置的绿色矩形框
    roi = (0, 100, 320, 48)

    img.draw_rectangle(roi, color=(0, 255, 0))

    # 识别ROI内的红色区域
    blobs = img.find_blobs([red_threshold], roi=roi, pixels_threshold=200, area_threshold=200)

    if blobs:
        # 找到最大的红色区域
        largest_blob = max(blobs, key=lambda b: b.pixels())
        x, y, w, h = largest_blob.rect()
        # 在检测到的区域内绘制红色矩形框，确保宽度和绿色框一致
        img.draw_rectangle((x, y, w, h), color=(255, 0, 0))

        if 10 < w <= 90:
            center_sent = False
            last_x_center = largest_blob.cx()  # 更新中点x坐标
            uart.write('X' + str(last_x_center) + '!@\n')
            i = 0
            if 130 <= largest_blob.cx() <= 190 and not t_sent:
                uart.write("t\n")  # 发送 't' 表示中心坐标在指定范围内
                uart.write("t\n")  # 发送 't' 表示中心坐标在指定范围内
                time.sleep_ms(1)
                uart.write("t\n")  # 发送 't' 表示中心坐标在指定范围内
                uart.write("t\n")  # 发送 't' 表示中心坐标在指定范围内
                t_sent = True  # 设置标志，表示已经发送过't'
            elif largest_blob.cx() < 130 or largest_blob.cx() > 190:
                t_sent = False  # 如果中心坐标离开范围，则重置t_sent标志

        elif w > 150 and not center_sent:
            time.sleep_ms(650)
            uart.write("c\n")  # 表示即将到达十字路口
            center_sent = True  # 设置标志，表示已经发送过中心坐标
        elif w <= 10 and not center_sent:
            #time.sleep_ms(350)
            uart.write("s\n")  # 发送 's' 表示没有检测到有效区域
            center_sent = True  # 设置标志，表示已经发送过中心坐标

        # 检查x坐标是否在150到170之间
        #if 150 <= largest_blob.cx() <= 170 and not t_sent:
            #uart.write("t\n")  # 发送 't' 表示中心坐标在指定范围内
            #t_sent = True  # 设置标志，表示已经发送过't'
    else:
        if not center_sent:
            uart.write("s\n")  # 没有检测到 blobs 时发送 's'
            center_sent = True

    # 控制循环速度
    time.sleep_ms(100)
