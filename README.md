包含内容/代码介绍：

1. 通过树莓派模拟物联网设备与AWS GreenGrass以及IoT Core进行交互，发送实时的数据到AWS IoT Core。

2. 传感器数据实时展现：数据到达IoT Core后，由AWS IoT规则引擎进行处理，筛选出温湿度指标。分两路输出到后端，
	a）一路将数据写入到Dynamodb表中。
	b）另外一路数据写入到kinesis data stream。使用Flask开发的web页面负责将Dynamodb表中收集到的实时数据使用echart控件动态展现出来，ajax页面每秒刷新一次。

3. 异常数据实时监测：
	EMR sparkstreaming 实时消费，上一步IoT 规则引擎写入到kinesis data stream中的数据，对数据进行实时监控分析，如果监控数据有异常，实时发送邮件告警。
	异常数据识别模型由孤立森林（Isolation Forest）算法训练而来。sparkstreaming 中调用了该模型实现异常数据检测。

4. 云端/APP端通过AWS IoT设备影子反向控制树莓派二极管灯开关，模拟云端/app端控制物联网设备

总体架构：

![image]()


云端/APP端远程控制树莓派二极管灯开关
![image]()



实时告警实现：

模式一：基于机器学习的物联网数据监控和异常数据实时告警
	SNS:
		1. 配置规则
	EMR:
		1. 使用 Spark Mlib/Python Sklearn 用历史数据训练 Isolation Forest 模型
		2. 启动EMR 集群 – Spark 组件
			预配置运行环境
			EMRFS 读S3内容，实现模型动态加载


模式二：基于经验规则的物联网数据监控和异常数据实时告警
	Greengrass Lambda:
		1. Lambda 接收Greengrass消息，指标运算
		2. 调用SNS服务

![image]()