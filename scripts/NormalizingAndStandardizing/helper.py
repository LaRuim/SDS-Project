import numpy as np
import scipy
from sklearn.preprocessing import MinMaxScaler


class NormStd:
    def __init__(self, dfColumn):
        self.array = np.array(dfColumn)

    def getZscore(self, array):
        return scipy.stats.zscore(array)

    def getPvalue(self, array):
        return scipy.stats.norm.sf(abs(array)) * 2

    def normalize(self, array):
        return self.array / np.linalg.norm(self.array)

    def getValues(self, label, mainDictionary=dict()):
        values = {'mean': self.array.mean(), 'variance': self.array.var(
        ), 'normalized': self.normalize(self.array), 'z-score': self.getZscore(self.array)}
        normArr = values['normalized']
        values['normMean'] = round(normArr.mean(), 3)
        values['normVar'] = round(normArr.var(), 3)
        values['pValue']: self.getPvalue(np.array(values['z-score']))
        zscoreArr = values['z-score']
        values['stdMean'] = round(zscoreArr.mean(), 3)
        values['stdVar'] = round(zscoreArr.var(), 3)
        values['inputArray'] = self.array
        mainDictionary[label] = values
        return mainDictionary
