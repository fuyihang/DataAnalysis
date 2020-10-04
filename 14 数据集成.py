#-*- coding: utf-8 -*- 

"""
########  本文件实现数据集成功能，包括：
# 1.数据追加
# 2.变量合并
#   1）左连接、右连接
#   2）内连接、外连接
#   3）左反连接、右反连接
# 3.数据集拼接
######################################################################
"""

import pandas as pd
# import numpy as np

######################################################################
########  数据追加
######################################################################
# 两个表的结构基本相同， 数据行合并，标题相同的字段会对齐
# 没有的字段值默认为NaN

filename = '客服中心10月份来电记录表.txt'
Tel_10 = pd.read_csv(filename,encoding='gbk',sep='\t')
print(Tel_10.columns.tolist())
print(Tel_10.shape)

filename = '客服中心11月份来电记录表.csv'
Tel_11 = pd.read_csv(filename, encoding='gbk')
print(Tel_11.columns.tolist())
print(Tel_11.shape)

# 数据追加，合并10-11月份
dfTel = Tel_10.append(Tel_11, ignore_index=True)
print(dfTel.shape)

# DataFrame.append
    # (other, ignore_index=False, 
    #  verify_integrity=False, sort=None)
    # other : DataFrame or Series/dict-like object, or list of these
    # The data to append.
    # ignore_index : boolean, default False
    #       True表示重新生成索引，
    #       False表示使用原来的索引
    # verify_integrity : boolean, default False
    #       True如果有重复索引则抛出异常ValueError
    # sort : boolean, default None
    #       True表示原表已经排序
    #       False表示原表没有排序
    #       None默认，表示系统自行处理排序

######################################################################
########  变量合并
######################################################################
# 两个表变量合并，一般需要指明关联的主键
# 合并主键：
    # 默认按相同字段合并
    # 也可由on, left_on, right_on指定
# 表的合并类型how：
    # left, right, outer, inner


filename = '客服中心话务员个人信息表.xlsx'
sheet = '话务员信息表'
rgt = pd.read_excel(filename, sheet)
print(rgt.columns.tolist())
print(rgt.shape)

lft = dfTel

# 默认按相同字段进行合并,容易出错
df = lft.merge(rgt, how='inner')    #默认how='inner'
print(df.shape)

# 按指定主键字段合并
df = lft.merge(rgt, how='left',on='话务员工号')
print(df.columns.tolist())
# 同名字段会默认添加后缀,后缀由参数suffixes=['_x','_y']确定

#如果两个表的关键名字不相同，则使用left_on和right_on
# df = lft.merge(rgt, how='inner',left_on='学号1', right_on='学号2')

# DataFrame.merge
    # (self, right, how='inner', on=None, left_on=None, right_on=None, 
    #       left_index=False, right_index=False, sort=False, suffixes=('_x', '_y'), 
    #       copy=True, indicator=False, validate=None)
    # right : DataFrame or named Series.要合并的对象
    # how : {‘left’, ‘right’, ‘outer’, ‘inner’}, default ‘inner’连接类型
    # on : label or list
    #       指定关联的列名，或者索引级别名称。左表和右表都应该有相同的字段
    # left_on /right_on: label or list, or array-like
    #       指定关联的列名，或者索引级别名称
    # left_index/right_index : bool, default False
    #       True时，表示使用索引进行关联
    # sort : bool, default False。合并后是否排序
    # suffixes : tuple of (str, str), default (‘_x’, ‘_y’)
    #           两个表有重名标题时，自动添加的后缀
    #           如果设为(False, False)，则有重名时会异常
    # copy : bool, default True。是否返回复制的数据集
    # indicator : bool or str, default False
    #           If True, adds a column to output DataFrame called “_merge” with information on the source of each row. 
    #           If string, column with information on source of each row will be added to output DataFrame, 
    #           and column will be named value of string. 
    #           Information column is Categorical-type and takes on a value of “left_only” for observations whose merge key only appears in ‘left’ DataFrame, “right_only” for observations whose merge key only appears in ‘right’ DataFrame, 
    #           and “both” if the observation’s merge key is found in both.
    # validate : str, optional。指定类型的合并。
    # “one_to_one” or “1:1”: check if merge keys are unique in both left and right datasets.
    # “one_to_many” or “1:m”: check if merge keys are unique in left dataset.
    # “many_to_one” or “m:1”: check if merge keys are unique in right dataset.
    # “many_to_many” or “m:m”: allowed, but does not result in checks

# DataFrame.join
    # (other, on=None, how='left', lsuffix='', rsuffix='', sort=False)
    # other : DataFrame, Series, or list of DataFrame
    #   要合并的右表，左表和右表的索引应该是相似的
    #   如果是序列Series，则要有name属性（用作合并后的列名）
    # on : str, list of str, or array-like, optional
    #   左表按照指定的主键与右表的索引键关联
    #   默认None按索引关联。
    # how : {‘left’, ‘right’, ‘outer’, ‘inner’}, default ‘left’
    #   连接类型：左连接，右连接，外连接，内连接
    # lsuffix : str, default ‘’
    #   左表后缀（字段名称相同时）
    # rsuffix : str, default ‘’
    #   右表后续（字段名称相同时）
    # sort : bool, default False
    #   是否按主键排序


######################################################################
########  数据集的拼接
######################################################################
# 特殊的合并（横向或纵向）

# 准备数据集
cols1 = ['学号','姓名','年龄']
data = [[1, '大千', 18],
        [2, '王二', 17],
        [3, '张三', 16],
        [4, '李四', 19] ]
lft = pd.DataFrame(data, columns=cols1)

idx = lft.index + 1
cols2 = ['学号','成绩', '姓名']
data = [[3, 76, '张三'],
        [4, 94, '李四'],
        [5, 87, '武开'],
        [6, 70, '陆辰'] ]
rgt = pd.DataFrame(data, index=idx, columns=cols2)


######## 横向拼接，会考虑字段对齐，相当于数据追加
# join来指示如何选择哪些列columns
df = pd.concat([lft, rgt], axis=0, join='inner')

######## 纵向拼接，会考虑索引对齐
# join来指标选取哪些行indexs
df = pd.concat([lft, rgt], axis=1, join='inner')


# pandas.concat
    # (objs, axis=0, join='outer', join_axes=None, 
    #           ignore_index=False, keys=None, levels=None, names=None, 
    #           verify_integrity=False, sort=None, copy=True)
    # objs : a sequence or mapping of Series, DataFrame, or Panel objects
    # axis : {0/’index’, 1/’columns’}, default 0
    # join : {‘inner’, ‘outer’}, default ‘outer’.合并后的表格字段
    #       inner表示取两个表公共的字段
    #       outer表示取两个表所有的字段
    # join_axes : list of Index objects
    #       Specific indexes to use for the other n - 1 axes instead of performing inner/outer set logic
    # ignore_index : boolean, default False
    #       If True, do not use the index values along the concatenation axis. 
    #       The resulting axis will be labeled 0, …, n - 1. 
    #       This is useful if you are concatenating objects where the concatenation axis does not have meaningful indexing information. 
    #       Note the index values on the other axes are still respected in the join.
    # keys : sequence, default None
    #       If multiple levels passed, should contain tuples. Construct hierarchical index using the passed keys as the outermost level
    # levels : list of sequences, default None
    #       Specific levels (unique values) to use for constructing a MultiIndex. Otherwise they will be inferred from the keys
    # names : list, default None
    #       Names for the levels in the resulting hierarchical index
    # verify_integrity : boolean, default False
    #       Check whether the new concatenated axis contains duplicates. 
    #       This can be very expensive relative to the actual data concatenation
    # sort : boolean, default None
    #       Sort non-concatenation axis if it is not already aligned when join is ‘outer’. The current default of sorting is deprecated and will change to not-sorting in a future version of pandas.
    #       Explicitly pass sort=True to silence the warning and sort. Explicitly pass sort=False to silence the warning and not sort.
    #       This has no effect when join='inner', which already preserves the order of the non-concatenation axis.
    # copy : boolean, default True
    #       If False, do not copy data unnecessarily

######################################################################
# outfile = 'outfile.xls'
# df.to_excel(outfile, index=False)
