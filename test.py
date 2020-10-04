

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

filename = 'Telephone.csv'
df = pd.read_csv(filename, encoding='gbk')

col = '教育水平'
eduLevel = ['初中','高中','大专','本科','研究生']
df[col] = df[col].astype('category').cat.set_categories(eduLevel)


catCols = ['居住地', '婚姻状况', '教育水平', '性别', '电子支付']
intCols = ['年龄', '收入', '家庭人数', '开通月数']
target = '消费金额'

sr = df['教育水平'].value_counts()
sr.sort_index(inplace=True)
sr.plot(kind='bar')
sr.plot(kind='pie', autopct='%1.1f%%')
sr.plot()

df2 = pd.pivot_table(df, 
            index='教育水平',
            columns='套餐类型',
            values='UID',
            aggfunc=np.size)
total = df2.sum(axis=1)
for col in df2.columns:
    df2[col] = df2[col]/total
df2.plot(kind='bar')

df['年龄'].plot(kind='hist',bins=10, edgecolor='k')
df['年龄'].plot(kind='box')




