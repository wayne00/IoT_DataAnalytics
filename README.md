内容介绍：
1. 通过树莓派模拟物联网设备与AWS GreenGrass以及IoT Core进行交互，发送实时的数据到AWS IoT Core。

2. 传感器数据实时展现：数据到达IoT Core后，由AWS IoT规则引擎进行处理，筛选出温湿度指标。分两路输出到后端，
	a）一路将数据写入到Dynamodb表中。
	b）另外一路数据写入到kinesis data stream。使用Flask开发的web页面负责将Dynamodb表中收集到的实时数据使用echart控件动态展现出来，ajax页面每秒刷新一次。

3. 异常数据实时监测：
	EMR sparkstreaming 实时消费，上一步IoT 规则引擎写入到kinesis data stream中的数据，对数据进行实时监控分析，如果监控数据有异常，实时发送邮件告警。
	异常数据识别模型由孤立森林（Isolation Forest）算法训练而来。sparkstreaming 中调用了该模型实现异常数据检测。
