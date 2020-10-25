import numpy as np
import scipy
from sklearn.preprocessing import MinMaxScaler


class NormStd:
    __array = []

    def __init__(self, dfColumn):
        self.__array = np.array(dfColumn)

    def __obtain_the_Z_score_value(self, array):
        return scipy.stats.zscore(array)

    def __obtain_the_P_value(self, array):
        return scipy.stats.norm.sf(abs(array)) * 2

    def __normalize_the_array_using_this_function(self, array):
        return array / np.linalg.norm(array)

    def NormalizeAndStandardize(self, label, mainDictionary=dict()):
        values = {'mean': self.__array.mean(), 'variance': self.__array.var(
        ), 'normalized': self.__normalize_the_array_using_this_function(self.__array), 'z-score': self.__obtain_the_Z_score_value(self.__array)}
        normArr = values['normalized']
        values['normMean'] = round(normArr.mean(), 3)
        values['normVar'] = round(normArr.var(), 3)
        values['pValue']: self.__obtain_the_P_value(
            np.array(values['z-score']))
        zscoreArr = values['z-score']
        values['stdMean'] = round(zscoreArr.mean(), 3)
        values['stdVar'] = round(zscoreArr.var(), 3)
        values['inputArray'] = self.__array
        mainDictionary[label] = values
        return mainDictionary
