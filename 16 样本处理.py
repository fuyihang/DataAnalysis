#-*- coding: utf-8 -*- 

import pandas as pd
import numpy as np

"""
########  本文件实现样本处理功能，包括：
# 1.筛选
# 2.抽样
#   2.1 简单抽样（不放回，放回）
#   2.2 间隔抽样
#   2.3 分层抽样
#   2.4 聚类抽样
# 3.样本平衡(同第1)
#   4.1 欠抽样
#   4.2 过抽样
######################################################################
"""

#读取数据集
filename = '../dataset/用户明细.csv'
df = pd.read_csv(filename)
print(df.columns.tolist())

######################################################################
########  筛选，见基础操作
######################################################################
cond = df['年龄'] > 20       #指定筛选条件
df2 = df[cond]              #进行筛选

######################################################################
########  抽样
######################################################################
# 行抽样和列抽样(由axis来决定)

# 1、随机排序（打乱数值集顺序）
np.random.seed(seed=2)      # 如果使用相同的seed种子，则每次生成的随即数都相同
sampler = np.random.permutation(len(df))    #生成0~len(df)-1范围内的随机排列数组

df2 = df.take(sampler, axis=0)                  #行抽样

# 2、随机抽样

# 2.1 无放回随机抽样

# 使用随机数组
sampler = np.random.randint(0,len(df),size=100) #生成100个随机数
df2 = df.take(sampler, axis=0)

# 抽取整数个
df2 = df.sample(n=100)

# 抽取百分比
df2 = df.sample(frac=.5)

# 2.2 有放回随机抽样（replace=True表示有放回）
df2 = df.sample(n=100, replace=True)

# 查看重复的值，会看到有很多
dpl = df2[df2.duplicated(subset=['用户ID'])]

# 3、分层抽样
gbr=df.groupby('性别')      #以字段进行分层

dctSampleNum={'男':20, '女':40}     #抽取个数

def typicalsamling(group,dctSampleNum):
    num = dctSampleNum[group.name]  #group.name保存性别的取值
    return group.sample(n=num)      #各组抽取的个数

df2 = df.groupby('性别', group_keys=False).apply(typicalsamling,dctSampleNum)


# 相关函数
    # DataFrame.take(indices, axis=0, convert=None, is_copy=True, **kwargs)
    # indices : array-like。整数数组来表示哪个位置
    # axis : {0 or ‘index’, 1 or ‘columns’, None}, default 0 行抽样还是列抽样
    # convert : bool, default True
    # Whether to convert negative indices into positive ones. For example, -1 would map to the len(axis) - 1. The conversions are similar to the behavior of indexing a regular Python list.
    # is_copy : bool, default True
    # Whether to return a copy of the original object or not.
    # **kwargs
    # For compatibility with numpy.take(). Has no effect on the output.

    # DataFrame.sample(n=None, frac=None, replace=False, weights=None, 
    #               random_state=None, axis=None)
    # n : int, optional,抽取的样本数量
    # frac : float, optional。抽取的样本的百分比
    # replace : bool, default False是否有放回抽样
    # weights : str or ndarray-like, optional
    # Default ‘None’ results in equal probability weighting. If passed a Series, will align with target object on index. Index values in weights not found in sampled object will be ignored and index values in sampled object not in weights will be assigned weights of zero. If called on a DataFrame, will accept the name of a column when axis = 0. Unless weights are a Series, weights must be same length as axis being sampled. If weights do not sum to 1, they will be normalized to sum to 1. Missing values in the weights column will be treated as zero. Infinite values not allowed.
    # random_state : int or numpy.random.RandomState, optional
    # Seed for the random number generator (if int), or numpy RandomState object.
    # axis : int or string, optional
    # Axis to sample. Accepts axis number or name. Default is stat axis for given data type (0 for Series and DataFrames, 1 for Panels).

    # DataFrame.groupby(by=None, axis=0, level=None, as_index=True, sort=True, 
    #           group_keys=True, squeeze=False, observed=False, **kwargs)
    # by : mapping, function, label, or list of labels
    # Used to determine the groups for the groupby. If by is a function, it’s called on each value of the object’s index. If a dict or Series is passed, the Series or dict VALUES will be used to determine the groups (the Series’ values are first aligned; see .align() method). If an ndarray is passed, the values are used as-is determine the groups. A label or list of labels may be passed to group by the columns in self. Notice that a tuple is interpreted a (single) key.
    # axis : {0 or ‘index’, 1 or ‘columns’}, default 0
    # Split along rows (0) or columns (1).
    # level : int, level name, or sequence of such, default None
    # If the axis is a MultiIndex (hierarchical), group by a particular level or levels.
    # as_index : bool, default True
    # For aggregated output, return object with group labels as the index. Only relevant for DataFrame input. as_index=False is effectively “SQL-style” grouped output.
    # sort : bool, default True
    # Sort group keys. Get better performance by turning this off. Note this does not influence the order of observations within each group. Groupby preserves the order of rows within each group.
    # group_keys : bool, default True
    # When calling apply, add group keys to index to identify pieces.
    # squeeze : bool, default False
    # Reduce the dimensionality of the return type if possible, otherwise return a consistent type.
    # observed : bool, default False
    # This only applies if any of the groupers are Categoricals. If True: only show observed values for categorical groupers. If False: show all values for categorical groupers.
    # New in version 0.23.0.
    # **kwargs
    # Optional, only accepts keyword argument ‘mutated’ and is passed to groupby.


######################################################################
########  样本平衡
######################################################################

