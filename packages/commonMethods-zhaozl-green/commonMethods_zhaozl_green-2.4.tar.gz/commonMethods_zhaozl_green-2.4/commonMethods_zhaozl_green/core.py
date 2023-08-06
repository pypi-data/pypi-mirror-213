"""
Notes:
    内容物为几个基础函数与类：

    - formatTime:获取符合需求格式的时间
    - printWithColor:打印所定义格式的字符串
    - moduleOfDataframe:计算DF中所指多个向量样本的模
    - cosineThetaOfVectors:计算向量组和单个向量间的夹角与余弦值
    - RandomGrouping:根据所需样本数量不重复地随机进行抽样

Examples:
    >>> from commonMethods_zhaozl_green.core import {
    >>>     formatTime, printWithColor, moduleOfDataframe, cosineThetaOfVectors, RandomGrouping
    >>> }
"""
import time
import numpy as np
import pandas as pd


pd.set_option(
    'display.max_columns', 10000, 'display.width', 10000,
    'display.max_rows', 50, 'display.min_rows', 20,
    'display.unicode.east_asian_width', True
)


def formatTime(formation: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    Notes:
        返回符合格式要求的时间字符串

    Args:
        formation: str,字符串格式,默认'%Y-%m-%d %H:%M:%S'

    Returns:
        时间字符串

    Examples:
        >>> formatTime(format='%Y-%m-%d %H:%M:%S')
    """
    return time.strftime(formation, time.localtime())


def printWithColor(msg, prefix="", suffix="", fontStyle="halflight", fontColor="white", backColor="green", withTime=True):
    """
    Notes:
        打印具有颜色和特定格式的字符串

    Args:
        msg: str, 需要进行打印的内容

    Keyword Args:
        prefix: str,前缀,默认""

        suffix: str,后缀,默认""

        fontStyle: str,下划线/粗体/斜体等,可选项,['halflight', 'bold', 'italic', 'underline', 'sparkle', 'fate', 'reverse'], 默认halflight

        fontColor: str,字体颜色,可选项,['black', 'red', 'green', 'yellow', 'blue', 'purple',  'cyan', 'white'], 默认"white"

        backColor: str,背景色,可选项,['black', 'red', 'green', 'yellow', 'blue', 'purple',  'cyan', 'white'], 默认green

        withTime: bool,是否打印时间,默认True

    Examples:
        >>> printWithColor("Some string", fontColor="black", fontStyle="bold")
    """
    FONTSTYLE = {
        "bold": "\033[1m",  # 设置高亮度
        "halflight": "\033[2m",  # 设置一半亮度
        "italic": "\033[3m",  # 斜体
        "underline": "\033[4m",  # 下划线
        "sparkle": "\033[5m",  # 闪烁
        "reverse": "\033[7m",  # 反显
        "fate": "\033[8m",  # 消隐
    }
    FONTCOLOR = {
        "black": "\033[30m",  # 设置字体为黑色
        "red": "\033[31m",  # 设置字体为红色
        "green": "\033[32m",  # 设置字体为绿色
        "yellow": "\033[33m",  # 设置字体为黄色
        "blue": "\033[34m",  # 设置字体为蓝色
        "purple": "\033[35m",  # 设置字体为紫色
        "cyan": "\033[36m",  # 设置字体为青色
        "white": "\033[37m"  # 设置字体为白色
    }
    BACKCOLOR = {
        "black": "\033[40m",  # 设置背景色为黑色
        "red": "\033[41m",  # 设置背景色为红色
        "green": "\033[42m",  # 设置背景色为绿色
        "yellow": "\033[43m",  # 设置背景色为黄色
        "blue": "\033[44m",  # 设置背景色为蓝色
        "purple": "\033[45m",  # 设置背景色为紫色
        "cyan": "\033[46m",  # 设置背景色为青色
        "white": "\033[47m"  # 设置背景色为白色
    }
    print(f"{prefix}{suffix}")
    print(f"{FONTSTYLE[fontStyle]}{FONTCOLOR[fontColor]}{BACKCOLOR[backColor]}{formatTime() if withTime else ''}: {msg}")


def moduleOfDataframe(df_input: pd.DataFrame) -> np.array:
    """
    Notes:
        计算一个dataframe所表达的（纵向）多个向量的模

    Args:
        df_input: dataframe, 需要进行模计算的数据表，列为维度，行为样本

    Returns:
        np.array,（纵向）模

    Examples:
        >>> print(np.shape(moduleOfDataframe(pd.DataFrame(np.random.randn(10, 5)))))
    """
    return np.reshape(df_input.apply(lambda _df: np.sqrt(sum(_df.values**2)), axis=1).values, (-1, 1))


def cosineThetaOfVectors(vector01: pd.DataFrame, vector02: pd.DataFrame, output="angle") -> list:
    """
    Notes:
        计算向量1（或多个向量1）与向量2的夹角余弦

    Keyword Args:
        vector01: pd.DataFrame，向量1
        vector02: pd.DataFrame，向量2
        output: str，输出为余弦值或角度值,可选['angle', 'cosine'],默认:angle

    Returns:
        list，向量1（或多个向量1）与向量2的夹角余弦或夹角

    Raises:
        ValueError: 当入参的列数量不相同时报出

    Examples:
        >>> vec01 = pd.DataFrame(np.random.randn(10, 5))
        >>> vec02 = pd.DataFrame(np.random.randn(1, 5))
        >>> print(vec01, '\n', vec02)
        >>> print(cosineThetaOfVectors(vec01, vec02))
        >>> print(cosineThetaOfVectors(vec01, vec02, output="cos"))
    """
    if np.shape(vector01)[1] != np.shape(vector02)[1]:
        raise ValueError(f"错误的维度值: vector01({np.shape(vector01)[1]}列) != vector01({np.shape(vector02)[1]}列)")
    _matmul = np.matmul(vector01.values, vector02.values.transpose())
    _matmul_mod = moduleOfDataframe(vector01) * moduleOfDataframe(vector02)
    _cosineTheta = np.divide(_matmul, _matmul_mod)
    _theta = np.divide(_matmul, _matmul_mod)
    _outputSwitch = {
        "angle": list(map(lambda x: np.arccos(x), _cosineTheta.ravel().tolist())),
        "cos": _cosineTheta.ravel().tolist()
    }
    return _outputSwitch[output]


class RandomGrouping:
    """
    Notes:
        按所需抽取出的样本比例，随机抽取不重复的样本。
        返回：抽取出的样本序号，剩余的样本序号，抽取出的样本，剩余的样本

    Args:s
        inputDf: pd.Dataframe,带抽取样本总体
        percentage: float,随机抽取样本的比例，(0, 1)

    Returns:
        randomSelect, dict, 随机筛选结果

        selectedRowNums, list，随机选出的序号

        remainedRowNums, list，随机筛选后剩余的序号

        selectedRow, pd.Dataframe，随机选出的样本

        remainedRow, pd.Dataframe，随机抽取后剩余的样本

    Examples:
        >>> vec01 = pd.DataFrame(np.random.randn(100, 5), columns=["a1", "a2", "a3", "a4", "a5"])
        >>> randomGroup = RandomGrouping(inputDf=vec01, percentage=0.9234)
        >>> print(randomGroup.randomSelect)
    """
    def __init__(self, inputDf: pd.DataFrame, percentage: float):
        self.__inputDf = inputDf
        self.__inputLength = len(inputDf)
        self.__percentage = percentage
        self.__randomSelect = []
        self.selectedRowNums = None
        self.remainedRowNums = None
        self.selectedRow = None
        self.remainedRow = None

    @property
    def randomSelect(self):
        """
        执行抽样
        """
        __needQuant = int(np.ceil(self.__inputLength * self.__percentage))
        __availableRowNums = list(np.arange(0, self.__inputLength))
        while len(self.__randomSelect) < __needQuant:
            __popLoc = np.random.randint(0, len(__availableRowNums))
            self.__randomSelect.append(__availableRowNums.pop(__popLoc))
        self.__randomSelect = np.sort(self.__randomSelect).tolist()
        # Set Attrs
        self.selectedRowNums = self.__randomSelect
        self.remainedRowNums = __availableRowNums
        self.selectedRow = self.__inputDf.iloc[self.__randomSelect, :].reset_index(drop=True)
        self.remainedRow = self.__inputDf.iloc[__availableRowNums, :].reset_index(drop=True)
        self.selectedRow.columns = self.__inputDf.columns
        self.remainedRow.columns = self.__inputDf.columns
        return {
            "selectedRowNums": self.selectedRowNums,
            "remainedRowNums": self.remainedRowNums,
            "selectedRow": self.selectedRow,
            "remainedRow": self.remainedRow
        }
