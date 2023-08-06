import pandas as pd
import numpy as np


class Shuffle:
    """
    Notes:
        - 将数据集进行随机打乱
        - 使用打乱秩序对新的数据集进行打乱
        - 恢复打乱的数据集

    Args:
        inputArray: array, 需要进行打乱的数据集

    Returns:
        shuffled
            打乱后的数据集

        shuffledIndex
            数据的打乱秩序

    Raises:
        01: 进行Shuffle的数据shape[0]应大于1

    Examples:
        >>> inputs_array = np.linspace(0, 5, 1000).reshape(-1, 1)
        >>> inputs_array_obj = Shuffle(inputs_array)
        >>> inputs_array_shuffled = inputs_array_obj.shuffled  # 获取打乱后的数据集
        >>> inputs_array_recovered = inputs_array_obj.recover(inputs_array_shuffled)  # 将打乱的数据集恢复原秩序
        >>> outputs_array = inputs_array_obj.shuffle(inputs_array)  # 将新的数据集按照其他数据集的打乱秩序进行打乱
    """
    def __init__(self, inputArray):
        self.__shapeCheck(inputArray)
        dataframe = pd.DataFrame(inputArray).reset_index().values
        np.random.shuffle(dataframe)
        self.shuffled = dataframe[:, 1:]
        self.shuffledIndex = dataframe[:, 0]

    def recover(self, inputArray):
        """恢复已经打乱的数据"""
        self.__shapeCheck(inputArray)
        dataframe = pd.DataFrame(inputArray).reset_index()
        dataframe["index"] = self.shuffledIndex
        return dataframe.sort_values(by="index").drop(columns=["index"]).values

    def shuffle(self, inputArray):
        """使用其他数据集的打乱秩序对行的数据集进行打乱"""
        self.__shapeCheck(inputArray)
        dataframe = pd.DataFrame(inputArray)
        cache = []
        for item in self.shuffledIndex:
            cache.append(dataframe.iloc[int(item), :].values.ravel()[0])
        return np.reshape(cache, np.shape(inputArray))

    @staticmethod
    def __shapeCheck(inputArray):
        if np.shape(inputArray)[0] == 1:
            raise ValueError(f"进行Shuffle的数据shape[0]应大于1")