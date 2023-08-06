def bibl(string):
    k = '''
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import t
from scipy.stats import f
import statsmodels.stats.api as sms
from statsmodels.compat import lzip
import numpy as np
from scipy import stats
import statsmodels.stats.diagnostic as dg
from scipy.stats import shapiro
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm
from sklearn.metrics import confusion_matrix, accuracy_score, roc_curve, auc
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.diagnostic import acorr_ljungbox
from scipy.spatial.distance import cdist
from linearmodels.panel import RandomEffects
from linearmodels.panel import PanelOLS
from linearmodels.panel import PooledOLS
from scipy import stats
from statsmodels.compat import lzip
import statsmodels.stats.api as sms
from scipy.stats import f
from sklearn.linear_model import LinearRegression as lr
import scipy.stats as stats
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
from arch import arch_model
    '''.split('\n')
    for el in k:
        if string.lower() in el.lower():
            print(el)

def copy(s):
    import win32clipboard

    string = s
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(string)
    win32clipboard.CloseClipboard()


def ser(string):
    a = """
    AIC - Критерий Акакике для лин регрессии
    BIC - Критерий Шварца для лин регрессии
    Weighted_Least_Squares - Взвешенный метод наименьших квадратов.
    Brousha_godfri - Тест Бройша – Годфри. Автокорреляция
    Sved_Ezenhart - Метод рядов Сведа-Эйзенхарта  Автокорреляция
    Kochrain_Orkatt - Процедура Кохрейна-Орката
    Hildret_Lu - Процедура Хилдрета – Лу.
    Farrara_globera - мультиколлинеарности: Алгоритм Фаррара-Глобера
    PCA - Метод главных компонент
    ACF_PACF - Функции ACF и PACF
    anomal_student - Для вычисления аномальных наблюдений методом стьюдента
    anomal_irvin - Для вычисления аномальных наблюдений методом Ирвина
    Krit_Serii_Osn_med - Критерий серий, основанный на медиане
    razn_sredn_urov - Проверка наличия тренда. Метод проверки разности средних уровней.
    Foster_Stuart -  Проверка наличия тренда. Метод Фостера-Стьюарта.
    skolz_sredn - Простая (среднеарифметическая) скользящая средняя
    weighted_skolz_sredn - Взвешенная (средневзвешенная) скользящая средняя. 
    srednhronolog - Среднехронологическа скользящая
    exponential_smoothing - Экспоненциальное сглаживание
    Zarembka -  Метод Зарембки.
    box_cox - Тест Бокса-Кокса
    Ber_Mck_Aler - Тест Бера МакАлера
    Makinona_white_davidson - Тест Маккинона Уайта Девидсона
    Arima - Как строить Arima
    pred_Arima - Интервальный прогноз для Arima
    white_noise_ljuing_box - тестирование на белый шум Льюнга бокса
    FDL - FDL
    ADL - ADL
    test_diki_fulera - ADF тест на единичный корень
    Getis_Ord - Пространственная автокорреляция по методологии А. Гетиса и Дж. Орда.
    Jiri - Пространственная автокорреляция по методологии Роберта Джири.
    params – параметры
    significance_of_parameters – проверка на значимость
    fisher – тест Фишера
    R – R^2+adj+средняя ошибка аппроксимации А
    Predict – предсказания
    Breuschpagan – тест Бройша-Пагана
    Goldfeld_Qandt – тест Голфеда-Квандта
    Spearmen – тест  ранговой корреляции Спирмена
    Park – тест Парка
    glayzer – тест Глейзера
    white – тест Вайта
    dw – тест Дарвина-Уотсона
    series_method – метод серии
    reset – reset-тест Рамсея
    shapiro_wilka – тест Шапиро-Вилка
    jarque_bera – тест Харкера Берка
    betta – Бэтта коэффы
    delta – дельта коэффы
    elastic – коэффы эластичности
    VIF – VIF коэффы
    logit – Логистическая регрессия  logit
    probit –  Пробит регрессия probit
    Boxplot – Ящик с усами
    dar_wats - Тест Дарбина-Уотсона
    ac_ljungbox - тест Льюинга-Бокса на автокорреляцию
    matrix_granitc – пример построения матрицы границ
    matrix_rasstoyaniiy - пример построения матрицы расстояний
    prostranstv_vesa - Алгоритм построения матрицы пространственных весов
    matrix_bin_blizc_sosedi - Бинарная матрица ближайших соседей
    matrix_dist_size - Матрица расстояний с учетом размера объекта
    fixed_m – построение модели с фиксированными эффектами
    pool_m – построение модели пул
    random_effects_model – построение модели со случайными эффектами
    hausman - Тест Хаусмана для панельных данных
    Broush_pagana - Тест Бройша-Пагана для панельных данных
    choy_panel - Тест Чоу для панельных данных
    choose_kriv_rosta - Выбор кривой роста
    prognoz_kriv_rosta - Прогнозирование с помощью кривой роста
    braun - прогнозирование Брауна
    holter_winters - Модель Хольта-Уинтерса
    teylor_weidg - Модель Тейла-Вейджа
    chetveryakov - Метод Четверикова
    prognoz_trend_model - прогнозирвоане на основе тренд модели
    macke_arch – ARCH
    make_garch  - GARCH
    test_choy – тест Чоу
    student - проверка выбросов Стьюдента
    Irvin - проверка выбросов Ирвин
    """
    k = a.split('\n')
    for i in k:
        if string.lower() in i.lower():
            print(i)
def student(k):
    '''
    from scipy import stats
    import numpy as np
    data = np.array(df['X'])
    t_stat, p_val = stats.ttest_1samp(data, np.mean(data))
    if p_val < 0.05:
        print("Выбросы присутствуют")
    else:
        print("Выбросов нет")
    '''
    return k

def Irvin(k):
    '''
    import numpy as np
    data = np.array(df['X'])
    mean = np.mean(data)
    std = np.std(data)
    upper_bound = mean + 2.5 * std
    lower_bound = mean - 2.5 * std
    anomalies = []
    for value in data:
        if value < 0:
            anomalies.append(value)
        elif value > upper_bound or value < lower_bound:
            anomalies.append(value)
    print(anomalies)
    
    '''
    return k
            
def AIC(k):
    '''
    import statsmodels.api as sm
    import numpy as np
    model = sm.OLS(y, x)
    results = model.fit()
    results.aic
    '''
    return k

def BIC(k):
    '''
    import statsmodels.api as sm
    import numpy as np
    model = sm.OLS(y, x)
    results = model.fit()
    results.bic
    '''
    return k

def Weighted_Least_Squares(k):
    """
    import statsmodels.api as sm
    import numpy as np
    model = sm.WLS(y, x, weights=1/x)
    results = model.fit()
    results.summary()
    """
    return k

def Brousha_godfri(k):
    """
    from scipy.stats import chi2
    import statsmodels.api as sm
    import numpy as np
    k = 5 # то на каком уровне проверяем гипотезу
    x = sm.add_constant(x)
    model = sm.OLS(y, x)
    results = model.fit()
    e = y - results.predict(x)
    e_x = []
    e_x.append(list(e))
    for i in range(1,k):
        e_x.append(list(e[i:]) + [0]*i)
    e_x = np.array(e_x).reshape(len(e_x[0]), -1)
    model = sm.OLS(y, e_x)
    results = model.fit()
    BG = len(y) * results.rsquared
    if BG > chi2.ppf(0.95, k):
        print('H0: p1 = p2 = 0 - отвергается\nавтокорреляция есть')
    else:
        print('H0: p1 = p2 = 0 - принимается\nавтокорреляция нет')
    """
    return k

def Sved_Ezenhart(k):
    """
    from scipy import stats
    import statsmodels.api as sm
    import numpy as np
    model = sm.OLS(y, x)
    results = model.fit()
    sp = results.predict(x) - y
    n1 = len(sp[sp>0])
    n2 = len(sp[sp<0])

    k = 1
    for ind in range(1, len(sp)):
        if (sp[ind-1] > 0 and sp[ind] < 0) or (sp[ind-1] < 0 and sp[ind] > 0):
            k+=1

    E = 2*n1*n2/(n1+n2) + 1
    D = (2*n1*n2*(2*n1*n2-n1-n2))/((n1+n2)**2)*(n1+n2-1)
    u = stats.norm.ppf(0.05/2)
    if  E-u*D <= k <= E+u*D:
        print('Автокор есть')
    else:
        print('Автокор нет')
    """
    return k

def Kochrain_Orkatt(k):
    """
    from scipy import stats
    import statsmodels.api as sm
    import pandas as pd
    x = np.array([1,2,3,4,5,6,7,8,9,10])
    y = x*10 + 5
    x = sm.add_constant(x)
    model = sm.OLS(y, x)
    results = model.fit()

    e = results.predict(x) - y
    et_1 = np.array(list(e[1:]) + [0])

    model = sm.OLS(et_1, e)
    results = model.fit()
    p = results.params[0]
    for i in range(100):
        y_t = p*np.append(y[1:],np.array([0]), axis = 0)- y

        x_t = p*np.append(x[1:],np.array([[0]*x.shape[1]]), axis = 0)- x
        model = sm.OLS(y_t, x_t)
        results = model.fit()
        e = results.predict(x_t) - y_t
        et_1 = np.append(e[1:],np.array([0]), axis = 0)
        model = sm.OLS(et_1, e)
        results = model.fit()
        p2 = results.params[0]
        p = p2
        p3 = p2

    if abs(p - p2) < 0.02:
        print(p2)
    else:
        print('Метод не сошелся')
    """
    
    return k

def Hildret_Lu(k):
    """
    from scipy import stats
    import statsmodels.api as sm
    import pandas as pd

    minim = 10**20
    p_ist = 0
    for i in range(-99, 100):
        p = i/100
        y_t = p*np.append(y[1:],np.array([0]), axis = 0)- y
        x_t = p*np.append(x[1:],np.array([[0]*x.shape[1]]), axis = 0)- x
        model = sm.OLS(y_t, x_t)
        results = model.fit()
        e = results.predict(x_t) - y_t
        if sum(e**2) < minim:
            minim = sum(e**2)
            p_ist = p
    print(p_ist)
    """
    return k

def Farrara_globera(k):
    """
    from scipy import stats
    import statsmodels.api as sm
    import pandas as pd
    from scipy.stats import chi2

    corr = pd.DataFrame(x).corr()
    det = np.linalg.det(corr)
    FG = -(x.shape[0] - 1 - (1/6)* (2*x.shape[1] + 5))*np.log(det)
    ch = chi2.ppf(0.95, (1/2)*(x.shape[1]**2 - x.shape[1]))
    if FG > ch:
        print('Мультиколлинеарность есть')
    else:
        print('Мультиколлинеарность нет')
    """
    return k

def Grebnev_regr(k):
    """
    from sklearn.linear_model import Ridge
    clf = Ridge(alpha=1.0)
    clf.fit(x.reshape(-1,1), y)
    print(clf.coef_)
    print(clf.intercept_)
    """
    return k

def PCA(k):
    """
    import numpy as np
    from sklearn.decomposition import PCA
    X = np.array([[-1, -1], 
                  [-2, -1], 
                  [-3, -2], 
                  [1, 1], 
                  [2, 1], 
                  [3, 2]])
    pca = PCA(n_components=1, svd_solver='full')
    pca.fit(X)
    pca.transform(X)
    """
    return k

def ACF_PACF(k):
    '''
    import pandas as pd
    import numpy as np
    import statsmodels.api as sm
    import matplotlib.pyplot as plt
    # Создаем временной ряд

    fig = plt.figure(figsize=(12,8))
    ax1 = fig.add_subplot(211)
    fig = sm.graphics.tsa.plot_pacf(ts, lags=50, ax=ax1)
    
    fig = plt.figure(figsize=(12,8))
    ax1 = fig.add_subplot(211)
    fig = sm.graphics.tsa.plot_acf(ts, lags=25, ax=ax1)
'''
    return k

def anomal_student(k):
    """
    from scipy import stats
    import numpy as np
    data = np.array(df['X'])
    t_stat, p_val = stats.ttest_1samp(data, np.mean(data))
    if p_val < 0.05:
        print("Выбросы присутствуют")
    else:
        print("Выбросов нет")
    """
    return k

def anomal_irvin(k):
    """
    import numpy as np
    data = np.array(df['X'])
    mean = np.mean(data)
    std = np.std(data)
    upper_bound = mean + 2.5 * std
    lower_bound = mean - 2.5 * std
    anomalies = []
    for value in data:
        if value < 0:
            anomalies.append(value)
        elif value > upper_bound or value < lower_bound:
            anomalies.append(value)
    print(anomalies)
    """
    return k

def Krit_Serii_Osn_med(k):
    """
    import numpy as np

    data = np.array([10, 12, 15, 14, 17, 19, 20, 22, 25, 28, 30, 32, 35, 38, 40])
    median = np.median(data)
    group1 = data[data >= median]
    group2 = data[data < median]
    n1 = len(np.where(np.diff(group1) != 0)[0]) + 1
    n2 = len(np.where(np.diff(group2) != 0)[0]) + 1
    S = min(n1, n2)
    alpha = 0.05
    n = len(data)
    critical_value = np.ceil((n - 1) * (1 - alpha))
    if S < critical_value:
        print("Временной ряд содержит тренд.")
    else:
        print("Временной ряд не содержит тренда.")
    """
    return k
def razn_sredn_urov(k):
    '''
    from scipy import stats
    sample1 = [1, 2, 3, 4, 5]
    sample2 = [6, 7, 8, 9, 10]
    t_stat, p_value = stats.ttest_ind(sample1, sample2)
    alpha = 0.05
    if p_value < alpha:
        print("Разность средних уровней выборок статистически значима.")
    else:
        print("Разность средних уровней выборок не статистически значима.")
    '''
    
    return k

def Foster_Stuart(k):
    '''
    import scipy as sci
    X = np.array([1,2,3,4,5,6,7,8,9,10])
    p_level=0.95
    a_level = 1 - p_level
    X = np.array(X)
    n = len(X)
    u = l = list()
    Xtemp = np.array(X[0])
    for i in range(1, n):
        Xmax = np.max(Xtemp)
        Xmin = np.min(Xtemp)
        u = np.append(u, 1 if X[i] > Xmax else 0)
        l = np.append(l, 1 if X[i] < Xmin else 0)
        Xtemp = np.append(Xtemp, X[i])

    d = np.int64(np.sum(u - l))
    S = np.int64(np.sum(u + l))
    mean_d = 0
    mean_S = 2*np.sum([1/i for i in range(2, n+1)])
    std_d = (mean_S)**0.5
    std_S = (mean_S - 4*np.sum([1/i**2 for i in range(2, n+1)]))**0.5
    t_d = (d - mean_d)/std_d
    t_S = (S - mean_S)/std_S
    df = n
    t_table = sci.stats.t.ppf((1 + p_level)/2 , df)
    conclusion_d = 'independent observations' if t_d <= t_table else 'dependent observations'
    conclusion_S = 'independent observations' if t_S <= t_table else 'dependent observations'       
    result = pd.DataFrame({
        'n': (n),
        'p_level': (p_level),
        'a_level': (a_level),
        'notation': ('d', 'S'),
        'statistic': (d, S),
        'normalized_statistic': (t_d, t_S),
        'crit_value': (t_table),
        'normalized_statistic ≤ crit_value': (t_d <= t_table, t_S <= t_table),
        'conclusion': (conclusion_d, conclusion_S)
        },
        index=['Foster_Stuart_test (trend in means)', 'Foster_Stuart_test (trend in variances)'])

    result
    '''
    return k

def skolz_sredn(k):
    """
    data = np.array(X)
    window_size = 2
    moving_averages = []
    for i in range(window_size - 1, len(data)):
        window = data[i - window_size + 1:i + 1]
        moving_averages.append(sum(window) / window_size)

    moving_averages
    """
    return k

def weighted_skolz_sredn(k):
    '''
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
weights = [0.1, 0.2, 0.3, 0.4]
weighted_moving_averages = []
for i in range(len(data)):
    if i < len(weights):
        window = data[:i+1]
        weighted_moving_averages.append(sum([a*b for a,b in zip(window, weights[:i+1])]) / sum(weights[:i+1]))
    else:
        window = data[i-len(weights)+1:i+1]
        weighted_moving_averages.append(sum([a*b for a,b in zip(window, weights)]) / sum(weights))

weighted_moving_averages
    '''
    return k
def srednhronolog(k):
    '''
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    window_size = 3
    rolling_midpoint_averages = []
    for i in range(len(data)):
        if i < window_size//2:
            window = data[:i+window_size//2+1]
            rolling_midpoint_averages.append(sum(window) / len(window))
        elif i >= len(data)-window_size//2:
            window = data[i-window_size//2:]
            rolling_midpoint_averages.append(sum(window) / len(window))
        else:
            window = data[i-window_size//2:i+window_size//2+1]
            rolling_midpoint_averages.append(sum(window) / len(window))
    rolling_midpoint_averages
    '''
    return k
def exponential_smoothing(k):
    """
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    alpha = 0.5
    smoothed_data = [data[0]]
    for i in range(1, len(data)):
        smoothed_value = alpha * data[i] + (1 - alpha) * smoothed_data[-1]
        smoothed_data.append(smoothed_value)
    smoothed_data 
    """
    return k

def Zarembka(k):
    '''
    from scipy.stats import gmean
    x = np.array([1,2,3,4,5,6,7,8,9,10])
    y = x*10 + 5

    y_geom = gmean(y)
    y_ = y/y_geom

    from scipy import stats
    import statsmodels.api as sm
    import pandas as pd
    x = sm.add_constant(x)
    model1 = sm.OLS(y_, x)
    results1 = model1.fit()
    ESS1 =  sum((results1.predict(x) - y_)**2)

    model2 = sm.OLS(np.log(y_), x)
    results2 = model2.fit()
    ESS2 =  sum((results2.predict(x) - np.log(y_))**2)

    Z = abs((len(y)/2)*np.log(ESS1/ESS2))
    if Z > chi2.ppf(0.95, 1):
        print('Выбираем полулогарифмическую')
    else:
        print('Выбираем линейную')
    '''
    return k
def box_cox(k):
    """
    import numpy as np
    from scipy import stats
    X = np.array([1,2,3,4,5,6,7,8,9,10])
    y = x*10 + 5
    xt, lmbda = stats.boxcox(X)
    print('Lambda parameter:', lmbda)
    # F = (y^lmda - 1)/ lambda см метод зарембки
    """
    return k

def Ber_Mck_Aler(k):
    '''
    from scipy.stats import gmean
    x = np.array([1,2,3,4,5,6,7,8,9,10])
    y = x*10 + 5
    x = sm.add_constant(x)


    results1 = sm.OLS(y, x).fit()
    y_oc1 = results1.predict(x)
    results2 = sm.OLS(np.log(y), x).fit()
    y_oc2 = results2.predict(x)

    results1 = sm.OLS(np.e**y_oc1, x).fit()
    e1 = np.e**y_oc1 - results1.predict(x)
    results2 = sm.OLS(y_oc2, x).fit()
    e2 = y_oc2 - results2.predict(x)

    new_x_1 = np.append(x, e1.reshape(-1,1), axis = 1)
    new_x_2 = np.append(x, e2.reshape(-1,1), axis = 1)

    results1 = sm.OLS(y, new_x_1).fit()
    results2 = sm.OLS(np.log(y), new_x_2).fit()
    results2.summary()
    # Если x2, ну или последний xi, у какой-то модели значим, то выбираем её первая линейн
    # вторая логарифм. Если у обоих моделей последний воэф не значим, значит берем дургой тест 
    '''
    return k

def Makin_white_Davids(k):
    '''
    from scipy.stats import gmean
    x = np.array([1,2,3,4,5,6,7,8,9,10])
    y = x*10 + 5
    x = sm.add_constant(x)


    results1 = sm.OLS(y, x).fit()
    y_oc1 = results1.predict(x)
    results2 = sm.OLS(np.log(y), x).fit()
    y_oc2 = results2.predict(x)

    for_ln = y_oc1 - np.e**y_oc2
    for_regr = np.log(y_oc1) - y_oc2

    new_x_1 = np.append(x, for_regr.reshape(-1,1), axis = 1)
    new_x_2 = np.append(x, for_ln.reshape(-1,1), axis = 1)

    results1 = sm.OLS(y, new_x_1).fit()
    results2 = sm.OLS(np.log(y), new_x_2).fit()
    results1.summary()
    # Если x2, ну или последний xi, у какой-то модели значим, то выбираем её первая линейн
    # вторая логарифм. Если у обоих моделей последний коэф не значим, значит берем дургой тест 
    '''
    return k

def Arima(k):
    """
    import matplotlib.pyplot as plt
    import statsmodels.api as sm
    X = np.array([1,2,3,4,5,6,7,8,9,10])
    # ACFPACF
    fig = plt.figure(figsize=(12,8))
    ax1 = fig.add_subplot(211)
    fig = sm.graphics.tsa.plot_acf(X, lags=4, ax=ax1)
    fig = sm.graphics.tsa.plot_pacf(X, lags=4, ax=ax1)
    # model
    p, d, q = (1,1,0)
    model = sm.tsa.ARIMA(X, order=(p, d, q))
    model_fit = model.fit()
    model_fit.forecast(steps=1) 
    # Есть ещё 
    statsmodels.tsa.statespace.sarimax.SARIMAX(endog, exog=None, order=(1, 0, 0), seasonal_order=(0, 0, 0, 0),) 
    """
    return k
def pred_Arima(k):
    '''
    from scipy.stats import t
    import pandas as pd
    alpha = 0.4
    d = X
    forecast = np.zeros(len(d))
    lvl = np.zeros(len(d))
    er = np.zeros(len(d))
    lvl[0] = d[0]
    er[0] = d[1] - d[0]
    for i in range(1, len(d)):
        if i == 1:
            lvl[i] = d[i]
            er[i] = d[i] - d[i-1]
        else:
            lvl[i] = alpha * d[i] + (1 - alpha) * lvl[i-1]
            er[i] = alpha * (d[i] - d[i-1]) + (1 - alpha) * er[i-1]
        forecast[i] = lvl[i] + er[i]
    forecast[0] = d[0]- 3
    sse = np.sum(er**2)
    std_er = np.sqrt(sse / (len(d) - 2))
    coeff = t.isf(0.05/2, len(X) - 1)
    d = pd.DataFrame({'Нижняя граница':forecast[-4:] - coeff * std_er,'Прогноз':forecast[-4:],'Верхняя граница':forecast[-4:] + coeff * std_er,})
    d
    '''
    return k

def white_noise_ljuing_box(k):
    '''
    import matplotlib.pyplot as plt
    import statsmodels.api as sm
    X = np.array([1,2,3,4,5,6,7,8,9,10])

    sm.stats.diagnostic.acorr_ljungbox(X)
    # Вероятно сюда нужно пихать остатки потому что белый шум вроде про остатки.
    '''
    return k

def FDL(k):
    '''содержит лаги экзогенной переменной по сути линейная регрессия
    y = xt-1 + xt-2 ...
    помощь в лагах np.append(x[1:],np.array([[0]*x.shape[1]])
    '''
    return k

def ADL(k):
    '''содержит лаги экзогенной переменной по сути линейная регрессия + эндогенная (смешанная)
    y =yt-1+ yt-2 + xt-1 + xt-2 ...
    помощь в лагах np.append(x[1:],np.array([[0]*x.shape[1]]), axis = 0)
    как строить, не знаю...
    '''
    return k

def test_diki_fulera(k):
    """
    l = sm.tsa.stattools.adfuller(X)
    print(f'ADF: {l[0]}, p-value: {l[1]}, critical_val: {l[4]["5%"]}')
    if l[0] < -l[4]["5%"]:
        print('Единичный корень есть')
    else:
        print('Единичного корня нет')
    """
    return k

def Getis_Ord(k):
    """
    
    x = np.random.random((10,10))
    Vij = 1/x
    W = Vij/Vij.sum(axis = 1)

    s1 = 0
    s2 = 0
    for i in range(len(x)):
        for j in range(len(x[0])):
            s1 += W[i,j]*x[i,i]*x[j,j]
            s2 += x[i,i]*x[j,j]
    G = s1/s2
    E_G = W.sum()/(len(W)**2 - len(W))
    if G > E_G:
        print('Наблюдается пространственная кластерицация объектов с высокими значениями')
    else:
        print('Наблюдается пространственная кластерицация объектов с низкими значениями')
    
    #from libpysal.weights import Kernel
    #import pysal
    #w = Kernel(data.geometry)
    #Getis_Ord = pysal.explore.esda.Getis_Ord(data['variable'], w) (-1, 1) -отриц автокор
        
    """
    return k

def Jiri(k):
    '''
    x = np.random.random((10,10))
    Vij = 1/x
    W = Vij/Vij.sum(axis = 1)

    s1 = 0
    s2 = 0
    for i in range(len(x)):
        for j in range(len(x[0])):
            s1 += W[i,j]*(x[i,i] - x[j,j])**2
            s2 += (x[i,i] - np.mean(x))**2
    C = ((len(x[0]) - 1)/(2*W.sum()))* (s1/s2)

    if C == 1:
        print('Пространственная кореляция отсутствует')
    elif 0 < C < 1:
        print('Положительная пространственная кореляция')
    elif 1 < C < 2:
        print('Отрицательная пространственная кореляция')
        
    #from libpysal.weights import Kernel
    #import pysal
    #w = Kernel(data.geometry)
    #GM_Lag = pysal.explore.esda.GM_Lag(data['variable'], w) (-1, 1) -отриц автокор

    '''
    return k 



def params(k):
    '''
    self.n = df_x.shape[0]
    try:
      self.k = df_x.shape[1]
    except:
      self.k = 1
    self.df_x = df_x
    self.df_y = df_y
    self.df_x_b = sm.add_constant(df_x)
    self.model = sm.OLS(self.df_y,self.df_x_b).fit()
    self.rnd_dev = self.model.predict(self.df_x_b) - np.array(self.df_y)
    
    return self.model.params
    '''
    return(k)
    
def significance_of_parameters(k):
    """
    self.n = df_x.shape[0]
    try:
      self.k = df_x.shape[1]
    except:
      self.k = 1
    self.df_x = df_x
    self.df_y = df_y
    self.df_x_b = sm.add_constant(df_x)
    self.model = sm.OLS(self.df_y,self.df_x_b).fit()
    self.rnd_dev = self.model.predict(self.df_x_b) - np.array(self.df_y)
    
    a = 0.95
    
    #|t_calc| < t_tabl not significant
    print('t_tabl:', t.ppf(1-a, self.n-self.k-1))
    print('t_calc:\n', self.model.tvalues)
    """
    return(k)

def fisher(k):
    """
    #Н0: b_1 = ... = b_n = 0
    #Н1: b_1 != ... != b_n != 0
    
    #If F_calc > F_tabl, then Н0 rejected
    self.n = df_x.shape[0]
    try:
      self.k = df_x.shape[1]
    except:
      self.k = 1
    self.df_x = df_x
    self.df_y = df_y
    self.df_x_b = sm.add_constant(df_x)
    self.model = sm.OLS(self.df_y,self.df_x_b).fit()
    self.rnd_dev = self.model.predict(self.df_x_b) - np.array(self.df_y)
    
    a = 0.95

    print('F_tabl:', f.ppf(1-a,self.k, self.n-self.k-1))
    print('F_calc:', self.model.fvalue)
    """
    return(k)
    
def R(k):
    '''
    self.n = df_x.shape[0]
    try:
      self.k = df_x.shape[1]
    except:
      self.k = 1
    self.df_x = df_x
    self.df_y = df_y
    self.df_x_b = sm.add_constant(df_x)
    self.model = sm.OLS(self.df_y,self.df_x_b).fit()
    self.rnd_dev = self.model.predict(self.df_x_b) - np.array(self.df_y)
    
    print('R = ',self.model.rsquared)
    print('R_adj = ',self.model.rsquared_adj)
    print('Average relative approximation errors = ', sum(abs(((self.model.predict(self.df_x_b)-self.df_y)/self.df_y)))/(self.n))
    '''
    return(k)
    
def predict(k):
    """
    self.n = df_x.shape[0]
    try:
      self.k = df_x.shape[1]
    except:
      self.k = 1
    self.df_x = df_x
    self.df_y = df_y
    self.df_x_b = sm.add_constant(df_x)
    self.model = sm.OLS(self.df_y,self.df_x_b).fit()
    self.rnd_dev = self.model.predict(self.df_x_b) - np.array(self.df_y)
    
    X = [] # Надо написать(!)
    col = '...' # Надо написать(!)
    
    #pd.DataFrame([[1,1,2],[1,2,2]], columns = ['const','x1','x2']), 'x1' 
    P = self.model.predict(X)
    print('y = ', P)
  
    Se_2 = 1/(self.n-self.k-1)*sum((self.df_y - self.df_y.mean())**2)
    Se = Se_2**0.5      
    X = X[col]
    min_ = P-Se * t.ppf(1-0.05, self.n-self.k-1) * (1 + 1/self.n + (X-self.df_x.mean())**2/(sum((self.df_x-self.df_x.mean()**2))) )**0.5
    max_ = P[0]+Se * t.ppf(1-0.05, self.n-self.k-1) * (1 + 1/self.n + (X-self.df_x.mean())**2/(sum((self.df_x-self.df_x.mean()**2))) )**0.5
    print('Confidence interval Y:\n from', min_, '\n to', max_)
    """
    return(k)
    
def breuschpagan(k):
    """
    self.n = df_x.shape[0]
    try:
      self.k = df_x.shape[1]
    except:
      self.k = 1
    self.df_x = df_x
    self.df_y = df_y
    self.df_x_b = sm.add_constant(df_x)
    self.model = sm.OLS(self.df_y,self.df_x_b).fit()
    self.rnd_dev = self.model.predict(self.df_x_b) - np.array(self.df_y)
    
    #If p_value > a homoscedasticity
    
    names = ['Lagrange multiplier statistic', 'p-value','f-value', 'f p-value']
    test = sms.het_breuschpagan(self.model.resid, self.model.model.exog)
    print(lzip(names, test)[1])
    """
    return(k)
    
def Goldfeld_Qandt(k):
    """
    #If p_value > a homoscedasticity
    self.n = df_x.shape[0]
    try:
      self.k = df_x.shape[1]
    except:
      self.k = 1
    self.df_x = df_x
    self.df_y = df_y
    self.df_x_b = sm.add_constant(df_x)
    self.model = sm.OLS(self.df_y,self.df_x_b).fit()
    self.rnd_dev = self.model.predict(self.df_x_b) - np.array(self.df_y)
    test = sm.stats.diagnostic.het_goldfeldquandt(self.df_y, self.df_x_b, drop=0.2)
    print('p_value -', test[1])
    """
    return(k)
    
def spearmen(k):
    """
    #if p_value > a homoscedasticity
    self.n = df_x.shape[0]
    try:
      self.k = df_x.shape[1]
    except:
      self.k = 1
    self.df_x = df_x
    self.df_y = df_y
    self.df_x_b = sm.add_constant(df_x)
    self.model = sm.OLS(self.df_y,self.df_x_b).fit()
    self.rnd_dev = self.model.predict(self.df_x_b) - np.array(self.df_y)
    
    col = '...' # Надо написать(!)
    
    test = stats.spearmanr(self.df_x[col], abs(np.array(self.rnd_dev)))
    print(test)
    """
    return(k)
    
def park(k):
    """#if coeff significance not homoscedasticity P < a
    self.n = df_x.shape[0]
    try:
      self.k = df_x.shape[1]
    except:
      self.k = 1
    self.df_x = df_x
    self.df_y = df_y
    self.df_x_b = sm.add_constant(df_x)
    self.model = sm.OLS(self.df_y,self.df_x_b).fit()
    self.rnd_dev = self.model.predict(self.df_x_b) - np.array(self.df_y)
    
    col = '...' # Надо написать(!)
    
    x = np.array(self.df_x[col])
    ln_x = np.log(x)
    u_2 = np.array(self.rnd_dev)**2
    ln_u_2 = np.log(u_2)

    X = pd.DataFrame({'ln(x)':ln_x})
    X = sm.add_constant(X)

    model = sm.OLS(ln_u_2, X)
    results = model.fit()
    print(results.summary().tables[1])
    """
    return(k)
    
def glayzer(k):
    """
    #if coeff significance not homoscedasticity P < a
    self.n = df_x.shape[0]
    try:
      self.k = df_x.shape[1]
    except:
      self.k = 1
    self.df_x = df_x
    self.df_y = df_y
    self.df_x_b = sm.add_constant(df_x)
    self.model = sm.OLS(self.df_y,self.df_x_b).fit()
    self.rnd_dev = self.model.predict(self.df_x_b) - np.array(self.df_y)
    
    col = '...' #Надо написать(!)
    
    x = np.array(self.df_x[col])
    u = abs(np.array(self.rnd_dev))

    # x**(-1)
    X = 1/x
    X = sm.add_constant(X)
    model = sm.OLS(u, X)
    results = model.fit()
    print(results.summary().tables[1])

    # x**(-0.5)
    X = 1/x**(0.5)
    X = sm.add_constant(X)
    model = sm.OLS(u, X)
    results = model.fit()
    print(results.summary().tables[1])

    # x**(0.5)
    X = x**(0.5)
    X = sm.add_constant(X)
    model = sm.OLS(u, X)
    results = model.fit()
    print(results.summary().tables[1])

    # x**(-1)
    X = x**(1.5)
    X = sm.add_constant(X)
    model = sm.OLS(u, X)
    results = model.fit()
    print(results.summary().tables[1])

    # x
    X = x
    X = sm.add_constant(X)
    model = sm.OLS(u, X)
    results = model.fit()
    print(results.summary().tables[1])
    """
    return(k)
    
def white(k):
    """
    #if coeff significance not homoscedasticity P < a
    self.n = df_x.shape[0]
    try:
      self.k = df_x.shape[1]
    except:
      self.k = 1
    self.df_x = df_x
    self.df_y = df_y
    self.df_x_b = sm.add_constant(df_x)
    self.model = sm.OLS(self.df_y,self.df_x_b).fit()
    self.rnd_dev = self.model.predict(self.df_x_b) - np.array(self.df_y)
    
    col = '...' #надо написать(!)
    
    x = np.array(self.df_x[col])
    x_2 = np.array(self.df_x[col])**2
    u_2 = np.array(self.rnd_dev)**2

    X = pd.DataFrame({'x':x,'x_2':x_2})
    X = sm.add_constant(X)

    model = sm.OLS(u_2, X)
    results = model.fit()
    print(results.summary().tables[1])
    """
    return(k)
    
def dw(k):
    """
    self.n = df_x.shape[0]
    try:
      self.k = df_x.shape[1]
    except:
      self.k = 1
    self.df_x = df_x
    self.df_y = df_y
    self.df_x_b = sm.add_constant(df_x)
    self.model = sm.OLS(self.df_y,self.df_x_b).fit()
    self.rnd_dev = self.model.predict(self.df_x_b) - np.array(self.df_y)
    
    Durbin_Wotson = pd.DataFrame(self.model.summary().tables[2])[3].loc[0]
    Durbin_Wotson = float(str(Durbin_Wotson).replace(' ',''))
    dl = 1.27
    du = 1.45

    a = 0
    b = 4
    print('Durbin_Wotson=', Durbin_Wotson)
    print(f'{a:0.2f}---{dl:0.2f}---{du:0.2f}---{(b-du):0.2f}---{(b-dl):0.2f}---{b:0.2f}')
    print('    cov>0        cov=0         cov<0')
    """
    return(k)
    
def series_method(k):
    """#if <k< not autocorrelation
    self.n = df_x.shape[0]
    try:
      self.k = df_x.shape[1]
    except:
      self.k = 1
    self.df_x = df_x
    self.df_y = df_y
    self.df_x_b = sm.add_constant(df_x)
    self.model = sm.OLS(self.df_y,self.df_x_b).fit()
    self.rnd_dev = self.model.predict(self.df_x_b) - np.array(self.df_y)
    
    a = 0.95
    
    sp = self.rnd_dev
    n1 = len(sp[sp>0])
    n2 = len(sp[sp<0])
    
    k = 1
    for ind in range(1, len(sp)):
      if (sp[ind-1] > 0 and sp[ind] < 0) or (sp[ind-1] < 0 and sp[ind] > 0):
        k+=1

    E = 2*n1*n2/(n1+n2)
    D = (2*n1*n2*(2*n1*n2-n1-n2))/((n1+n2)**2)*(n1+n2-1)
    u = stats.norm.ppf(1 - a/2)
    print('left -', E-u*D)
    print('k -', k)
    print('right -', E+u*D)
    """
    return(k)
    
def reset(k):
    """
    #p_value > 0.05 No new
    self.n = df_x.shape[0]
    try:
      self.k = df_x.shape[1]
    except:
      self.k = 1
    self.df_x = df_x
    self.df_y = df_y
    self.df_x_b = sm.add_constant(df_x)
    self.model = sm.OLS(self.df_y,self.df_x_b).fit()
    self.rnd_dev = self.model.predict(self.df_x_b) - np.array(self.df_y)

    reset = dg.linear_reset(self.model, power = 2, test_type = 'fitted', use_f = True)
    print('Ramsey-Reset Test F-Statistics:', np.round(reset.fvalue, 6))
    print('Ramsey-Reset Test P-Value:', np.round(reset.pvalue, 6))
    """
    return(k)
    
def shapiro_wilka(k):
    """
    #if p_value > a norm
    self.n = df_x.shape[0]
    try:
      self.k = df_x.shape[1]
    except:
      self.k = 1
    self.df_x = df_x
    self.df_y = df_y
    self.df_x_b = sm.add_constant(df_x)
    self.model = sm.OLS(self.df_y,self.df_x_b).fit()
    self.rnd_dev = self.model.predict(self.df_x_b) - np.array(self.df_y)
    
    print('p_value', shapiro(self.rnd_dev)[1])
    """
    return(k)
    
def jarque_bera(k):
    """
    #if p_value > a norm
    self.n = df_x.shape[0]
    try:
      self.k = df_x.shape[1]
    except:
      self.k = 1
    self.df_x = df_x
    self.df_y = df_y
    self.df_x_b = sm.add_constant(df_x)
    self.model = sm.OLS(self.df_y,self.df_x_b).fit()
    self.rnd_dev = self.model.predict(self.df_x_b) - np.array(self.df_y)
    
    print('p_value', stats.jarque_bera(self.rnd_dev)[1])
    """
    return(k)
    
def betta(k):
    '''
    self.n = df_x.shape[0]
    try:
      self.k = df_x.shape[1]
    except:
      self.k = 1
    self.df_x = df_x
    self.df_y = df_y
    self.df_x_b = sm.add_constant(df_x)
    self.model = sm.OLS(self.df_y,self.df_x_b).fit()
    self.rnd_dev = self.model.predict(self.df_x_b) - np.array(self.df_y)
    
    for el in self.df_x.columns:
      
      print('betta',el,'-',self.model.params[el]*(np.var(self.df_x[el], ddof = 1))**0.5/(np.var(self.df_y, ddof = 1))**0.5)
    '''
    return(k)
    
def delta(self):
    '''
    self.n = df_x.shape[0]
    try:
      self.k = df_x.shape[1]
    except:
      self.k = 1
    self.df_x = df_x
    self.df_y = df_y
    self.df_x_b = sm.add_constant(df_x)
    self.model = sm.OLS(self.df_y,self.df_x_b).fit()
    self.rnd_dev = self.model.predict(self.df_x_b) - np.array(self.df_y)
    
    for el in self.df_x.columns:
      
      print('delta',el,'-',self.model.params[el]*np.mean(self.df_x[el])/(np.mean(self.df_y)))
    '''
    return(k)
    
def elastic(k):
    '''
    self.n = df_x.shape[0]
    try:
      self.k = df_x.shape[1]
    except:
      self.k = 1
    self.df_x = df_x
    self.df_y = df_y
    self.df_x_b = sm.add_constant(df_x)
    self.model = sm.OLS(self.df_y,self.df_x_b).fit()
    self.rnd_dev = self.model.predict(self.df_x_b) - np.array(self.df_y)
    matrix = self.df_x.join(self.df_y)
    for el in self.df_x.columns:
      r = matrix.corr().loc[['y'],[el]].values[0][0]

      print('elastic',el,'-',self.model.params[el]*r/self.model.rsquared)
    '''
    return(k)
    
def VIF(k):
    """
    self.n = df_x.shape[0]
    try:
      self.k = df_x.shape[1]
    except:
      self.k = 1
    self.df_x = df_x
    self.df_y = df_y
    self.df_x_b = sm.add_constant(df_x)
    self.model = sm.OLS(self.df_y,self.df_x_b).fit()
    self.rnd_dev = self.model.predict(self.df_x_b) - np.array(self.df_y)
    vif = pd.DataFrame()
    vif['VIF'] = [variance_inflation_factor(self.df_x.values, i) for i in range(self.df_x.shape[1])]
    vif['variable'] = self.df_x.columns
    print(vif)
    """
    return(k)



def logit():
    """
    data = pd.read_csv('data.csv', delimiter = ';')
    X = data.iloc[:,1:]
    y = data.iloc[:,0]
    # y должен быть приведен в бинарный вид!
    y = y<=500

    #------------------------------------------------------------------------------------------------------------------
    import statsmodels.api as sm
    from sklearn.metrics import confusion_matrix, accuracy_score, roc_curve, auc

    X = sm.add_constant(X)
    logit_model = sm.Logit(y, X).fit()

    print(result.summary())
    # Вывод метрик для модели logit
    print('Метрики модели logit:')
    # print('Log-Likelihood:', logit_model.llf)
    print('Pseudo R-squared:', logit_model.prsquared)
    # print('Матрица ошибок:\n', confusion_matrix(y, logit_model.predict(X) > 0.5))
    # print('Точность:', accuracy_score(y, logit_model.predict(X) > 0.5))
    # fpr, tpr, thresholds = roc_curve(y, logit_model.predict(X))
    # print('AUC:', auc(fpr, tpr))
    print('Если значение данного коэффициента близко к единице, то модель регрессии считается адекватной реальным данным')
    """
    return 

def probit():
    """
    data = pd.read_csv('data.csv', delimiter = ';')
    X = data.iloc[:,1:]
    y = data.iloc[:,0]
    # y должен быть приведен в бинарный вид!
    y = y<=500

    #------------------------------------------------------------------------------------------------------------------
    import statsmodels.api as sm

    X = sm.add_constant(X)
    probit_model = sm.Probit(y, X).fit()

    print(result.summary())
    # Вывод метрик для модели probit
    print('Метрики модели probit:')
    # print('Log-Likelihood:', probit_model.llf)
    print('Pseudo R-squared:', probit_model.prsquared)
    # print('Матрица ошибок:\n', confusion_matrix(y_test, probit_model.predict(X) > 0.5))
    # print('Точность:', accuracy_score(y, probit_model.predict(X) > 0.5))
    # fpr, tpr, thresholds = roc_curve(y, probit_model.predict(X))
    # print('AUC:', auc(fpr, tpr))
    print('Если значение данного коэффициента близко к единице, то модель регрессии считается адекватной реальным данным')
    """
    return

def boxplot():
    '''
    data = pd.read_csv('data.csv', delimiter = ';')

    X = data.iloc[:,1:]
    y = data.iloc[:,0]
    # Построение boxplot
    fig, ax = plt.subplots()
    ax.boxplot(X)

    # Настройка осей и заголовка
    ax.set_xticklabels(X.columns)
    ax.set_ylabel('Values')
    ax.set_title('Boxplot Example')

    # Отображение графика
    plt.show()
    '''

def dar_wats():
    """
    from statsmodels.stats.stattools import durbin_watson
    data = pd.read_csv('data.csv', delimiter = ';')
    X = data.iloc[:,1:]
    y = data.iloc[:,0]

    # Вычисление статистики Дарбина-Уотсона
    dw_statistic = durbin_watson(X)

    # Вывод статистики Дарбина-Уотсона
    print(f"Статистика Дарбина-Уотсона: {dw_statistic}")
    print('Значение около 2 указывает на отсутствие автокорреляции, значения ниже 2 - на положительную автокорреляцию, а значения выше 2 - на отрицательную автокорреляцию')
    """

def ac_ljungbox():
    '''
    from statsmodels.stats.diagnostic import acorr_ljungbox


    data = pd.read_csv('data.csv', delimiter = ';')
    X = data.iloc[:,1:]
    y = data.iloc[:,0]

    # Вычисление статистики Льюинга-Бокса и p-значений
    print(acorr_ljungbox(X['<OPEN>'], lags=[5], return_df=True))
    print('Если p-значение меньше выбранного уровня значимости (обычно 0.05), то гипотеза об отсутствии автокорреляции отвергается, что указывает на наличие автокорреляции в ряде')
    print('Высокие значения статистики Льюинга-Бокса указывают на сильную автокорреляцию в ряде, даже если p-значение не ниже уровня значимости. В таком случае, можно сделать вывод о наличии автокорреляции, но это несет меньшую уверенность, чем при низком p-значении')
    '''

def matrix_granitc():
    '''
    df = pd.read_excel('Семинар 7 Данные для моделирования Логит, Пробит.xlsx', sheet_name = 0)
    df.fillna(1e-5, inplace = True)
    regions = df['Регион регистрации'].unique().tolist()
    # По данным из интернета:
    neighbours = {
        'Алтайский край': ['Красноярский край'],
        'Краснодарский край': ['Ростовская область', 'Ставропольский край'],
        'Белгородская область': ['Курская область', 'Воронежская область', 'Харьковская область (Украина)'],
        'Красноярский край': ['Иркутская область', 'Красноярский край'],
        'Брянская область': ['Калужская область', 'Орловская область', 'Смоленская область', 'Тверская область'],
        'Владимирская область': ['Ивановская область', 'Московская область', 'Нижегородская область', 'Рязанская область', 'Тульская область', 'Ярославская область'],
        'Воронежская область': ['Белгородская область', 'Курганская область', 'Липецкая область', 'Ростовская область', 'Саратовская область', 'Тамбовская область'],
        'Ивановская область': ['Владимирская область', 'Костромская область', 'Московская область',' Нижегородская область', 'Рязанская область', 'Тверская область', 'Ярославская область'],
        'Калужская область': ['Брянская область', 'Московская область', 'Орловская область', 'Смоленская область', 'Тульская область'],
        'Костромская область': ['Владимирская область', 'Ивановская область', 'Ярославская область'],
        'Курская область': ['Белгородская область', 'Брянская область', 'Орловская область', 'Рязанская область', 'Тамбовская область', 'Винницкая область']
    }
    # Сначала создадим матрицу, целиком заполненную нулями
    df_gran = pd.DataFrame(0, index=regions, columns=regions)

    # Теперь заполним в соответвии с данными, указанными в ячейке выше:
    # 1 - соседствуют, 0 - нет
    for city1, lst_city2 in neighbours.items():
        for city2 in lst_city2:
            if city1 and city2 in regions:
                df_gran.loc[city1, city2] = 1
                df_gran.loc[city2, city1] = 1

    # Добавим цвета
    def highlight_val(val):
        color = 'lightgreen' if val == 1 else 'white'
        return f'background-color: {color}'

    df_gran = df_gran.style.applymap(highlight_val)
    df_gran
    '''

def matrix_rasstoyaniiy():
    '''
    # Координаты центров регионов по данным из интернета:
    regions_coor = {
        'Алтайский край': [53.348070, 83.776860],
        'Краснодарский край': [45.035470, 38.975313],
        'Белгородская область': [50.629250, 37.674912],
        'Красноярский край': [56.012560, 92.870010],
        'Брянская область': [53.242600, 34.366220],
        'Владимирская область': [56.135740, 40.407640],
        'Воронежская область': [51.659250, 39.196920],
        'Ивановская область': [56.996870, 40.975050],
        'Калужская область': [54.513160, 36.261040],
        'Костромская область': [58.595080, 44.522280],
        'Курская область': [51.738180, 36.191250],
        'Липецкая область': [52.613980, 39.570330],
        'Московская область': [55.633200, 37.384940],
        'Орловская область': [52.968680, 36.069060],
        'Рязанская область': [54.619720, 39.746110],
        'Смоленская область': [54.786680, 32.045860],
        'Тамбовская область': [52.721920, 41.452120],
        'Тверская область': [56.858360, 35.917550],
        'Тульская область': [54.196940, 37.618010],
        'Ярославская область': [57.626560, 39.884470],
        'Москва': [55.755826, 37.617300]
    }
    # Сначала создадим матрицу, целиком заполненную нулями
    df_dist = pd.DataFrame(0, index=regions, columns=regions)

    # Теперь заполним в соответвии с данными, указанными в ячейке выше
    # Для определения кратчайшего расстояния между двумя точками можно использовать формулу гаверсинусов
    from math import sin, cos, sqrt, atan2, radians

    def haversine(lat1, lon1, lat2, lon2):
        # перевести координаты в радианы
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # радиус Земли в км
        R = 6371

        # разница координат
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        # формула гаверсинусов
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # кратчайшее расстояние между точками
        distance = R * c

        return round(distance,2)

    dist_lst = []
    for ind, region1 in enumerate(regions):
        if ind != len(df_dist):
            for region2 in regions[ind+1:]:
                dist_lst.append(haversine(regions_coor[region1][0], regions_coor[region1][1],
                                                         regions_coor[region2][0], regions_coor[region2][1]))
                df_dist.loc[region1, region2] = haversine(regions_coor[region1][0], regions_coor[region1][1],
                                                         regions_coor[region2][0], regions_coor[region2][1]) 
                df_dist.loc[region2, region1] = haversine(regions_coor[region1][0], regions_coor[region1][1],
                                                         regions_coor[region2][0], regions_coor[region2][1]) 
    df_dist
    '''

def prostranstv_vesa():
    '''
    # Координаты центров регионов по данным из интернета:
    regions_coor = {
        'Алтайский край': [53.348070, 83.776860],
        'Краснодарский край': [45.035470, 38.975313],
        'Белгородская область': [50.629250, 37.674912],
        'Красноярский край': [56.012560, 92.870010],
        'Брянская область': [53.242600, 34.366220],
        'Владимирская область': [56.135740, 40.407640],
        'Воронежская область': [51.659250, 39.196920],
        'Ивановская область': [56.996870, 40.975050],
        'Калужская область': [54.513160, 36.261040],
        'Костромская область': [58.595080, 44.522280],
        'Курская область': [51.738180, 36.191250],
        'Липецкая область': [52.613980, 39.570330],
        'Московская область': [55.633200, 37.384940],
        'Орловская область': [52.968680, 36.069060],
        'Рязанская область': [54.619720, 39.746110],
        'Смоленская область': [54.786680, 32.045860],
        'Тамбовская область': [52.721920, 41.452120],
        'Тверская область': [56.858360, 35.917550],
        'Тульская область': [54.196940, 37.618010],
        'Ярославская область': [57.626560, 39.884470],
        'Москва': [55.755826, 37.617300]
    }
    # Сначала создадим матрицу, целиком заполненную нулями
    df_dist = pd.DataFrame(0, index=regions, columns=regions)

    # Теперь заполним в соответвии с данными, указанными в ячейке выше
    # Для определения кратчайшего расстояния между двумя точками можно использовать формулу гаверсинусов
    from math import sin, cos, sqrt, atan2, radians

    def haversine(lat1, lon1, lat2, lon2):
        # перевести координаты в радианы
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # радиус Земли в км
        R = 6371

        # разница координат
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        # формула гаверсинусов
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # кратчайшее расстояние между точками
        distance = R * c

        return round(distance,2)

    dist_lst = []
    for ind, region1 in enumerate(regions):
        if ind != len(df_dist):
            for region2 in regions[ind+1:]:
                dist_lst.append(haversine(regions_coor[region1][0], regions_coor[region1][1],
                                                         regions_coor[region2][0], regions_coor[region2][1]))
                df_dist.loc[region1, region2] = haversine(regions_coor[region1][0], regions_coor[region1][1],
                                                         regions_coor[region2][0], regions_coor[region2][1]) 
                df_dist.loc[region2, region1] = haversine(regions_coor[region1][0], regions_coor[region1][1],
                                                         regions_coor[region2][0], regions_coor[region2][1]) 
    # построение матрицы пространственных весов
    def weights(dist_matrix):
        dist_matrix = dist_matrix.applymap(lambda x: 1/x if x!= 0 else 0)
        s = dist_matrix.sum().sum()
        return dist_matrix/s

    # Рассчитываем матрицу весов
    W = weights(df_dist)
    W
    '''

def matrix_bin_blizc_sosedi():
    '''
    # Координаты центров регионов по данным из интернета:
    regions_coor = {
        'Алтайский край': [53.348070, 83.776860],
        'Краснодарский край': [45.035470, 38.975313],
        'Белгородская область': [50.629250, 37.674912],
        'Красноярский край': [56.012560, 92.870010],
        'Брянская область': [53.242600, 34.366220],
        'Владимирская область': [56.135740, 40.407640],
        'Воронежская область': [51.659250, 39.196920],
        'Ивановская область': [56.996870, 40.975050],
        'Калужская область': [54.513160, 36.261040],
        'Костромская область': [58.595080, 44.522280],
        'Курская область': [51.738180, 36.191250],
        'Липецкая область': [52.613980, 39.570330],
        'Московская область': [55.633200, 37.384940],
        'Орловская область': [52.968680, 36.069060],
        'Рязанская область': [54.619720, 39.746110],
        'Смоленская область': [54.786680, 32.045860],
        'Тамбовская область': [52.721920, 41.452120],
        'Тверская область': [56.858360, 35.917550],
        'Тульская область': [54.196940, 37.618010],
        'Ярославская область': [57.626560, 39.884470],
        'Москва': [55.755826, 37.617300]
    }
    # Сначала создадим матрицу, целиком заполненную нулями
    df_dist = pd.DataFrame(0, index=regions, columns=regions)

    # Теперь заполним в соответвии с данными, указанными в ячейке выше
    # Для определения кратчайшего расстояния между двумя точками можно использовать формулу гаверсинусов
    from math import sin, cos, sqrt, atan2, radians

    def haversine(lat1, lon1, lat2, lon2):
        # перевести координаты в радианы
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # радиус Земли в км
        R = 6371

        # разница координат
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        # формула гаверсинусов
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # кратчайшее расстояние между точками
        distance = R * c

        return round(distance,2)

    dist_lst = []
    for ind, region1 in enumerate(regions):
        if ind != len(df_dist):
            for region2 in regions[ind+1:]:
                dist_lst.append(haversine(regions_coor[region1][0], regions_coor[region1][1],
                                                         regions_coor[region2][0], regions_coor[region2][1]))
                df_dist.loc[region1, region2] = haversine(regions_coor[region1][0], regions_coor[region1][1],
                                                         regions_coor[region2][0], regions_coor[region2][1]) 
                df_dist.loc[region2, region1] = haversine(regions_coor[region1][0], regions_coor[region1][1],
                                                         regions_coor[region2][0], regions_coor[region2][1]) 

    # Квартили расстояний D(q):
    quartiles = np.percentile(dist_lst, [25, 50, 75])

    print('25-й квартиль: {:.2f} км'.format(quartiles[0]))
    print('Медиана: {:.2f} км'.format(quartiles[1]))
    print('75-й квартиль: {:.2f} км'.format(quartiles[2]))

    def dist_q(x, D, γ = 2):
    # Матрица расстояний при q = 2 и γ = 2
    # Т.е медианное занчение является максимальным расстоянием, 
    # дальше которого взаимодействие между объектами является несущественным

        if x == 0:
            return 0
        elif x <= D:
    #         return 1/(x**γ)
    # Для бинарной:
            return 1
        else:
            return 0


    df_dist_2 = df_dist.applymap(lambda x: dist_q(x, quartiles[1], γ = 2))
    df_dist_2
    '''

def matrix_dist_size():
    '''
    from scipy.spatial.distance import cdist

    # Пример координат объектов и их размеров
    coordinates = [(1, 2), (3, 4), (5, 6)]
    sizes = [2, 3, 1]

    # Создание матрицы расстояний с учетом размера объекта
    dist_matrix = cdist(coordinates, coordinates, metric='euclidean')

    # Учет размера объекта
    for i in range(len(coordinates)):
        for j in range(len(coordinates)):
            dist_matrix[i, j] -= sizes[i] + sizes[j]

    # Вывод матрицы расстояний
    print(dist_matrix)
    '''


def pool_m():
    '''
    year = pd.Categorical(df["YEAR"])
    df = df.set_index(["MARK", "YEAR"])
    df["YEAR"] = year
    
    from linearmodels.panel import PooledOLS
    import statsmodels.api as sm

    exog_vars = ["column_1","column_2","column_3","column_4","column_6","column_7","column_8","column_9","column_10","column_11","column_12","column_13","column_15","column_16","column_17"]
    exog = sm.add_constant(df[exog_vars])
    pooled_mod = PooledOLS(df.target, exog)
    pooled_res = pooled_mod.fit(cov_type = 'clustered',
                        cluster_entity = True)
    print(pooled_res)
    #Variant 2
    #reg= sm.OLS(df.target, exog).fit(cov_type="HC3")
    #reg.summary()
    '''

def fixed_m():
    '''
    year = pd.Categorical(df["YEAR"])
    df = df.set_index(["MARK", "YEAR"])
    df["YEAR"] = year
    
    from linearmodels.panel import PanelOLS
    FE_mod = PanelOLS(df.target, exog, entity_effects = True, time_effects = True)
    FE_res = FE_mod.fit(cov_type = 'clustered',
                        cluster_entity = True)
    print(FE_res.summary)
    '''


def random_effects_model():
    '''
    year = pd.Categorical(df["YEAR"])
    df = df.set_index(["MARK", "YEAR"])
    df["YEAR"] = year
    
    from linearmodels.panel import RandomEffects
    RE_mod = RandomEffects(df.target, exog)
    RE_res = RE_mod.fit(cov_type = 'clustered',
                        cluster_entity = True)
    print(RE_res.summary)
    '''

def hausman():
    """
    from scipy import stats

    # Вычисление оценок параметров и их ковариационных матриц
    params_random_effects = RE_res.params
    cov_random_effects = RE_res.cov

    params_fixed_effects = FE_res.params
    cov_fixed_effects = FE_res.cov

    # Вычисление разницы оценок параметров
    diff_params = params_random_effects - params_fixed_effects

    # Вычисление ковариационной матрицы разницы оценок параметров
    cov_diff_params = cov_random_effects - cov_fixed_effects

    # Вычисление тестовой статистики Хаусмана
    hausman_stat = np.dot(np.dot(diff_params, np.linalg.inv(cov_diff_params)), diff_params)

    # Вычисление p-значения
    p_value = 1 - stats.chi2.cdf(hausman_stat, df=diff_params.shape[0])

    print("Hausman Test Statistic:", hausman_stat)
    print("P-value:", p_value)
    print('p-значение: p-значение показывает вероятность получить наблюдаемое значение статистики теста Хаусмана или более экстремальное значение, при условии, что нулевая гипотеза верна. Если p-значение меньше уровня значимости (обычно выбирают уровень значимости 0,05), то нулевая гипотеза отвергается в пользу альтернативной гипотезы, что указывает на наличие корреляции между случайными эффектами и регрессорами')
    """

def Broush_pagana():
    '''
    from linearmodels.panel import RandomEffects
    from linearmodels.panel import compare
    from statsmodels.stats.diagnostic import het_breuschpagan
    # Создание модели панельных данных
    model = PanelOLS(df.target, exog, entity_effects=True, time_effects=False)
    # Оценка модели
    results = model.fit()
    # Получение остатков
    residuals = results.resids

    # Выполнение теста Бройша-Пагана
    bp_test = het_breuschpagan(residuals, exog)

    print("Breusch-Pagan Test Statistic:", bp_test[0])
    print("P-value:", bp_test[1])
    # Variant 2
    # from statsmodels.compat import lzip
    # import statsmodels.stats.api as sms

    # test_result = sms.het_breuschpagan(reg.resid, reg.model.exog)
    # print('Статистика теста Бреуша-Пагана: ' + str(test_result[0]))
    # print('p-value теста Бреуша-Пагана: ' + str(1 - test_result[1]))
    print('Исходя из результатов теста Бреуша-Пагана, делаем выбор в пользу модели со случайными эффектами. Так как p_value < 0.05, то делаем выбор в пользу модели со случайными эффектами.')
    '''

def choy_panel():
    """
    df_for_chow = df.copy()
    df_for_chow['treat'] = 0
    df_for_chow['treat'][int(len(df['column_1'])/2):] = 1

    # df_for_chow=df_for_chow.sort_values(by='treat', ascending=True).reset_index().drop(columns=['id'])

    break_point = int(len(df['column_1'])/2)


    def linear_residuals(X, y):
        import pandas as pd
        import numpy as np
        from sklearn.linear_model import LinearRegression as lr

        #строим линейную модель
        model = lr().fit(X, y)

        # строим датафрейм с предсказанными значениями целевой метрики 
        summary_result = pd.DataFrame(columns = ['y_hat'])
        yhat_list = model.predict(X)
        summary_result['y_hat'] = yhat_list  

        # добавляем к датафрейму реальные значения целевой метрики
        summary_result['y_actual'] = y.values

        # вычисляем остатки
        summary_result['residuals'] = summary_result.y_actual - summary_result.y_hat

        # возводим остатки в квадрат
        summary_result['residuals_sq'] = summary_result.residuals ** 2
        return(summary_result)

    # пишем функцию, которая считает сумму квадратов остатков 
    def calculate_RSS(X, y):
        resid_data = linear_residuals(X, y)
        rss = resid_data.residuals_sq.sum()
        return(rss)

    def ChowTest(X, y, last_index_in_model_1, first_index_in_model_2):
        rss_pooled = calculate_RSS(X, y)
        # делим выборку на две подвыборке, в которой есть “слом”, наличие которого мы хотим проверить, и в котором слома нет

        X1 = X.iloc[:last_index_in_model_1]
        y1 = y.iloc[:last_index_in_model_1]
        rss1 = calculate_RSS(X1, y1)

        X2 = X.iloc[first_index_in_model_2:]
        y2 = y.iloc[first_index_in_model_2:]
        rss2 = calculate_RSS(X2, y2)

        # находим кол-во регрессоров + 1 для константы
        k = X.shape[1] + 1

        # находим кол-во наблюдений до слома
        N1 = X1.shape[0]

        # находим кол-во наблюдений после слома
        N2 = X2.shape[0]

        # вычисляем числитель для статистики Чоу
        numerator = (rss_pooled - (rss1 + rss2)) / k

        # вычисляем знаменатель для статистики Чоу
        denominator = (rss1 + rss2) / (N1 + N2 - 2 * k)

        # вычисляем статистику Чоу
        Chow_Stat = numerator / denominator

        # статистика Чоу имеет распределение Фишера с k и N1 + N2 - 2k степенями свободы
        from scipy.stats import f

        # считаю p-value
        p_value = 1 - f.cdf(Chow_Stat, dfn = 5, dfd = (N1 + N2 - 2 * k))
        result = (Chow_Stat, p_value)
        print('Chow_Stat', Chow_Stat)
        print('p_value', p_value)
        return(result)

    ChowTest(y=df.target, X = exog,  
            last_index_in_model_1=break_point-1,  
            first_index_in_model_2=break_point)[1]
    print('Если p-значение меньше выбранного уровня значимости, можно сделать вывод о статистически значимых различиях в качестве модели между двумя подходами. Это может указывать на то, что модель с фиксированными эффектами лучше объясняет данные или обладает более точными оценками параметров по сравнению с моделью пула.')
    """


def choose_kriv_rosta():
    """
    # сначала надо построить график
    y = array
    plt.plot(y)
    plt.show()

    t = [i for i in range(1, len(y+1))]

    # Сглаживание скользящей средней (по 3м точкам)
    t_sgl = []
    for ind, el in enumerate(y[1:-1]):
        t_sgl.append((y[ind-1]+y[ind+1]+el)/3) 
    # Добавляем первое и последнее знач   
    t_sgl = [(5*y[0]+2*y[1]-y[2])/6] + t_sgl
    t_sgl = t_sgl + [(5*y[-1]+2*y[-2]-y[-3])/6]
    # Первый средний прирост delta(y)
    dy = []
    for ind, el in enumerate(t_sgl[1:-1]):
        dy.append((t_sgl[ind-1]-t_sgl[ind+1])/2)
    # Второй средний прирост delta^2(y)
    dy2 = []
    for ind, el in enumerate(dy[1:-1]):
        dy2.append((dy[ind-1]-dy[ind+1])/2)

    #dy/y
    dyy = np.array(dy)/(y[1:-1])


    # Строим графики всего (в отдельных ячейках):
    plt.plot(t_sgl)
    plt.show()
    plt.plot(dy)
    plt.show()
    plt.plot(dy2)
    plt.show()
    plt.plot(dyy)
    plt.show()
    # Дальше выбираем изходя из табл:
    # Показатель - Характер изменения - Кривая роста
    # delta(y_t) - Примерно постоянный - Полином первого порядка
    # delta(y_t) - Примерно линейный - Полином второго порядка
    # delta^2(y_t) - Примерно линейный - Полином третьего порядка
    # (delta(y_t))/y_t - Примерно постоянный - Экспонента
    # Ln(delta(y_t)) - Примерно линейный - Модифицированная экспонента
    # Ln((delta(y_t))/y) - Примерно линейный - Кривая Гомперца
    # Ln((delta(y_t))/(y^2)) - Примерно линейный - Логистическая кривая
    """

def prognoz_kriv_rosta(k):
    '''
y = np.array([i for i in range(200, 1000, 100)])
x = np.array([i for i in range(1,16,2)])
series = pd.Series(y, index=x)
import scipy.stats as stats
from sklearn.linear_model import LinearRegression as lr
t = [i for i in range(1, len(y)+1)]
model = lr()
model.fit(pd.DataFrame(t), y)
y_pred = model.predict(pd.DataFrame(t))
lst_e = y_pred - y
lst_e_2 = lst_e**2


model2 = lr()
model2.fit(pd.DataFrame({'Column1': t, 'Column2': np.array(t)**2}), y)
y_pred2 = model2.predict(pd.DataFrame({'Column1': t, 'Column2': np.array(t)**2}))
lst_e2 = y_pred2 - y
lst_e_22 = lst_e2**2

t_avg = np.array(t).mean()
sum_t_otkl_2 = np.sum((np.array(t)-t_avg)**2)


alpha = 0.05
n = len(y)
k = 1
t_kritich = stats.t.ppf(1 - alpha / 2, n-k-1)
print('Первая')
print(f'сумма кв отклонений {np.sum(lst_e_2)}')
Se = (np.sum(np.array(lst_e_2))/(n-k-1))**0.5
delta_k = Se*t_kritich*((1+1/n+(n+k-t_avg)**2/sum_t_otkl_2)**0.5)


t_4 = [len(y)+1, len(y)+2, len(y)+3, len(y)+4]
y_pred = model.predict(pd.DataFrame(t_4))
print(y_pred)
for i in range(4):
    print(f'От {y_pred[i]-delta_k}, до {y_pred[i]+delta_k}')


alpha = 0.05
n = len(y)
k = 2
t_kritich = stats.t.ppf(1 - alpha / 2, n-k-1)

print('Вторая')
print(f'сумма кв отклонений {np.sum(lst_e_22)}')
Se = (np.sum(np.array(lst_e_22))/(n-k-1))**0.5
delta_k = Se*t_kritich*((1+1/n+(n+k-t_avg)**2/sum_t_otkl_2)**0.5)

t_4 = [len(y)+1, len(y)+2, len(y)+3, len(y)+4]
y_pred = model.predict(pd.DataFrame(t_4))
print(y_pred)
for i in range(4):
    print(f'От {y_pred[i]-delta_k}, до {y_pred[i]+delta_k}')
    '''
def holter_winters():
    '''
from statsmodels.tsa.holtwinters import ExponentialSmoothing
# оптимальные alpha, betta и gamma подбираются алгоритмом
model = ExponentialSmoothing(y, seasonal_periods=4, trend='add', seasonal='add')
model_fit = model.fit()

forecast = model_fit.forecast(8)  

print(forecast)
    '''

def teylor_weidg():
    '''
    from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
    # Надо написать, что оптимальные параметры подбираются алгоритмом
    # применение модели Тейла-Вейджа
    model = ExponentialSmoothing(y, trend='add', seasonal='add', seasonal_periods=12)
    fit_model = model.fit()

    # прогнозирование значений на тестовой выборке
    forecast = fit_model.forecast(12)

    # вывод результатов
    print('Прогноз на 12 месяцев:')
    print(forecast)
    '''

def braun():
    '''
from scipy.stats import t
alpha = 0.4
d = df['X']
forecast = np.zeros(len(d))
lvl = np.zeros(len(d))
er = np.zeros(len(d))
lvl[0] = d[0]
er[0] = d[1] - d[0]
for i in range(1, len(d)):
    if i == 1:
        lvl[i] = d[i]
        er[i] = d[i] - d[i-1]
    else:
        lvl[i] = alpha * d[i] + (1 - alpha) * lvl[i-1]
        er[i] = alpha * (d[i] - d[i-1]) + (1 - alpha) * er[i-1]
    forecast[i] = lvl[i] + er[i]
forecast[0] = d[0]- 3
sse = np.sum(er**2)
std_er = np.sqrt(sse / (len(d) - 2))
coeff = t.isf(0.05/2, df.shape[0] - 1)
d = pd.DataFrame({'Нижняя граница':forecast[-4:] - coeff * std_er,'Прогноз':forecast[-4:],'Верхняя граница':forecast[-4:] + coeff * std_er,})
d
    '''

def chetveryakov(k):
    '''
import pandas as pd
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
n = len(df)
t = np.arange(n)
ts = np.array(df['X'])
d = pd.DataFrame({'Date':t, 'X': ts})
d.set_index('Date', inplace=True)
res = sm.tsa.seasonal_decompose(d, model='additive', period=12)
fig, axs = plt.subplots(4, 1, figsize=(10, 10))
axs[0].plot(d)
axs[0].set_ylabel('Original')
axs[1].plot(res.trend)
axs[1].set_ylabel('Trend')
axs[2].plot(res.seasonal)
axs[2].set_ylabel('Seasonal')
axs[3].plot(res.resid)
axs[3].set_ylabel('residual')
plt.tight_layout()
plt.show()
fig, axs = plt.subplots(2, 1, figsize=(10,10))
axs[0].set_title('first')
axs[0].plot(df.rolling(window=96, center=True).mean())
axs[1].set_title('Second ')
axs[1].plot(df.rolling(window=len(df)//3, center=True).mean())
plt.show()
    '''

def prognoz_trend_model(k):
    '''
    # Просто прогнозируем для своей модели (выбираем исходя из кривых (см. choose_kriv_rosta))

    t = [i for i in range(1, len(y)+1)]
    # Линейная
    model = LinearRegression()
    model.fit(pd.DataFrame(t), y)
    y_pred = model.predict(pd.DataFrame(t))
    # Ошибкa
    lst_e = y_pred - y
    # Ошибка ** 2
    lst_e_2 = lst_e**2

    alpha = 0.05
    n = len(y)
    k = 1
    l = 1 #число параметров трендовой модели (?)
    t_kritich = stats.t.ppf(1 - alpha / 2, n-k-1)
    print('Первая')
    print(f'сумма кв отклонений {np.sum(lst_e_2)}')
    Se = (np.sum(np.array(lst_e_2))/(n-l))**0.5
    U_k = Se*t_kritich*((1+1/n+3*(n+2*k-1)**2/(n*(n**2-1)))**0.5)

    # Делаем прогноз на 4 t вперед 
    t_4 = [len(y)+1, len(y)+2, len(y)+3, len(y)+4]
    # Точечный
    y_pred = model.predict(pd.DataFrame(t_4))
    print(y_pred)
    # Интервальные
    for i in range(4):
        print(f'От {y_pred[i]-U_k}, до {y_pred[i]+U_k}')

    print()
    # Для полиномов второго и третьего порядка используется выражение, в котором начало отсчета времени перенесено на середину временного ряда наблюдений: 
    # где t_k время прогноза (НЕ ЗНАЮ, МБ НАДО БРАТЬ t+1), а суммирование выполняется по всем значениям временного ряда, где t>(-(n-1)/2) and t>((n-1)/2)
    t_new = []
    for el in t: #Чтобы подробно
        if el>(-(n-1)/2) and el>((n-1)/2):
            t_new.append(el)
    t=t_new
    for i in range(4):
        t_k = len(y)+i+1
        v = np.sum(np.array(t)**4)-2*(t_k**2)*np.sum(np.array(t)**2)+n*(t_k**4)
        U_k = Se*t_kritich*((1+1/n+t_k**2/np.sum(np.array(t)**2)+v)**0.5)
        print(f'От {y_pred[i]-U_k}, до {y_pred[i]+U_k}')
    '''
    return k


def make_garch(k):
    """
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    y = np.array([i for i in range(200, 1000, 100)])
    x = np.array([i for i in range(1,16,2)])
    series = pd.Series(y, index=x)

    from arch import arch_model

    # Параметр q относится к лагам скользящего среднего. Он указывает, сколько предыдущих значений ошибок (инноваций) будет использоваться для моделирования изменчивости.
    # Параметр p относится к лагам авторегрессии. Он указывает, сколько предыдущих квадратов ошибок (квадраты инноваций) будет использовано для моделирования изменчивости (гетероскедастичности) вариации. 
    # Таким образом, p и q имеют разные роли в модели GARCH. Параметр p отражает архивную зависимость и учитывает влияние прошлой вариации на текущую, а параметр q отражает условную гетероскедастичность и учитывает влияние прошлых ошибок на текущую вариацию.
    am = arch_model(y, mean='Zero', vol='GARCH', p=2, q = 2)
    # параметр update_freq относится к частоте обновления параметров модели во время обучения
    res = am.fit(update_freq=5)
    print(res.summary())

    yhat = res.forecast(horizon=4) #Прогнощируем 4 значения вперед
    # Вывод результатов прогнозирования
    print(yhat.variance.values[-1, :])
    plt.plot(yhat.variance.values[-1, :])
    plt.show()

    forecast_mean = yhat.mean.iloc[-1]
    forecast_variance = yhat.variance.iloc[-1]

    print(forecast_mean)
    print(forecast_variance)
    """
    return k


def make_arch(k):
    """
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    y = np.array([i for i in range(200, 1000, 100)])
    x = np.array([i for i in range(1,16,2)])
    series = pd.Series(y, index=x)

    from arch import arch_model

    am = arch_model(y, mean='Zero', vol='ARCH', p=2)
    # параметр update_freq относится к частоте обновления параметров модели во время обучения
    res = am.fit(update_freq=5)
    print(res.summary())

    yhat = res.forecast(horizon=4) #Прогнощируем 4 значения вперед
    # Вывод результатов прогнозирования
    print(yhat.variance.values[-1, :])
    plt.plot(yhat.variance.values[-1, :])
    plt.show()

    forecast_mean = yhat.mean.iloc[-1]
    forecast_variance = yhat.variance.iloc[-1]

    print(forecast_mean)
    print(forecast_variance)
    """
    return k

def test_choy():
    '''
    # ТЕСТ ЧОУ НА СТРУКТУРНЫЕ ИЗМЕНЕНИЯ В ДАННЫХ
    import statsmodels.api as sm

    # Создаем фиктивные данные о зарплатах в двух регионах
    region1 = [10, 15, 20, 25, 30]
    region2 = [5, 10, 15, 20, 25]
    Для нас - 2 варианта (сужу по теории).
    # 1: создать 2 модели. Одну со структурными изменениями. Другую - без
    # Или разбить со структурными на 2 части пополам (это странно), но в теории не указано
    # Есть еще предположение: ТестЧоу - это метод, который позволяет проверить предположение о необходимости разбиения основной выборочной совокупности на части или подвыборки, потому что модели регрессии для подвыборок могут быть более эффективными, чем общая модель регрессии для всей выборочной совокупности.

    # Объединяем данные в один датафрейм
    data = pd.DataFrame({'region1': region1, 'region2': region2})

    # Оцениваем регрессионную модель для каждого региона
    model1 = sm.OLS(data['region1'], sm.add_constant(np.arange(1, 6))).fit()
    model2 = sm.OLS(data['region2'], sm.add_constant(np.arange(1, 6))).fit()

    # Оцениваем регрессионную модель для всех данных вместе
    model_all = sm.OLS(data.values.flatten(), sm.add_constant(np.arange(1, 11))).fit()

    # Проводим тест Чоу
    chow_test = sm.stats.anova_lm(model1, model2, model_all)
    p_value = chow_test['Pr(>F)'][2]

    # Выводим результаты
    if p_value < 0.05:
        print('Наблюдаются структурные изменения в данных')
    else:
        print('Структурные изменения в данных не наблюдаются')
    # Если p-value меньше 0.05, то мы можем отвергнуть нулевую гипотезу о том, что структуры данных в двух выборках одинаковы, и сделать вывод о наличии структурных изменений. Если же p-value больше 0.05, то мы не можем отвергнуть нулевую гипотезу и делаем вывод о том, что структуры данных в двух выборках одинаковы.

    # ТЕСТ ЧОУ ДЛЯ ПРОРКИ НА ГЕТЕРОСКЕДАСТИЧНОСТЬ
    # Создаем массивы данных
    y1 = np.array([1, 2, 3, 4, 5])
    x1 = np.array([2, 4, 6, 8, 10])
    y2 = np.array([2, 4, 6, 8, 10])
    x2 = np.array([1, 3, 5, 7, 9])

    # Строим модели
    model1 = sm.OLS(y1, sm.add_constant(x1))
    model2 = sm.OLS(y2, sm.add_constant(x2))

    # Обучаем модели
    results1 = model1.fit()
    results2 = model2.fit()

    # Вычисляем остатки
    residuals1 = results1.resid
    residuals2 = results2.resid

    # Вычисляем суммы квадратов остатков
    SSR1 = np.sum(residuals1**2)
    SSR2 = np.sum(residuals2**2)

    # Вычисляем статистику Чоу
    chow_statistic = ((SSR2 - SSR1) / 2) / (SSR1 / (y1.size - 4))

    # Вычисляем p-value
    p_value = 1 - stats.chi2.cdf(chow_statistic, 2)

    print("Статистика Чоу:", chow_statistic)
    print("p-value:", p_value)
    # В данном случае нулевая гипотеза состоит в отсутствии гетероскедастичности. Если p-value меньше выбранного уровня значимости (обычно 0.05), то нулевая гипотеза отвергается, и можно сделать вывод о наличии гетероскедастичности.
    '''


def t(word):
    
    k_my = '''
    Адаптивная модель прогнозирования Брауна --- Адапт. Модели приспосабливают структуру и параметры к изменениям свойств процесса Как и в трендовых фактором является время. Все они построены на двух схемах: скольз средн и авторегресс. Брауна для краткосрочн.
    Y(t+k) = A0; Y(t+k) = A0+A1K; Y(t+k) = A0+A1K+A2K^2; наивная.первого.второго порядка.
    1)По нескольким первым точкам находим значения а1 а0 и предсказываем следующее значение, затем считаем ошибку следующего предсказания (e(t+k)=y(t+k)-y_прогн)
    2)A0(t+1) = a0 + a1(t) + (1-b)^2 * e(t); a1(t+1) = a1(t) + (1-b)^2 * e(t); b – бетта коэф. (дисконтирования данных)
    3)Далее находим следующий прогноз и возвращаемся к пункту нахождения ошибки
    Можно дополнить точечный прогноз интервальным U(k) = S*t*sqrt(1+1/n + (3*(n+2k-1)^2)/(n^3 - n)) |||
    Моделирование тренд-сезонных процессов. Типы функциональных зависимостей. --- 
    Определение степени гладкости тренда -> выявление наличия сезонных колебаний - > фильтрация компонент ряда -> (укрупнен анализ сезонной волны, анализ эволюции сезонной волны) -> Исследование факторов сезонности -> блок прогноза.
    Это позволяет выделить тренды и сезонности в данных и предсказать будущие значения. Для моделирования тренд-сезонных процессов используются различные методы, включая классические методы регрессионного анализа, методы экспоненциального сглаживания и методы ARIMA (авторегрессионная интегрированная скользящая средняя). 
    Чаще всего на практике приходится иметь дело с рядами,включающими три компоненты - тренд, сезонную и случайную составляющие. Такие процессы принято называть тренд-сезонными. В зависимости от вида связи между компонентами может бытьпостроена:
    аддитивная модель: y = ft + St + Ct +  Et
    мультипликативная модель временного ряда: yt = ft St Ct Et
    модель смешанного типа: y = ftStC+Et
    |||
    Модель Хольта-Уинтерса ---
    Модель является моделью трехпараметрического экспоненциального сглаживания.Три параметра сглаживания предполагается подбирать наилучшим образом, в зависимости от решаемой задачи. Проблема оптимизации параметров адаптивной модели является фокусом внимания при практическом применении этого метода.
    Построение модели Хольта-Уинтерса с линейным ростом: Y(t + k) = [a(t) + k • b(t)] • F(t + k - L),
    где k - период упреждения, Y(t) - расчетное значение показателя для t периода; a(t),b(t) и F(t) коэффициенты модели, которые адаптируются (уточняются) по мере перехода от членов ряда с номером (t - L) к t; F(t + k - L)- значение коэффициента сезонности того периода, для которого рассчитывается соответствующий показатель. L - период сезонности (для квартальных данных L = 4). Коррекция параметров на каждом шаге:
    a(t) = a(Y(t)/F(t - L)) + (1 - a)(a(t-1) + b(t-1));
    b(t) = B(a(t) - a(t - 1)) + (1 - B)b(t - 1);
    F(t) = ү *(Y(t)/a(t))+ (1 - y)F(t - L),где a, В и ү - параметры сглаживания. Первое уравнение описывает сглаженный ряд, второе уравнение служит для оценки тренда, третье уравнение для оценки сезонности. Прогнозирование производится после оптимизации параметров сглаживания по следующей формуле: Ў(t + p) = (a(t) + pb(t))F(t - L + p). 
    |||
    Модель Тейла-Вейджа (мультипликативная модель) --- это мультипликативная модель, которая используется для прогнозирования временных рядов с учетом тренда и сезонности. Она является одним из методов декомпозиции ряда на трендовую, сезонную и остаточную компоненты.
    Yt = at + bt * t + gi, gi – сезонная компонента.
    Этапы построения модели Тейла-Вейджа включают:
    1.Декомпозиция ряда: Сначала ряд декомпозируется на трендовую, сезонную и остаточную компоненты. Для этого применяются методы сглаживания и фильтрации данных, такие как скользящее среднее или экспоненциальное сглаживание, чтобы выделить общую тенденцию роста или спада (тренд), сезонные колебания и остаточную компоненту.
    2.Оценка тренда: В модели Тейла-Вейджа трендовая компонента ряда описывается мультипликативной функцией. То есть значения тренда умножаются на значения других компонент (сезонность, остатки) для получения исходных данных. Тренд может быть оценен, например, с помощью методов линейной регрессии или экспоненциального сглаживания.
    3.Оценка сезонной компоненты: Сезонная компонента ряда описывает повторяющиеся колебания, которые происходят с определенной периодичностью (например, каждый месяц или каждый год). Для оценки сезонной компоненты можно использовать различные методы, такие как сезонное сглаживание или дамми-переменные.
    4.Прогнозирование: После оценки тренда и сезонной компоненты модель Тейла-Вейджа позволяет сделать прогноз на будущие периоды, учитывая их взаимодействие. Прогнозирование проводится путем умножения прогнозируемого тренда на прогнозируемую сезонность и добавления ожидаемой остаточной компоненты.
    Модель Тейла-Вейджа является одним из методов анализа и прогнозирования временных рядов, который учитывает тренд и сезонность. Она может быть полезна для выявления общих паттернов и прогнозирования будущих значений ряда.
    |||
    Метод Четверикова --- это метод выделения тренда и сезонности из временных рядов. Он основывается на разложении временного ряда на четыре компоненты: тренд, сезонность, цикл и случайную компоненту.
    Этап 1.
    Исходный ряд у выравнивается по формуле среднехронологической с периодом 1 год, т.е. Т = 12. Невыровненные значения в начале и в конце ряда отбрасывают. Получают предварительную оценку тренда yt = f’t и вычисляют отклонения исходного ряда от выровненного l = Yij – f’tj
    Этап 2.
    Для каждого года і вычисляется среднеквадратическое отклонение и полученные отклонения нормируются Lij = lij/отклонение 
    Этап 3.
    По нормированным отклонениям вычисляется предварительная средняя сезонная волна s1j = sum_i(Lij)/m
    Этап 4.
    Средняя предварительная сезонная волна умножается на среднеквадратичное
    отклонение каждого года и вычитается из исходного ряда, получается первая оценка
    тренда fij = Yij – Sj*sigmaj
    Этап 5.
    Получаемый тренд сглаживают скользящей средней по пяти точкам и получают новую
    оценку тренда fj. Чтобы не потерять точки в начале и в конце ряда их сглаживают по
    трем точкам, причем для крайних точек используют специальные формулы сглаживания:
    f1 = (5f1 +2f2 – f3)/6; fn = (5fn +2fn-1 – fn-2)/6
    Этап б.
    Вычисляют новые отклонения исходного ряда у: от тренда f2; l2 = yt – f2t для полученных отклонений вновь выполняют пункты 2 и 3 и получают окончательную среднюю сезонную волну S2.
    Этап 7.
    Вычисляют остаточную компоненту Eij =  l2ij – Sj* sigma_i  и определяют k; - коэффициент напряженности сезонной волны: ki = sum(lij*E2ij)/sum(e2ij)
    |||
    Мультипликативная (аддитивная) модель ряда динамики при наличии тенденции: этапы построения. --- это статистический метод, который позволяет анализировать временные ряды и учитывать как сезонные, так и трендовые компоненты данных. Построение такой модели включает несколько этапов. Вот основные этапы построения мультипликативной (аддитивной) модели ряда динамики при наличии тенденции:
    1.Предварительный анализ ряда: Прежде чем строить модель, необходимо провести предварительный анализ ряда данных. Включает в себя визуализацию временного ряда, исследование его стационарности и выявление наличия тренда и/или сезонности.
    2.Декомпозиция ряда: Разложение временного ряда на компоненты - тренд, сезонность, цикл и остаток (случайную составляющую). Это может быть выполнено с использованием методов, таких как скользящее среднее, экспоненциальное сглаживание или STL-декомпозиция.
    3.Удаление тренда: Тренд представляет собой долгосрочное изменение ряда со временем. Можно применить методы сглаживания, такие как скользящее среднее или экспоненциальное сглаживание, для удаления тренда из исходного ряда.
    4.Удаление сезонности: Если ряд содержит явную сезонность, ее необходимо удалить для получения стационарного ряда. Методы, такие как разностное сглаживание или использование сезонного лага, могут быть применены для удаления сезонной компоненты.
    5.Приведение к аддитивной или мультипликативной форме: В зависимости от природы тренда и сезонности, можно выбрать между аддитивной или мультипликативной моделью. В аддитивной модели ряд представляется в виде суммы тренда, сезонности, цикла и остатка, а в мультипликативной модели ряд представляется в виде произведения этих компонент.
    6.Оценка параметров модели: Для построения модели необходимо оценить параметры для каждой компоненты. Это может включать использование метода наименьших квадратов или метода максимального правдоподобия.
    7.Прогнозирование: После построения модели можно использовать ее для прогнозирования будущих значений временного ряда. Это может быть выполнено путем продолжения тренда, сезонности и цикла в будущем и добавления остатка.
    |||
    Моделирование периодических колебаний (гармоники Фурье) --- основано на представлении периодической функции в виде суммы гармонических функций различных частот и амплитуд. Этот подход основан на теореме Фурье, которая утверждает, что любая периодическая функция может быть разложена на бесконечную сумму гармонических компонент.
    Вот основные шаги для моделирования периодических колебаний с использованием гармоник Фурье:
    1.Определение периода: Определите период колебаний, то есть время, через которое функция повторяется.
    2.Сбор данных: Соберите достаточное количество точек данных для построения модели. Это может быть сделано экспериментально или с помощью имеющихся временных рядов.
    3.Вычисление спектра: Примените преобразование Фурье к исходным данным, чтобы получить спектральное представление ряда. Преобразование Фурье позволяет выделить амплитуды и фазы гармонических компонент, составляющих ряд.
    4.Выбор гармоник: Из спектра выберите наиболее значимые гармоники. Здесь важно учитывать амплитуду и фазу каждой гармоники.
    5.Построение модели: Используйте выбранные гармоники для построения модели. Модель будет состоять из суммы гармонических функций с определенными амплитудами и фазами, соответствующими выбранным гармоникам.
    6.Валидация модели: Проверьте, насколько хорошо построенная модель соответствует исходным данным. Можно сравнить модельные значения с исходными данными и оценить показатели соответствия, такие как средняя квадратичная ошибка или коэффициент детерминации.
    7.Прогнозирование: Используйте модель для прогнозирования будущих значений ряда. Это можно сделать, продолжив суммирование гармонических функций в будущем с использованием полученных амплитуд и фаз.
    |||
    Прогнозирование одномерного временного ряда случайной компоненты (распределение Пуассона). --- есть ряд, в котором отсутствует трен, те ряд является стационарным Такие временные ряды на практике встречаются крайне редко. необходимо убедиться в том, что тенденция отсутствует. Для прогнозирования таких рядов применяются вероятностные статистические методы, например метод, в основе которого лежит использование закона распределения Пуассона (распределения редких явлений) с плотностью: p = e^-x
    Этапы реализации метода:
    1.	Осуществляется последовательное сравнение каждого следующего значения уровня исходного временного ряда со значением предыдущего уровня. При этом знаком «+» отмечается возрастание значения уровня, а «–» – убывание. Причем первый уровень всегда отмечается знаком «-». Знак «+» показывает, сколько периодов времени исследуемое явление возрастает и этот временный период принято считать благоприятной тенденцией.
    2.	Строится специальная таблица, характеризующая виды тенденции, длину благоприятной тенденции (τ) и частоту повторения благоприятной тенденции (f). При этом две первые графы таблицы: вид тенденции и длина благоприятной тенденции существуют априори, и исследователь только частотой определяет наличие того или иного вида тенденции в исследуемом временном ряду. Длина же благоприятной тенденции (τ) определяется числом плюсов между двумя минусами в ряду динамики «+» и «–».
    3.	На основе данных таблицы определяется средняя длина благоприятной тенденции по формуле вида: t_sr = sum(t*f)/sum(f); lambda = 1/t_sr Данный показатель характеризует, сколько в среднем раз за рассматриваемый период времени, совершалось прерывание благоприятной тенденции.
    4.	Вероятность благоприятной тенденции определяется на основе следующей модификации закона распределения Пуассона: p = e^(-lambda*L) где: р — вероятность совершения благоприятной тенденции; lambda — интенсивность прерывания благоприятной тенденции; L — период упреждения (число лет сохранения благоприятной тенденции).
    |||
    Функциональные преобразования переменных в линейной регрессионной модели. Метод Зарембки. Особенности применения. --- Очень коротко: Всегда отдаем предполчтение линейным моделям, однако модели разной функц формы нельзя сравнивать. Метод зарембки сравнивает 
    Y1 = A1 + A2X + U (1) И  LNY = B1 + B2X + LNU (2)
    1)Вычисл ср геом = корень н степени из произвдения н игреков
    2)Пересчитываются yi* = yi/ср геом
    3)Строятся дв модели выше по этим y 
    4)Если |n/2 ln(ESS1/ESS2)|> X^2 то полулограифм, иначе линейн
    Применение: метод Зарембки применяется для выбора из двух форм моделей (несравнимых непосредственно), в одной из которых зависимая переменная входит с логарифмом, а в другой - нет.
    |||
    Функциональные преобразования переменных в линейной регрессионной модели. Тест Бокса-Кокса. Особенности применения. --- Очень коротко: Всегда отдаем предполчтение линейным моделям Если стоит вопрос о выборе линейной или логарифмической моделями регрессии, то использовать при этом критерий суммы квадратов отклонений нельзя, потому что общая сумма квадратов отклонений для логарифмической модели намного меньше, чем для линейной модели регрессии. Если, однако модели разной функц формы нельзя сравнивать с помощью стандартных критериев Метод Бокса Кокса сравнивает 
    Y1 = A1 + A2X + U (1) И  LNY = B1 + B2X + LNU (2)
    Тест Бокса-Кокса основывается на утверждении, что (1-y) и lny F = (y^L – 1)/L при L = 1 и L = 0 
    1)Вычисл ср геом = корень н степени из произвдения н игреков
    2)Пересчитываются yi* = yi/ср геом
    3)Yi = (y*^L)/L Xi = (Xi^L)/L
    4)Далее оцениваем регрессию используя пересчитанные переменные
    5)Выбираем модель с наименьшей суммой квдаратов остатков ESS
    Результативная переменная у в нормальной линейной моделирегрессии является непрерывной величиной, способной принимать любые значения из заданного множества. Но помимо нормальных линейных моделей регрессии существуют модели регрессии, в которых переменная у должна принимать определённый узкий круг заранее заданных значений.
    Применение: Тест Бокса-Кокса применяется для выбора из двух форм моделей (несравнимых непосредственно), в одной из которых зависимая переменная входит с логарифмом, а в другой - нет.
    |||
    Функциональные преобразования переменных в линейной регрессионной модели. Критерий Акаике  и Шварца. Особенности применения. --- Очень коротко: Всегда отдаем предполчтение линейным моделям Если стоит вопрос о выборе линейной или логарифмической моделями регрессии, то использовать при этом критерий суммы квадратов отклонений нельзя, потому что общая сумма квадратов отклонений для логарифмической модели намного меньше, чем для линейной модели регрессии. Если, однако модели разной функц формы нельзя сравнивать с помощью стандартных критериев
    Y1 = A1 + A2X + U (1) И  LNY = B1 + B2X + LNU (2)
    AIC = ln(ESSk/n) + 2k/n +1 + ln(2*pi), при увеличении объясняющих переменных первое слагаемое в правой части уменьшается, второе – увеличивается. Лучше та у которой статистика меньше.
    Критерий шварца. SC = ln(ESSk/n) + kln(n)/n + 1 + ln(2pi), при увеличении объясняющих переменных первое слагаемое, уменьшается, второе увеличивается. Лучще та у которой меньше статистика. 
    Особенности применения методов: критерий Акаике подходит для выбора лучшей из нескольких статистических моделей (любых). Для малых выборок применяют скорректированный критерий Акаике, Критерий Шварца аналогичен Акаике, но налагает больший штраф за использование доп. параметров. 
    |||
    Функциональные преобразования переменных в линейной регрессионной модели. Тест Бера. Тест МакАлера. Особенности применения. --- Очень коротко: Всегда отдаем предполчтение линейным моделям Если стоит вопрос о выборе линейной или логарифмической моделями регрессии, то использовать при этом критерий суммы квадратов отклонений нельзя, потому что общая сумма квадратов отклонений для логарифмической модели намного меньше, чем для линейной модели регрессии. Если, однако модели разной функц формы нельзя сравнивать с помощью стандартных критериев.
    Y1 = A1 + A2X + U (1) И  LNY = B1 + B2X + LNU (2)
    Был только объединенный…….
    Тест Бера_МакАлера
    Оцениваем регрессии и выводим оцененные y и lny, по ним считаем e^y = B0 + BiXi + E1; ln(y) = B0 + BiXi + E2. Далее оцениваем еще ln(y) = B0 + BiXi + O1* E1 + U, y = B0 + BiXi + O2* E2 + U
    Тот из O1 O2 что значим, та модель и победила, иначе другой тест. Применим тогда когда выбор стоит между линейной и полулогарифмической. 
    |||
    Функциональные преобразования переменных в линейной регрессионной модели. Тест МакКиннона. Тест Уайта. Тест Дэвидсона. Особенности применения. --- Очень коротко: Всегда отдаем предполчтение линейным моделям Если стоит вопрос о выборе линейной или логарифмической моделями регрессии, то использовать при этом критерий суммы квадратов отклонений нельзя, потому что общая сумма квадратов отклонений для логарифмической модели намного меньше, чем для линейной модели регрессии. Если, однако модели разной функц формы нельзя сравнивать с помощью стандартных критериев.
    Y1 = A1 + A2X + U (1) И  LNY = B1 + B2X + LNU (2)
    Y – искомые; y, lny – оцененные 
    Оцениваем регрессии и выводим оцененные y и lny, 
    lnY = B0 + BiXi + O1(y – e^y) + E
    Y = B0 + BiXi + O2(ln(y) – lny) + E 
    Тот из O1 O2 что значим, та модель и победила, иначе другой тест. Применим тогда когда выбор стоит между линейной и полулогарифмической. 
    |||
    Модели с распределенными лаговыми переменными. --- Величину L, характеризующую запаздывание в воздействии фактора на результат, называют в эконометрике лагом, а временные ряды самих факторных переменных, сдвинутые на один или более моментов времени, — лаговыми переменными. Эконометрическое моделирование осуществляется с применением моделей, содержащих не только текущие, но и лаговые значения факторных переменных. Эти модели называются моделями с распределенным лагом. Модель вида yt = a + b0xt + b1xt-1 + b2xt-2 + e  является примером модели с распределенным лагом. 
    Оценка модели с лагами зависит от количества лагов:
    А) если количество лагов конечно, то оценивание производится путем сведения к множественной линейной регрессии;
    Б) если число лагов бесконечно, то применяется метод последовательного увеличения количества лагов или преобразование Койка.
    |||
    Оценка моделей с лагами в независимых переменных. Преобразование Койка. --- Оценка модели с распределенными лагами во многом зависит от того, конечное или бесконечное число лагов она содержит. 
    Yt = a + B0xt + B1xt-1 + B2xt-2 + Bkxt-k + E; k - конечное или бесконечное
    Метод последовательного увеличения количества лагов по данному методу уравнения рекомендуется оценивать с последовательно увеличивающимся количеством лагов. Признаков завершения процедуры увеличения количества лагов может быть несколько: а) при добавлении нового лага какой-либо коэффициент регрессии Bk при переменной Xt-k меняет знак. Тогда в уравнении регрессии оставляют переменные, коэффициенты при которых знак не поменяли; 
    б) при добавлении нового лага коэффициент регрессии при переменной становится статически незначимым. Очевидно, что в уравнении будут использоваться только переменные, коэффициенты при которых остаются статически значимыми.
    В распределении Койка предполагается, что коэффициенты («веса») при лаговых значениях объясняющей переменной убывают в геометрической прогрессии:Bk = B0*L^k (Можно выписать уравнение) Согласно теории уравнение с неизвестными a B0 и L можно решить разными способами.
    |||
    Полиномиально распределенные Лаги Алмон. В --- При использовании преобразования Койка на коэффициенты регрессии накладываются достаточно жесткие ограничения. Предполагается, что «веса» коэффициентов при лаговых переменных убывают в геометрической прогрессии. В ряде случаев такое предположение весьма уместно, но в некоторых других оно не выполняется. Встречаются ситуации, когда значения лаговой объясняющей переменной за 3-4 периода от момента наблюдения оказывают на зависимую переменную большее влияние, чем текущее или предшествующее ему значение объясняющей переменной. Распределенные лаги Алмон позволяют достаточно гибко моделировать такие изменения. Для простоты изложения схемы Алмон положим, что В подчиняется зависимости: Bi = (a0 + a1*i + a2*i), тогда yt = a + sum(a0 + a1*i + a2*i)*xt-I + E
    Значения а, а0 , а1, а2 могут быть оценены по МНК. При этом случайные отклонения E, удовлетворяют предпосылкам МНК. Коэффициенты В определяются из соотношения (9.46). Отметим, что для применения схемы Алмон необходимо вначале определиться с количеством лагов k. Обычно это количество находится подбором, начиная с «разумного» максимального, постепенно его уменьшая. После определения k необходимо подобрать степень т полинома (9.45). Недостатком метода является взаимная корреляция переменных zri, которая повышается с ростом степени полинома. Это увеличивает стандартные ошибки коэффициентов a в соотношениях, аналогичных (9.48).
    |||
    Авторегрессионные модели --- Существует несколько моделей авторегрессии, которые широко используются для анализа временных рядов и прогнозирования.
    1.AR (Авторегрессия) модель: простейшая модель авторегрессии, где значение временного ряда прогнозируется на основе его предыдущих значений. В модели AR(p) (где р - порядок модели) прогнозируемое значение ряда зависит от р предыдущих значений. Модель AR может быть представлена уравнением: Xi = c + sum(ai*Xt-i) + E Где a параметры модели (коэффициенты авторегрессии), с - постоянная (часто для упрощения предполагается равной нулю), E - белый шум. Простейшим примером является авторегрессионный процесс первого порядка AR(1)-процесс Для данного процесса коэффициент авторегрессии совпадает с коэффициентом автокорреляции первого порядка.
    2.ARMA (Авторегрессия-скользящее среднее) модель: Эта модель комбинирует авторегрессионную и скользящую среднюю модели. В модели ARMA(р, q) (где р - порядок авторегрессии, q - порядок скользящей средней) прогнозируемое значение ряда зависит от размера предыдущих значений и q предыдущих ошибок. Уравнение модели ARMA имеет вид Xi = c + sum(ai*Xt-i) + sum(bi*Et-i) + E
    3.3. ARIMA (Интегрированная авторегрессия-скользящее среднее) модель: Эта модель является расширением ARMA модели, учитывающим интегрирование временного ряда для обеспечения стационарности. В модели ARIMA (p, d, q) (где р - порядок авторегрессии, d - порядок интегрирования, q - порядок скользящей средней) Модель ARIMA(p, d, q) для нестационарного временного ряда X1 имеет вид: deltaX = c + sum(ai*delta Xt-i) + sum(bi*delta Et-i) + E; delta - оператор разности временного ряда порядка d
    |||
    Авторегрессионные модели с распределенными лагами. --- Авторегрессионные модели с распределенными лагами (Distributed Lag Models) являются моделями, где зависимая переменная связана предыдущими значениями как авторегрессионной модели, но распределенными (временно отдаленными) лагами. Эти модели полезны при моделировании долгосрочных эффектов и динамических зависимостей во временных рядах. Вот некоторые примеры авторегрессионных моделей с распределенными лагами:
    1.ARDL (Autoregressive Distributed Lag) модель: это модель, которая комбинирует авторегрессию с лагами и распределенными лагами. В модели ADL (р, q) прогнозируемое значение зависимой переменной связано с ее предыдущими значениями и значениями объясняющих переменных с различными лагами. Уравнение ARDL модели может иметь следующий вид: yt = a0 + a1t + sum(w*yt-i) + sum(sum(Bji*xjt-1)) + E
    2.ADL (Autoregressive Distributed Lag) модель: это модель, которая применяется в эконометрике для анализа долгосрочных эффектов и динамических зависимостей. В ADL модели зависимая переменная связана с лагами ее предыдущих значений и лагами объясняющих переменных. Уравнение ADL модели может быть представлено следующим образом: yt = a0 + sum(ai*yt-i) + sum(bj*xt-j) + E; Модель ADL(p, 0) - это модель авторегрессии AR(p) (в общем случае, возможно с экзогенной переменной без лагов), а модель ADL(0, q) - это модель распределённого лага DL(q).\
    |||
    Стационарные временные ряды. Определения стационарности, лаговой переменной, автоковариационной функции временного ряда, автокоррляционной функции, коррелограммы,  коэффициенты корреляции между разными элементами стационарного временного ряда с временным лагом .  ---  Стационарные процессы описывают явления, имеющие стационарный характер относительно течения времени. Существуют два определения стационарности - сильное и слабое. 
    Стационарность - это свойство временного ряда, которое означает, что его статистические характеристики не меняются со временем.
    Лаговая переменная - это переменная, влияние которой характеризуется некоторым запозданием. 
    Автоковариационная функция (Autocovariance Function) временного ряда является мерой ковариации между значениями ряда в различных моментах времени. Она показывает, насколько связаны между собой отклонения значений ряда в разных временных точках.Автокорреляционная функция показывает степень линейной статистической связи между значениями временного ряда. Численно, автокорреляционная функция представляет собой последовательность коэффициентов корреляции между исходным рядом, и его копией, сдвинутой на заданное число интервалов ряда 
    Коррелограмма (автокоррелограмма) показывает численно и графически автокорреляционную функцию (АКФ), иными словами, коэффициенты автокорреляции (и их стандартные ошибки) для последовательности лагов из определенного диапазона (например, от 1 до 30). На коррелограмме обычно отмечается диапазон в размере двух стандартных ошибок на каждом лаге, однако обычно величина автокорреляции более интересна, чем ее надежность, потому что интерес в основном представляют очень сильные (а, следовательно, высоко значимые) автокорреляции.
    Коэффициенты корреляции между разными элементами стационарного временного ряда с лагом h называются коэффициентами автокорреляции порядка h. Функция p(h) = corr(xt, xt+h) называется автокорреляционной функцией (AFC) стационарного временного ряда. Для коэффициента автокорреляции справедливо также следующее: corr(xt, x2) = p(s-t).
    |||
    Стационарные временные ряды. Определения частной автокорреляционной функции, белого шума, автоковариационная функция для белого шума, ACF для белого шума, частная автокорреляционная функция для белого шума. --- Стационарность - это свойство временного ряда, которое означает, что его статистические характеристики не меняются со временем.
    Частная автокорреляционная функция (Partial Autocorrelation Function, PACF) - это функция, которая измеряет корреляцию между значениями временного ряда на разных временных отрезках, учитывая влияние промежуточных значений. P_part(h) = corr(xt,..,xt+h|xt+1,.., xt+h-1)
    Ряд Ut называется белым шумом (white noise), если E(Ut) = 0, Var(Ut) = const, cov(Ut, Ut+h) = 0 при h!= 0
    Автоковариационная функция для белого шума: y(h) = (sigma^2 if h = 0, else 0)
    ACF для белого шума: p(h) = (1 if h = 0, else 0)
    Частная автокорреляционная функция для белого шума P_part(h) =  (1 if h = 0, else 0)
    |||
    Модели стационарных временных рядов: модель  (классический вид и через лаговый оператор). Авторегрессионный многочлен, авторегрессионная часть и часть скользящего среднего. --- 
    Общий вид модели ARMA: Xi = c + sum(ai*Xt-i) + sum(bi*Et-i) + E 
    Используя лаговый оператор: xt = a1 + sum(ai*Lj*xt) + et + sum(Oi*Li*et)
    Можно переписать:  (1 -  sum(ai*Lj))*xt = a1 + (1+sum(Oi*Li))*et
    Авторегрессионый многочлен - (1 -  sum(ai*Lj))
    Авторегрессионую часть и часть скользящего среднего сами найдете
    |||
    Модели стационарных временных рядов: модель . Доказательство утверждения: Модель ARMA(1, q) стационарна тогда и только тогда, когда --- Xi = c + sum(ai*Xt-i) + sum(bi*Et-i) + E 
    ARMA(1, q) : Xi = c + a1*Xt-1 + sum(bi*Et-i) + E 
    Модель ARMA(1, q) стационарна тогда и только тогда, когда a1 < 1
    Ext = c + sum(ai*E(Xt-I)) + sum(bi*E(et-i)) + e => Ext = c + sum(ai*E(Xt-I))= c
    Следовательно Ext = c/(1- sum(ai)) = c/a1
    |||
    Модели стационарных временных рядов: Модель , Среднее, дисперсия и ACF для MA(q). Модель . ---
    ARMA: Xi = c + sum(ai*Xt-i) + sum(bi*Et-i) + E 
    MA = ARMA(0,q)
    Ext = c+ E(ut)+ O1*E(ut-1) ....= c\
    Var(ARMA(0,q)) = var( c + sum(bi*Et-i) )  = (1 + sum(bi^2))*Var(Et)
    ACF: p(h) = 0 при |h|>q 
    |||
    Модели стационарных временных рядов: Модель AR(p). Доказательство утверждения: Модель AR(p) определяет стационарный ряд ⇐⇒ выполнено условие стационарности: все корни многочлена  по модулю больше единицы. Модель . ---
    AR: Xi = c + sum(ai*Xt-i) + E 
    Авторегресиионый многочлен: ф(z) = 1-ф1z-…-фpz^p
    Рассмотрим ARMA(1,q) Xi = c + a1*Xt-1 + sum(bi*Et-i) + E 
    Тогда ф(z) = 1-фz и егшо корень z0 = 1/ф Так как |z0| > 1 <==> |Ф|<1, то это будет условие стационарности для этого ряда.
    |||
    Прогнозирование для модели ARMA. Условия прогнозирования. Периоды прогнозирования. Информативность прогнозов. --- Пусть известны значения ряда и шоки и, до периода Т.  и на основе них будем строить "оптимальный" прогноз на период Т+r (r = 1,2,…).
    Оптимальность прогноза будем понимать в смысле среднего квадратического отклонения Начнём с прогнозирования на один период. Для ARMA-модели cov(Ut+1,Xt) = 0, cov(Ut+1,Ut) = 0 Пусть т = 1, тогда просто подставляем в формулу.Оптимальный прогноз на один период
    Для общего случая запишем правило последовательного построения оптимального прогноза на т шагов:
    1. записываем ARMA-формулу для Xt+r
    2. "отбрасываем" будущие шоки Ut+r-1,…,Ut+1
    3. заменяем будущие значения Xt+r-1, Xt+1 на их прогнозы, полученные на предыдущих шагах.
    Замечание. Прогнозы вычисляются последовательно для т = 1, 2, …
    Для стационарной ARMA-модели существует предел lim Xt+r = E(Xt) т.е. долгосрочный прогноз "мало отличается" от тривиального прогноза - математического ожидания. 
    Утверждение. Модели стационарных рядов (ARMA) дают только краткосрочные "содержательные" прогнозы. Долгосрочные прогнозы не являются информативными. Из построения следует, что при т > q формула для Xt+r не включает внешние шоки, т.к. при переходе к следующему шагу "часть МА" сокращается на одно слагаемое.
    |||
    Оценка и тестирование модели: Предварительное тестирование на белый шум. --- Для построения моделей необходимо провести предварительный анализ стационарного ряда. Для этого тестируется гипотеза: Ho: xt~ WN(mu,sigma^2). Точнее тестируется (для некоторого К > 0) гипотеза: H0: p(1) = **= p(K) = 0. Обычно используется две тестовых Q-статистики, которые автоматтически вычисляются в компьютерных пакетах:
    • Box G.E.D., Pierce D.A., 1970 (устаревшая):
    Qbp = n*sum(p^2(h).)
    • Ljung G.M., Box G.E.D., 1978:
    Q = n(n + 2) sum(p^2(h)/n-h)
    Критическое значение имеет хи-квадрат распределения X^2, = X^2k(а), поэтому для проверки гипотезы применяем следующее статистическое правило:
    • При Q > X^2, отвергаем (и H0).
    • При Q < X^2, не отвергаем
    Или альтернативно делаем вывод с помощью Р-значения. Замечание. Применение Q-статистик оправдано только для больших выборок. Это асимптотический тест!
    |||
    Оценка модели и тестирование гипотез временного ряда. --- Оценивание модели ARMA(p, q) происходит с помощью метода максимального правдоподобия (из-за нелинейности в части МА). 
    Тестирование гипотез о значимости коэффициента проводится стандартным для метода максимального правдоподобия путём:
    • Проверка значимости коэффициента: тестовая статистика z=фj/sj
    • Проверка совместной значимости: LR или W статистики.
    Отметим, что модель AR(p) можно оценить, используя метод наименьших квадратов. В этом случае система нормальных уравнений есть система Юла-Уолкера
    р(h) = Ф1*р(h - 1)+...+Фp*p(h - р), h= 1....р
    |||
    Информационные критерии для сравнения моделей и выбора порядка временного ряда: Акаике, Шварца, Хеннана-Куина. Условия их применения. --- 
    AIC = lnS^2 + 2(p+q+1)/n
    SIC= lnS^2 + ((p+q)lnn)/n
    HQC = lnS^2 +  2*(p+q)*(ln(lnn))/n
    Выбиарем модель с наименьшим значением критерияЗамечание. Эмпирически критерий Акаике имеет тенденцию к завышению порядка при больших выборках поэтому Байесовский критерий или критерий Шварца считается предпочтительнее для оцениванию подрядка. Критерий Ханнана-Куинна может недооценивать порядок при небольших объемах выборки.
    |||
    Проверка адекватности модели: тесты на автокорреляцию временного ряда Дарбина-Уотсона, Льюинга-Бокса. --- Проверка адекватности модели
    Проверка адекватности, т.е. проверка согласованности выбранной и оцененной модели с наблюдениями, как и в регрессионном анализе, основано на исследовании остатков. А именно, остатки должны моделировать процесс нормально распределенного белого шума. Тесты на автокорреляцию Тесты на автокорреляцию позволяют проверить "адекватность" выбранного порядка модели. Идея состоит в том, что если порядок модели "правильный", то остатки й, "моделируют" белый шум (в частности, ототсутствует автокорреляция). Так как модель содержит лаговые значения зависимой переменной, то критерий Дарбина Уотсона для исследования ошибок на автокорреляцию неприменим. Статистика DW будет смещенной в сторону уменьшения.
    H0: pu(1) = … = pu(K) = 0
    Статистика для Льюинга-Бокса. Q = n(n + 2) sum(p^2(h)/n-h), где pu(h) - автокорреляционная функция ACF для ряда остатков ut. H0 отвергается при Q > X^2,K-p-q(a), 
    DW = sum(et - et-1)^2/sum(e^2)
    DW < dL => p>0
    Du < DW < 4-dU => p=0
    DW > 4-dL => p<0
    Ограничения теста:
    1. Применим, только если в модели есть константа
    2. Нельзя применять, если в правой части уравнения есть лагированное значение зависимой переменной (Уt-1)
    3. Корректен только в случае, если в модели автокорреляция не выше первого порядка
    |||
    Линейная регрессия для стационарных рядов: Модель FDL --- Модель FDL – это модель линейной регрессии, которая используется для анализа стационарных временных рядов.
    Y_t = c + sum(xt-i*Bi) + u, Если u~WN(0, sigma), то к модели FDL Применимы все выводы стандартной линейной регрессии. 
    |||
    Линейная регрессия для стационарных рядов. Модель ADL. --- Модель авторегрессии-распределённых лагов ADL(p,q) включает лаги регрессоров до порядка q и лаги зависимой переменной до порядка p. Y_t = c + sum(xt-i*Bi) + sum(Oi*yt-i)+ u
    Для использования модели необходимо проверить стационарность,
    для этого все корни многочлена φ(z) = 1−φ1z− · · ·−φ z^p (в том числе из C) должны быть по модулю больше единицы. Если ut ∼WN(0, σ2) и выполнено условие стационарности, то к модели ADL применимы все выводы стандартной линейной регрессии. Замечание. Так как модель регрессии содержит лаговые значения за- висимой переменной, то статистика DW будет смещена и тест ДарбинаУотсона к данной модели неприменим.
    |||

    Понятие TS-ряда. Модель линейного тренда. Модель экспоненциального тренда. --- TS (Time Series) - это статистический метод анализа данных, который используется для изучения изменения переменных во времени. Он представляет собой последовательность наблюдений, произведенных в равные промежутки времени. Класс TS временных рядов – ряды, становящиеся стационарными после вычитания из них детерминированного тренда.

    Определение. Ряд, называется стационарным относительно тренда, если для него имеет место представление y= f(t) +v, где f(t) - детерминированная функция (тренд или долгосрочная тен-
    денция), V- стационарный ряд с нулевым средним. Следовательно, Ext= f(t) и Var(a) = Var(u) = const.AПеречислим основные модели тренда.
    Модель линейного тренда задается уравнением xt=B+ Bit+ut=1,.
    Будем предполагать, что ошибки Ut удовлетворяют условиям теоремы
    Гаусса - Маркова, поэтому к модели линейного тренда применимы вы-
    воды стандартной линейной модели регрессии. В частности, среднее зна-
    чение Е.л, линейно зависит от времени t: E(xt), =Bo + Bt.
    Коэффициент B имеет следующую интерпретацию: это есть среднее
    приращение временного ряда за один период времени deltaEx = Ext - Ext-1=
    Следовательно, с увеличением времени,
    • при B > 0 во временном ряду есть «тенденция к возрастанию»,
    • при B < О во временном ряду есть «тенденция к убыванию», причем средняя скорость изменения временного ряда за один период времени постоянна.
     Модель экспоненциального тренда задается уравнением
    ln(xt) = B0 + B1t+ u. Будем предполагать, что ошибки и удовлетворяют условиям теоремы Гаусса - Маркова. Тогда к модели линейного тренда применимы выводы стандартной линейной модели регрессии. В частности, среднее значение зависит от экспоненциально Eln(xt) = B0 + B1t.
    Для коэффициента 31 получаем следующую интерпретацию:
    Delta ln(xt) = E(Ln(xt)) - E(Ln(xt-1) )= B1.
    Следовательно, за один период времени (в среднем) значение изменяется в ехр(B1) раз. 
    |||
    Нестационарные временные ряды: случайное блуждание, стохастический тренд, случайное блуждание со сносом. --- Рассмотрим модель AR(1) xt = φxt−1 + ut, ut ~ WN(0, σ2u).
    Φ = 1 - случайное блуждание; Xt = sum(Ut) + x0
     sum(Ut) (Сумма от 1 до t) - называется стохастическим трендом.
    Отсюда можно сделать вывод, что случайное блуждание нестационарно и есть сумма всех прошлых шоков.
     Рассмотрим модель AR(1) xt =с + φxt−1 + ut, ut ~ WN(0, σ2u).Φ = 1 - случайное блуждание со сносом Xt = sum(Ut) +t*c+ x0
    |||
    Дифференцирование ряда: определение, DS-ряды. --- Определение. Ряд xt называется интегрированным порядка k, если
    1 xt не TS-ряд и нестационарный;
    2 k – минимальный порядок такой, что ∆kxt – стационарный или TS-ряд.
    Обозначение: xt ~ I(k).
    Замечание. Если xt – стационарный ряд, то формально xt ~ I(0).
    Определение. Ряд xt называется DS-рядом, если xt ~ I(k) для неко-торого k.
    |||
    Подход Бокса-Дженкинса. ---
    1) Проверка ряда на стационарность.
    2) Если ряд не является стационарным, то находится его разность порядка d, которая является стационарным рядом.
    3) Для стационарного ряда необходимо выбрать р и q (с помощью ACF, PACF).
    4) Оценивание параметров модели (0 - i, а - i).
    5) Проверка остатков модели.
    6) Использование модели для прогнозирования.
    |||
    Модель ARIMA --- Модели ARMA(X), описанные выше, могут использоваться только для стационарных данных временных рядов. Однако на практике многие временные ряды демонстрируют нестационарное поведение. Временные ряды, которые содержат трендовые и сезонные модели, также носят нестационарный характер. Таким образом, с точки зрения приложения модели ARMA неадекватны для правильного описания нестационарных временных рядов, которые часто встречаются на практике. По этой причине предлагается модель ARIMA, которая является обобщением модели ARMA и включает случай нестационарности В моделях ARIMA нестационарные временные ряды преобразуются в стационарные путем взятия разностей d-го порядка [2]:
    Процесс ARIMA(p, d, q).
    I обозначает integrated.
    ARIMA(p, 1, q):
    Y, - нестационарный процесс, а
    deltaYt, = Yt, - Yt-1 стационарный процесс ARMA(p, q).
    ARIMA(p, d, q):
    Y, - нестационарный процесс, а
    Delta^d(Y) - стационарный процесс ARMA(p, q).
    ARMA: Xi = c + sum(ai*Xt-i) + sum(bi*Et-i) + E 
    |||
    Тест ADF на единичный корень. --- Стандартным и часто используемым тестом на единичный корень является расширенный тест Дики-Фуллера ( ADF-test)Единичный корень - это свойство временного ряда, при котором он нестационарен и имеет тренд. Тест Дики-Фулера позволяет определить, является ли временной ряд стационарным или нет. Поэтому проверка гипотезы о единичном корне в данном представлении означает проверку нулевой гипотезы о равенстве нулю коэффициента b. Поскольку случай «взрывных» процессов исключается, то тест является односторонним, то есть альтернативной гипотезой является гипотеза о том, что коэффициент b меньше нуля. Статистика теста (DF-статистика) — это обычная t-статистика для проверки значимости коэффициентов линейной регрессии. Однако, распределение данной статистики отличается от классического распределения t-статистики (распределение Стьюдента или асимптотическое нормальное распределение). Распределение DF-статистики выражается через винеровский процесс и называется распределением Дики — Фуллера.
    У теста имеется три варианта реализации:
    1.Без константы и тренда delta y = b*yt-1
    2. С константой, но без тренда:y =b0 + b*yt-1
    3. С константой и линейным трендом:y =b0+ b1*t+ b*yt-1
    Для каждой из трёх тестовых регрессий существуют свои критические значения DF-статистики, которые берутся из специальной таблицы Дики — Фуллера (МакКиннона)
    Если в тестовые регрессии добавить лаги первых разностей временного ряда, то распределение DF-статистики (а значит, критические значения) не изменится. Такой тест называют расширенным тестом Дики — Фуллера (Augmented DF, ADF). Необходимость включения лагов первых разностей связана с тем, что процесс может быть авторегрессией не первого, а более высокого порядка. Рассмотрим на примере модели AR(2), delta yt = (a1 + a2 - 1) yt-1 - a2delta(yt-1) + E
    Тест Дики — Фуллера, как и многие другие тесты, проверяют наличие лишь одного единичного корня. Однако, процесс может иметь теоретически несколько единичных корней. В этом случае тест может быть некорректным
    |||
    Модель ARCH --- ARCH (Autoregressive Conditional Heteroskedasticity) модель используется для анализа временных рядов, в которых наблюдается изменчивость дисперсии. ARCH модель позволяет оценить и предсказать будущую изменчивость дисперсии на основе прошлых данных.
    ARCH-моделью порядка q (обозначают ARCH(q)) называют временной ряд u_{t} с функцией условной дисперсии следующего вида:
    Sigma^2 = w + sum(ai * u^2_t-i)
    Для недопущения отрицательных значений дисперсии предполагается, что все коэффициенты модели неотрицательны, причём константа строго положительна.
    Для оценки параметров ARCH модели необходимо выполнить следующие шаги:
    1. Выбрать подходящую модель ARCH, например, ARCH(1) или ARCH(p), где p - количество лагов.
    2. Оценить параметры модели ARCH с помощью метода максимального правдоподобия (maximum likelihood estimation). Для этого необходимо определить функцию правдоподобия и максимизировать ее значение, используя численные методы.
    3. Проверить значимость параметров модели ARCH с помощью статистических тестов, таких как тест Вальда или тест Ликelihood ratio.
    4. Проверить соответствие модели данных с помощью диагностических тестов, например, теста Льюнга-Бокса или теста Арчибальда.
    5. Использовать оцененные параметры для прогнозирования будущей изменчивости дисперсии и принятия решений на основе полученных результатов.
    |||
    Модель GARCH. --- 
    ARCH-модель предполагает зависимость условной дисперсии только от квадратов прошлых значений временного ряда. Обобщить данную модель можно предположив, что условная дисперсия зависит также от прошлых значений самой условной дисперсии. Это так называемый обобщённый ARCH (Generalized ARCH — GARCH).
    Sigma^2 = w + sum(ai * u^2_t-i) + sum(B*sigma^2_t-j)
    Меняем на GARCH
    Для оценки параметров ARCH модели необходимо выполнить следующие шаги:
    1. Выбрать подходящую модель ARCH, например, ARCH(1) или ARCH(p), где p - количество лагов.
    2. Оценить параметры модели ARCH с помощью метода максимального правдоподобия (maximum likelihood estimation). Для этого необходимо определить функцию правдоподобия и максимизировать ее значение, используя численные методы.
    3. Проверить значимость параметров модели ARCH с помощью статистических тестов, таких как тест Вальда или тест Ликelihood ratio.
    4. Проверить соответствие модели данных с помощью диагностических тестов, например, теста Льюнга-Бокса или теста Арчибальда.
    5. Использовать оцененные параметры для прогнозирования будущей изменчивости дисперсии и принятия решений на основе полученных результатов.
    |||
    Область применения панельных данных. Преимущества использования панельных данных. --- Панельные данные используются в различных областях, где необходимо изучать поведение одних и тех же объектов в течение времени. Например, в экономике панельные данные используются для анализа изменений экономических показателей фирм, стран или регионов в течение определенного периода времени.,
    Термин "панельные данные" (panel data) пришел из обследований индивидов, и в  этом контексте "панель" представляла собой группу индивидов, за которыми регулярно  осуществляли наблюдения в течение определенного периода времени. В настоящее время  методы анализа панельных данных получили большое распространение, и понимание  панельных данных стало намного шире. Наряду с термином "панельные данные" иногда  также используется термин "лонгитюдные данные" (longitudinal data). Панельные данные состоят из повторных наблюдений одних и тех же выборочных  единиц, которые осуществляются в последовательные периоды времени. В качестве  объектов наблюдения могут выступать индивиды, домашние хозяйства, фирмы, страны и   т.д. Примером панельных данных могут быть ежегодные обследования одних и тех же  домашних хозяйств или индивидов (например, для определения изменения их  благосостояния), ежеквартальные данные об экономической деятельности отдельных  компаний, ежегодные социально-экономические показатели для регионов одной страны  или для группы стран и т.д.
    Преимущества использования панельных данных:
    1. Увеличение точности анализа. Панельные данные позволяют учитывать изменения в поведении объектов в течение времени, что повышает точность анализа и позволяет получать более точные выводы.
    2. Учет индивидуальных особенностей объектов. Панельные данные позволяют учитывать индивидуальные особенности объектов, что может быть важным при анализе поведения фирм, стран или регионов.
    3. Возможность анализа динамики изменений. Панельные данные позволяют анализировать динамику изменений в поведении объектов в течение времени, что может быть полезно при прогнозировании будущих изменений.
    4. Экономия времени и ресурсов. Использование панельных данных позволяет экономить время и ресурсы, так как данные о поведении объектов уже собраны и не требуют дополнительных затрат на сбор информации.
    5. Возможность контроля за влиянием факторов. Панельные данные позволяют контролировать влияние различных факторов на поведение объектов, что может быть полезно при принятии решений.
    |||
    Модели панельных данных и основные обозначения. --- 
    Модель Пула 
    Модель регрессии с фиксированным эффектом
    Модель регрессии со случайным эффектом
    Пусть имеются данные yit, xit, I = 1,…, N Здесь N – количество субъектов, а Т 
    – число последовательных моментов времени. Требуется оценить 
    модель линейной связи между переменными Y и X. В общем случае Х является вектором конечной размерности k (может существовать p независимых факторов). Рассмотрим сбалансированные панели, где для каждой пространственной единицы имеется одинаковое число наблюдений по всем периодам времени. Тогда общее числонаблюдений будет N*T . При N=1 и достаточно большом T получаются временные ряды, а при T = 1 и достаточно большом N получаются пространственные данные. Попробуй представить это векторами типа [yi1, yi2 …]
    |||
    Модель пула (Pool model). --- При отсутствии значимых различий (неоднородности) между пространственными объектами выборки, возможно построение регрессии по объединенной выборке (pooled regression) – пула. Это модель сквозной регрессии: 
    Yit = Xitb + a + eit с остатками , удовлетворяющими требованиям МНК. В этом случае мы имеем дело с  обычной линейной регрессией с NT наблюдениями, удовлетворяющей предположениям классической нормальной линейной модели. Для получения эффективных оценок вектора  коэффициентов достаточно использовать обычный метод наименьших квадратов (OLS) . Полученные при этом оценки b и а являются наилучшими линейными несмещенными оценками (BLUE – best linear unbiased estimate) вектора β.
    ||| 
    Модель регрессии с фиксированным эффектом (fixed effect model) --- yit = Xitb+ai + eit
    В отличие от предыдущего случая свободный член ai принимает различные значения для каждого объекта выборки. Смысл его в том, чтобы отразить влияние пропущенных или  ненаблюдаемых переменных, характеризующих индивидуальные особенности исследуемых объектов не меняющиеся со временем. Термин "фиксированные эффекты"означает, что константа в уравнении регрессии может различаться между объектами, но для каждого конкретного объекта константа является постоянной во времени, т.е. не изменяется с течением времени t.
    Оценка коэфициентов считается через обычнфй МНК. 
    Эта модель является довольно гибкой, так как, в отличие от предыдущей модели, она 
    позволяет учитывать индивидуальную гетерогенность объектов. Однако, за эту гибкость 
    часто приходится расплачиваться потерей значимости оценок (из-за увеличения их 
    стандартных ошибок), так как приходится оценивать N лишних параметров. Если 
    количество субъектов анализа N велико, необходимость обращать матрицу высокой 
    размерности (N+K) вызывает вычислительные трудности. 

    Проверка гипотезы H1 (следует ли использовать модель с фиксированными 
    эффектами М1, либо строить модели отдельно для каждого объекта М0)
    F1 = ((S1-S0)/(N-1)*k)/(S0/N*(T-k-1))Если значение F1 статистически незначимо, то следует использовать модель с фиксированными эффектами. 

    Проверка гипотезы H2 (следует ли использовать единую модель для всех объектов 
    М2, либо строить модели отдельно для каждого объекта М0)
    F2 = ((S2-S0)/(k+1)*(N-1))/(S0/N*(T-k-1))Если значение F2 статистически незначимо, то следует использовать модель с фиксированными эффектами. 
    |||
    Модель регрессии со случайным эффектом (random effect model). --- В ряде ситуаций N субъектов, для которых имеются статистические данные, рассматриваются как случайная выборка из некоторой более широкой совокупности (популяции), и исследователя интересуют не конкретные субъекты, попавшие в выборку, а обезличенные субъекты, имеющие заданные характеристики. Соответственно, в таких ситуациях предполагается, что αi являются случайными величинами, и мы говорим тогда о модели со случайными эффектами (random effects). В такой модели αi уже не интерпретируются как значения некоторых фиксированных параметров и не подлежат оцениванию. Вместо этого оцениваются параметры распределения случайных величин αi. Yi= lambda + Xitb +ai + E 
    В матричной записи уравнение имеет вид: y = X*b + u, u = a + E, E(U) = 0, D(U) = D(a + E) = сумме их сигм
     Как и в модели с фиксированными эффектами, случайные эффекты αi также отражают наличие у субъектов исследования некоторых индивидуальных характеристик, не изменяющихся со временем в процессе наблюдений, которые трудно или даже невозможно наблюдать или измерить. Однако теперь значения этих характеристик встраиваются в состав случайной ошибки, как это делается в классической модели регрессии, в которой наличие случайных ошибок интерпретируется как недостаточность включенных в модель объясняющих переменных для полного объяснения изменений объясняемой переменной.Эта модель является компромиссом между двумя предыдущими (пулом и моделью с фиксированными эффектами), поскольку она является менее ограничительной, чем первая модель, и позволяет получать более статистически значимые оценки, чем вторая. Если сформулированные предположения выполняются, оценки обобщенного метода наименьших квадратов (GLS) этой модели будут несмещенными.
    |||
    Тест Бройша-Пагана для панельных данных. --- Для сравнения модели со случайными эффектами со сквозной регрессией (моделью пула) используется тест Бройша-Пагана. Это критерий для проверки в рамках RE-модели (со стандартными предположениями) гипотезы о равенстве межгрупповой дисперсии ошибок нулю: H0 = sigma^2_a = 0 сведение к модели пула. BP = NT/(2*(T-1))[sum(sum(Eij)^2)/sum(sum(Eij^2))]^2
    Статистика критерия Бройша–Пагана распределена по X^2(1). Соответственно, гипотеза H0 отвергается в пользу модели со случайными эффектами, если наблюдаемое значение статистики BP превышает критическое значение, рассчитанное по распределению X^2(1).
    |||
    Тест Хаусмана для панельных данных. --- Для сравнения модели со случайными эффектами с моделью с фиксированными эффектами используется тест Хаусмана. Модель со случайным эффектом имеет место только в случае некоррелированности случайного эффекта с регрессорами. Это требование часто бывает нарушено. Как было показано Мундлаком, учет подобной корреляции приводит к регрессии, в которой МНК-оценки коэффициентов наклона совпадают с оценками «within». В тесте проверяются следующие гипотезы: H0 = cov(ai, Xit) = 0,H1 = cov(ai, Xit) != 0 
    M = q tetta q, q = bw - bОМНК который распределен поX^2(k). Если остаемся в области Н0, следует пользоваться моделью RE со случайными эффектами. Если попадаем в критическую область, следует пользоваться моделью FE c фиксированными эффектами. 
    |||

    Тест Лагранжа для панельных данных. --- Выбор моделей для панельных данных базируется на формальных тестах. Тестирование модели без эффектов против модели со случайными эффектами выполняется при помощи теста множителей Лагранжа.
    Тест множителей Лагранжа  — статистический тест, используемый для проверки ограничений на параметры статистических моделей, оцененных на основе выборочных данных. Является одним из трёх базовых тестов проверки ограничений наряду с тестом отношения правдоподобия и тестом Вальда. Тест является асимптотическим, то есть для достоверности выводов требуется достаточно большой объем выборки.
    Проверяется нулевая гипотеза:
    H0: sigma_1^2 = sigma_i^2 = f(фи0)
    H1: sigma_i^2 = f(фи0+zi*фи)
    LM = (NT/(2(T-1)))*[T^2 * sum(uj^2)/ sum(sum(uij^2))]^2 
    LM>X^2 - нулевая отвергается 
    Замечание. Результаты теста существенно зависят от спецификации регрегрессионного уравнения. Гипотеза об отсутствии случайного индивидуального эффекта редко отвергается, если модель сформулирована в темпах роста. Если даже этот эффект наблюдался в уровнях, он исчезает в темпах роста.
    |||
    Вычисление значения оценок параметров β и а в модели с фиксированным эффектом. --- 
    Y = XitB + ai + eit; В матричной форме - y = Xb + ZA + e; A - вектор конст; Z - блочно диоганальная матрица фиктивных переменных. В этом случае оценка коэфициентов считается через обычный МНК 
    B = [X’X  XZ  ]^-1  [X’ Y]
           [Z’X   Z’Z]        [Z’ Y]
    Численно те же самые оценки можно получить Взяв среднее от всех переменных
    ср_yi = ср_хi *b + ai + ср_e
    Далее если сделать подстановку y* = yit - ср_y 
    Y* = X* b + e*
    Получив b, a вычисляем - ai = ср_yi - ср_Xi
    |||
    Отражение пространственных эффектов. Бинарная матрица граничных соседей. Приведите пример. --- Бинарная матрица граничных соседей -
    Wij = {0 if i = j, 1 if I граничит j, 0 не граничит}
    это наиболее простой способ учета пространственных взаимосвязей согласно данной матрице на исследуемые объекты оказывают влияние только те соседи, которые граничат с ними из-за бинарности матрицы при нормализации ее значений получается, что на территорию оказывается влияние соседних территорий с одними и теми же пространственными весами.Основная идея в модели, построенной на такой матрице, заключается в предположении, что на регион влияют только его непосредственные соседи, с которыми регион имеет общие границы. Соответственно пренебрегаем влиянием регионов, с которыми нет общей границы 
    Пример: просто регион граничит не граничит, какое-нибудь выдуманное государство придумай.
    |||
    Отражение пространственных эффектов. Бинарная матрица ближайших соседей. Приведите пример. --- Wij = {0 if i = j, 1 if dij < di(k), 0 dij > di(k)}
    di(k) - минимально
    • В этом случае число соседей для каждого объекта будет равно к.
    • Рассчитываются расстояния от данного объекта до всех имеющихся объектов. Затем берется к минимальных расстояний
    • И k-е расстояние для данного объекта является той границей, за которой взаимодействия не учитываются. при использовании данной матрицы, для получения устойчивых результатов учитываются 10-25 ближайших соседей
    Как правило, коэффициент у может принимать значения от 1 до 10. Но чаще всего коэффициент у считается равным двум. В этом случае коэффициент матрицы весов представляет собой аналог коэффициента гравитации: притяжение регионов обратно пропорционально квадрату расстояния. Таким образом, чем дальше находятся регионы географически, тем меньшее влияние они оказывают друг на друга. В случае, если д < 4, критическим расстоянием отсечения, дальше которого взаимовлияние считается несущественным, считается соответствующий квартиль расстояния О(d). В случае, когда d= 4, в матрице весов учитываются все расстояния, так что нули содержат только элементы главной диагонали.
    Пример: просто регион граничит не граничит и еще соседи соседей, какое-нибудь выдуманное государство придумай.
    |||
    Отражение пространственных эффектов. Матрица расстояний. Приведите пример. ---
    Wij = {0 if i = j, 1/dij, if dij < D(q), 0 dij > D(q)}, dij - расстояние между объектами, D(q) - квартили расстояний. 
    Матрица расстояний является аналогом гравитационной модели притяжение объектов обратно пропорционально квадрату расстояния между ними. поэтому, чем дальше располагаются объекты друг от друга, тем меньше они взаимодействуют.
    * Если q<4, то соответствующий квартиль расстояния D(q) является максимальным расстоянием, дальше которого взаимодействие между объектами является несущественным.
    * Если q-4, то происходит учет всех расстояний (в весовой матрице нулевыми будут только элементы главной диагонали).
    Пример: просто расстояние между регионами, только обрати внимание на формулу, все растояния должны быть 0.00123, какое-нибудь выдуманное государство придумай.
    |||
    Отражение пространственных эффектов. Матрица расстояний с учетом размера объекта. Приведите пример. --- Wij = {0 if i = j, Ai/dij, if dij < D(q), 0 dij > D(q)}dij - расстояние между объектами, D(q) - квартили расстояний, Aj - показатель отражающий весомость соседнего объекта. 
    Данный подход позволяет учесть дополнительный параметр, характеризующий каждый из объектов: его размер, площадь важность (весомость) в исследуемых процессах Его уровень социально-экономического развития. Здесь нужно отметить: для того чтобы избежать проблем идентификации, вес а пространственной матрицы должны быть экзогенны по отношению к модели. Пример: просто расстояние между регионами, только обрати внимание на формулу, все расстояния должны быть 0.025, какое-нибудь выдуманное государство придумай.
    |||
    Алгоритм построения матрицы пространственных весов. Приведите пример. --- 1. Формирование матрицы расстояний административными центрами субъектов РФ (Х)) между 1) по линейным расстояниям; 2) по автомобильным дорогам, железнодорожным магистралям, авиационным, речным сообщениям 3) по смежным границам (с использованием бинарных переменных 1 и 0). 2. Стандартизация расстояний в матрице по строкам 3. Преобразование матрицы расстояний в относительную V = 1/Xij 4. Формирование матрицы стандартизированных дистанций между территориями Wij = Vij/sum(Vij).  Пример: просто расстояние между регионами, только обрати внимание на формулу, все расстояния должны быть 0.0015, какое-нибудь выдуманное государство придумай.
    |||
    Пространственная автокорреляция по методологии А. Гетиса и Дж. Орда. Недостатки методологии. --- Самыми распространёнными показателями, которые используют для выявления пространственной автокорреляции индекса Гетиса – Орда G = sumsum(wij * Yi * Yj)/sumsum(Yi * Yj), где wij - элементы нормированной по строкам взвешивающей матрицы W. E(G) = sumsum(wij)/N(N-1); zG = (G - E[G])/(sqrt(V[G])) 
    G > E(G) - Наблюдается пространственная кластеризация объектов с высокими значениями
    G < E(G) - Наблюдаеотся пространственная кластеризация объектов с низкими значениями 
    Рост Z - повышение интенсивности пространственной кластеризации. 
    Показатель Getis-Ord (G) используется когда:
    • данные распределены достаточно равномерно,
    • необходимо найти неожиданные всплески высоких значений в пространстве
    Недостатки методики Гитиса-Орда
    Однородность распределения показателей социально экономического развития по территориальным системам встречается крайне редко В условиях высокой поляризованности социально экономического развития данный метод дает ложные результаты
    С помощью индекса Гетиса – Орда проверяется гипотеза только о наличии или отсутствии положительной автокорреляции (т. е. о наличии кластеров), однако возможно получение более детальной информации о самих кластерах, если они выявлены, а именно – основная гипотеза состоит в отсутствии кластеров, а альтернативная гипотеза – в доминировании кластеров с бо́льшим значением рассматриваемого показателя или кластеров с малым значением рассматриваемого показателя.
    |||
     Пространственная автокорреляция по методологии Роберта Джири. --- Является одним из показателей общей пространственной корреляции, который вычисляется для выявления возможной пространственной зависимости  В случае сложной структуры (когда отношения между соседними объектами имеют «нелинейный» характер), более точную картину пространственных взаимосвязей можно получить, используя показатели пространственной автокорреляции П. Морана или С Джири. С = ((n-1)/2*S0)[sumsum(wij(Yi - Yj)^2)/sumsum(Yi - средн_Y)], S0 = sumsum(wij), Y - исследуемый признак. 
    C = 1 пространственная корреляция отсутствует
    0 < C < 1 Положительная пространственная корреляция
    1 < C < 2 Отрицательная пространственная корреляция
    Оценка статистической значимости. Zc = (C - E[C])/SD[C], Величина Z определяет на какое количество стандартных отклонений фактическое значение статистики Р. Джири удалено от ожидаемого среднего значения (E). Z<0 Положительная пространственная корреляция. Z>0 Отрицательная пространственная корреляция
    |||
    Пространственная автокорреляция по методологии Морана П. --- Индекс Морана, показатель, позволяющий выявлять региональные кластеры. Является одним из самых популярных показателей, который вычисляется для выявления пространственных кластеров (наряду с индексами Гири и Гитиса - Орда). Индекс Морана для выбранного показателя Y рассчитывается по формуле: I(Y) = (sumsum(Yi - Y)(Yj - Y))/sum((Yi - средн_Y)^2),  wi,j - элементы нормированной по строкам взвешивающей матрицы
    W, i, j = 1, …,n.
    Индекс Морана может принимать значения -1 < I(Y) < 1. С его помощью можно проверить гипотезу :H0: I = E(I) (т. е. значения исследуемого показателя в рассматриваемых регионах являются случайной величиной) при альтернативных гипотезах. H1: I > E(I) Положительная автокореляция. H1: I < E(I) Отрицательная автокореляция. 
    Тестовая статистика: Z = (I - E(I))/Var(I), если Z>Za Нулевая отвергается.
    |||
    Пространственная кластеризация территорий. Локальный индекс автокорреляции П. Морана (Ili) --- Локальные индексы автокорреляции П. Морана позволяют:
    1.Установить полюса роста пространственных кластеров
    2.Оценить силу взаимовлияния полюсов роста на другие территории
    3.Оценить направление пространственной корреляции (прямая / обратная)
    I_Li = N* (xi - mu) * sum(wij(xj - mu))/sum(xi = mu) 
    При ILi < 0 наблюдается отрицательная автокорреляция для территории і, данная территория существенно отличается по исследуемому показателю от соседних территорий (outlier)
    При ILi > 0 - автокорреляция положительная, данная территория по исследуемому показателю подобна соседним территориям (cluster) 
    При | ILi | > | Ili | - подобие/различие территории і с окружающими ее соседними территориями является большим, чем в случае территории j и ее соседей.
    Матричные методы расчета составляющих локального индекса Морана В процессе исследования характеристик взаимовлияния изучаемой территории (территорий) и всех ближних или дальних ее (их) соседей возможно вести поиск для: 
    а) любой территории в отдельности; 
    б) совокупности территорий, объединенных по одному критерию (например, для каждого ядра в отдельности, для совокупности ядер при изучении влияния на территорию Самарской области) – для территориальных кластеров (подкластеров как составляющих кластеров) и всей совокупности территорий (районов); 
    Матричные методы расчета составляющих локального индекса Морана В процессе исследования характеристик взаимовлияния изучаемой территории (территорий) и всех ближних или дальних ее (их) соседей возможно вести поиск для: 
    а) любой территории в отдельности; 
    б) совокупности территорий, объединенных по одному критерию (например, для каждого ядра в отдельности, для совокупности ядер при изучении влияния на территорию Самарской области) – для территориальных кластеров (подкластеров как составляющих кластеров) и всей совокупности территорий (районов); 
    |||
    Матрица взаимовлияния Л. Анселина (LISA). --- 
    оценить тесноту взаимосвязи между исследуемыми объектами пространстве. 
    выявить направление данных взаимосвязей (прямые и обратные)
    Vij = 1/xij
    Wij = Vij/sum(Vij)
    LISA= Zi Zj Wij
    LISA, - индекс локальной автокорреляции между двумя регионами;
    w - элемент матрицы пространственных весов для регионов i j;
    z - стандартизированные значения показателя одного региона:
    Z = (xi - mu)/sqrt(sum((xi - срзнач_xi)^2)/n)

    Выделение в матрице значений, превышающих среднее значение локального индекса автокорреляции, позволит: выявить зоны взаимовлияния полюсов роста, установить территории, получающие импульс от их развития или способствующие их развитию
    где LISA - сила взаимовлияния между двумя конкретными территориями.
    '''

    k_an = '''
    $$$Вопрос 1 --- Линейная модель множественной регрессии. Основные предпосылки метода наименьших квадратов ---  
    Линейная модель множественной регрессии - это статистическая модель, которая позволяет описать зависимость между одной зависимой переменной и несколькими независимыми переменными
    y = b_0+X*b+E
    1)M(E)=0
    2)D(E)=const и независим. от перем.
    3)Автокорреляция отсутствует
    4)Мультиколлениарность отсутствует
    5)Модель линейна
    $$$Вопрос 2 --- Нелинейные модели регрессии. Подходы к оцениванию. Примеры --- 
    Различают два класса нелинейных регрессий:
    Нелинейные относительно включенных в анализ: y^^_x= a+b*x+c*x^2, y^^_x= a+b*x+c*x^2+d*x^3; равносторонняя гипербола y^^_x=a+b/x; y^^_x=a+b*ln(x)-полулогарифмическая
    Нелинейные относительно оцен.парам.: y^^_x = a*b^x-показат; y^^_x=a*x^b-степенная;y^^_x=e^(a+b*x)-экспоненциальная
    В моделях, нелинейных по переменным и линейных по параметрам, регрессоры, имеющие степень, отличную от первой, заменяются другими независимыми переменными первой степени, и к новой системе переменных применяется обычный МНК. После того как получено уравнение с оцененными параметрами, введенные в него новые независимые переменные заменяются на первоначальные. 
    Например, для преобразования гиперболической регрессии:
    Y = a + b*1/X+eps
    к линейному виду используется замена:
    X^~= 1/X
    Оцениваются параметры лин рег модели
    Y=a+b*X^~+eps
    $$$Вопрос 3 --- Тестирование правильности спецификации: типичные ошибки спецификации модели. Тест Рамсея, условия применения теста. --- 
    Ошибки: Отбрасывание знач, Добавление незнач, Выбор непр функц зависимости (
    Н_0 прав
    Н_1 неправ
    1)^y_i=b_i*x_i + b_1+E
    2)y_i = b_i*x_i+b_1+^y^2*a_2 + … + ^y^m*a_m+u
    3)F = [(RSS_R = RSS_UR)/(m-1)]/[RSS_UR/(n-(k+-m-1)])
    4)H_1: F>F_a (m-1, n-(k+m-1))
    Признаки хорошей: простота/скупость, единственность, согласов с теорией
    Схема: Подбор начал модели, оценка параметров, проверка качества
    Условия применения: 1) Модель линейна 2) достаточное кол-во наблюдений 3) отсутствие мультиколлениарности 4) нормальность распределения случ ошибки 
    $$$Вопрос 4 --- Тестирование правильности выбора спецификации: типичные ошибки, Критерий Акаике, Критерий Шварца --- 
    AIC = 2k + 2ln(L)/ AIC = 2k + n[ln(RSS)] в случае сравнения моделей на выборках одмнаковой длины,выражение можно упростить , выкидывая члены зависящие только от n , (макс знач функции правдоподобия);   BIC = -2 * log(L) + k * log(n), где L - функция правдоподобия модели, k - количество параметров в модели, n - количество наблюдений.
    Условия применения критерия Акаике:
    1. Модели должны быть линейными.
    2. Наличие достаточного количества наблюдений для оценки модели.
    3. Отсутствие мультиколлинеарности между независимыми переменными.
    4. Нормальность распределения случайной ошибки.
    Условия применения критерия Шварца:
    1. Модели должны быть линейными.
    2. Наличие достаточного количества наблюдений для оценки модели.
    3. Отсутствие мультиколлинеарности между независимыми переменными.
    4. Нормальность распределения случайной ошибки.
    5. Модели должны быть однородными (одинаковые переменные во всех моделях).
    Акаике: использует жестую функцию для сложных моделей
    Шварц: больше: модели с небольшим объемом данных
    $$$Вопрос 5 --- Гетероскедастичность: определение, причины, последствия. Тест Голдфеда-Квандта и особенности его применения --- 
    Гетероскедастичность - это нарушение гомоскедастичности (одинаковости дисперсии) ошибок модели. 
    Причиной гетероскедастичности часто являются эффект масштаба, а так же характерно для для перекрестных параллельных данных, неправильная спецификация модели, выбросы в данных.
    Последствия: Рассчитанные оценки неэффективны так как увеличенная дисперсия снижает вероятность получения чистых оценок. Выводы на основе t статистик и p значений будут недостоверными
    Тест Голдфелда — Квандта (англ. Goldfeld-Quandt test) — процедура тестирования гетероскедастичности случайных ошибок регрессионной модели, применяемая в случае, когда есть основания полагать, что стандартное отклонение ошибок может быть пропорционально некоторой переменной
    1)Сортируются по убыв
    2)Делятся на выборки по значению выбранной объясняющей переменной.
    F = RSS_1/RSS_2 (при равных выборках) > F(m-k:m-k) гетераскед имеет место
    Особенности применения теста Голдфеда-Квандта включают следующее:
    1. Тест можно применять только для линейных моделей с одной объясняющей переменной.
    2. Перед применением теста необходимо разбить выборку на две подгруппы по значению выбранной объясняющей переменной.
    4. Нулевая гипотеза теста заключается в равенстве дисперсий ошибок модели для двух подгрупп.
    6. Тест Голдфеда-Квандта не является единственным методом диагностики гетероскедастичности и его результаты могут быть дополнены другими тестами и методами.

    $$$Вопрос 6 --- Гетероскедастичность: определение, причины, последствия. Тест ранговой корреляции Спирмена и особенности его применения ---
    Гетероскедастичность - это нарушение гомоскедастичности (одинаковости дисперсии) ошибок модели. 
    Причиной гетероскедастичности часто являются эффект масштаба, а так же характерно для для перекрестных параллельных данных, неправильная спецификация модели, выбросы в данных.
    Последствия: Рассчитанные оценки неэффективны так как увеличенная дисперсия снижает вероятность получения чистых оценок. Выводы на основе t статистик и p значений будут недостоверными
    При использовании данного теста предполагается, что дисперсия отклонения будет либо увеличиваться, либо уменьшаться с увеличением значений Х. Поэтому для регрессии, построенной по МНК, абсолютные величины отклонений e_i и значения x_i будут коррелированны.
    1.Значения х_i и e_i ранжируются (упорядочиваются по величинам). 
    2.определяется коэффициент ранговой корреляции:
    r_x,e =1- 6 *(sum(d^2_i)/(n(n^2 - 1))) [d_i - разность между рангами x_i и e_i, n- число наблюдений)
    3.статистика t = (r_x,e*sqrt(n-2)) / (sqrt(1-r^2_x,e))
    4.табличное t = распр.Стьюдент с числом степ свободы v=n-2
    Следовательно, если наблюдаемое значение t-статистики превышает табличное, то необходимо отклонить гипотезу о равенстве нулю коэффициента корреляции ,а, следовательно, и об отсутствии гетероскедастичности.
    Если в модели регрессии больше чем одна объясняющая переменная, то проверка гипотезы может осуществляться с помощью t-статистики для каждой из них отдельно.
    Особенности применения теста ранговой корреляции Спирмена включают следующее:
    1. Тест может быть применен для любых типов данных, которые можно преобразовать в ранговую шкалу.
    2. Тест выполняется на основе вычисления ранговых коэффициентов корреляции между двумя переменными.
    3. Нулевая гипотеза теста заключается в отсутствии связи между двумя переменными.
    5. Тест ранговой корреляции Спирмена не требует нормальности распределения данных и устойчив к выбросам.
    $$$Вопрос 7 --- Гетероскедастичность: определение, причины, последствия. Тест Тест Бреуша-Пагана и особенности его применения. --- 
    Гетероскедастичность - это нарушение гомоскедастичности (одинаковости дисперсии) ошибок модели. 
    Причиной гетероскедастичности часто являются эффект масштаба, а так же характерно для для перекрестных параллельных данных, неправильная спецификация модели, выбросы в данных.
    Последствия: Рассчитанные оценки неэффективны так как увеличенная дисперсия снижает вероятность получения чистых оценок. Выводы на основе t статистик и p значений будут недостоверными
    Тест: предполагается, что дисперсия случ ошибки зависит от нескольких независимых переменных. 
    s^2_i = y_0+y_1*z_i1+…+y_m*Z_im
    Этапы тестирования:
    Этапы тестирования:
    1. Рассчитывают МНК-оценки коэффициентов регрессии.
    2. Находят остатки е_i
    3. Находят квадраты остатков е^_i
    4. Рассчитывают коэффициент детерминации R ^2 для регрессии e^2_i = y_0+y_1*z_i1+…+y_m*Z_im
    5. вычисляют X^2_набл = n*R^2
    6. Если X^2_набл превосходит критическое значение статистики Хи-квадрат набл для m степеней свободы, гетероскедастичность присутствует.
    Применение теста Бреуша-Пагана имеет следующие особенности:

    - Тест может применяться только для линейных регрессионных моделей.

    - Тест не учитывает возможное наличие автокорреляции ошибок в модели.

    - Тест не дает информации о том, какая переменная является источником гетероскедастичности.

    - Тест не предлагает способов коррекции гетероскедастичности, а только позволяет выявить ее наличие.

    - В случае отсутствия гетероскедастичности тест может давать ложноположительные результаты, особенно при малых выборках. Поэтому рекомендуется использовать его только при больших выборках (например, более 100 наблюдений)
    $$$Вопрос 8 --- Гетероскедастичность: определение, причины, последствия. Тест Тест Глейзера и особенности его применения --- 
    Гетероскедастичность - это нарушение гомоскедастичности (одинаковости дисперсии) ошибок модели. 
    Причиной гетероскедастичности часто являются эффект масштаба, а так же характерно для для перекрестных параллельных данных, неправильная спецификация модели, выбросы в данных.
    Последствия: Рассчитанные оценки неэффективны так как увеличенная дисперсия снижает вероятность получения чистых оценок. Выводы на основе t статистик и p значений будут недостоверными
    Особенности применения теста Глейзера включают следующее:
    1. Тест Глейзера может быть применен только в том случае, если данные измеряются дважды на одной и той же группе людей или если две группы людей сопоставляются на основе некоторых характеристик.
    2. Тест выполняется путем вычисления разности между парами значений из двух выборок.
    3. Нулевая гипотеза теста заключается в отсутствии различий между средними значениями двух связанных выборок.
    5. Тест Глейзера требует нормальности распределения данных и устойчив к выбросам.
    |E| = a+b*x_i^k + б
    a,b - неизвестные параметры, зависят от ур. регрессии
    k - задается произвольно, обычно k может быть равно: -2;-1;-0,5;0,5;1;2.
    Дается оценка значимости b, если он значим - гетероскедастичность в остатке (т.е. отсутствие зависимости х от у)
    Если изменится форма регрессии, то параметры меняются. t>t табл -> параметры значимы -> гетероскедастичность по определенному фактору (x_i).
    Если гетероскедастичность хотя бы по одному тесту -> остатки гетероскедастичны в общем и тест Глейзера можно не продолжать
    $$$Вопрос 9 --- Способы корректировки гетероскедастичности: взвешенный метод наименьших квадратов (ВМНК) и особенности его применения ---
    Для повышения качества моделей используют метод взвешенных наименьших квадратов. Суть: смягчаем гетероскедастичность путем деления каждого наблюдаемого значения на соответствующее ему значение дисперсии**0.5. y_i = b_o + b_1*x_i + e_i
    Случай 1: (Дисперсии sig^2_i известны)
    1) Каждую величину делят на известную sig_i
    y_i/sig_i= b_o * 1/sig_i + b_1* x_i/sig_i + e_i/sig_i -> парная регрессия
    2) у* = b_0*z_i+ b_1*x^*_1 + u_i (поясняю, тут х со звездочкой и индексом 1)-> множественная без свободного члена
    По МВНК для преобразованных значений оценивается уравнение регрессии с гарантированными качественными оценками (несмещенными, эффективными и состоятельными)
    Случай 2: (Дисперсии sig^2_i неизвестны)
    a) Предполагается, что sig^2_i пропорциональны X_i
    Тогда sig_i = sqrt(x_i) => y_i//sqrt(x_i) = b_o * 1/sqrt(x_i) + b_1* sqrt(x_i) + u_i
    б) Предполагается, что sig^2_i пропорциональны X2
    Тогда sig_i = X_i => y^*= b_o*z_i + b_1 + u_i
    Для выбора случая а) или б) целесообразно опираться на анализ графиков: (по оу e^2_i, по ох X_i )
    Б, если линия в первой четверти, как ) чуть наклоненная, как парабола (оси не пересекает)
    А, если просто прямая в первой четверти (оси не пересекает)
    $$$Вопрос 10 --- Автокорреляция: определение, причины, последствия. Тест Дарбина-Уотсона и особенности его применения ---
    Автокорреляция - это явление, когда значения ошибок модели регрессии коррелируют между собой. Например:  если ошибка в одной точке времени положительна, то вероятность того, что ошибка в следующей точке времени тоже будет положительной, выше, чем если бы ошибки были независимыми.
    Причины автокорреляции могут быть различными, например, это может быть связано с неправильным выбором функциональной формы модели, неучтенными факторами, которые влияют на зависимую переменную, или с ошибками в данных.
    Последствия: Оценки перестают быть эффективными => увеличивается дисперсия оценок, которая снижает вероятность получения максимально точных оценок. Выводы на основании t и F будут ненадежными
    DW = (sum(n;t=2)((e_t-e_(t-1))^2)) / (sum(n;t=1)(e^2_i)) э(принадлежит) [0;2)u(объединение)(2;4] (поясняю, sum(над знаком суммы;под знаком суммы)(что суммируем)) 
    Есди DW около 2, то автокоррел нет
    Ограничения: - для тех моделей, что содержат своб чл
    - для данных с одинаковой периодичностью
    - Не применим для авторегрессионных моделей
    Предпосылки: - случ возмущение распределено нормально
    - не подвержено гетероскедастичности
    $$$Вопрос 11 --- Автокорреляция: определение, причины, последствия. Тест Дарбина-Уотсона и особенности его применения ---
    Автокорреляция - это явление, когда значения ошибок модели регрессии коррелируют между собой. Например:  если ошибка в одной точке времени положительна, то вероятность того, что ошибка в следующей точке времени тоже будет положительной, выше, чем если бы ошибки были независимыми.
    Причины автокорреляции могут быть различными, например, это может быть связано с неправильным выбором функциональной формы модели, неучтенными факторами, которые влияют на зависимую переменную, или с ошибками в данных.
    Последствия: Оценки перестают быть эффективными => увеличивается дисперсия оценок, которая снижает вероятность получения максимально точных оценок. Выводы на основании t и F будут ненадежными.
    Тест Бройша-Годфри является одним из методов для выявления автокорреляции в остатках модели регрессии. Он основан на сравнении суммы квадратов автокорреляций остатков модели с теоретическими значениями, которые могут быть получены при условии независимости остатков.

    Для применения теста Бройша-Годфри необходимо выполнить следующие шаги:
    1. Оценить модель регрессии и получить остатки.
    2. Проверить наличие автокорреляции в остатках с помощью графика автокорреляционной функции (ACF) и частной автокорреляционной функции (PACF).
    3. Вычислить статистику теста Бройша-Годфри:
    BG = n * R^2
    где n - количество наблюдений, R^2 - коэффициент детерминации модели регрессии.
    4. Сравнить значение статистики BG с критическим значением из таблицы распределения хи-квадрат с числом степеней свободы, равным количеству лагов автокорреляции.
    Если значение статистики BG превышает критическое значение, то нулевая гипотеза о независимости остатков отвергается, что свидетельствует о наличии автокорреляции в остатках.
    Однако, при применении теста Бройша-Годфри необходимо учитывать особенности его применения. В частности, тест может быть чувствителен к выбору лагов автокорреляции, поэтому необходимо проводить несколько тестов с разным числом лагов. Также, тест может давать ложноположительные результаты при наличии других форм зависимости между переменными, например, при наличии гетероскедастичности. Поэтому, при использовании теста Бройша-Годфри необходимо учитывать все особенности и проводить комплексный анализ данных.
    $$$Вопрос 12 --- Автокорреляция: определение, причины, последствия. H – тест и особенности его применения ---
    Автокорреляция - это явление, когда значения ошибок модели регрессии коррелируют между собой. Например:  если ошибка в одной точке времени положительна, то вероятность того, что ошибка в следующей точке времени тоже будет положительной, выше, чем если бы ошибки были независимыми.
    Причины автокорреляции могут быть различными, например, это может быть связано с неправильным выбором функциональной формы модели, неучтенными факторами, которые влияют на зависимую переменную, или с ошибками в данных.
    Последствия: Оценки перестают быть эффективными => увеличивается дисперсия оценок, которая снижает вероятность получения максимально точных оценок. Выводы на основании t и F будут ненадежными
    Следует отметить, что критерий Дарбина-Уотсона имеет два недостатка: он пригоден для выявления автокорреляции только соседних уровней ряда, а также неприменим для регрессионных моделей, содержащих в составе объясняющих переменных зависимую переменную с временным лагом в один момент времени у_(t-1), то есть для авторегрессионных моделей.
    Для авторегрессионных моделей разработаны специальные тесты обнаружения
    автокорреляции, в частности h-статистика Дарбина, которая определяется по формуле:
    h = c^^*sqrt(n / (1-D_(b_(y_(t-1))))) (поясняю, c^^-с с крышечкой), где = 1-0,5*d - оценка автокорреляции первого порядка.
    D_(b_(y_(t-1))) - выборочная дисперсия коэффициента регрессии при лаговой переменной y_(t-1) (квадрат стандартной ошибки параметра (m^2__(b_(y_(t-1)) при переменной у), n- число наблюдений.
    Полученное значение h-статистики сравнивается с критической точкой u_(alpha/2). Если | h|> u_(alpha/2), то наличие автокорреляции подтверждается. Основная проблема с использованием этого теста заключается в невозможности вычисления h при n* D_(b_(y_(t-1))) >1.
    $$$Вопрос 13 --- Автокорреляция: определение, причины, последствия. Метод рядов Сведа-Эйзенхарта и особенности его применения ---
    Автокорреляция - это явление, когда значения ошибок модели регрессии коррелируют между собой. Например:  если ошибка в одной точке времени положительна, то вероятность того, что ошибка в следующей точке времени тоже будет положительной, выше, чем если бы ошибки были независимыми.
    Причины автокорреляции могут быть различными, например, это может быть связано с неправильным выбором функциональной формы модели, неучтенными факторами, которые влияют на зависимую переменную, или с ошибками в данных.
    Последствия: Оценки перестают быть эффективными => увеличивается дисперсия оценок, которая снижает вероятность получения максимально точных оценок. Выводы на основании t и F будут ненадежными
    Ряд – непрерывная последовательность одинаковых знаков. Длина ряда – кол-во знаков в ряду
    n_1 – кол_во +, n_2 – кол_во -, k – кол-во рядов

    При достаточно большом числе наблюдений (n_1 >10 , n_2>10) случайная величина k имеет асимптотические нормальные распред
    M(k) = (2*n_1*n_2) / (n_1+n_2) + 1 
    Sig_k = (2*n_1*n_2*(2*n_1*n_2-n_1-n_2)) / ((n_1+n_2)^2*(n_1+n_2-1))
    Если M_k – u_(alpha/2)*D_k<=k<= M_k + u_(alpha/2)*D_k, то гипотеза об отсутствии автокорреляции отклоняется, те автокорр есть 
    Особенностью применения метода рядов Сведа-Эйзенхарта является то, что он не требует предположения о распределении данных и может быть использован для любых типов данных. Однако он чувствителен к выбросам и может давать неправильные результаты, если выборки имеют разную дисперсию. Поэтому перед применением метода рядов Сведа-Эйзенхарта необходимо провести анализ выбросов и проверить равенство дисперсий в выборках
    $$$Вопрос 14 --- Модель с автокорреляцией случайного возмущения. Оценка моделей с авторегрессией ---
    Автокорреляция — статистическая взаимосвязь между последовательностями величин одного ряда. Чтобы посчитать автокорреляцию, используется корреляция между временным рядом и её сдвинутой копией от величины временного сдвига. Сдвиг ряда называется лагом.
    AR (авторегрессия) - это компонента модели ARMA и ARIMA, которая описывает зависимость текущего значения временного ряда от его предыдущих значений. Порядок модели AR(p) определяет количество предыдущих значений, которые учитываются при расчете текущего значения.
    Коэффициенты авторегрессии (AR-коэффициенты) описывают, как сильно каждый предыдущий элемент влияет на текущее значение временного ряда. Чем больше порядок модели, тем больше коэффициентов авторегрессии нужно определить.
    Модели с авторегрессией (AR) используются для прогнозирования временных рядов, где значения в текущий момент времени зависят от значений в предыдущие моменты времени. Оценка таких моделей включает в себя следующие шаги:
    1. Выбор порядка модели: порядок модели AR определяет, сколько предыдущих значений временного ряда будет использоваться для прогнозирования текущего значения. Порядок модели может быть выбран на основе статистических тестов и анализа автокорреляционной функции.
    2. Оценка коэффициентов модели: после выбора порядка модели, коэффициенты модели AR могут быть оценены с помощью метода наименьших квадратов или метода максимального правдоподобия.
    3. Проверка адекватности модели: проверка адекватности модели включает в себя анализ остатков модели, чтобы убедиться, что они не содержат систематических ошибок и случайны.
    4. Прогнозирование: после оценки модели и проверки ее адекватности, можно использовать ее для прогнозирования будущих значений временного ряда.
    Оценка моделей с авторегрессией является важным инструментом для анализа временных рядов и прогнозирования будущих значений. в данных перед ее применением.
    $$$Вопрос 15 --- Процедура Кохрейна-Оркатта ---
    Это итерационная процедура. Алгоритм:
    1.Оцениваем исходную регрессию Y_t = b_1+b_2*X_t+u_t
    2.Сохраняем остатки e_t=Y_t-Y^^_t, t=1…T (поясняю, Y^^ - это Y с крыш)
    3.В кач первого приближения параметра р берем МНК оценку регрессии e_t = p*e_(t-1)+eps_t (нет константы!)
    4.Замена Y^*_t = Y_t – p*Y_(t-1); X^*_t=X_t-p*X_(t-1)    (4)
    Эта замена возможна для t = 2..T
    Тогда формально мы перейдем к уже известной нам спецификации мод лин рег: Y^*_t=b_1+b_2*X^*_t+eps_t     (5)
    5.Проводим преобразование переменных по формулам (4) и, если необходимо, восстанавливаем первое наблюдение с помощью поправки Прайса-Уинстона
    6.Оцениваем рег (5). Находим остатки и повторяем процедуру, пока не удовлетворим неравенству abs(p_i – p_(i+1)) < alpha, alpha > 0. Alpha задается заранее
    7.В кач оценки параметра авторегрессии берем последнее значение p^^_(i+1)
    Если процедура не будет сходиться, то это намек на наличие автокорреляции более высокого порядка
    $$$Вопрос 16 --- Процедура Хилдрета – Лу ---
    1.Y^*_t = Y_t – p*Y_(t-1); X^*_t=X_t-p*X_(t-1)    (4)
    Эта замена возможна для t = 2..T
    Тогда формально мы перейдем к уже известной нам спецификации мод лин рег: Y^*_t=b_1+b_2*X^*_t+eps_t     (5)
    2.Все значения параметра авторегрессии р лежат от -1 до 1
    Следовательно, идея состоит в том, чтобы их этого интервала с небольшим шагом выбирать различные значения и оценивать для каждого из них регрессию
    При этом следим за суммой квадратов остатков RSS. В качестве р берет то его значение, для которого RSS мин
    По сути перебор
    $$$Вопрос 17 --- Оценка влияния факторов, включенных в модель. Коэффициент эластичности, Бета-коэффициент, Дельта – коэффициент ---
    Коэффициент эластичности показывает, насколько процентное изменение зависимой переменной связано с процентным изменением одной из независимых переменных. Если коэффициент эластичности больше единицы, то изменение одной переменной приведет к более значительному изменению зависимой переменной. Если коэффициент эластичности меньше единицы, то изменение одной переменной приведет к менее значительному изменению зависимой переменной.
    Средний коэфф эласт : Э^-_j=y’(x^-_j)*(x^-_j)/(y^-)   (символ^-  это символ с чертой сверху)
    Бета-коэффициент показывает, как изменение одной независимой переменной влияет на зависимую переменную при учете влияния других независимых переменных. Бета-коэффициенты могут быть использованы для сравнения влияния различных независимых переменных на зависимую переменную.
    betta^-_j=betta^^_j*(S_(x_(x_ij)))/(S_(y_i))  (betta^^ - betta с крышечкой)
    Дельта-коэффициент показывает, насколько изменение одной независимой переменной влияет на зависимую переменную при фиксированных значениях других независимых переменных. Дельта-коэффициенты могут быть использованы для оценки влияния изменения конкретной переменной на зависимую переменную при условии, что все остальные переменные остаются неизменными
    delta_j = r_(y_i,x_ij)*(betta^^_j)/(R^2)
    $$$Вопрос 18 --- Мультиколлинеарность: понятие, причины и последствия ---
    Мультиколлинеарность – связь между объясняющими (независимыми) переменными.
    Виды:
    · Строгая, совершенная
    · Нестрогая, несовершенная
    Причины
    Наличие мультиколлинеарности в экономических данных обусловлено причин-следственной закономерностью, наличию транзитивности.
    Последствия
    · Большие дисперсия в оценках, расширение интервальных оценок
    · Оценки перестают быть самостоятельными
    · Уменьшается t-статистика
    · Затрудняется оценка вклада каждой экзогенной переменной в 
    дисперсию
    · Неправильные знаки коэффициентов регрессии
    $$$Вопрос 19 --- Выявление мультиколлинеарности: коэффициент увеличения дисперсии (VIF –тест) ---
    VIF-тест используется для определения наличия мультиколлинеарности между независимыми переменными в модели. Он рассчитывает коэффициент увеличения дисперсии для каждой независимой переменной, который показывает, насколько сильно она коррелирует с другими независимыми переменными в модели. Если VIF-значение больше 10, то это может указывать на наличие мультиколлинеарности, что может привести к неправильным оценкам коэффициентов регрессии и ухудшению качества модели.
    Строится регрессия для каждого j-ого регрессора
    x1 = f(x2,X3, …), берем R^2 … xn = f(x1, x2, …), берем R^2
    VIF_i =1 / (1 – R^2_j)
    Если VIF > 10, то сильно коррелируют
    $$$Вопрос 20 --- Выявление мультиколлинеарности: Алгоритм Фаррара-Глобера ---
    Алгоритм Фаррара-Глобера является методом для выявления мультиколлинеарности в модели. Он основан на рассмотрении корреляционной матрицы между независимыми переменными
    Алгоритм Фаррара-Глобера выявления мультиколлинеарности
    1. Находим корреляционную матрицу и её определитель
    2. Вычисляем наблюдаемое значение статистики
    FG_набл = -[ n - 1 – 1/6*(2k + 5) ]ln(det[R])
    3. Находим табличное значение статистики Хи-квадрат
    Хи^2(alpha,1/2*k*(k - 1))
    4. Если FG_набл >= Хи^2, то мультиколлинеарность существует


    $$$Вопрос 21 --- Построение гребневой регрессии. Суть регуляризации ---
    Гребневая регрессия (ridge regression) - это метод линейной регрессии, который использует регуляризацию для уменьшения влияния мультиколлинеарности в данных. 
    Мультиколлинеарность - это явление, когда два или более признака в модели сильно коррелируют друг с другом, что может привести к переоценке весов признаков и неправильному прогнозированию. Гребневая регрессия решает эту проблему, добавляя к функции потерь штрафной член, который ограничивает значения весов признаков.
    Матрица X^T*X близка к вырожденной, поэтому можно искусственно улучшить обусловленность данной матрицы.
    X^T*X + tilda*L, где tilda (пишется, как маленькая русская т, только крышечка волнистая)- некоторый коэффициент, L - диагональная матрица из элементов главной диагонали Х^T*Х
    Оценки коэффициентов, полученные данным способом, будут состоятельными, но смещёнными.
    Смещение тем больше, чем больше tilda
    B = [(X^T*X + tilda*L)^(-1)] * X^T*X
    Для начала берем tilda = 1/100 постепенно увеличиваем, пока коэффициент регрессии не
    стабилизируется. Обычно тtilda принад [0.1; 0.5]

    Суть регуляризации заключается в добавлении штрафа за большие значения коэффициентов, чтобы уменьшить их влияние на модель. Параметр регуляризации lambda позволяет настраивать величину штрафа: при lambda =0 гребневая регрессия эквивалентна обычной линейной регрессии, а при lambda стрем к беск все коэффициенты стремятся к нулю.
    $$$Вопрос 22 --- Алгоритм пошаговой регрессии---
    Пошаговая регрессия (отбор наиболее информативных признаков в модель)
    Абсолютно надёжным методом поиска наилучшего состава регрессоров из списка является перебор всех возможных комбинаций. Существует несколько вариантов направленности алгоритма
    1. Включения (каждую итерацию включается по одному фактору)
    2. Исключения (каждую итерацию исключается факторы)
    3. Двунаправленный (сочетание 1 и 2 методов)
    Целевой функцией для оптимизации является R^2 всей модели и t-статистика для каждого из факторов
    $$$Вопрос 23 --- Метод главных компонент (PCA) как радикальный метод борьбы с мультиколлинеарностью ---
        Метод главных компонент (PCA) является еще одним методом борьбы с мультиколлинеарностью. Он используется для уменьшения размерности данных путем проекции на новые оси, называемые главными компонентами, которые объясняют наибольшую дисперсию в данных.
    В контексте линейной регрессии, PCA может быть использован для уменьшения количества признаков в модели и уменьшения мультиколлинеарности. После проекции данных на главные компоненты, новые признаки могут быть использованы в качестве входных данных для линейной регрессии.
    Однако, PCA также имеет свои ограничения. Он может быть менее интерпретируемым, чем гребневая регрессия, и может потерять некоторую информацию при проекции данных на новые оси. Кроме того, он также требует настройки параметров, таких как количество главных компонент, которые должны быть использованы.
    Алгоритм Метод главных компонент (PCA)
    1. Стандартизация данных: вычитаем из каждого признака его среднее значение и делим на стандартное отклонение.
    2. Вычисление ковариационной матрицы: находим ковариационную матрицу для стандартизированных данных.
    3. Вычисление главных компонент: находим собственные векторы и собственные значения ковариационной матрицы.
    4. Сортировка главных компонент: сортируем главные компоненты по убыванию их собственных значений.
    5. Выбор количества главных компонент: выбираем количество главных компонент, которые будут использоваться в модели, на основе объясненной дисперсии.
    6. Проекция данных на новые оси: проецируем стандартизированные данные на выбранные главные компоненты.
    7. Использование новых признаков: используем новые признаки в качестве входных данных для линейной регрессии или других алгоритмов машинного обучения.
    $$$Вопрос 24 --- Фиктивная переменная и правило её использования ---
    Фиктивные (искусственные) переменные - позволяют в регрессионных моделях учесть влияние качественных переменных. Фиктивные переменные (ФП) — это переменные бинарного типа "0-1" (индикатор изучаемого признака): d_t = 0 – отсутствие признака в наблюдении t,1 – присутствие 
    Значение d_t = 0 называется базовым (сравнительным), его выбор определяется целями исследования, или принимается произвольно. Фиктивная переменная может быть также индикатором принадлежности наблюдения к некоторой подвыборке.
    Правила использования фиктивной переменной: если модель принимает k альтернативных значений, то в модель включают k-1 переменную.В регрессионных моделях применяются фиктивные переменные двух типов: переменные сдвига и переменные наклона.
    Переменные наклона: Пример спецификации регрессионной модели с фиктивной переменной наклона: Y_t =a+b*X_t + c*d_t*X_t+eps_t, t =1…n, где a,b,c- параметры модели, X_t – значение «непрерывного» регрессора в наблюдении t, d_t - значение «бинарного» регрессора в наблюдении t.
    Фиктивная переменная входит в уравнение в мультипликативной форме.
    Переменные сдвига: Пример спецификации регрессионной модели с фиктивной переменной сдвига:
    Y_t =a+b*X_t + c*d_t+eps_t где а,b,c - параметры модели, t =1,…, n, X_t, - значение «непрерывного»
    регрессора в наблюдении t, d_t -  значение «бинарного» регрессора в наблюдении t.

    Фиктивная переменная сдвига - это переменная, которая меняет точку пересечения линии регрессии с осью ординат в случае применения качественной переменной. Фиктивная переменная наклона - это та переменная, которая изменяет наклон линии регрессии в случае использования качественной переменной
    $$$Вопрос 25 --- Модель дисперсионного анализа ---
    Модель дисперсионного анализа (ANOVA) - модель, где все экзогенные переменные факторные
    E(y|D) = betta_0+ gamma*D + eps
    Значимость gamma проверяется с помощью t-статистики Стьюдента
    Данные модели являются кусочно-постоянными функциями
    Являются скудными по информативности и крайне редко используются в эконометрическом анализе
    $$$Вопрос 26 --- Модель ковариационного анализа ---
    ANCOVA (англ. Analysis of Covariance) – это расширенная модель ковариационного анализа, которая позволяет учитывать влияние как категориальных, так и количественных факторов на зависимую переменную. 
    В ANCOVA используется анализ дисперсии, чтобы проверить статистическую значимость различий между группами по зависимой переменной, а также учитывается влияние других факторов на зависимую переменную. 
    Дополнительно в ANCOVA проводится анализ ковариации, который позволяет оценить влияние некоторых переменных на зависимую переменную, при этом контролируя влияние других переменных.
    Модель ковариационного анализа (ANCOVA) - модель, в которой экзогенные переменные представлены как количественными, так и качественными факторами E(y|D) = betta_0 + betta_1*x + gamma*D + eps
    $$$Вопрос 27 --- Фиктивные переменные в сезонном анализе ---
    Сезонность - это регулярные повторяющиеся колебания в данных, связанные с временными факторами, такими как месяцы, кварталы или годы. Например, продажи леденцов могут быть выше в летние месяцы и ниже в зимние, что связано со сменой сезонов. Фиктивные переменные часто используются для устранения сезонного фактора. Для учета n - сезонов используется n-1 факÍтор
    Например, для 4 времен года (зима, весна, лето, осень) модель будет выглядеть следующим образом
    E(ylx,D1,D2,D3) = betta_0 + betta_1 + gamma_1* D_1 + gamma_2* D_2 + gamma_3* D_3 + eps; D1 – зима, D2 – весна, D3 - лето
    $$$Вопрос 28 --- Фиктивная переменная сдвига: спецификация регрессионной модели с фиктивной переменной сдвига; экономический смысл параметра при фиктивной переменной; смысл названия ---
    Фиктивная переменная сдвига оказывает влияние на точку пересечения линии регрессии и оси OY.
    Спецификация: E(Y|D,X) = betta_0 + betta_1*X + gamma*D + eps
    График: оси х и у. две параллельные прямые. Показан сдвиг по оу. Расстояние между прямыми = gamma
    Часто используются при построении изменяющихся в динамике моделей, когда в разные периоды
    времени может действовать и не действовать признак (цикличные модели)

    $$$Вопрос 29 --- Фиктивная переменная наклона: спецификация регрессионной модели с фиктивной переменной наклона; экономический смысл параметра при фиктивной переменной; смысл названия ---
    Фиктивная переменная наклона оказывает влияние на наклон линии регрессии. В результате
    получаем кусочно-линейную функцию. Спецификация: y_t = betta_0 + betta_1*x_t + gamma*D_t*x + eps_t
    На графике можно показать, две прямые с разными углами наклона
    В экономике часто отображает изменения в различных экономических процессах (налоги, курсы
    валют, политические факторы)
    $$$Вопрос 30 --- Определение структурных изменений в экономике: использование фиктивных переменных, тест Чоу ---
    Структурные изменения в экономике - это изменения в составе и структуре производства, потребления, трудовых ресурсов и других экономических факторов, которые приводят к изменению характеристик экономики в целом. Такие изменения могут быть вызваны различными факторами, включая технологические инновации, изменения в потребительском поведении, демографические изменения, изменения в политической и экономической среде и другие факторы. Определение структурных изменений в экономике позволяет анализировать их последствия для различных секторов экономики и разрабатывать стратегии для адаптации к новым условиям.
    Для проверки значимости структурных изменений в спецификацию регресссионной модели включают фиктивные переменные сдвига и наклона Y_t = B_0 + B_1* X_t + sig_1* d_t + sig_2* d_t* X_t + eps_t,
    с индикатором d_t = система(0, t<=t_0 – до структурных изменений; 1, t>t_0 – после структур ищменений) - бинарная переменная; t_o - точка структурных изменений.
    остатков модели, оцененной по подвыборкам, которые формируютются с учетом предположений о структурных изменениях. Объемы подвыборок – n_1 и n_2, причем n = n_1 + n_2. Равенство ESS_0 = ESS_1+ ESS_2 возможно только в случае совпадения оценок параметров B^(i), i = 0, 1, 2, всех трех регрессий H_0 : = B^(0) = B^(1) = B^(2)
    v2 = (n_1- k) + (n_2 - k) = n - 2k, v_1 = {n - k - [(n_1 - k) + (n_2 - k)]} = k.	
    Сравнение вычисленного значения статистики с критическим F_кр(v_1,v_2), определенным для уровня значимости а, позволяет проверить нулевую гипотезу, и если F_чоу <F_кр, то нулевая гипотеза не отклоняется, и структурные изменения незначимо влияют на эндогенную переменную модели, нет оснований для разбиения выборки на две части.
    Статистика Чоу предназначена для проверки устойчивости модели к структурным изменениям на всем интервале исследования. Ее модификация F_(Чоу_f) = [(ESS_0 – ESS_1) /(n – n_1)] /[ESS_1/(n_1-k)]~F(n – n_1,n - k)позволяет сравнить качество прогнозов, полученных по всем выбор точным данным и данным до структурных изменений.
    $$$Вопрос 31 --- Модели бинарного выбора. Недостатки линейной модели ---
    Модели бинарного выбора являются статистическими моделями, которые используются для анализа ситуаций, когда наблюдается два возможных исхода. Они широко применяются в экономике, маркетинге, социологии и других областях, где необходимо прогнозировать вероятность выбора одного из двух вариантов.
    Недостатки линейной модели заключаются в том, что она предполагает линейную зависимость между зависимой и независимыми переменными. Однако в реальной жизни часто наблюдаются нелинейные связи между переменными, что может привести к неточным прогнозам и ошибкам в анализе данных. Кроме того, линейная модель не учитывает возможные взаимодействия между переменными, что также может привести к неточным результатам.
    В отличие от линейной модели, модели бинарного выбора позволяют учитывать нелинейные связи между переменными и возможные взаимодействия между ними. Они также позволяют оценивать вероятность выбора каждого из двух вариантов и прогнозировать результаты в различных ситуациях. Однако эти модели также имеют свои недостатки, такие как сложность оценки параметров и интерпретации результатов.
    Одной из наиболее распространенных моделей бинарного выбора является логит-модель. Она используется для анализа ситуаций, когда наблюдается два возможных исхода, например, когда человек решает купить или не купить продукт.
    $$$Вопрос 32 --- Модели множественного выбора: модели с неупорядоченными альтернативными вариантами ---
    Модели с неупорядоченными альтернативными вариантами, также известные как модели множественного выбора с ограниченной зависимой переменной, предполагают, что каждая альтернатива имеет свою уникальную наблюдаемую характеристику, которая влияет на вероятность ее выбора. Например, при анализе предпочтений потребителей, каждый продукт может иметь свою уникальную цену, качество и другие характеристики, которые влияют на вероятность его выбора.
    В них предполагается, что наблюдаемое значение выбора t-м индивидуумом j-го варианта (y_t=j) связывается со значениями факторов, сопутствующих его выбору, эконометрическим уравнением следующего вида: y_t=h(a, z_tj)+e_tj, где h – функция, отражающая характер влияния факторов на выбор t-м индивидуумом j-го варианта; e_tj - ошибка модели; а - вектор параметров модели; z_tj- вектор независимых переменных -значений факторов, влияющих на выбор его индивидуума, которые могут характеризовать самого индивидуума, альтернативный вариант, либо и то и другое одновременно. 
    Функция логита выбора для модели с неупорядоченными альтернативными вариантами выглядит следующим образом:
    P(i) = exp(Vi) / ∑j exp(Vj), где P(i) - вероятность выбора i-го варианта, Vi - общая оценка i-го варианта, ∑j exp(Vj) - сумма всех экспонент оценок всех вариантов.
    $$$Вопрос 33 --- Модели множественного выбора: модели с упорядоченными альтернативными вариантами ---
    Модели множественного выбора с упорядоченными альтернативными вариантами используются для анализа поведения потребителей при выборе товаров или услуг, которые имеют определенные характеристики. Эти модели предполагают, что потребитель оценивает каждый альтернативный вариант по некоторой шкале и выбирает тот вариант, который наиболее удовлетворяет его предпочтениям.
    Одной из наиболее распространенных моделей множественного выбора с упорядоченными альтернативными вариантами является модель логита порядка. В этой модели потребитель оценивает каждый альтернативный вариант по некоторой шкале, которая может быть непрерывной или дискретной. Затем эти оценки преобразуются в вероятности выбора каждого варианта с помощью функции логита порядка.
    Пример. Состояние здоровья. Варианты ответов:1 – fair, 2 – good, 3- excellent
    Y_i = 1,2, ...,m
    Y^*_i = x’_i*betta+eps_i, Y_i = j, если c_(j-1)<Y^*_i<c_j, j=1…m
    с_0 = -беск … c_m = беск
    Р(Y_i = j) = F(c_j- x’_i*betta) – F(c_(j-1) – x’_i*betta),
    L = П(m, j=1)П(i:Y_i=j)(F(c_j-x’_i*betta)-F(c_(j-1)-x’_i*betta))->max (снизу подписать betta, c)
    Оценка параметров с помощью метода максимальногоправдоподобия
    $$$Вопрос 34 --- Модели множественного выбора: гнездовые logit-модели ---
    Для гнездовой logit-модели безусловную вероятность выбора j-го варианта и l -й группы можно представить как произведение условной вероятности выбора j-го варианта при условии, что была выбрана l-я группа, и безусловной вероятности выбора l-й группы.
    Заметим, что внутри группы ошибки гомоскедастичны. Специфика гнездовой logit-модели, ее отличие от условной logit-модели, состоит в подходе к определению вероятности выбора I-й группы. Для того чтобы раскрыть эту специфику, введем переменную I_l (ай с индеком эл), характеризующую "ценность" l-й группы. В гнездовой logit-модели "ценность" l-й группы рассматривается как дополнительный фактор, влияющий на выбор этой группы, т. е. вероятность выбора 1-й группы определяется следующим образом:
    P_l = (e^(gamma’*z_i+tilda_l*I_l)) / (sum(L, I=l)(gamma\*z_l+tilda_l*I_l)). Параметр tilda_l-параметр, который и отличает гнезд логит модель от условной логит мод. В последней он принимает значений =1. 
    В гнездовой logit-модели значение параметра tilda_l оценивается вместе с параметрами gamma.
    Качество оценок, получаемых на основе гнездовой logit-модели, во многом определяется правильностью построения дерева альтернативных вариантов. Отметим, что на практике достаточно трудно оценить, соответствует ли выбранная структура такого дерева исходным условиям модели, состоящих в постулировании определенных допущений относительно дисперсий ошибок (постоянство дисперсий ошибок внутри группы и различие дисперсий в разных группах).
    $$$Вопрос 35 --- Модели счетных данных (отрицательная биномиальная модель, hurdle-model) ---
    В практических исследованиях достаточно часто приходится сталкиваться с зависимыми переменными, которые представляют собой результаты подсчетов. Примерами таких переменных являются число выданных за год патентов, количество выпускников вузов, число аварий на судах и т. д. Эконометрическая модель в этом случае связывает количество произошедших событий (у) с факторами, характеризующими условия, сопровождавшие эти события.
    Отрицательная биномиальная модель (Negative Binomial Model) – это статистическая модель, которая используется для описания счетных данных, где среднее значение и дисперсия не равны друг другу. Вид отрицательной биномиальной модели можно представить следующим образом:
    P(Y=k) = (k+r-1)C(r-1) * p^r * (1-p)^k-r+1
    где Y – случайная величина, описывающая количество событий до достижения заданного числа неудач, k – количество событий, r – параметр формы (shape parameter), p – вероятность успеха в каждом событии, C – биномиальный коэффициент.
    В отличие от обычной биномиальной модели, где дисперсия равна среднему значению, в отрицательной биномиальной модели дисперсия больше среднего значения, что позволяет учитывать различия в дисперсии в данных.
    Hurdle-model – это статистическая модель, которая используется для анализа счетных данных с избытком нулей. В отличие от отрицательной биномиальной модели, где учитывается только дисперсия, в Hurdle-model учитывается и вероятность нулевых значений. Модель состоит из двух частей: первая часть – это бинарная модель, которая определяет вероятность нулевых значений, вторая часть – это отрицательная биномиальная модель, которая описывает количество событий при условии, что они не являются нулевыми.
    Вид Hurdle-model можно представить следующим образом:
    P(Y=0) = exp(-λ)
    P(Y=k) = (1-exp(-λ)) * (λ/(λ+k))^k
    где Y – случайная величина, описывающая количество событий до достижения заданного числа неудач, λ – параметр интенсивности
    Hurdle-model широко используется в экономике, медицине, социологии и других областях для анализа счетных данных с избытком нулей, например, для анализа количества посещений врача или количества аварий на дорогах.
    $$$Вопрос 36 --- Модели усеченных выборок ---
    Усечённая регрессия — модель регрессии в условиях, когда выборка осуществляется только из тех наблюдений, которые удовлетворяют априорным ограничениям, которые обычно формулируются как ограничение снизу и (или) сверху зависимой переменной. Урезание выборки приводит к смещенности МНК -оценок, поэтому оцениваются такие модели с помощью метода максимального правдоподобия.
    Используют различные модели усеченных выборок, такие как: 1. Модель Тобита - это модель, которая используется для анализа усеченных выборок с нормальным распределением. 2. Модель Heckman - это модель, которая используется для анализа усеченных выборок с неслучайным отбором.3. Модель логит-усечения - это модель, которая используется для анализа усеченных выборок с бинарными переменными. 4. Модель экспоненциальной регрессии - это модель, которая используется для анализа усеченных выборок с экспоненциальным распределением. 
    Мат описание: Пусть y удовлетворяет обычной лин рег мод y_t = x^T_t*b+eps_t, но в выборку попадают только те данные, для которых y_min <= y_t <= y_max
    Если урезание только снизу, то макс порог равен бесконечности, если только сверху – то нижний порог равен минус беск.
    $$$Вопрос 37 --- Модели цензурированных выборок (tobit-модель) ---
    Tobit-модель является одним из методов анализа цензурированных данных. Она используется для оценки параметров регрессионной модели, когда наблюдения могут быть цензурированы сверху или снизу.
    Цензурирование сверху означает, что значения переменной зависимой переменной ограничены сверху некоторым значением, которое не может быть измерено. Например, мы исследуем уровень дохода среди жителей города. Однако, некоторые люди могут не хотеть сообщать свой точный доход или его значение может быть ограничено по каким-то причинам (например, максимальная зарплата в организации). В этом случае, выборка данных будет цензурированной, так как некоторые значения дохода будут неизвестными или ограниченными сверху. 
    Tobit-модель описывает зависимость между переменной зависимой переменной и набором объясняющих переменных. Она учитывает цензурирование выборки и позволяет оценить параметры регрессии, учитывая ограничения на значения переменной зависимой переменной.
    Основная идея Tobit-модели заключается в том, что зависимая переменная Y может быть разделена на две компоненты: наблюдаемую Y* и не наблюдаемую U. Если Y* > 0, то Y = Y*, иначе Y = 0. Таким образом, Tobit-модель описывает зависимость между Y* и объясняющими переменными. Y^*_t = X’_t*betta + u_t, t = 1..T
    Оценка параметров модели производится с использованием метода максимального правдоподобия. Tobit-модель может быть расширена для учета нескольких источников цензурирования и для моделирования зависимости между цензурированными значениями и объясняющими переменными.
    Tobit-модель широко используется в эконометрике для анализа данных о доходах, расходах, продажах и других переменных, которые могут быть цензурированы.
    $$$Вопрос 38 --- Модели случайно усеченных выборок (selection model) ---
    Модель случайно усеченных выборок (selection model) используется для анализа данных, когда выборка наблюдений не является полной из-за наличия усечения (truncation). Усечение может быть двух типов: снизу (left truncation), когда наблюдения, у которых значение переменной меньше определенного порога, не включаются в выборку, и сверху (right truncation), когда наблюдения, у которых значение переменной больше определенного порога, не включаются в выборку.
    Модель случайно усеченных выборок предполагает, что вероятность усечения зависит от значений переменных и может быть описана функцией распределения. Для оценки параметров модели используются методы максимального правдоподобия или методы байесовской статистики.
    Методы оценки параметров модели случайно усеченных выборок могут быть различными, в зависимости от выбранного подхода. Например, при использовании метода максимального правдоподобия параметры модели оцениваются путем максимизации функции правдоподобия, которая учитывает как наблюдаемые данные, так и информацию об усечении выборки.
    $$$Вопрос 39 --- Логит-модель. Этапы оценки. Области применения ---
    Логит-модель – это статистическая модель, используемая для анализа зависимости бинарной переменной от набора объясняющих переменных. Бинарная переменная принимает только два значения, например, 0 или 1, женщина или мужчина, выжил или не выжил и т.д. Логит-модель позволяет оценить вероятность наступления события (например, выживания) в зависимости от значений объясняющих переменных (например, возраст, пол, класс билета и т.д.).

    Вероятность наступления события в логит-модели описывается функцией: p_i=F(z_i)=1/(1+e^(-(betta_1+betta_2*x_i))). z_i – лин комб незав факторов 
    Предельное воздействие величины z на вероятность есть производная функции вероятности: f(z) = dp/dz=(e^(-z))/((1+e^(-z))^2)
    Этапы оценки логит-модели:
    1. Сбор данных и выбор объясняющих переменных.
    2. Спецификация модели – выбор функциональной формы зависимости между бинарной переменной и объясняющими переменными.
    3. Оценка параметров модели – используя метод максимального правдоподобия.
    4. Проверка качества модели – анализ остатков, проверка наличия взаимосвязи между остатками и объясняющими переменными.
    5. Применение модели – использование модели для прогнозирования вероятности наступления события на новых данных.
    Области применения логит-модели:
    - Медицинская статистика (например, прогнозирование вероятности заболевания в зависимости от возраста, пола, образа жизни и т.д.).
    - Маркетинговые исследования (например, прогнозирование вероятности покупки товара в зависимости от цены, бренда, рекламы и т.д.).
    - Социологические исследования (например, прогнозирование вероятности голосования за определенного кандидата в зависимости от политических взглядов, образования, дохода и т.д.).
    $$$Вопрос 40 --- Пробит-модель. Этапы оценки. Области применения ---
    Пробит-модель – это статистическая модель, используемая для анализа зависимости бинарной переменной от набора объясняющих переменных. Она также позволяет оценить вероятность наступления события в зависимости от значений объясняющих переменных, но использует другую функциональную форму зависимости.
    Пробит-модель - альтернативная модель двоичного выбора. Для нее используется стандартное норм распр для моделирования зависимости F(Z). p_i = F(Z_i) – функция завиит от переменной Z, которая в свою очередь зависит от выбранных факторов: Z=betta_1 + betta_2*X_2 + betta_k*X_k
    Этапы оценки пробит-модели:
    1. Сбор данных и выбор объясняющих переменных.
    2. Спецификация модели – выбор функциональной формы зависимости между бинарной переменной и объясняющими переменными.
    3. Оценка параметров модели – используя метод максимального правдоподобия.
    4. Проверка качества модели – анализ остатков, проверка наличия взаимосвязи между остатками и объясняющими переменными.
    5. Применение модели – использование модели для прогнозирования вероятности наступления события на новых данных.
    Области применения пробит-модели:
    - Финансовая статистика (например, прогнозирование вероятности дефолта компании в зависимости от финансовых показателей).
    - Экономические исследования (например, прогнозирование вероятности безработицы в зависимости от макроэкономических показателей).
    - Экологические исследования (например, прогнозирование вероятности появления определенного вида животных в зависимости от климатических условий и других факторов).
    - Исследования в области образования (например, прогнозирование вероятности успешной сдачи экзамена в зависимости от уровня образования и других факторов).
    $$$Вопрос 41 --- Метод максимального правдоподобия ---
    Меtтод максимаfльного правдоподобия— это метод оценивания неизвестного параметра путём максимизации функции правдоподобия в которой в качестве переменных рассматриваются искомые параметры. Еще раз подчеркнем тот факт, что в функции максимального правдоподобия значения У считаются фиксированными, а переменными являются параметры вектора Θ (дальше Tetta)
    Цель метода - найти такие значения параметров, при которых функция правдоподобия достигает максимума.
    f(Y_i)=f(Y_i, Tetta), L(Y, Tetta) = П(n, i=1)(f(Y_i, Tetta))
    Еще один вараинт записи функц правдоподобия:
    L(b) = П(Y_i=1)(F(b_0+b_1*X_1i+…+b_k*X_ki))*П(Y_i=0)(1- F(b_0+b_1*X_1i+…+b_k*X_ki))
    Часто для упрощения процесса нахождения неизвестных параметров функцию правдоподобия логарифмируют, получая логарифмическую функцию правдоподобия 
    Дальнейшее решение по ММП предполагает нахождение таких значений Θ, при которых функция правдоподобия (или ее логарифм) достигает максимума. Найденные значения Θ; называют оценкой максимального правдоподобия. 
    Оценки параметров, полученные с использованием ММП, являются:
     – состоятельными, т.е. с увеличением объема наблюдений разница между оценкой и фактическим значением параметра приближается к нулю;
     – инвариантными: В частности, если с помощью ММП мы оценили величину дисперсии какого-либо показателя (af), то корень из полученной оценки будет оценкой среднего квадратического отклонения (σ,), полученной по ММП.
     – асимптотически эффективными;
     – асимптотически нормально распределенными.
    $$$Вопрос 42 --- Свойства оценок метода максимального правдоподобия ---
    Оценки, полученные методом максимального правдоподобия, обладают следующими свойствами:
    1. Асимптотическая несмещенность: при увеличении размера выборки оценки метода максимального правдоподобия стремятся к истинным значениям параметров модели.
    2. Эффективность: оценки метода максимального правдоподобия являются наиболее эффективными среди всех несмещенных оценок, то есть имеют наименьшую дисперсию.
    3. Состоятельность: при условии, что модель правильно специфицирована, оценки метода максимального правдоподобия сходятся к истинным значениям параметров при увеличении размера выборки.
    4. Инвариантность: оценки метода максимального правдоподобия инвариантны к преобразованию параметров модели, то есть при замене параметров на их функции оценки не меняются.
    5. Асимптотическая нормальность: при увеличении размера выборки оценки метода максимального правдоподобия асимптотически распределены нормально вокруг истинных значений параметров модели.
    6. Устойчивость: оценки метода максимального правдоподобия устойчивы к выбросам и наличию наблюдений с большими весами.
    $$$Вопрос 43 --- Информационная матрица и оценки стандартных ошибок для оценок параметров logit и probit моделей. Интерпретация коэффициентов в моделях бинарного выбора ---
    Информационная матрица - это матрица вторых производных логарифма функции правдоподобия  по параметрам модели. Она используется для вычисления оценок стандартных ошибок для оценок параметров методом максимального правдоподобия.
    Для логит и probit моделей, коэффициенты регрессии интерпретируются как изменение в логарифме шансов (log-odds) или в вероятности (probability) в зависимости от соответствующих значений предикторов.
    В логит модели, коэффициенты регрессии означают изменение в логарифме шансов (log-odds) при изменении значения предиктора на единицу. Например, если коэффициент равен 0.5, то увеличение значения предиктора на единицу приведет к увеличению логарифма шансов на 0.5.
    В probit модели, коэффициенты регрессии означают изменение в вероятности (probability) при изменении значения предиктора на единицу. Например, если коэффициент равен 0.5, то увеличение значения предиктора на единицу приведет к увеличению вероятности на 0.5.
    Оценки стандартных ошибок используются для проверки значимости коэффициентов и для построения доверительных интервалов для оценок параметров. Чем меньше ошибка, тем более точной является оценка параметра.
    $$$Вопрос 44 --- Мера качества аппроксимации и качества прогноза logit и probit моделей ---
    Для оценки качества аппроксимации и прогноза logit и probit моделей используются различные меры:
    Одной из наиболее распространенных мер является псевдо R-квадрат . Он показывает, насколько хорошо модель подходит к данным и может быть рассчитан для логит и probit моделей. Однако, следует отметить, что псевдо R-квадрат не является абсолютной мерой качества модели и не может быть использован для сравнения моделей, которые используют разные наборы предикторов.
    Другой мерой качества аппроксимации является AIC (Akaike Information Criterion. Критерий Акаике) - это статистический критерий, который используется для выбора наилучшей модели из нескольких альтернативных моделей. Он основан на принципе минимальной длины описания , который гласит, что наилучшая модель должна быть наиболее точной и при этом иметь наименьшее количество параметров.
    AIC вычисляется по формуле: AIC = 2k - 2ln(L), где k - количество параметров в модели, а L - максимальное значение функции правдоподобия для данной модели. Чем меньше значение AIC, тем лучше модель.
    Однако, следует отметить, что AIC не является абсолютной мерой качества модели и не может быть использован для сравнения моделей с разными наборами предикторов. Кроме того, AIC не учитывает размер выборки и может давать различные результаты при использовании разных методов оценки параметров.
    Байесовский информационный критерий Bayesian Information Criterion (BIC) - это статистический критерий, который используется для выбора наилучшей модели из нескольких альтернативных моделей. Он основан на принципе минимальной длины описания (minimum description length), который гласит, что наилучшая модель должна быть наиболее точной и при этом иметь наименьшее количество параметров.
    BIC вычисляется по формуле: BIC = kln(n) - 2ln(L), где k - количество параметров в модели, n - размер выборки, а L - максимальное значение функции правдоподобия (likelihood) для данной модели. Чем меньше значение BIC, тем лучше модель.
    BIC отличается от AIC тем, что он штрафует модели за большое количество параметров более сильно, чем AIC. Это связано с тем, что BIC базируется на более жестких предположениях о распределении параметров в модели
    $$$Вопрос 45 --- Временные ряды: определение, классификация, цель и задача моделирования временного ряда ---
    Временной ряд представляет собой последовательность наблюдений за определенным явлением во времени. Например, это может быть ежемесячная выручка компании, цена на акции, температура воздуха и т.д.
    Один из основных аспектов временного ряда - это его периодичность. Если временной ряд имеет явную периодичность, то его можно разделить на циклы, которые повторяются через определенные промежутки времени. Например, ежедневный временной ряд может иметь недельную или месячную периодичность.
    Другой важный аспект временного ряда - это его стационарность. Стационарность означает, что статистические свойства временного ряда не меняются со временем. Это означает, что среднее значение, дисперсия и корреляционная структура остаются постоянными на протяжении всего временного ряда. Если временной ряд не является стационарным, то его можно преобразовать, чтобы сделать его стационарным.
    Цель моделирования временного ряда - это прогнозирование будущих значений на основе прошлых данных. Для этого используются различные методы, такие как авторегрессионные модели, скользящие средние, ARIMA-модели и т.д. Задача моделирования временного ряда заключается в выборе наиболее подходящей модели для описания и прогнозирования временного ряда.
    Доп:
    Одним из основных методов моделирования временного ряда является ARIMA-модель. Она представляет собой комбинацию авторегрессионной модели (AR) и интегрированной модели скользящего среднего (MA). ARIMA-модель позволяет учитывать как периодичность, так и стационарность временного ряда.
    Другой метод моделирования временного ряда - это экспоненциальное сглаживание. Он используется для прогнозирования временных рядов с низкой периодичностью и нестационарностью. Экспоненциальное сглаживание представляет собой метод, который учитывает вес прошлых наблюдений в прогнозировании будущих значений
    $$$Вопрос 46 --- Исследование структуры одномерного временного ряда ---
    Исследование структуры одномерного временного ряда включает в себя анализ тренда, сезонности и случайной составляющей.
    Тренд представляет собой долгосрочное изменение уровня временного ряда. Он может быть возрастающим, убывающим или отсутствовать вовсе. Для анализа тренда можно использовать метод скользящей средней или экспоненциального сглаживания.
    Сезонность представляет собой периодические изменения уровня временного ряда, которые повторяются через определенные промежутки времени. Например, ежегодная сезонность может быть связана с изменением погодных условий или поведением потребителей в различные сезоны года. Для анализа сезонности можно использовать метод декомпозиции временного ряда на тренд, сезонность и случайную составляющую.
    Случайная составляющая представляет собой остаточную часть временного ряда, которая не может быть объяснена трендом или сезонностью. Она может содержать различные факторы, такие как шумы, ошибки измерений и т.д. Для анализа случайной составляющей можно использовать методы статистического анализа, такие как тест на стационарность или коррелограмму.
    Цикличность представляет собой периодические изменения уровня временного ряда, которые не повторяются через определенные промежутки времени, как это происходит в случае с сезонностью. Цикличность может быть связана с экономическими циклами, политическими событиями или другими длительными процессами, которые повторяются в истории. Для анализа цикличности можно использовать методы спектрального анализа или вейвлет-анализа.
    $$$Вопрос 47 --- Функциональные зависимости временного ряда. Предварительный анализ временных рядов ---
    Для анализа временных рядов необходимо провести предварительный анализ, который включает в себя следующие шаги:
    1. Визуальный анализ графика временного ряда. На графике необходимо оценить наличие тренда, сезонности, цикличности и случайной составляющей.
    2. Оценка статистических характеристик временного ряда. Необходимо оценить среднее значение, стандартное отклонение, коэффициент вариации и другие статистические показатели.
    3. Анализ автокорреляционной функции (ACF) и частной автокорреляционной функции (PACF). ACF показывает корреляцию между значениями ряда на разных лагах времени, а PACF учитывает только прямые связи между значениями на разных лагах.
    4. Тестирование на стационарность. Стационарность означает, что статистические характеристики временного ряда не меняются со временем. Для тестирования стационарности можно использовать тест Дики-Фуллера или КПСС. Но лучше всего построить графики мат ожидания и дисперсии. Если будет стремиться к линейной функции, то стационарность очень вероятна
    5. Моделирование временного ряда. На основе предварительного анализа можно выбрать модель временного ряда, которая будет учитывать тренд, сезонность, цикличность и случайную составляющую.
    Доп:
    Функциональные зависимости временного ряда могут быть описаны различными моделями, такими как авторегрессионная модель (AR), интегрированная авторегрессионная модель (ARIMA), модель экспоненциального сглаживания (ETS) и другие. 
    $$$Вопрос 48 --- Процедура выявления аномальных наблюдений. Причины аномальных значений. Блочные диаграммы по типу «ящика с усами» ---
    Процедура выявления аномальных наблюдений включает в себя следующие шаги:
    1. Визуальный анализ графика временного ряда. На графике необходимо обратить внимание на значения, которые сильно отличаются от общей тенденции ряда.
    2. Расчет статистических показателей. Необходимо оценить выбросы, используя статистические методы, такие как правило трех сигм или интерквартильный размах.
    Причины аномальных значений. Необходимо исследовать причины появления аномальных значений, такие как ошибки измерения, изменения в процессах или системах, ошибки в данных и т.д.
    Блочные диаграммы по типу «ящика с усами». - метод, позволяющий визуально оценить выбросы и их распределение в данных. Пример:
    Рисунок бокс плот: посередине медиана. Верх прямоугольника-верхний квартиль, низ-нижний. Конец верхнего уса – верхняя граница, нижнего – нижняя. Точки за пределами – выбросы.
    Причины аномальных значений могут быть различными, такими как ошибки измерения, изменения в процессах или системах, ошибки в данных и т.д. Поэтому для выявления аномалий необходимо проводить комплексный анализ данных и искать причины возникновения аномальных значений.
    $$$Вопрос 49 --- Процедура выявления аномальных наблюдений на основе распределения Стьюдента. Особенности применения метода. Анализ аномальных наблюдений ---
    Процедура выявления аномальных наблюдений на основе распределения Стьюдента основана на том, что выбросы могут быть определены как наблюдения, которые имеют очень высокое или очень низкое значение, отличающееся от остальных значений в выборке. Распределение Стьюдента используется для определения того, насколько вероятно, что наблюдение является выбросом.
    Особенностью этого метода является то, что он учитывает размер выборки и учитывает степень свободы, что позволяет более точно определить выбросы. Для определения аномальных наблюдений на основе распределения Стьюдента используется формула:
    t = (x - μ) / (s / sqrt(n))
    где t - значение статистики Стьюдента, x - значение наблюдения, μ(поясняю, мю) - среднее значение выборки, s - стандартное отклонение выборки и n - размер выборки.
    Значение t можно использовать для определения того, насколько вероятно, что наблюдение является выбросом. Если значение t больше определенного порогового значения (обычно 2 или 3), то наблюдение считается аномальным.
    Анализ аномальных наблюдений может быть полезен для выявления ошибок в данных, а также для определения значимости выбросов и их влияния на результаты анализа. Однако, не всегда выбросы являются ошибками, и их удаление может привести к потере важной информации. Поэтому, перед удалением выбросов необходимо тщательно проанализировать данные и определить их значимость.
    $$$Вопрос 50 --- Процедура выявления аномальных наблюдений на основе метода Ирвина. Особенности применения метода. Анализ аномальных наблюдений ---
    Метод Ирвина используется для выявления аномальных наблюдений в выборке. Он основан на том, что выбросы могут быть определены как наблюдения, которые находятся далеко от центра выборки в пространстве многомерных переменных.
    Применение метода Ирвина включает следующие шаги:
    1. Вычисление средних значений и ковариационной матрицы для всех переменных в выборке.
    2. Вычисление расстояния Махаланобиса для каждого наблюдения. Расстояние Махаланобиса учитывает корреляцию между переменными и позволяет определить, насколько далеко находится наблюдение от центра выборки.
    Расстояние Махаланобиса, формула имеет
    следующий вид:

    p_sum(x,y)=(x-y)^T*sum^(-1)(x-y) (поясняю, p_sum – p с индексом значка суммы. (х,у) никак с суммой не связаны), где sum - общая внутригрупповая дисперсионно-ковариационная матрица.
    3. Определение порогового значения расстояния Махаланобиса на основе распределения хи-квадрат с числом степеней свободы, равным числу переменных в выборке.
    4. Определение аномальных наблюдений как тех, чье расстояние Махаланобиса превышает пороговое значение.
    Особенностью метода Ирвина является то, что он учитывает корреляцию между переменными и может быть применен к выборкам с большим числом переменных. Однако, для его применения необходимо, чтобы выборка была достаточно большой (обычно не менее 50 наблюдений).
    Анализ аномальных наблюдений может помочь выявить ошибки в данных, а также определить важность выбросов и их влияние на результаты анализа. Однако, как и при использовании метода Стьюдента, не всегда выбросы являются ошибками, и их удаление может привести к потере важной информации. Поэтому, перед удалением выбросов необходимо тщательно проанализировать данные и определить их значимость.
    $$$Вопрос 51 --- Проверка наличия тренда. Критерий серий, основанный на медиане. Особенности применения метода ---
    Критерий серий, основанный на медиане, используется для проверки наличия тренда в временных рядах. Он основан на разделении ряда на серии, где каждая серия состоит из последовательности значений, упорядоченных по возрастанию или убыванию. Затем вычисляется количество серий и их длины, и на основе этого строится статистика критерия.
    Применение критерия серий основанного на медиане включает следующие шаги:
    1. Разделение временного ряда на серии. Для этого можно использовать различные методы, например, методы знаковых серий или медианных серий.
    2. Вычисление количества серий и их длины.
    3. Вычисление статистики критерия на основе количества серий и их длины.
    Формула выборочной медианы: Y_med = система(y_((n+1)/2),если п-нечетное; 1/2*(y_(n/2)+y_(n/2+1)), если n - четное)
    Образуем серии «плюсов» и «минусов»:
    «Плюс» если у(t)>y_med ,
    «Минус» если у(t)<y_med
    Под «серией» понимается последовательность плюсов подряд идущих плюсов и подряд идущих минусов: v(n) - общее число серий; К_mах - протяженность самой длинной серии.
    4. Определение критического значения статистики критерия на основе таблиц стандартных значений.
    5. Сравнение вычисленной статистики критерия с критическим значением и принятие решения о наличии или отсутствии тренда в ряде.
    Особенностью критерия серий, основанного на медиане, является его устойчивость к выбросам и отсутствие требования о нормальности распределения данных. Однако, для его применения необходимо, чтобы ряд был достаточно длинным (обычно не менее 20 наблюдений).
    При применении критерия серий необходимо учитывать, что он может давать ложноположительные результаты в случае наличия сезонности или цикличности в ряде. Поэтому, перед использованием критерия необходимо провести анализ ряда и определить его особенности.
    $$$Вопрос 52 --- Проверка наличия тренда. Метод проверки разности средних уровней. Особенности применения метода ---
    Метод проверки разности средних уровней используется для проверки наличия тренда в временных рядах. Он основан на сравнении средних значений двух групп наблюдений, разделенных по времени.
    Применение метода проверки разности средних уровней включает следующие шаги:
    1. Разделение временного ряда на две группы наблюдений: первую группу, которая соответствует начальному периоду ряда, и вторую группу, которая соответствует последующему периоду ряда.
    2. Вычисление среднего значения для каждой группы наблюдений.
    3. Вычисление разности между средними значениями двух групп наблюдений.
    4. Определение критического значения статистики критерия на основе таблиц стандартных значений.
    5. Сравнение вычисленной статистики критерия с критическим значением и принятие решения о наличии или отсутствии тренда в ряде.
    t = abs(y^-_1-y^-_2) / (sig*sqrt(1/n_1+1/n_2)), sig = sqrt(((n_1-1)*sig^2_1+(n_2-1)*sig^2_2) / (n-2))


    Особенностью метода проверки разности средних уровней является его простота и удобство в использовании. Однако, для его применения необходимо, чтобы ряд был достаточно длинным (обычно не менее 20 наблюдений).
    При применении метода проверки разности средних уровней необходимо учитывать, что он может давать ложноположительные результаты в случае наличия сезонности или цикличности в ряде. Поэтому, перед использованием метода необходимо провести анализ ряда и определить его особенности. Кроме того, метод не подходит для рядов с нестационарной дисперсией.
    $$$Вопрос 53 --- Проверка наличия тренда. Метод Фостера-Стьюарта. Особенности применения метода ---
    Метод Фостера-Стьюарта также используется для проверки наличия тренда в временных рядах. Он основан на анализе коэффициента наклона линейной регрессии, построенной для временного ряда.
    Применение метода Фостера-Стьюарта включает следующие шаги:
    1. Построение линейной регрессии для временного ряда.
    2. Определение значимости коэффициента наклона линейной регрессии с помощью статистики t-критерия Стьюдента.
    3. Определение критического значения статистики t-критерия на основе таблиц стандартных значений.
    4. Сравнение вычисленной статистики t-критерия с критическим значением и принятие решения о наличии или отсутствии тренда в ряде.
    q_t = system(1, y_t>y_(t-1)>…>y_1;0, иначе) p_t = system(1, y_t>y_(t-1)>…>y_1;0, иначе)
    d_t = q_t-p_t 
    D = sum(n, t=2)(d_t) sig_D=sqrt(2*sum(n, t=2)(1/t))~sqrt(2*ln(n)-0.8456)\
    t_набл = D/sig_D
    t_tabl берется из таблицы значений стандартных ошибок для sig_D для n 
    Особенностью метода Фостера-Стьюарта является его чувствительность к выбросам и аномалиям в данных. Поэтому, перед использованием метода необходимо провести анализ ряда и удалить выбросы и аномалии, если они есть.
    Кроме того, метод Фостера-Стьюарта не подходит для рядов с нелинейным трендом или сезонностью. В таких случаях необходимо использовать другие методы анализа временных рядов, например, методы декомпозиции или экспоненциального сглаживания.
    Также следует учитывать, что метод Фостера-Стьюарта может давать ложноположительные результаты в случае наличия автокорреляции в ряде. Поэтому, перед использованием метода необходимо провести анализ автокорреляции и определить ее структуру.
    $$$Вопрос 54 --- Сглаживание временных рядов. Простая (среднеарифметическая) скользящая средняя. Взвешенная (средневзвешенная) скользящая средняя. Среднехронологическая. Экспоненциальное сглаживание ---
    Сглаживание временных рядов – это метод, который используется для устранения шумов и случайных колебаний в данных. Он позволяет выделить основной тренд и увидеть более явно изменения в ряде.
    Простая скользящая средняя – это метод, который заключается в расчете среднего значения по определенному количеству последовательных значений ряда. Например, для скользящей средней на 5 периодов, каждое значение рассчитывается как среднее арифметическое пяти последовательных значений. Этот метод дает равный вес всем значениям ряда.
    Взвешенная скользящая средняя – это метод, который использует различные веса для каждого значения ряда. Веса определяются на основе значимости каждого периода. Например, если наблюдения более свежие, то им может быть присвоен больший вес.
    Среднехронологическая скользящая средняя – это метод, который использует веса, которые изменяются по мере приближения к текущему периоду. В отличие от простой скользящей средней и взвешенной скользящей средней, он учитывает изменение значимости периодов со временем.
    Экспоненциальное сглаживание – это метод, который использует взвешенную сумму всех предыдущих значений ряда, с весами, которые уменьшаются экспоненциально по мере удаления от текущего периода. Этот метод учитывает все предыдущие значения ряда, но дает больший вес более свежим наблюдениям.
    Выбор метода сглаживания зависит от характеристик временного ряда и целей анализа. Например, простая скользящая средняя может быть полезна для устранения случайных колебаний в данных, а экспоненциальное сглаживание может быть более эффективным для выделения тренда в ряде.
    $$$Вопрос 55 --- Трендовые модели. Без предела роста. Примеры функций. Содержательная интерпретация параметров ---
    Трендовые модели являются одним из классов моделей, используемых для анализа временных рядов и прогнозирования будущих значений. Они представляют собой модели, которые пытаются описать общую тенденцию или направление изменения в данных.
    Одна из популярных трендовых моделей - это модель экспоненциального роста, которая описывает процесс, в котором переменная увеличивается (или уменьшается) с постоянной темпом на протяжении некоторого времени. Примером функции, описывающей экспоненциальный рост, может быть:
    y(t) = a * exp(b * t)
    где y(t) - значение переменной в момент времени t, a - начальное значение переменной, b - коэффициент роста, t - время.
    Параметры этой модели имеют следующую содержательную интерпретацию:
    Начальное значение переменной (a): Это значение переменной в момент времени t=0. Оно указывает на уровень, с которого начинается процесс роста или убывания.
    Коэффициент роста (b): Этот параметр определяет скорость изменения переменной со временем. Если b положительный, то переменная растет, а если b отрицательный, то переменная убывает. Величина b указывает на скорость изменения: чем больше абсолютное значение b, тем быстрее изменяется переменная.
    Трендовые модели могут быть полезны для прогнозирования долгосрочных тенденций и выявления общих закономерностей в данных. Однако следует помнить, что они не всегда могут точно предсказать будущие значения, особенно если в данных присутствуют случайные флуктуации или другие факторы, которые не учитываются в модели. Поэтому важно использовать трендовые модели с осторожностью и дополнять их другими методами анализа данных при необходимости
    ИЗ ЕЕ ПРЕЗЫ:
    Прямая (полином 1ой степ) y_t=a_0+a_1*t
    Парабола (полином 2ой степ) y_t = a_0 + a_1*t + a_2*t^2
    Экспонента y_t = exp(a_0+a_1*t)
    Ссодержательная интерпретация параметров:
    a_0 во всех моделях без пред роста задает нач условия, а в моделях с пределом роста – асимптоту функции
    a_1 определяет скорость или интенсивность развития
    a_2 изменение скорости или интенсивности развития
    $$$Вопрос 56 --- Трендовые модели. С пределом роста без точки перегиба. Примеры функций. Содержательная интерпретация параметров ---
    Трендовые модели предназначены для описания долгосрочных тенденций во временных рядах. Они могут быть использованы для прогнозирования будущих значений ряда на основе его прошлого поведения. Одна из таких моделей - модель с пределом роста без точки перегиба.
    Примерами функций, которые могут использоваться для моделирования ряда с пределом роста без точки перегиба, являются логистическая функция и экспоненциальная функция с ограничением. Логистическая функция имеет следующий вид:
    f(x) = L / (1 + exp(-k(x-x0)))
    где L - предел роста, k - скорость роста, x0 - точка перегиба.
    Экспоненциальная функция с ограничением имеет следующий вид:
    f(x) = L - a * exp(-kx)
    где L - предел роста, a - начальное значение, k - скорость роста.
    Параметры этих функций могут быть интерпретированы следующим образом:
    - L - предел роста или уровень насыщения, к которому стремится ряд.
    - k - скорость роста или уменьшения.
    - x0 - точка перегиба или момент, когда ряд начинает замедлять свой рост.
    - a - начальное значение или уровень, с которого начинается рост.
    Интерпретация параметров модели зависит от конкретного контекста и может быть разной для разных рядов. Например, в случае моделирования роста населения, L может представлять максимальную вместимость планеты, а k - скорость роста населения. В случае моделирования продаж товаров, L может представлять максимальный объем продаж, а k - скорость роста продаж.
    ИЗ ЕЕ ПРЕЗЫ:
    Модифицированная экспонента имеет вид:
    f(t) = k + a*b^t, где а < 0; 0 < b < 1; k - асимптота, значение которой считается известным.
    Параметры а и b можно найти, как и для простой экспоненты, перенесся к в левую часть: f(t) - k = a*b^t.
    Более сложным вариантом экспоненциальной кривой является логарифмическая парабола: f(t) = a_0*a_1^t*a_2^(t^2).
    Прологарифмировав это выражение, получим параболу: ln(y_t) = ln(a_0) + t*ln(a_1)+ t^2*ln(a_2).
    Таким образом, оценку параметров логарифмической параболы можно опять осуществить с помощью метода наименьших квадратов, используя систему нормальных уравнений для параболы.
    $$$Вопрос 57 --- Трендовые модели. С пределом роста и точкой перегиба или кривые насыщения. Примеры функций. Содержательная интерпретация параметров ---
    Существуют кривые с пределом роста и точкой перегиба или кривые насыщения (S-образные кривые). Эти кривые описывают как бы два последовательных лавинообразных процесса (когда прирост зависит от уже достигнутого уровня): один с ускорением развития, другой - с замедлением. S-образные кривые находят применение в демографических исследованиях, в страховых расчетах, при решении задач прогнозирования научно-технического прогресса, при определении спроса на новый вид продукции.
    ИЗ ЕЕ ПРЕЗЫ:
    К кривым с пределом роста и точкой перегиба относятся кривая Гомперца и логистическая кривая (Перла-Рида).
    Кривая Гомперца имеет вид: f(t) = k*a^(b^t). Если а> 1, асимптота, равная k, лежит ниже кривой, а сама кривая изменяется монотонно: при b < 1 - монотонно убывает; при b > 1 - монотонно возрастает.
    В кривой Гомперца выделяют четыре участка: на первом - прирост функции незначителен, на втором - прирост увеличивается, на третьем участке прирост примерно постоянен, на четвертом - происходит замедление темпов прироста и функция приближается к значению k.
    Применяя дважды логарифмирование, получим линейное уравнение: In(f(t)) = In(k) + b^t*ln(a), In(Inf(t) - Inc) – In(ln(a)) + t*ln(b).
    Уравнение логистической кривой получается путем замены в модифицированной экспоненте f(t) обратной величиной 1/f(t): 1/f(t) = k+a*b^t.
    Используются и другие формы записи уравнения логистической кривой: f(t) = k/(1-a*e^(-b*t)), f(t)=k/(1+a*b^t), f(t)=k/(1+10(a-b*t))
    При t ->-inf логистическая кривая стремится к нулю, а при t -> +inf к асимптоте, равной значению параметра k.
    Кривая симметрична относительно точки перегиба с координатами:
    t = In(b/a); f(t) = k/2
    Одним из примеров таких моделей является модель роста населения, где L может представлять максимальную вместимость планеты, k - скорость роста населения, x0 - момент, когда население начинает стабилизироваться, а a - начальное количество людей. В случае моделирования продаж товаров L может представлять максимальный объем продаж, k - скорость роста продаж, x0 - момент, когда спрос начинает уменьшаться, а a - начальный объем продаж. В общем случае, интерпретация параметров зависит от конкретной модели и контекста.
    $$$Вопрос 58 --- Выбор кривой роста ---
    Для выбора кривой роста используется метод характеристик прироста, основанный на использовании отдельных характерных свойств рассмотренных выше кривых.
    Процедура выбора кривых с использованием этого метода включает выравнивание ряда Y_t с помощью скользящей средней (обычно среднеарифметической по трем точкам) и определение средних приростов и производных величин:
    delta(y_t) =(y_(t+1)-y_(t-1))/2- первый средний прирост;
    delta^2(y_t) = =(y_(t+1)-y_(t-1))/2 - второй средний прирост;
    delta(y_t)/y_t, ln(delta(y_t)), ln(delta((y_t)/y)), ln((delta(y_t)) / (y^2_t))- производные величины.
    В соответствии с характером изменений средних приростов и производных показателей выбирается вид кривой роста с помощью таблицы:
    Показатель - Характер изменения - Кривая роста
    delta(y_t) - Примерно постоянный - Полином первого порядка
    delta(y_t) - Примерно линейный - Полином второго порядка
    delta^2(y_t) - Примерно линейный - Полином третьего порядка
    (delta(y_t))/y_t - Примерно постоянный - Экспонента
    In(delta(y_t)) - Примерно линейный - Модифицированная экспонента
    In((delta(y_t))/y) - Примерно линейный - Кривая Гомперца
    In((delta(y_t))/(y^2)) - Примерно линейный - Логистическая кривая
    На практике отбирают две-три кривые роста и окончательный вывод делают исходя из значений критерия, в качестве которого принимают сумму квадратов отклонений фактических значений уровней от расчетных.
    Из рассматриваемых кривых предпочтение будет отдано той, которой соответствует минимальное значение критерия.
    $$$Вопрос 59 --- Прогнозирование с помощью кривой роста ---
    При экстраполяционном прогнозировании (более сложное) экономических процессов необходимо определить два элемента: точечный и интервальный прогнозы.
    Точечный прогноз - это значение экономического показателя в будущем, определенное путем подстановки значения времени в уравнение выбранной кривой роста.
    Совпадение фактических данных в будущем и точечного прогнозного значения маловероятно.
    Точечный прогноз дополняют двухсторонними границами, т.е. таким интервалом, в котором с большой степенью вероятности ожидается фактическое значение прогнозируемого показателя.
    Этап 1 Точечный прогноз
    в построенную модель подставляют соответствующие значения фактора t = n + k, входящие в интервал упреждения. Например, для линейной модели прогноз выглядит следующим образом:
    y^^_прогноз(n+k) = a_0 + a_1*(n + k)
    Этап 2 Интервальный прогноз
    Ширину доверительного интервала для линейной трендовой модели определяют так:
    U(k) = S_(Y^^)*t_alpha* sqrt(1+1/n+((n+k-t^-)^2)/ (sum(n, t=1)((t-t^-)^2))), где S_(Y^^)=sqrt((sum(n, t=1)(eps^2_t) )/ ( n-m-1))
    верхняя и нижняя границы прогноза: Верхняя граница = y_прогноз + U(k), Нижняя граница = y_прогноз - U(k).
    Если же в качестве трендовой модели выбрана нелинейная модель, которую можно линеаризовать, приведя к линейной многофакторной форме, то ширину доверительного интервала можно определить матричным способом:
    U(k) = S_(Y^^)*t_alpha*sqrt(1+x^(->)^T_0(X^T*X)^(-1)*x^(->)_0) (поясняю, x^(->)^T_0 – это икс со значком вектора сверху, индексом ноль и степенью Т), где x^(->)_0- вектор прогнозных оценок регрессоров.
    $$$Вопрос 60 --- Прогнозирование временного ряда на основе трендовой модели ---
    Интервальным прогноз определяется с помощью доверительного интервала
    Y^^_факт(t) = f_t + U(k), где y^^_факт(t) - фактическое значение в будущем; U(k), - доверительный интервал. 
    Для линейного тренда доверительный интервал определяется формулой
    U(k) = S_(Y^^)*t_alpha*sqrt(1+1/n + (3*(n+2*k-1)^2)/(n(n^2-1))), где k - период упреждения, т.е. число шагов, на которые делается прогноз; t_alpha – критерий Стьюдента для числа степеней свободы n- 2 уровня значимости аlpha.
    Стандартная ошибка аппроксимации прогнозируемого показателя определяется выражением S_(Y^^)=sqrt((sum(n,1)(y_t-f_t))/()n-l) где l - число параметров трендовой модели.
    Для полиномов второго и третьего порядка используется выражение, в котором начало отсчета времени перенесено на середину временного ряда наблюдений:
    U(k) = S_(Y^^)*t_alpha*sqrt(1+1/n+(t^2_k)/(sum(n, t=1)(t^2))+(sum(n,t=1)(t^4)-2*t^2_k*sum(n, t=1)(t^2)+n*t^4_k)/(n*sum(n, t=1)(t^4)-(sum(n,t=1)(t^2))^2))
    где t_k- время прогноза, а суммирование выполняется по всем значениям временного ряда
    -(n-1)/2 < t < (n-1)/2 
    Несмотря на то, что приведенные формулы позволяют определить прогноз на любое число шагов, попытка заглянуть слишком далеко приведет к очень большим ошибкам. Длина периода упреждения не должна превышать одной трети длины ряда наблюдений.
    '''
    
    main = list(map(lambda x: x.split('---'),k_my.split('|||')))

    l = list(map(lambda x: x.split('---'),k_an.split('$$$')))[1:]
    for el in l:
        main.append([el[1], el[2]]) 
    
    if type(word) == str:
        for ind, el in enumerate(main):
            if word.lower() in el[0].lower():
                print(ind, '---', el[0])
    if type(word) == int:
          print(main[word][1])
