import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, pearsonr, spearmanr, kendalltau, \
    f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

#veri setlerimizi çekelim:

data = pd.read_excel("/Users/didemerkan/Desktop/DSMLBC-5.HFT/ab_testing.xlsx" ,sheet_name="Control Group")
data1 = pd.read_excel("/Users/didemerkan/Desktop/DSMLBC-5.HFT/ab_testing.xlsx" ,sheet_name="Test Group")

df_testing = data.copy()
df_control = data1.copy()

df_testing.head()
df_control.head()

df_control.describe().T
df_testing.describe().T

df_testing["Purchase"].mean()  # 550.8940587702316
df_control["Purchase"].mean()  # 582.1060966484675


#Confidence Interval
sms.DescrStatsW(df_testing["Purchase"]).tconfint_mean()  # (508.0041754264924, 593.7839421139709)
sms.DescrStatsW(df_control["Purchase"]).tconfint_mean()  # (530.5670226990063, 633.645170597929)

# Görev 1: Hipotezi kuralım:

# H0 : M1=M2 (Maximum bidding ile yeni tanıtılan average bidding arasında istatistiksel olarak anlamlı bir farklılık yoktur.)
# H1 : M1!=M2 (..vardır.)

df_testing["Purchase"].mean()  # 550.8940587702316
df_control["Purchase"].mean()  # 582.1060966484675

# Aralarında fark var ama şans eseri ortaya cıkmıs olabilir mi kaygılarını gidermek için AB testini uygulamalıyız.:

############################
# Varsayım Kontrolü
############################

#1 Normallik Varsayımı
#2 Varyans Homojenliği

############################
# Normallik Varsayımı (Normallik varsayım testi için shapiro testi kullanılabilir.)
############################

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.

# p-value <  0.05 ise  HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.


test_stat, pvalue = shapiro(df_testing["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#p-value = 0.5891

test_stat, pvalue = shapiro(df_control["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#p-value = 0.1541

# Test grubu için: p < 0.05 değil, H0 REDDEDİLEMEZ, yani normal dağılım varsayımı sağlanmaktadır.
# Kontrol grubu için : p < 0.05 değil, H0 REDDEDİLEMEZ, yani normal dağılım varsayımı sağlanmaktadır.

# Varyans Homojenligi Varsayımı

# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir

test_stat, pvalue = levene(df_testing["Purchase"],
                           df_control["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#Test Stat = 2.6393, p-value = 0.1083

# p < 0.05 değil H0 REDDEDİLEMEZ. Yani varyanslar homojen değerdedir.

# Hipotezin Uygulanması

# 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)
# 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)

# Eğer normallik sağlanmazsa her türlü nonparametrik test yapacağız.
# Eger normallik sağlanır varyans homojenliği sağlanmazsa ne olacak?
# T test fonksiyonuna arguman gireceğiz.


# H0: M1 = M2 (... iki grup ortalamaları arasında ist ol.anl.fark yoktur.)
# H1: M1 != M2 (...vardır)


############################
# Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)
############################

test_stat, pvalue = ttest_ind(df_control["Purchase"],df_testing["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.

# Test Stat = 0.9416, p-value = 0.3493

# O zaman H0 reddedilemez yani istatistiki olarak anlamlı bir fark yoktur.!

############################
# Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)
############################


test_stat, pvalue = mannwhitneyu(df_testing["Purchase"], df_control["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Test Stat = 723.0000, p-value = 0.2308

# H0: M1 = M2 (... iki grup ortalamaları arasında ist ol.anl.fark yoktur.)
# H1: M1 != M2 (...vardır)

# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.
#H0 reddedilmez.!

# Test ve Control grupları arasında %95 güven aralığı ile istatistiki olarak anlamlı bir farklılık yoktur.

# Görev 3:

# Normallik varsayımı için shapiro kullanıldı.
# Varyans homojenliği için levene kullanıldı.
# Normallik ve varyans homojenliği varsayımları sağlandığı için, anlamlı bir farklılık olup olmadığını ölçmek için ise parametrik test olan Bağımsız İki Örneklem T Testi kullanıldı.
# Eğer normallik varsayımı sağlanıp varyans homojenliği sağlanmasaydı yine Bağımsız iki örneklem T Testi kullanılırdı.
# Fakat test içerisindeki "equal_var=True" argümanını False olarak değiştirilirdi.

# Görev 4:

# Hipotez testi sonucu iki grup ortalamaları arasında anlamlı bir fark olmadığı gözlemlenmiştir.
# Müşterilere average bidding tavsiyesinin, şirket çıkarlarına çok da bir fayda sağlanamayacağı söylenebilir, gözleme bir süre daha devam etmesi söylenebilir.