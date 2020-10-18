#-*- coding: utf-8 -*- 

########  本文件实现数据集的读取与保存操作，包括
# Part 1.手工构造数据集
# Part 2.从CSV文件读取
# Part 3.从Excel文件读取
# Part 4.从数据库读取
# Part 5.保存数据集
######################################################################

import numpy as np
import pandas as pd

######################################################################
########  Part 1.手工构造数据集
######################################################################

# 1、创建索引Index
# 
idx = pd.Index([1,2,3], dtype=None)
print(idx)

idx = pd.Index(range(10))   #RangeIndex
print(idx)

idx = pd.Index(data=list('abc'), name='人员')
print(idx)

dates = ['2020-01-01', '2020-05-01']
idx = pd.DatetimeIndex(         #DatetimeIndex
        data=dates,
        name='日期')
print(idx)

# 索引类对象Index
# Int64Index, UInt64Index, Float64Index
# RangeIndex, 
# CategoricalIndex, 
# IntervalIndex, 
# MultiIndex,
# DatetimeIndex, TimedeltaIndex, PeriodIndex, 

# 2、创建序列Series
# 
# 默认的位置索引
sr = pd.Series([4,7,5,3])
sr.index.name='工作年限'
print(sr)

# 指定标签索引
sr = pd.Series([4,7,5,3], index=['a','b','c','d'], 
            name='工作年限',dtype='int8')
sr.index.name='人员'
print(sr)

# 指定标签索引
sr = pd.Series([1,'John',25,'初中毕业'],
            index=['ID','name','age','education'],
            name='个人信息',
            dtype='object')
print(sr)

# 访问series中单个索引对应的值
print(sr['name'])
print(sr['age'])


# 3、创建数据集DataFrame
idx = pd.date_range('5/1/2018', periods=8)
df = pd.DataFrame(np.random.randn(8, 3), index=idx,
                    columns=['A', 'B', 'C'])
print(df)

# pandas.date_range
    # (start=None, end=None, periods=None, freq=None, tz=None, 
    #                   normalize=False, name=None, closed=None, **kwargs)
    # start : str or datetime-like, optional，起始时间
    # end : str or datetime-like, optional，终止时间
    # periods : integer, optional，周期数量
    # freq : str or DateOffset, default ‘D’，周期偏移
        # Frequency strings can have multiples, e.g. ‘5H’. See here for a list of frequency aliases.
    # tz : str or tzinfo, optional 时区名如‘Asia/Hong_Kong’，默认为当地时区timezone-naive
    # normalize : bool, default False，
    # Normalize start/end dates to midnight before generating date range.
    # name : str, default None，Name of the resulting DatetimeIndex.
    # closed : {None, ‘left’, ‘right’}, optional
        # Make the interval closed with respect to the given frequency to the ‘left’, ‘right’, or both sides (None, the default).
    # **kwargs
        # For compatibility. Has no effect on the result.


######################################################################
########  Part 2.从CSV文件读取
######################################################################

# 默认以utf-8编码格式
filename = '用户明细.csv'
df = pd.read_csv(filename)      #索引为整数索引（0~N） 
print(df.columns.tolist())      #标题名称
print(df.head())

# 也可指定编码格式
filename = 'Telephone.csv'
df2 = pd.read_csv(filename,encoding='gbk')
print(df2.columns.tolist())      #标题名称

# 其它常用参数
# skiprows，跳过指定的行数不要读
# nrows，读取指定的行数
# index_col，指定该列当成标签索引列
    # 也可以在读取完成后重新设置索引列
    # df = pd.read_csv(filename)
    # df.set_index('用户ID', inplace=True)
    # print(df.head())

# pandas.read_csv
    # (filepath_or_buffer, sep=sep, delimiter=None, header='infer', 
    #           names=None, index_col=None, usecols=None, squeeze=False, 
    #           prefix=None, mangle_dupe_cols=True, dtype=None, engine=None, 
    #           converters=None, true_values=None, false_values=None, 
    #           skipinitialspace=False, skiprows=None, skipfooter=0, nrows=None, 
    #           na_values=None, keep_default_na=True, na_filter=True, verbose=False, 
    #           skip_blank_lines=True, parse_dates=False, infer_datetime_format=False, 
    #           keep_date_col=False, date_parser=None, dayfirst=False, iterator=False, 
    #           chunksize=None, compression='infer', thousands=None, decimal=b'.', 
    #           lineterminator=None, quotechar='"', quoting=csv.QUOTE_MINIMAL, 
    #           doublequote=True, escapechar=None, comment=None, encoding=None, 
    #           dialect=None, tupleize_cols=None, error_bad_lines=True, 
    #           warn_bad_lines=True, delim_whitespace=False, 
    #           low_memory=_c_parser_defaults['low_memory'], memory_map=False, 
    #           float_precision=None)
    # 重要说明：
    #sep 字段分隔符,默认为','。
    #header 指定列标题位置
    #   0，默认，表示第一行为标题；
    #   None，表示没有标题;
    #   列表，表示自定义标题）
    #index_col 指定索引列（默认None，为整数索引0~N；其它整数列表或标签列表，表示指定索引列）
    #encoding 指定编码格式(如'utf-8','gbk')


######################################################################
########  Part 3.从Excel文件读取
######################################################################

filename = '某公司销售数据.xlsx'
sheet = '全国订单明细'        #默认为第1个sheet
df3 = pd.read_excel(filename, sheet_name=sheet)


# # 一次读取多个sheet
# with pd.ExcelFile(filename) as xls:
#     dfUsers = pd.read_excel(xls, '用户明细', index_col='用户ID')
#     dfOrders = pd.read_excel(xls, '订购明细')


#pandas.read_excel
    # (io, sheet_name=0, header=0, names=None, index_col=None, 
    #           parse_cols=None, usecols=None, squeeze=False, dtype=None, 
    #           engine=None, converters=None, true_values=None, 
    #           false_values=None, skiprows=None, nrows=None, na_values=None, 
    #           keep_default_na=True, verbose=False, parse_dates=False, 
    #           date_parser=None, thousands=None, comment=None, skip_footer=0, 
    #           skipfooter=0, convert_float=True, mangle_dupe_cols=True, kwds)


######################################################################
########  Part 4.从数据库读取
######################################################################
# 略





######################################################################
########  Part 5.保存数据集
######################################################################

# 假定前面数据集df已经处理好

# 1、保存为CSV文件
outfile = 'outfile.csv'
df.to_csv(outfile)  #保存数据集

# 2、保存为Excel文件
# 需要openyxl扩展包: pip install openpyxl

outfile = 'outfile.xlsx'
# 如果df中带中文，也可以指定编码gbk或者utf_8_sig
df.to_excel(outfile, index=False, encoding='gbk')

# DataFrame.to_csv
    # (path_or_buf=None, sep=', ', na_rep='', 
    #       float_format=None, columns=None, header=True, index=True, index_label=None, 
    #       mode='w', encoding=None, compression='infer', quoting=None, quotechar='"', 
    #       line_terminator=None, chunksize=None, tupleize_cols=None, date_format=None, 
    #       doublequote=True, escapechar=None, decimal='.')
    # 重要参数说明：
    # sep    字段分隔符
    # header 是否要保存标题
    # index  是否要保存索引。默认保存索引，一般整数索引时不建议保存
    # 

# DataFrame.to_excel
    # (excel_writer, sheet_name='Sheet1', na_rep='', float_format=None, 
    #       columns=None, header=True, index=True, index_label=None, startrow=0, startcol=0, 
    #       engine=None, merge_cells=True, encoding=None, inf_rep='inf', verbose=True, 
    #       freeze_panes=None)
    # 重要参数说明
    # sheet_name 可以指定保存的sheet名称
    # index 是否要保存索引（需要设置df.index.name-索引标题名称）
    # header 是否要保存标题



# 文件、目录表示形式================

## 2.1）windows系统的路径表示
# 绝对路径
# path = r'C:\Users\OneDrive\Python\数据分析'       #注意前面有r字符
# path = 'C:\\Users\\OneDrive\\Python\\数据分析'    #或者用双反斜杠
# path = 'C:/Users/OneDrive/Python/数据分析'        #或者用斜杠即可

# 相对路径
# path = '.'    #当前路径
# path = '..'   #上一级路径
# path = '用户明细.csv'     #当前目录下的文件
# path = '../dataset/用户明细.csv'      #上一级目录下的dataset子目录下的文件

## 2.2）MACOS/Linux/Unix等操作
# 绝对路径
# filename = '/Users/fusx/Documents/OneDrive/Python/dataset/用户明细.csv' 
# 相对路径，类似windows表示

## 2.3）获取/修改当前工作目录

# 获取当前工作目录
import os
path = os.getcwd()
print(path)

# 更改当前工作目录
# path = '/Users/fusx/Documents/OneDrive/Python/数据分析'
# os.chdir(path)
