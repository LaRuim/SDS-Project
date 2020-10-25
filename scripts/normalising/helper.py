import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy


def getZscore(array):
    return (array - array.mean(axis=0)) / array.std(axis=0)


def getPvalue(array):
    return scipy.stats.norm.sf(abs(array)) * 2


def normalize(array):
    newArray = (array - array.min()) / (array.max() - array.min())
    return newArray


def getValues(array):
    values = {'mean': array.mean(), 'variance': array.var(
    ), 'normalized': normalize(array), 'z-score': getZscore(array)}
    normArr = values['normalized']
    values['normMean'] = round(normArr.mean(), 3)
    values['normVar'] = round(normArr.var(), 3)
    values['pValue']: getPvalue(values['z-score'])
    zscoreArr = values['z-score']
    values['stdMean'] = round(zscoreArr.mean(), 3)
    values['stdVar'] = round(zscoreArr.var(), 3)
    return values
