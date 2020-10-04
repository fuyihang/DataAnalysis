#-*- coding: utf-8 -*- 

"""
########  本文件实现数据集的基础操作，包括
# 一.数据集构造
    # 1.手工构造
    # 2.路径表示
    # 3.读取CSV文件
    # 4.读取Excel文件
    # 5.读取数据库（略）
# 二.数据集的基本操作
    # 1. 数据集属性
    # 2. 数据类型
    # 3. 排序
    # 4. 数据访问：行、列、块访问、值
    # 5. 数据新增：行、列, 新增/插入
    # 6. 数据修改：修改单值、重新编码、替换行列
    # 7. 数据删除：行、列、空值
    # 8. 数据操作：移位、转置、筛选、空值检测、非空值检测
# 三.保存数据集

######################################################################
""" 

import numpy as np
import pandas as pd

######################################################################
########  一、数据集构造
######################################################################

# 1、手工创建数据集================

##1.1）创建索引Index
# 
idx = pd.Index([1,2,3])
print(idx)

idx = pd.Index(data=list('abc'), name='人员')
print(idx)

dates = ['2020-01-01', '2020-02-01']
idx = pd.DatetimeIndex(
        data=dates,
        name='日期')
print(idx)

# 还有其它索引类对象
# RangeIndex, CategoricalIndex, IntervalIndex, 
# MultiIndex,
# DatetimeIndex, TimedeltaIndex, PeriodIndex, 
# Int64Index, UInt64Index, Float64Index

##1.2）创建序列Series
# 
# 默认位置索引
sr = pd.Series([1,'John',25,'初中毕业'])
print(sr.to_list())

# 指定标签索引
sr = pd.Series([4,7,5,3], index=['a','b','c','d'], 
            name='工作年限',dtype='int8')
sr.index.name='人员'

##1.3）创建数据集DataFrame
idx = pd.date_range('5/1/2018', periods=8)
df = pd.DataFrame(np.random.randn(8, 3), index=idx,
                    columns=['A', 'B', 'C'])
col = 'A'
cols = ['A', 'C']


# 2、文件、目录表示形式================

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

# 3、读取CSV文件================

# 默认以utf-8编码格式
filename = '用户明细.csv'
df = pd.read_csv(filename)      #索引为整数索引（0~N） 
print(df.columns.tolist())      #标题名称
print(df.head())

sr = df['性别'].value_counts()
sr.plot(kind='bar', title=sr.name)

# # 也可指定编码格式
# filename = 'Telephone.csv'
# df2 = pd.read_csv(filename,encoding='gbk')
# print(df2.columns.tolist())      #标题名称

# 其它常用参数
# skiprows，跳过指定的行数不要读
# nrows，读取指定的行数
# index_col，指定该列当成标签索引列
    # 也可以在读取完成后重新设置索引列
    # df = pd.read_csv(filename)
    # df.set_index('用户ID', inplace=True)
    # print(df.head())

# 4、读取Excel文件================

filename = '某公司销售数据.xlsx'
sheetname = '全国订单明细'        #默认为第1个sheet
df3 = pd.read_excel(filename, sheet_name=sheetname)

# # 一次读取多个sheet
# with pd.ExcelFile(filename) as xls:
#     dfUsers = pd.read_excel(xls, '用户明细', index_col='用户ID')
#     dfOrders = pd.read_excel(xls, '订购明细')

# 5、从数据库读取（略）================



# 相关函数
    # 读CSV文件
    # pandas.read_csv(filepath_or_buffer, sep=sep, delimiter=None, header='infer', 
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

    # 读Excel文件
    # pandas.read_excel(io, sheet_name=0, header=0, names=None, index_col=None, 
    #           parse_cols=None, usecols=None, squeeze=False, dtype=None, 
    #           engine=None, converters=None, true_values=None, 
    #           false_values=None, skiprows=None, nrows=None, na_values=None, 
    #           keep_default_na=True, verbose=False, parse_dates=False, 
    #           date_parser=None, thousands=None, comment=None, skip_footer=0, 
    #           skipfooter=0, convert_float=True, mangle_dupe_cols=True, kwds)

    # 时间范围
    # pandas.date_range(start=None, end=None, periods=None, freq=None, tz=None, 
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
########  二、数据常规操行
######################################################################

################# 数据集基本属性 ################

df = dfUsers

print('数据集的行数、列数：', df.shape)
print('数据集的行数：', df.shape[0])
print('数据集的列数：', df.shape[1])

print('数据集的索引：', df.index)
#可以给索引列一个标题（后续保存时的字段名）
df.index.name = '序号'

print('数据集的标题：',df.columns)
# lt = df.columns.to_list()

print('数据集的值：\n', df.values)

print('数据集的维度：',df.ndim)     #一般DataFrame为2维，Series为1维

print('数据集是否为空：',df.empty)  #bool型

print('数据的个数：',df.size)     #等于=行数*列数

################# 列访问 ################
##访问方式有两种：
# 1.位置索引position：按位置顺序(整数)索引,iloc
# 2.标签索引Label：   按字段标题/索引标签,loc

# 1.按标题名称访问
sr = df.loc[:, '年龄']    #
sr = df['年龄']           #单列，返回Series对象

df2 = df[['年龄']]         #如果这样，则返回DataFrame对象

df2 = df[['用户ID','年龄']]     #多列，返回DataFrame对象
# 相当于df2 = df.loc[:, ['用户ID','年龄']]

# 2.按位置索引访问
sr  = df.iloc[:, 2]     #单列
df2 = df.iloc[:, [0,2]] #多列
df2 = df.iloc[:, 0:3]   #连续列

################# 数据类型 ################
# dtype的取值字符串含义
# 字符串：object
# 整型：int8, int16, int32, int64(默认-int)，以及uint8, uint16, uint32, uint64
# 浮点数：float16, float32, float/float64(默认), float128
# 复数：complex64, complex128, complex256
# 布尔型：bool
# 日期：datetime64[ns]
# 时间差：timedelta64[ns]
# 特殊的类别变量：category

# 1.查询所有列的数据类型
sr = df.dtypes    #返回Series

# 查看各类型的字段个数
# sr = df.get_dtype_counts()
sr = df.dtypes.value_counts()

# 2.查看指定字段的数据类型
type = df.dtypes['年龄']

# 3.判断字段类型
if df.dtypes['年龄'] == np.int:
    print('该列是int类型')

# 4.修改指定列的数据类型
# 注：如果转换失败（比如有空值），默认会抛出异常; 指定errors='ignore'就表示不要抛出异常
df['年龄'] = df['年龄'].astype('int8', errors='ignore')
df['年龄'] = df['年龄'].astype(np.int8, errors='ignore')

# 5。指定多列修改类型。注意两种语句返回值的差异。
#一列一个类型，返回全部列
df2 = df.astype({'用户ID':'int32','年龄':'int8'})

#多列一个类型，只返回2列
df2 = df[['用户ID','年龄']].astype('int32')
df[['用户ID','年龄']] = df2     #则会修改原来的数据集

# 6.转换数据类型
df['年龄'] = pd.to_numeric(df['年龄'], downcast='float')

df['注册日期'] = pd.to_datetime(df['注册日期'], format='%Y/%m/%d')

# 7.也可使用apply函数转换
# 类似的函数有pd.to_datetime，pd.to_timedelta
df['年龄'] = df['年龄'].apply(pd.to_numeric).astype('int8')
df['注册日期'] = df['注册日期'].apply(pd.to_datetime, format='%Y/%m/%d')

# 8.显示小数位数
# df[col].round(decimals=2)         #只显示小数点后2位，四舍五入
# df[col].map(lambda x: ('%.2f')%x) #自定义函数显示格式，但注意返回的类型是字符串哟


# 9.设置所有列的数据类型
# 不太常用,注意不会修改原数据集。
# df2 = df.astype('int32')

# 相关函数
    # 选取指定类型的数据集
    # df2 = df.select_dtypes(include=['number', 'object'], exclude=['unsignedinteger'])

    # DataFrame.astype(dtype, copy=True, errors='raise', **kwargs)[source]
    # dtype: data type, or {col:dtype,...}
    # copy: bool ,default True,默认返回一个复制列，而不是原始列
    # errors : {‘raise’, ‘ignore’}, default ‘raise’ 是否抛出异常
    # 注：如果df中有空值，默认会异常; 所以，需要设置errors='ignore'
    # 一般建议使用pd.numeric等函数

# 转换为数字
    # pandas.to_numeric(arg, errors='raise', downcast=None)
    # arg : list, tuple, 1-d array, or Series
    # errors : {‘ignore’, ‘raise’, ‘coerce(置为Nan)’}, 
    # downcast : {‘integer’, ‘signed’, ‘unsigned’, ‘float’} 
    #           None：默认float64
    #           integer or signed:表示最小的有符号整数np.int8
    #           unsigned: 表示最小的无符号整数np.uint8
    #           float: 表示最小的浮点数np.float32

# 转换为日期
    # pandas.to_datetime(arg, errors='raise', dayfirst=False, yearfirst=False, 
    #           utc=None, box=True, format=None, exact=True, unit=None, 
    #           infer_datetime_format=False, origin='unix', cache=False)
    # arg : integer, float, string, datetime, list, tuple, 1-d array, Series, or DataFrame/dict-like
    # errors : {‘ignore’, ‘raise’, ‘coerce’}, default ‘raise’
    # dayfirst : boolean, default False
    # Specify a date parse order if arg is str or its list-likes. If True, parses dates with the day first, eg 10/11/12 is parsed as 2012-11-10. Warning: dayfirst=True is not strict, but will prefer to parse with day first (this is a known bug, based on dateutil behavior).
    # yearfirst : boolean, default False
    # Specify a date parse order if arg is str or its list-likes.
    # If True parses dates with the year first, eg 10/11/12 is parsed as 2010-11-12.
    # If both dayfirst and yearfirst are True, yearfirst is preceded (same as dateutil).
    # Warning: yearfirst=True is not strict, but will prefer to parse with year first (this is a known bug, based on dateutil behavior).
    # New in version 0.16.1.
    # utc : boolean, default None
    # Return UTC DatetimeIndex if True (converting any tz-aware datetime.datetime objects as well).
    # box : boolean, default True
    # If True returns a DatetimeIndex or Index-like object
    # If False returns ndarray of values.
    # format : string, 格式字符串“%d/%m/%Y”, note that “%f” will parse all the way up to nanoseconds.
    # exact : boolean, True by default
    # If True, require an exact format match.
    # If False, allow the format to match anywhere in the target string.
    # unit : string, default ‘ns’
    # unit of the arg (D,s,ms,us,ns) denote the unit, which is an integer or float number. This will be based off the origin. Example, with unit=’ms’ and origin=’unix’ (the default), this would calculate the number of milliseconds to the unix epoch start.
    # infer_datetime_format : boolean, default False
    # If True and no format is given, attempt to infer the format of the datetime strings, and if it can be inferred, switch to a faster method of parsing them. In some cases this can increase the parsing speed by ~5-10x.
    # origin : scalar, default is ‘unix’
    # Define the reference date. The numeric values would be parsed as number of units (defined by unit) since this reference date.
    # If ‘unix’ (or POSIX) time; origin is set to 1970-01-01.
    # If ‘julian’, unit must be ‘D’, and origin is set to beginning of Julian Calendar. Julian day number 0 is assigned to the day starting at noon on January 1, 4713 BC.
    # If Timestamp convertible, origin is set to Timestamp identified by origin.
    # New in version 0.20.0.
    # cache : boolean, default False
    # If True, use a cache of unique, converted dates to apply the datetime conversion. May produce significant speed-up when parsing duplicate date strings, especially ones with timezone offsets.
    # New in version 0.23.0.

# 转换为日期差
    # pandas.to_timedelta(arg, unit='ns', box=True, errors='raise')
    # arg : str, timedelta, list-like or Series.
    # unit : str, default ‘ns’. arg的单位(‘Y’, ‘M’, ‘W’, ‘D’, ‘days’, ‘day’, ‘hours’, hour’, ‘hr’, ‘h’, ‘m’, ‘minute’, ‘min’, ‘minutes’, ‘T’, ‘S’, ‘seconds’, ‘sec’, ‘second’, ‘ms’, ‘milliseconds’, ‘millisecond’, ‘milli’, ‘millis’, ‘L’, ‘us’, ‘microseconds’, ‘microsecond’, ‘micro’, ‘micros’, ‘U’, ‘ns’, ‘nanoseconds’, ‘nano’, ‘nanos’, ‘nanosecond’, ‘N’).
    # box : bool, default True
    #       If True returns a Timedelta/TimedeltaIndex of the results.
    #       If False returns a numpy.timedelta64 or numpy.darray of values of dtype timedelta64[ns].
    # errors : {‘ignore’, ‘raise’, ‘coerce’}, default ‘raise’
    #       If ‘raise’, then invalid parsing will raise an exception.
    #       If ‘coerce’, then invalid parsing will be set as NaT.
    #       If ‘ignore’, then invalid parsing will return the input.

# 自定义函数 转换
    #DataFrame.apply(func, axis=0, broadcast=None, raw=False, reduce=None, 
    #       result_type=None, args=(), **kwds)
    #func : Function to apply to each column or row.
    # axis : {0 or ‘index’, 1 or ‘columns’}, default 0
    # broadcast : bool, optional
    #   Only relevant for aggregation functions:
    #   False or None : returns a Series whose length is the length of the index or the number of columns (based on the axis parameter)
    #   True : results will be broadcast to the original shape of the frame, the original index and columns will be retained.
    # raw : bool, default False
    #   False : passes each row or column as a Series to the function.
    #   True : the passed function will receive ndarray objects instead. If you are just applying a NumPy reduction function this will achieve much better performance.
    # reduce : bool or None, default None
    #   Try to apply reduction procedures. If the DataFrame is empty, apply will use reduce to determine whether the result should be a Series or a DataFrame. If reduce=None (the default), apply’s return value will be guessed by calling func on an empty Series (note: while guessing, exceptions raised by func will be ignored). If reduce=True a Series will always be returned, and if reduce=False a DataFrame will always be returned.
    # result_type : {‘expand’, ‘reduce’, ‘broadcast’, None}, default None
    #   These only act when axis=1 (columns):
    #   ‘expand’ : list-like results will be turned into columns.
    #   ‘reduce’ : returns a Series if possible rather than expanding list-like results. This is the opposite of ‘expand’.
    #   ‘broadcast’ : results will be broadcast to the original shape of the DataFrame, the original index and columns will be retained.
    #   The default behaviour (None) depends on the return value of the applied function: list-like results will be returned as a Series of those. However if the apply function returns a Series these are expanded to columns.
    # args : tuple
    #   Positional arguments to pass to func in addition to the array/series.
    # **kwds
    #   Additional keyword arguments to pass as keywords arguments to func.

# Numpy中数据类型层次
    # numpy.generic,
    #   numpy.bool_,
    #   numpy.datetime64,
    #   numpy.object_]
    #  [[numpy.number,
    #    [[numpy.integer,
    #      [numpy.signedinteger,
        #        numpy.int8,
        #         numpy.int16,
        #         numpy.int32,
        #         numpy.int64, numpy.int
        #         numpy.int64,
        #         numpy.timedelta64,
    #       [numpy.unsignedinteger,
        #         numpy.uint8,
        #         numpy.uint16,
        #         numpy.uint32,
        #         numpy.uint64,
        #         numpy.uint64]]],
    #     [numpy.inexact,
    #      [[numpy.floating,
    #        [numpy.float16, numpy.float32, numpy.float64, numpy.float128]],
    #       [numpy.complexfloating,
    #        [numpy.complex64, numpy.complex128, numpy.complex256]]]]]],
    #   [numpy.flexible,
    #    [[numpy.character, [numpy.bytes_, numpy.str_]],
    #     [numpy.void, [numpy.record]]]],
    #   还有一个特殊的category，表示类别变量

################# 排序 ################

# 升降序
# 1.列标题排序(默认升序),注意：默认inplace=False原数据集不改变
df2 = df.sort_index(axis=1, ascending=False)
df2 = df.sort_index(axis='columns', ascending=False)

# 2.按索引排序
df2 = df.sort_index(axis='index', ascending=False)
df2 = df.sort_index()    #默认axis=0，ascending=True

# 3.按指定字段
df2 = df.sort_values(by='年龄', ascending= True)

# 4.多字段排序
df2 = df.sort_values(by=['省份','性别'], ascending= True)
df2 = df.sort_values(by=['省份','性别'], ascending=[True, False]) #不同字段排序方式不一样

# 自定义顺序

# 5.按标题 自定义排序
cols = ['用户ID','年龄','省份','性别','注册日期']   #指定标题顺序
df2 = df.reindex(columns=cols)
df2 = df.reindex(cols, axis='columns')

# 6.按索引 自定义排序
# 比如将空值提前显示
age = df.loc[2,'年龄']
df.loc[2,'年龄'] = np.nan

df2 = df['年龄'].sort_values(na_position='first')  #df2空值在前
df = df.reindex(df2.index)         #将df重新按照指定的索引排序
# df = df.reindex(df2.index, asxis = 'index')

#恢复数据及顺序
df.loc[2,'年龄'] = age  
df.sort_index(axis=0, ascending=True, inplace=True)

# 7.按字段 自定义排序。
# 字段为有序类型，比如学历
#自定义顺序列表
eduList = ['初中','高中','大专','本科','研究生'] 

#先构造一个学历字段（字符串类型）
#有放回抽样
srEdu = pd.Series(eduList).sample(n=len(df), replace=True)
srEdu.index = range(len(df))    #重新赋值索引
df['学历'] = srEdu

# 修改字段类型为category类型,并设定顺序
df['学历'] = df['学历'].astype('category').cat.set_categories(eduList)

#按学历高低进行升序
df2 = df.sort_values(by='学历', ascending=True)

# 按索引/标题进行排序
    # DataFrame.sort_index(axis=0, level=None, ascending=True, inplace=False, kind='quicksort', 
    #                       na_position='last', sort_remaining=True, by=None)
    # axis = 0或'index', 默认行排序，按索引值排序，
    # axis = 1或'columns'，表示标题排序，
    # level : int or level name or list of ints or list of level names
    #       if not None, sort on values in specified index level(s)
    # ascending 升序或降序
    # inplace : bool, 是否修改原数据集
    # kind : {‘quicksort’, ‘mergesort’, ‘heapsort’}, 排序算法
    # na_position : {‘first’, ‘last’} 排序后空值的位置
    # sort_remaining : bool

# 按字段值进行排序
    # DataFrame.sort_values(by, axis=0, ascending=True, inplace=False, 
    #                       kind='quicksort', na_position='last')
    # by : str or list of str
    # axis : {0 or ‘index’, 1 or ‘columns’},
    # 当axis=1时，by应该为行索引（要求所有字段的类型都相同，否则出现整形和字符串型比较，抛出异常），较少用。
    # kind : {‘quicksort’, ‘mergesort’, ‘heapsort’}
    # na_position : {‘first’, ‘last’}

# 按自定义的索引/标题进行排序
    # DataFrame.reindex(labels=None, index=None, columns=None, axis=None, method=None, copy=True, 
    #                   level=None, fill_value=nan, limit=None, tolerance=None)
    # labels : array-like, optional 指定排序的列表，默认是索引列表
    # index, columns : array-like, optional指定索引和标题的排序
    # axis ：指明前面的标签是索引还是标题
    # method : {None, ‘backfill’/’bfill’, ‘pad’/’ffill’, ‘nearest’} 如果缺失时的填充方式
    # level : int or name
    #       Broadcast across a level, matching Index values on the passed MultiIndex level.
    # fill_value : scalar, default np.NaN 数据缺失时，默认填充的值
    # limit : int, default None 填充时的最大次数
    # tolerance : optional

################# 行访问 ################
# 行访问，即按索引访问。有两种索引方式：
# 位置索引position，即iloc元组
# 标签索引Label：即loc元组

# 1.位置索引
sr  = df.iloc[2]       #单行，返回Series对象
df2 = df.iloc[[1,2,4]] #多行，指定行号列表，返回DataFrame
df2 = df.iloc[0:10]    #连续行，切片访问

# 2.标签索引，整数标签
# 要将dfUsers的索引重新设置为'用户ID'
df.set_index('用户ID', inplace=True)

sr = df.loc[100000]                    #单行
df2 = df.loc[[100000,100002,100004]]   #多行
df2 = df.loc[100000:100004]            #连续行

# 3.布尔数组,布尔列表
# 常用于筛选（判断条件返回的都是布尔数组）
cond = df['省份'] == '广东'     #cond变量一个bool数组
df2 = df.loc[cond] 
df2 = df[cond]     #经常简写成这样


## 4.标签索引，日期标签
# # 单行
# sr  = df.loc[pd.to_datetime('20180502')]
# sr  = df.loc['20180502']    #好像使用字符串日期也可以

# # 多行，不连续行
# rows = [pd.to_datetime('20180502'), pd.to_datetime('20180504')]
# df2 = df.loc[rows]
# # df2 = df.loc[['20180502', '20180504']]   #这样不行
# df2 = df.loc[[pd.to_datetime('20180502'),pd.to_datetime('20180504')]]

# # 连续行
# df2 = df.loc['2018-05-02':'2018-05-04']
# df2 = df.loc['2018-05-04':'2018-06']          #这样也可以
# # 或者
# rows = pd.date_range(start='20180502',end='20180504')
# df2 = df.loc[rows]

################# 块访问，多行多列 ################
# 1.位置索引
df2 = df.iloc[2:5, 0:2]         #连续行或列，切片访问
df2 = df.iloc[[1,2,4], [0,2]]   #不连续行或列，列表
df2 = df.iloc[[1,2,4], 0:3]     #混合
srRow = df.iloc[2,0:3]          #单行多列
srCol = df.iloc[2:5, 2]         #单列多行

# 2.标签索引
cols = ['省份','性别']
print(df.head())
df2 = df.loc[[100000,100002,100006], cols] #不连续行 
df2 = df.loc[100000:100006, cols]          #连续行

sr = df.loc[100000, cols]                  #单行多列
sr = df.loc[[100000,100002,100006], '性别'] #单列多行,非连续行
sr = df.loc[100000:100006, '性别']          #单列多行，连续行

# # 3.标签索引，日期标签
# cols = ['A','C']
# #连续行
# df2 = df.loc['20180502':'20180504', cols]
# rows = pd.date_range(start='20180502',end='20180504')
# df2 = df.loc[rows,cols]
# # 不连续行
# rows = [pd.to_datetime('20180502'), pd.to_datetime('20180504')]
# df2 = df.loc[rows, cols]
# # 单行多列
# srRow = df.loc['20180502', cols]
# srRow = df.loc[pd.to_datetime('20180502'), cols]
# # 多行单列
# rows = pd.date_range(start='20180502',end='20180504')
# srCol = df.loc[rows, 'B']
# srCol = df.loc['20180502':'20180504', 'B']

################# 字段值访问 ################
# 1.位置索引
val = df.iloc[5, 1]
val = df.iat[5, 1]

# 2.标签索引,日期标签
col = '注册日期'
val = df.loc[100000,col]
val = df.at[100000,col]

# # 3.标签索引,日期标签
# val = df.loc['20180502',col]
# val = df.at[pd.to_datetime('20180502'),col]

################# 修改操作 ################
# 1.修改数据类型，参考前面

# 2.修改标题
# 1）修改部分标题名
df2 = df.rename(columns={'年龄':'age', '省份':'province'})
# df2 = df.rename({'A':'a', 'B':'b'}, axis='columns')

# 2）替换整个标题列
colms = ['省份','性别','年龄','注册日期','学历']
df.columns = colms

# 3.修改索引
# 1）单个映射
mapper = {100000:200000, 100001:200001}
df2 = df.rename(index=mapper)
df2 = df.rename(mapper, axis=0)


# mapper = {pd.to_datetime('20180501'):pd.to_datetime('20180601'), \
#             pd.to_datetime('20180503'):pd.to_datetime('20180603')}
# df2 = df.rename(index=mapper)
# df2 = df.rename(mapper,axis='index')

# 注意：标签索引值是有可能相同的
# df2.iloc[7]  #这样只返回第7个位置的行，只有一行
# df2.loc[7]   #这样访问将会得到所有标签索引值为7的行，可能有多行

# 2）替换整个索引列
idx = pd.Index(range(len(df)))
df2 = df.set_index(idx)
# df.index = range(len(df))   #或者直接赋值

# 3）重新指定索引字段
# df2 = df.set_index('用户ID')      #可以重新指定索引列

# 4.修改字段值
# 1）修改单个字段值
df.iat[0,2] = 30             #按posion设置
df.at[100001,'年龄'] = 17    #按label设置


# 2）替换值
#  将特定值 映射 替换为另一个值  重新编码
# 单个替换
df2 = df['性别'].replace('男', 1)
df2 = df['性别'].replace('女', 0)


# 批量替换
eduLevels = ['初中','高中','大专','本科','研究生']
newValues = [1,2,3,4,5]
df2 = df['学历'].replace(eduLevels, newValues)


# 相关函数
    # 修改标题或索引
    # DataFrame.rename(mapper=None, index=None, columns=None, axis=None, 
    #               copy=True, inplace=False, level=None)
    # mapper, index, columns : dict-like or function, optional
    # dict-like or functions transformations to apply to that axis’ values. Use either mapper and axis to specify the axis to target with mapper, or index and columns.
    # axis : int or str, optional
    # Axis to target with mapper. Can be either the axis name (‘index’, ‘columns’) or number (0, 1). The default is ‘index’.
    # copy : boolean, default True
    # Also copy underlying data
    # inplace : boolean, default False
    # Whether to return a new DataFrame. If True then value of copy is ignored.
    # level : int or level name, default None
    # In case of a MultiIndex, only rename labels in the specified level.

    # 修改索引列，指定索引字段
    # DataFrame.set_index(keys, drop=True, append=False, inplace=False, 
    #                       verify_integrity=False)
    # keys : label or array-like or list of labels/arrays
    # This parameter can be either a single column key, a single array of the same length as the calling DataFrame, or a list containing an arbitrary combination of column keys and arrays. Here, “array” encompasses Series, Index and np.ndarray.
    # drop : bool, default True，Delete columns to be used as the new index.
    # append : bool, default False，Whether to append columns to existing index.
    # inplace : bool, default False
    # verify_integrity : bool, default False
    # Check the new index for duplicates. Otherwise defer the check until necessary. Setting to False will improve the performance of this method.

    # 替换字段值
    # DataFrame.replace(to_replace=None, value=None, inplace=False, 
    #               limit=None, regex=False, method='pad')
    # to_replace : str, regex, list, dict, Series, int, float, or None
    # How to find the values that will be replaced.
    # numeric, str or regex:
    # numeric: numeric values equal to to_replace will be replaced with value
    # str: string exactly matching to_replace will be replaced with value
    # regex: regexs matching to_replace will be replaced with value
    # list of str, regex, or numeric:
    # First, if to_replace and value are both lists, they must be the same length.
    # Second, if regex=True then all of the strings in both lists will be interpreted as regexs otherwise they will match directly. This doesn’t matter much for value since there are only a few possible substitution regexes you can use.
    # str, regex and numeric rules apply as above.
    # dict:
    # Dicts can be used to specify different replacement values for different existing values. For example, {'a': 'b', 'y': 'z'} replaces the value ‘a’ with ‘b’ and ‘y’ with ‘z’. To use a dict in this way the value parameter should be None.
    # For a DataFrame a dict can specify that different values should be replaced in different columns. For example, {'a': 1, 'b': 'z'} looks for the value 1 in column ‘a’ and the value ‘z’ in column ‘b’ and replaces these values with whatever is specified in value. The value parameter should not be None in this case. You can treat this as a special case of passing two lists except that you are specifying the column to search in.
    # For a DataFrame nested dictionaries, e.g., {'a': {'b': np.nan}}, are read as follows: look in column ‘a’ for the value ‘b’ and replace it with NaN. The value parameter should be None to use a nested dict in this way. You can nest regular expressions as well. Note that column names (the top-level dictionary keys in a nested dictionary) cannot be regular expressions.
    # None:
    # This means that the regex argument must be a string, compiled regular expression, or list, dict, ndarray or Series of such elements. If value is also None then this must be a nested dictionary or Series.
    # See the examples section for examples of each of these.
    # value : scalar, dict, list, str, regex, default None
    # Value to replace any values matching to_replace with. For a DataFrame a dict of values can be used to specify which value to use for each column (columns not in the dict will not be filled). Regular expressions, strings and lists or dicts of such objects are also allowed.
    # inplace : bool, default False
    # If True, in place. Note: this will modify any other views on this object (e.g. a column from a DataFrame). Returns the caller if this is True.
    # limit : int, default None
    # Maximum size gap to forward or backward fill.
    # regex : bool or same types as to_replace, default False
    # Whether to interpret to_replace and/or value as regular expressions. If this is True then to_replace must be a string. Alternatively, this could be a regular expression or a list, dict, or array of regular expressions in which case to_replace must be None.
    # method : {‘pad’, ‘ffill’, ‘bfill’, None}
    # The method to use when for replacement, when to_replace is a scalar, list or tuple and value is None.
    # Changed in version 0.23.0: Added to DataFrame.

################# 行操作：增删换移 ################
# 下面构建新的数据集示例

idx = pd.Index(range(10,18))
df = pd.DataFrame(np.random.randn(8, 3), index=idx, columns=['A', 'B', 'C'])

# 1.末尾新增行
# 标签索引不存在时，就添加
df.loc[8] = [1,2,3]

# 不指定索引，在末尾新增行
# 但索引将会自动改变为位置索引
sr = pd.Series([1,5,9], index=df.columns)
df = df.append(sr, ignore_index=True)   #ignore_index=True避免索引相同

# 2.插入一行 (没有直接的函数)
# 由于标签索引难以处理，所以只适合于位置索引的插入行,即索引可以重新设定。
# 可以先分段，再插入，再合并
df1 = df.iloc[:2,:]
df2 = df.iloc[2:,:]
df1.loc[len(df1)] = [20]*len(df.columns)
df = df1.append(df2,ignore_index=True)

# 3.修改行
# (索引存在时赋值就是修改)
# 按标签修改
df.loc[9] = [10,20,30]
# 按位置修改, 修改为空行
df.iloc[9] = [np.nan]*len(df.columns)

# 4.删除行

# 1）删除单行。 
# # 注意：标签索引行不存在时，会异常。需要指明errors='ignore'就不会抛异常
df2 = df.drop(0, axis=0, errors='ignore')

# 2）删除多行
rows = [2,8]
df2 = df.drop(rows, axis=0)

# 删除连续行
rows = df.loc[2:8]          #按标签
# rows = df.iloc[2:8]         #按位置也可以
df2 = df.drop(rows.index,axis='index')  #删除指定索引行      

# 3）行移位
# 基本不用，除非各字段类型完全相同
# 相当于移位单行，再赋值
df.loc[10] = df.loc[10].shift(1)

################# 列操作：增删换移 ################
# 列新增/修改,注意，将改变原有数据集
#   如果行不存在，则添加整行；
#   如果行存在，则替换整行值

df['D'] = [np.nan]*len(df)          #新增空列，末尾增加
df['D'] = np.array([2]*len(df))     #替换列
df.insert(1, 'id', range(len(df))) #插入列（前插）,按位置索引
df2 = df.drop('D',axis='columns')   #删除列
df2 = df.drop(['C','D'],axis=1)     #删除多列,字段不存在会有KeyError异常
sr = df.pop('id')                  #弹出并返回该列，注意会马上修改原数据集
sr = df['A'].shift(2)               #向下移动2个位置，常用于移动平均等时序预测

# 相关函数
    # 添加行
    # DataFrame.append(other, ignore_index=False, verify_integrity=False, sort=None)
    # other : DataFrame or Series/dict-like object, or list of these
    # The data to append.
    # ignore_index : boolean, default False
    # If True, do not use the index labels.
    # verify_integrity : boolean, default False
    # If True, raise ValueError on creating index with duplicates.
    # sort : boolean, default None
    # Sort columns if the columns of self and other are not aligned. The default sorting is deprecated and will change to not-sorting in a future version of pandas. Explicitly pass sort=True to silence the warning and sort. Explicitly pass sort=False to silence the warning and not sort.

    # 删除行或列
    # DataFrame.drop(labels=None, axis=0, index=None, columns=None, 
    #               level=None, inplace=False, errors='raise')
    # labels : single label or list-like，Index or column labels to drop.
    # axis : {0 or ‘index’, 1 or ‘columns’}, default 0
    # index, columns : single label or list-like
    # Alternative to specifying axis (labels, axis=1 is equivalent to columns=labels).
    # New in version 0.21.0.
    # level : int or level name, optional
    # For MultiIndex, level from which the labels will be removed.
    # inplace : bool, default False
    # If True, do operation inplace and return None.
    # errors : {‘ignore’, ‘raise’}, default ‘raise’
    # If ‘ignore’, suppress error and only existing labels are dropped.

    # 删除列，并返回该列，原数据集被修改
    # DataFrame.pop(item)
    # item : str
    # Column label to be popped

    # 插入列
    # DataFrame.insert(loc, column, value, allow_duplicates=False)
    # loc : int，Insertion index. Must verify 0 <= loc <= len(columns)
    # column : string, number, or hashable object
    # label of the inserted column
    # value : int, Series, or array-like
    # allow_duplicates : bool, optional

    # 移动字段
    # DataFrame.shift(periods=1, freq=None, axis=0, fill_value=None)
    # periods ：int 移动的次数，可正可负
    # freq : DateOffset, tseries.offsets, timedelta, or str, optional
    # fill_value : object 默认填充Nan

################# 筛选数据 ################

# 指定条件
cond = dfUsers['年龄'] > 30      #返回一个bool值列表sr
# cond = (df['A']<0) & (df['B']>0)  #复合条件，可以使用& |等实现多重条件筛选
df2 = dfUsers[cond]          #返回指定条件的数据集

# 上面两条件语句可以合并为下面一条语句
df2 = dfUsers[dfUsers['年龄']> 30]

#筛选多个特定的值
cond = dfUsers['年龄'].isin([23, 40])
# cond = dfUsers['省份'].isin(['广东', '广西'])
df2 = dfUsers[cond]

col = '年龄'
df2 = dfUsers[dfUsers[col].isna()]        #检测缺失值
df2 = dfUsers[dfUsers[col].isnull()]      #同上
# 如果df2.empty==True则表示没有缺失值

df2 = dfUsers[dfUsers[col].notna()]       #检测非缺失值
df2 = dfUsers[dfUsers[col].notnull()]       #同上

################# 其它操作 ################
#转置
df2 = df.T


######################################################################
########  数据集保存
######################################################################

index = pd.date_range('5/1/2018', periods=8)
df = pd.DataFrame(np.random.randn(8, 3), index=index,
                    columns=['A', 'B', 'C'])

df.index.name = 'Date'      #给索引加一个标题

# 假定数据集保存在df变量中
outfile = 'outfile.csv'
df.to_csv(outfile)  #保存数据集

# pip install openpyxl
outfile = 'outfile.xlsx'
# 如果df中带中文，也可以指定编码gbk或者utf_8_sig
df.to_excel(outfile, index=False,encoding='gbk')

# 相关函数
    # 保存为CSV文件
    # DataFrame.to_csv(path_or_buf=None, sep=', ', na_rep='', 
    #       float_format=None, columns=None, header=True, index=True, index_label=None, 
    #       mode='w', encoding=None, compression='infer', quoting=None, quotechar='"', 
    #       line_terminator=None, chunksize=None, tupleize_cols=None, date_format=None, 
    #       doublequote=True, escapechar=None, decimal='.')
    # 重要参数说明：
    # sep    字段分隔符
    # header 是否要保存标题
    # index  是否要保存索引。默认保存索引，一般整数索引时不建议保存
    # 

    # 保存为Excel文件
    # DataFrame.to_excel(excel_writer, sheet_name='Sheet1', na_rep='', float_format=None, 
    #       columns=None, header=True, index=True, index_label=None, startrow=0, startcol=0, 
    #       engine=None, merge_cells=True, encoding=None, inf_rep='inf', verbose=True, 
    #       freeze_panes=None)
    # 重要参数说明
    # sheet_name 可以指定保存的sheet名称
    # index 是否要保存索引（需要设置df.index.name-索引标题名称）
    # header 是否要保存标题
