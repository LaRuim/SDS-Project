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

    def NormalizeAndStandardize(self):
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
        newValues = {
            'Original Mean': round(values['mean'], 2),
            'Original Variance': round(values['variance'], 2),
            'Normalized Mean': round(values['normMean'], 2),
            'Normalized Variance': round(values['normVar'], 2),
            'Standardized Mean': round(values['stdMean'], 2),
            'Standardized Variance': round(values['stdVar'], 2)
        }
        return newValues
