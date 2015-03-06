# coding: utf8

import pandas
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
from scipy import stats
from sklearn.preprocessing import scale
from sklearn import svm
from sklearn.decomposition import PCA

# Переменные в Питоне, записанные в верхнем регистре,
# символизируют константы и обычно записываются в начале файла
# после подключения модулей
OUTLIER_FRACTION = 0.01

girls = pandas.read_csv('girls.csv', header=0)

#Посмотрим общую статистику
#print  girls.info()

#print  girls.describe()

#print girls[['Month','Year']][girls['Waist'] == 89]

# Для обучения модели оставим только численные параметры, кроме года.
# Запишем их в массив NumPy girl_params, попутно преобразовав к типу float64.
# Шкалируем данные так, чтобы все признаки лежали в диапазоне от -1 до 1.
girl_params = np.array(girls.values[:,2:], dtype="float64")
girl_params = scale(girl_params)

# Далее выделяем 2 главных компонента в данных, чтоб их можно было отобразить.
# Тут нам пригодилась библиотека Scikit-learn Principal Component Analysis (PCA).
# Также нам не помешает сохранить число наших девушек
X = PCA(n_components=2).fit_transform(girl_params)
girls_num = X.shape[0]

# Создаем экземпляр классификатора с гауссовым ядром и «скармливаем» ему данные.
clf = svm.OneClassSVM(kernel="rbf")
clf.fit(X)

# Порог определяется статистически, как такое расстояние
# до разделяющей поверхности, что у OUTLIER_FRACTION
# (в нашем случае у одного) процента выборки оно больше
# (т.е в нашем случае, threshold — это 1%-перцентиль массива
# расстояний до разделяющей поверхности).
dist_to_border = clf.decision_function(X).ravel()
threshold = stats.scoreatpercentile(dist_to_border,
            100 * OUTLIER_FRACTION)
is_inlier = dist_to_border > threshold

# Отображение
xx, yy = np.meshgrid(np.linspace(-7, 7, 500), np.linspace(-7, 7, 500))
n_inliers = int((1. - OUTLIER_FRACTION) * girls_num)
n_outliers = int(OUTLIER_FRACTION * girls_num)
Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)
plt.title("Outlier detection")
plt.contourf(xx, yy, Z, levels=np.linspace(Z.min(), threshold, 7),
                         cmap=plt.cm.Blues_r)
a = plt.contour(xx, yy, Z, levels=[threshold],
                            linewidths=2, colors='red')
plt.contourf(xx, yy, Z, levels=[threshold, Z.max()],
                         colors='orange')
b = plt.scatter(X[is_inlier == 0, 0], X[is_inlier == 0, 1], c='white')
c = plt.scatter(X[is_inlier == 1, 0], X[is_inlier == 1, 1], c='black')
plt.axis('tight')
plt.legend([a.collections[0], b, c],
           ['learned decision function', 'outliers', 'inliers'],
           prop=matplotlib.font_manager.FontProperties(size=11))
plt.xlim((-7, 7))
plt.ylim((-7, 7))
plt.show()

print girls[is_inlier == 0]
