#-*- coding: utf-8 -*- 

########  本文件实现基本的统计操作功能，包括：
# 1.描述统计describe()
# 2.分类计数value_counts()
# 3.分箱/分段计数value_counts(bins)
# 4.分类汇总
#   4.1 分组groupby
#   4.2 汇总方式：计数、求和、平均值...
#   4.3 常用聚合函数
# 5.透视表
# 6.日期统计
######################################################################

import pandas as pd
import numpy as np


# 1.读取数据集
filename = '用户明细.csv'
df = pd.read_csv(filename)
print(df.columns.tolist())

# 2.整理数据
col = '注册日期'
df[col] = df[col].astype('datetime64[ns]')

################# 描述统计 ################

# describe()返回描述信息，
#   1)如果字段是数值型，则返回包括count,mean,std,min,25%,50%,75%,max共8个值
#       其中count是非空值的个数，可以使用len(df) - count来识别有多少个空值
#   2）如果字段是字符串型，则返回count,unique,top,freq共4个值
#   3）如果字段是日期，则返回count,unique,top,freq,first,last共6个值

des = df['年龄'].describe()
print(des)


#对于数值型变量，还可生成并计算新的字段：极差、变异系数、IQR四分位数
col = '年龄'
des = df[col].describe()
des.loc['range'] = des.loc['max']-des.loc['min']    #极差
des.loc['CV'] = des.loc['std']/des.loc['mean']      #变异系数
des.loc['IQR'] = des.loc['75%']-des.loc['25%']      #四分位数间距

des.loc['sum'] = df[col].sum()      #求和
des.loc['var']  = df[col].var()     #方差
des.loc['skew'] = df[col].skew()    #偏度
des.loc['kurt'] = df[col].kurt()     #峰度
print(des)


des = df['学历'].describe()
print(des)

des = df['注册日期'].describe()
print(des)


# 描述统计
#DataFrame.describe(percentiles=None, include=None, exclude=None)
    #   percentiles : 百分比列表，默认为[.25, .5, .75]
    #   include : ‘all’, list-like of dtypes or None (default), optional
        # 'all'，表示所有的字段
        # 类型列表,如['int','categorical']，表示对指定数据类型的字段进行统计
        # None, 表示仅对数值字段进行统计
        # 注：对Series对象无效

    #   exclude : list-like of dtypes or None (default), optional,
        # 黑名单，与include取值类似
        
################# 分类计数 (类别变量)################

# 分类计数, 返回计数
sr = df['性别'].value_counts()

# 返回百分比
sr = df['学历'].value_counts(normalize=True)

# 相关函数
    # 唯一值计数
    # Series.value_counts(normalize=False, sort=True, ascending=False, 
    #               bins=None, dropna=True)
    # normalize : boolean, 默认False返回计数；True则返回占比
    # sort : boolean, default True，默认按值排序
    # ascending : boolean, default False，默认降序排列
    # bins : integer, optional
    #   Rather than count values, group them into half-open bins, 
    #   a convenience for pd.cut, only works with numeric data.
    # dropna : boolean, default True，不包含空值的计数。

################# 分箱计数/分段计数 (数值变量)################

# 对数值型变量分段统计
sr = df['年龄'].value_counts(bins=10, sort=False)
print(sr)
sr = df['年龄'].value_counts(bins=10, normalize=True, sort=False)

# 因为value_counts会默认按值排序，
# 所以需要指定sort=False参数，保持索引的顺序性


################# 分类汇总 ################
# 用户明细，是以utf-8编码，以\t分隔
filename = '订购明细.csv'
df = pd.read_csv(filename, sep='\t')
print(df.columns.tolist())

col = '订购日期'
df[col] = df[col].astype('datetime64[ns]')

# 1.先分组

# 单类别分组
col = '产品'
grouped = df.groupby(col)

# 2、分组访问
# 1）遍历分组
# name是前面’产品‘列的取值，或者元组（如果是多列）
# group是DF对象
for name, group in grouped:
    print(name) 
    print('\t行数：',len(group))

# 2）选择其中某一个分组
df2 = grouped.get_group('产品A')

# 3、分类汇总、分组统计
avgCol = '数量'
sr = grouped[avgCol].sum()      #按产品求销量
# 类似函数,first,last,sum,mean,std,count,size等

# 4、使用numpy统计函数库
sr = grouped[avgCol].agg(np.sum)

#一次完成多个计算
df2 = grouped[avgCol].agg([np.sum, np.mean, np.std])

# # 5、多类别分组
# cols = ['省份', '性别']
# grouped = df.groupby(cols)

# # 访问某个组的数据集
# dfgdF = grouped.get_group(('广东','女'))

# sr = grouped['年龄'].mean()      #求不同组的平均年龄
# sr = grouped['年龄'].agg(np.sum)
# df2 = grouped['年龄'].agg([np.max, np.mean, np.min]) 
# df2 = grouped.agg({'省份':np.size, '年龄':np.sum})  # 不同的列，进行不同的统计
# sr = df2.loc[('广东','男')]


# 常用聚合函数
    # sum, mean, count, max, min, std, var, sem(标准误差)


################# 透视表（交叉表） ################

# 注意：values指定的字段必须是数值型的
filename = '用户明细.csv'
df = pd.read_csv(filename)

# 二维交叉表，按居住地+性别-->年龄(和)
df2 = pd.pivot_table(df, 
                index=['学历'], 
                columns=['性别'],
                values='年龄',
                aggfunc='sum')

# 横向合计
df2['sum'] = df2.sum(axis=1)
# 纵向合计
df2.loc['sum'] = df2.sum(axis=0)


# DataFrame.groupby
    # (by=None, axis=0, level=None, as_index=True, 
    #            sort=True, group_keys=True, squeeze=False, observed=False, **kwargs)

    # 聚合函数：mean, sum, min, max,,std,var,first,last,
    #   sem(组均方差)，describe(描述统计),nth(第N个值)
    #   size(组大小)，count(各列的组大小)
    #   注意：上述函数排除空值

# pandas.pivot_table
    # (data, values=None, index=None, columns=None, 
    #           aggfunc='mean', fill_value=None, margins=False, 
    #           dropna=True, margins_name='All', observed=False)
    # 参数说明：透视表
    # data : DataFrame
    # values : 要汇总的列
    # index : column, Grouper, array, or list of the previous
    #       If an array is passed, it must be the same length as the data. 
    #       The list can contain any of the other types (except list). 
    #       Keys to group by on the pivot table index. 
    #       If an array is passed, it is being used as the same manner as column values.
    # columns : column, Grouper, array, or list of the previous
    #       If an array is passed, it must be the same length as the data. 
    #       The list can contain any of the other types (except list). 
    #       Keys to group by on the pivot table column. 
    #       If an array is passed, it is being used as the same manner as column values.
    # aggfunc : 函数，函数列表，字典。默认是numpy.mean
    #       如果是函数列表，则透视表的标题为函数名称
    #       如果是字典，则key是要汇总的列，而value是函数或函数列表
    # fill_value : scalar, default None
    #       缺失值的填充值。
    # margins : boolean, default False
    #       Add all row / columns (e.g. for subtotal / grand totals)
    # dropna : boolean, default True
    #       Do not include columns whose entries are all NaN
    # margins_name : string, default ‘All’
    #       Name of the row / column that will contain the totals when margins is True.
    # observed : boolean, default False
    #   This only applies if any of the groupers are Categoricals. 
    #   If True: only show observed values for categorical groupers. 
    #   If False: show all values for categorical groupers.

################# 日期分类 ################

filename = '订购明细.csv'
df = pd.read_csv(filename, sep='\t')

# 确保数据类型正确
col = '订购日期'
df[col] = df[col].astype('datetime64[ns]')
print(df.dtypes)

# 1.提取时间段，年、月、日
sr = df[col].dt.year 
sr = df[col].dt.quarter
sr = df[col].dt.month
sr = df[col].dt.day
sr = df[col].dt.week
sr = df[col].dt.hour
sr = df[col].dt.minute
sr = df[col].dt.second
sr = df[col].dt.date

# 其余属性描述Property	Description
    # year	The year of the datetime
    # month	The month of the datetime
    # day	The days of the datetime
    # hour	The hour of the datetime
    # minute	The minutes of the datetime
    # second	The seconds of the datetime
    # microsecond	The microseconds of the datetime
    # nanosecond	The nanoseconds of the datetime
    # date	Returns datetime.date
    # time	Returns datetime.time
    # dayofyear	The ordinal day of year
    # weekofyear	The week ordinal of the year
    # week	The week ordinal of the year
    # dayofweek	The numer of the day of the week with Monday=0, Sunday=6
    # weekday	The number of the day of the week with Monday=0, Sunday=6
    # weekday_name	The name of the day in a week (ex: Friday)
    # quarter	Quarter of the date: Jan=Mar = 1, Apr-Jun = 2, etc.
    # days_in_month	The number of days in the month of the datetime
    # is_month_start	Logical indicating if first day of month (defined by frequency)
    # is_month_end	Logical indicating if last day of month (defined by frequency)
    # is_quarter_start	Logical indicating if first day of quarter (defined by frequency)
    # is_quarter_end	Logical indicating if last day of quarter (defined by frequency)
    # is_year_start	Logical indicating if first day of year (defined by frequency)
    # is_year_end	Logical indicating if last day of year (defined by frequency)


# 2.将索引按照指定格式显示

# 确保标签索引是日期型
# df.set_index(col,inplace=True)
df.index = df[col]

# A或Y年，Q季度，M月，D日，H时，T分，S秒
df2 = df.to_period('D')
print(df2.head())

# 3.按日期统计注册人数
valCol = '用户ID'
sr = df[valCol].resample('Y').count()    #按年统计
print(sr)

sr = df[valCol].resample('Y').count().to_period('Y')
print(sr)

sr = df[valCol].resample('Q').count().to_period('Q')
sr = df[valCol].resample('M').count().to_period('M')
sr = df[valCol].resample('D').count().to_period('D')
sr = df[valCol].resample('5Min').count().to_period('5Min')
print(sr)

# 3.筛选日期数据

filename = '用户明细.csv'
df = pd.read_csv(filename)

# 确保数据类型正确
col = '注册日期'
df[col] = df[col].astype('datetime64[ns]')
print(df.dtypes)

# 确保标签索引是日期型
# df.set_index(col,inplace=True)
df.index = df[col]

#按年筛选
df2 = df['2011']
df2 = df['2011':'2015']

#按月、日筛选
df2 = df['2011-9'] 
df2 = df['2011-8':'2012-3']
df2 = df['2011-8-1':'2011-9-1']
df2 = df['2011-07-01':'2011-08']


df2 = df[:'2011-02-1']     #2.1号之前(包含)的数据
df2 = df['2011-09-1':]     #9.1号之后(包含)


# 关于日期描述字符. 下面中的简写C-custom, B-business,
# B business day
# C custom business day
######### 年份
# A year end
# BA business year end
# AS year start
# BAS business year start
######### 季节
# Q quarter end
# BQ business quarter end
# QS quarter start
# BQS business quarter start
######### 月份
# M month end
# BM business month end 
# CBM custom business month end
# MS month start
######### 半月份
# SMS semi-month start
# SM semi-month end(15th and end of month)
# BMS custom business start
# CBMS custom business month start
######### 周
# W weekly
######### 日
# D calendar day
######### 小时
# BH business hour
# H hourly 
######### 分钟
# T,min minutely
######### 秒
# S secondly
######### 毫秒
# L,ms microseconds
######### 微秒
# N  nanoseconds

