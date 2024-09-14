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
  
