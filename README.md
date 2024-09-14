# 2024RT-Thread 全球嵌入式电子设计竞赛 作品-基于瑞萨RA8D1的轮式机器人
#一、 项目简介
本项目旨在开发一个基于Vision Board和Maix Cam的智能送药小车。小车通过视觉识别来确定目标位置，并自主导航到指定地点进行药物配送。小车的核心处理单元是Texas Instruments的MSPM0G3507微控制器。

## 功能描述
- 视觉识别：通过Maix Cam识别特定目标病房号码，通过vision board 来寻找路径。
- 自动导航：小车根据识别结果和预设路线，自动前往目标位置。
- 智能送药：到达指定位置后，发送通知或提醒，进行药物投递。

## 硬件组成
- **主控板**：TI MSPM0G3507
- **视觉模块**：Maix Cam + Vision Board
- **电机驱动**：直流减速电机及其驱动器 双路TB6612电机驱动模块
- **电源模块**：12V锂电池或其他移动电源
- **传感器**：灰度传感器用来辅助运行的轨迹，使其沿正确的路径行驶。
- **其他**：按钮、LED指示灯等

## 软件架构
1. **视觉处理**：Maix Cam 进行目标识别，并通过UART或SPI与MSPM0G3507通信。
2. **导航控制**：MSPM0G3507接收视觉数据，结合小车的运动控制算法（PID控制），控制电机驱动模块实现路径规划。
3. **避障功能**：通过超声波传感器获取环境信息，避免碰撞。
4. **通信模块**：与外部设备通信，用于状态通知（如WiFi或蓝牙模块）。

## 工作流程
1. 启动小车，进入待机状态。
2. Maix Cam通过摄像头识别病房号码，连续识别到10次相同的病房号码即锁定病房，不再受其他病房号码的影响。
3. 视觉数据通过通信接口传送至主控MSPM0G3507。
4. 主控单元根据识别结果和预设的导航算法控制小车运动。
5. 小车到达指定位置后，完成送药任务并发送通知。

## 硬件连接
1. **Maix Cam** -> **MSPM0G3507**
   - UART/SPI接口：用于传输识别数据
2. **电机驱动模块** -> **MSPM0G3507**
   - GPIO/PWM：控制小车前进、后退和转向
3. **灰度传感器** -> **MSPM0G3507**
   - I2C接口：获取循迹数据
4. **电源模块**：为小车提供电力

## 软件开发

### 开发环境配置
- **TI MSPM0G3507**
  - 使用TI Code Composer Studio (CCS)进行开发。
  - 安装MSPM0/ARM编译器支持包。
  
- **Maix Cam**
  - 使用Sipeed IDE或者K210开发工具链进行模型训练和编程。
  
### Vision Board配置
1. 连接Maix Cam到Vision Board。
2. 通过Vision Board的接口与小车进行物理连接（如UART/SPI接口）。

### Maix Cam配置
1. 安装必要的驱动和固件。
2. 编写图像处理算法，训练目标识别模型。
3. 通过Maix Cam的接口输出识别结果。

### 主控单元 MSPM0G3507 编程
1. 配置UART/SPI接口，接收Maix Cam传输的识别数据。
2. 编写路径规划和运动控制算法，结合电机驱动器控制小车移动。
3. 集成避障传感器数据，处理障碍物信息并调整行驶路线。

## 未来改进
- 增加多种视觉识别目标，提高系统灵活性。
- 提高导航算法的智能性，使小车更具适应性和效率。
- 增加远程控制功能，允许手动干预。

  #二、项目详解

  vision board 在openmvide中编写代码截图

  ![img](https://github.com/lqr0323/-2024---RA8D1-/blob/main/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202024-09-14%20094335.png)

   vision board 端代码
  # 智能送药小车摄像头视觉处理代码解析

## 概述
该代码实现了通过摄像头检测图像中的红色区域，并通过UART与主控通信，输出相关的坐标和指令。具体的功能包括：
1. 识别图像中红色区域的中心坐标。
2. 根据红色区域的位置和大小，发送不同的指令（`t`、`c`、`s`等）给主控板。
3. 通过定时器定期发送最新的红色区域中心位置。

## 主要模块解析

### 1. 传感器初始化
```
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
```
通过 ```sensor.reset()``` 初始化摄像头模块。
使用 ```sensor.set_pixformat(sensor.RGB565)``` 设置摄像头为RGB模式。
使用 ```sensor.set_framesize(sensor.QVGA)``` 设置图像分辨率为 320x240。
使用 ```sensor.skip_frames(time=2000)``` 跳过前两秒的帧，确保摄像头稳定工作。  
UART 通信初始化
```uart = UART(1, 115200, timeout_char=1000)```
初始化UART接口，波特率为115200，超时为1000毫秒。用于小车与主控之间的数据传输。
3. 红色阈值
```red_threshold = (10, 150, 15, 127, 15, 127)```
定义红色物体的HSV阈值范围，用于在图像中识别红色区域。需要根据具体环境调整。
4. 标志变量
```
center_sent = False
last_x_center = 0
t_sent = False
```
center_sent: 标志位，表示是否已经发送了中心坐标或其它信号。
last_x_center: 记录上次发送的红色区域的X轴中心坐标。
t_sent: 标志位，表示是否已经发送过't'信号。
5. 定时器中断
```
def send_uart(timer):
    global last_x_center
    if last_x_center != 0:
        uart.write('X' + str(last_x_center) + '!@\n')
```
定义定时器中断回调函数 send_uart(timer)。每当定时器触发时，检查是否有新的中心坐标并通过UART发送。
使用 Timer(4, freq=2) 设置定时器，每0.5秒触发一次，调用回调函数。
6. 主循环
```
while True:
    clock.tick()
    img = sensor.snapshot()
    roi = (0, 100, 320, 48)
    img.draw_rectangle(roi, color=(0, 255, 0))
```
在主循环中，摄像头每帧捕获一张图像，并定义感兴趣区域(ROI)为 (0, 100, 320, 48)，即图像中间的一部分。
通过 img.draw_rectangle(roi, color=(0, 255, 0)) 在该区域画一个绿色的矩形框，用于后续红色检测的范围。
7. 识别红色区域
```
blobs = img.find_blobs([red_threshold], roi=roi, pixels_threshold=200, area_threshold=200)
```
使用 img.find_blobs 函数在指定ROI中寻找符合红色阈值的区域。区域的像素和面积阈值分别设置为200，保证只识别较大的红色区域。
8. 处理检测到的红色区域  
```
largest_blob = max(blobs, key=lambda b: b.pixels())
x, y, w, h = largest_blob.rect()
```
条件处理：
区域宽度在10到90之间时：

发送红色区域的中心坐标：
```
uart.write('X' + str(last_x_center) + '!@\n')
```
如果中心坐标在 [130, 190] 范围内且没有发送过t信号，则连续发送四次't'：
```
uart.write("t\n")
t_sent = True
```
区域宽度大于150时：

表示即将到达十字路口，发送 c：
```
uart.write("c\n")
```
区域宽度小于等于10时：

如果没有有效的红色区域，则发送 s 信号，表示停止：
```
uart.write("s\n")
```
9. 没有找到红色区域
如果没有检测到任何红色区域，则发送停止信号 s：
```
uart.write("s\n")
```
10. 循环控制
```
time.sleep_ms(100)
```
每次循环结束后，程序暂停100毫秒，以控制帧率。
