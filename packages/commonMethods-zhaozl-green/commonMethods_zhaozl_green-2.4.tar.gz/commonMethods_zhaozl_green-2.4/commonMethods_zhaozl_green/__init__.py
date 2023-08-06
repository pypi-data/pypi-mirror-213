"""
Notes:
    - core中：
        - formatTime:获取符合需求格式的时间
        - printWithColor:打印所定义格式的字符串
        - moduleOfDataframe:计算DF中所指多个向量样本的模
        - cosineThetaOfVectors:计算向量组和单个向量间的夹角与余弦值
        - RandomGrouping:根据所需样本数量不重复地随机进行抽样

Notes:
    - toolbox中：
        * timeTrans: 通过输入list(int)或者int形式的时间戳unixTimestamp，与形如'%Y/%m/%d %H:%M:%S'的formation，对时间戳进行计算并输出string

        * mysqlOperator: mysql数据库操作， 包括创建table、添加列、新增数据、更新数据、查询数据

        * comtradeParser: 通过输入符合comtrade规范的文件名，对数据内容进行输出

        * processBar: 包括以下几个不同样式的进度条：

            ** Wave, 波浪形进度条

            ** Rectangle, 方框形进度条

            ** SelfDefine, 自定义符号样式的进度条

            ** FocusedLine, 可自定义符号样式的具有当前正在执行进度位置的进度条

            ** OceanWave, 波浪型动态指示条

        * trendAnalyzer:

            ** trendAnalyzer: 使用三阶滑动平均与一阶导对输入数据的快速/缓慢的上升/下降状态进行判断

            ** trendPredict: 通过不断输入一时间序列的数值，顺序地对所定义窗口1内的数值进行三阶滑动平均处理，并计算所定义窗口2内的时序数据一阶导，通过对所定义窗口3内一阶导数据均值进行判断，以确定原始数据的上升/下降情况，包括：是否处理上升/下降状态，是否处于快速/慢速变化状态

        * bounceAnalyzer: 对新传入的数据进行缓存记录，通过平均值计算等方法对跳变状态与持续跳变状态进行判断

        * evennessDetermine: 包括两种方法

            ** compareWithOthersAverage, 同类测点温度值稳定，单一测点温度测量在正常范围内，但明显高于除本测点外的同类平均值

            ** circleSimilarity, 全体测点与均值圆的相似度, 使用向量间的相似度进行衡量

            ** modulo， 向量的模计算

            ** angleCal， 向量间夹角余弦值计算

        * shuffle: 包括三种方法（之一为构造函数）

            ** 将数据集进行随机打乱

            ** 使用打乱秩序对新的数据集进行打乱

            ** 恢复打乱的数据集
"""
from .core import *