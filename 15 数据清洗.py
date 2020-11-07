#-*- coding: utf-8 -*- 

########  本文件实现数据清洗功能，主要是异常数据的处理，包括：
# 1.重复值
# 2.缺失值：即空值
# 3.错误数据：取值范围外的数据
# 4.离群值：即偏离的值
######################################################################

import pandas as pd
import numpy as np


filename = '某公司销售数据.xlsx'
sheet = '全国订单明细'
df = pd.read_excel(filename, sheet)


######################################################################
########  一、重复值处理
######################################################################

# 1、重复字段值处理

# 1)查看重复值
col = '订单号'
cond = df.duplicated(subset=[col], keep='first')
dpl = df[cond]

# 2)删除重复项
# 删除指定index
df2 = df.drop(index=dpl.index, axis=0)

# 盲删除
df2 = df.drop_duplicates(subset=[col], keep='first')


# 3)空值特殊处理
# 注意：两个空值，也会被看成是重复值。上面会把重复的空值也删除掉哟
# 如果要查看排除空值的重复值，则需要如下处理
cond = df.duplicated(subset=[col])
dpl = df[df[col].notnull()][cond]

# 2、重复标题处理 
idx = pd.Index([1,2,3,3,6,9,9])
colms = ['A','B','B','C','C']
dfTest = pd.DataFrame(np.random.randn(len(idx), len(colms)), 
                index=idx, columns=colms)
if not dfTest.columns.is_unique:
    print('数据集有重复的标题名称！')

# 1)查看重复标题
dplCols = dfTest.columns[dfTest.columns.duplicated()]
print('重复标题:', list(dplCols))

# 2)查看所有重复的列['B','B','C','C']
dpl1 = dfTest[dplCols]

# 3)只查看重复的最后的列['B','C']
dpl2 = dfTest.loc[:, dfTest.columns.duplicated()]

# 4)选出未重复的列
df2 = dfTest.loc[:, ~dfTest.columns.duplicated()]

# 5)修改标题名称
# 在其后增加位置后缀
colms = []
for pos, name in enumerate(dfTest.columns):
    if name in dplCols:
        colms.append('{}_{}'.format(name,pos+1))
    else:
        colms.append(name)
dfTest.columns = colms
print(dfTest)

# 3、重复索引处理
# 标签索引值是有可能重复的，在某些场景下是需要去重的

# 1)判断索引是否重复
if  not dfTest.index.is_unique :
    print('数据集有重复的索引！')

# 2)查看重复索引
dpl = dfTest[dfTest.index.duplicated()]

# 3)删除重复索引列，即 筛选非重复项
df2 = dfTest.iloc[~dfTest.index.duplicated()]

# 4)修改索引标识
idxs = []
idxLast = max(dfTest.index)+1     #假定索引是整数索引,最大索引
dplRows = dfTest[dfTest.index.duplicated(keep=False)] #找到所有重复项
print(dplRows)

for pos, idx in enumerate(dfTest.index):
    if idx in dplRows.index:
        idxs.append(idx+idxLast+pos)
    else:
        idxs.append(idx)
print(idxs)

df2 = dfTest.set_index(pd.Index(idxs))
print(df2)

# 相关函数
    # DataFrame.duplicated(self, subset=None, keep='first')
    # subset : column label or sequence of labels, optional
    #   指定列标签，默认为所有列
    # keep : {‘first’, ‘last’, False}, default ‘first’
    #   重复值的返回取舍
    #   first : 除了第一个，其余全为重复值
    #   last :  除了最后一个，其余全为重复值
    #   False : 所有重复的都返回

    # 删除重复项
    # DataFrame.drop_duplicates(subset=None, keep='first', inplace=False)
    # subset : column label or sequence of labels, 待处理的列，默认是所有列
    # keep : {‘first’, ‘last’, False}, default ‘first’
    # keep  1)first除第一个外，其余删除
    #       2）last除最后一个外，其余删除
    #       3）False所有重复的都删除
    # inplace : boolean, default False 是否修改原有数据集

    # 删除行或列
    # DataFrame.drop(labels=None, axis=0, index=None, columns=None, 
    #               level=None, inplace=False, errors='raise')
    # labels : single label or list-like, 
    #       待删除的index或column标签
    # axis : {0 or ‘index’, 1 or ‘columns’}, default 0
    # index, columns : single label or list-like
    # level : int or level name, optional。
    #       多层索引时用，指定索引层级
    # inplace : bool, default False
    # errors : {‘ignore’, ‘raise’}, default ‘raise’
    # 标签不存在时删除，是否抛出异常。

######################################################################
########  二、错误值处理
######################################################################
# 也称无效值，主要是在有效取值范围之外的值，不包括空值。

col = '订单数量'

#1、查看无效值/错误值：取值范围外的数据
cond = (df[col] > 0)  #指定取值范围
dfErr = df[~cond]     #范围外的为无效值（包含空值）

# 如果不想包含空值，可以指定范围外条件
cond = df[col] < 0
dfErr = df[cond]    #此时不包含空值

#2、将无效值修改为其它值
# df[col][dfErr.index] = np.nan  #置空
# df[col][dfErr.index] = abs(df[col][dfErr.index])  #绝对值

# 查看空值
# dfnull = df[ df[col].isnull() ]

# 3、删除无效值（删除事行）
df.drop(index = dfErr.index, inplace=True)
# df.drop(dfErr.index, axis='index', inplace=True)

# 4、重新编码（比如性别本身是用0，1表示，但填写时还是填写为女男
# df['性别'][df['性别']=='女'] = 0
# df['性别'][df['性别']=='男'] = 1
# df.replace('女', 0, inplace=True)
# df.replace('男', 1, inplace=True)

######################################################################
########  三、离群值、极端值处理（3σ原则）
######################################################################
import matplotlib.pyplot as plt

col = '折扣点'
plt.boxplot(df[col])

des = df[col].describe()

# ####### 按照 标准差std 来检测##############

# 1.查找极端值
# 极端值:5个标准差外的值。注意要用float强制转换
std5min = float(des['mean'] - 5*des['std'])
std5max = float(des['mean'] + 5*des['std'])
print('3σ原则-极端值范围:[{0:.2f}-{1:.2f}]'.format(std5min,std5max))

cond = (df[col] < std5min) | (df[col] > std5max)
df_extreme = df[cond]  
print('3σ原则-极端值列表：\n', df_extreme)

# 2.处理极端值
df[col][df_extreme.index] = np.nan    #置空
df.drop(df_extreme.index, axis='index', inplace=True)   # 截尾法，删除

# 3.查找离群值
# 离群值:3个标准差外的值。
std3min = float(des['mean'] - 3*des['std'])
std3max = float(des['mean'] + 3*des['std'])
print('3σ原则-离群值范围:[{0:.2f}-{1:.2f}]'.format(std3min,std3max))

df_outlier = df[(df[col] < std3min) | (df[col] > std3max) ]
print('3σ原则-离群值列表：\n', df_outlier)

# 4.处理离群值
# df[col][df_outlier.index] = np.nan    #置空
# df.drop(df_outlier.index, axis='index', inplace=True)   # 截尾法，删除
df[col][df[col]<std3min] = std3min        #缩尾法
df[col][df[col]>std3max] = std3max

# ####### 按照 四分位距IQR 来检测##############

# 1.查找极端值
# 极端值，3个IQR范围之外的值
des.loc['IQR'] = des.loc['75%'] - des.loc['25%']
IQRmin = float(des.loc['25%'] - 3*des.loc['IQR'])
IQRmax = float(des.loc['75%'] + 3*des.loc['IQR'])
print('IQR原则-极端值范围:[{0:.2f}-{1:.2f}]'.format(IQRmin,IQRmax))

df_extreme = df[(df[col]<IQRmin) | (df[col]>IQRmax)] 
print('IQR原则-极端值列表：\n', df_extreme)

# 2.极端值处理
df[col][df_extreme.index] = np.nan    #置空
df[col][(df[col]<IQRmin) | (df[col]>IQRmax)] = np.nan     #置空
# df.drop(df_extreme.index, axis='index', inplace=True)   # 删除

# 3.查找离群值
# 离群值:1.5个IQR外的值。
IQRmin = float(des.loc['25%'] - 1.5*des.loc['IQR'])
IQRmax = float(des.loc['75%'] + 1.5*des.loc['IQR'])
print('IQR原则-离群值范围:[{0:.2f}-{1:.2f}]'.format(IQRmin,IQRmax))

df_outlier = df[(df[col] < IQRmin) | (df[col] > IQRmax) ]  
print('IQR原则-离群值列表：\n', df_outlier)

# 4.离群值处理
print('IQR原则-离群值缩尾.')
# df[col][df_outlier.index] = np.nan    #置空
# df[col][(df[col]<IQRmin) | (df[col]>IQRmax)] = np.nan
# df.drop(df_outlier.index, axis='index', inplace=True)   #截尾法，删除
df[col][df[col]<IQRmin] = IQRmin        #缩尾法
df[col][df[col]>IQRmax] = IQRmax

######## 若涉及到多个变量，则可以基于K均值来检测离群值 ##############
# 参考文档末尾

######################################################################
########  四、缺失值处理
######################################################################

# 统计各列的缺失值
sr = df.isnull().sum()
cols = sr[sr > 0].index.tolist()
print('存在缺失值的列：',cols)

# 1.查看缺失值列表
col = '订单数量'
cond = df[col].isnull()
dfNull = df[ cond ]
# dfNull = df[ df[col].isna() ]
print(dfNull)

# 2.空字符串 （仅限于col字段是字符串型，否则抛出异常）
# dfNull = df[df[col].str.strip()=='']

# 合并起来
# dfNull = df[ df[col].isnull() | (df[col].str.strip()=='')]
# print('当前数据集中的缺失值个数:', dfNull.shape[0])

# 3.缺失值处理，方式有：
# 1）删除
# 2）固定值，平均值，众数等等
# 3）邻近值（向下填充，向上填充）
# 4）两点插值法
# 5）拉格朗日插值法

# 1）缺失值删除
col = '订单数量'
df.dropna(subset=[col], inplace=True)
# df.drop(index=dfNull.index, inplace=True)

# 2）填充指定值, 否则默认为平均值
col = '运输成本'
dfNull = df[ df[col].isnull() ]

val = 20                #替换固定值
val = df[col].mean()    #平均值
val = df[col].median()  #中位数
df[col].fillna(val, inplace=True)   #填充值

# 3）邻近值填充
# 向下填充, 可以使用limit限制填充的次数
df2 = df[col].fillna(method='ffill',limit = None)
# 向上填充
df2 = df[col].fillna(method='bfill', limit  = None)

# 4）两点插值法: 前后两点的均值来填充
df[col].interpolate(inplace=True)

# 5）拉格朗日插值法==============
# 默认取前后各5个值做插值，构造函数，再利用函数来计算缺失值
from scipy.interpolate import lagrange

def ployinterp_column(sr, index, k=5):
    #取前后各K个数
    ltPos = list(range(index-k, index)) + list(range(index+1, index+1+k))
    y = sr[ltPos] 
    y = y[y.notnull()] #剔除空值
    return lagrange(y.index, list(y))(index) #插值并返回插值结果

k = 5
#逐个元素判断是否需要插值
for idx in df.index:
    if df[col].isnull()[idx]:     #如果为空即插值。
        val = ployinterp_column(df[col], idx, k)
        df[col][idx] = val

# 函数原型
    # 删除空值
    # DataFrame.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
    # axis : {0 or ‘index’, 1 or ‘columns’}, default 0
    # how : {‘any’, ‘all’}, default ‘any’
    #       ‘any’ : 只要有一个空值就删除
    #       ‘all’ : 整行或整列全部为空值时才删除
    # thresh : int, optional，Require that many non-NA values.
    # subset : array-like, optional，指定标签索引
    # Labels along other axis to consider, e.g. if you are dropping rows these would be a list of columns to include.
    # inplace : bool, default False


    # DataFrame.fillna(value=None, method=None, axis=None, inplace=False, 
    #                   limit=None, downcast=None, **kwargs)
    # value : scalar, dict, Series, or DataFrame
    # method :backfill/bfill向上填充, pad/ffill向下填充,None默认固定值填充
    #                      ，，默认填充，   
    # inplace : boolean, default False  是否修改原数据集
    # limit : int, default None 填充次数

    # 插值法
    # DataFrame.interpolate(method='linear', axis=0, limit=None, inplace=False, 
    #           limit_direction='forward', limit_area=None, downcast=None, **kwargs)
    # method : str, default ‘linear’，Interpolation technique to use. One of:
    # ‘linear’: Ignore the index and treat the values as equally spaced. This is the only method supported on MultiIndexes.
    # ‘time’: Works on daily and higher resolution data to interpolate given length of interval.
    # ‘index’, ‘values’: use the actual numerical values of the index.
    # ‘pad’: Fill in NaNs using existing values.
    # ‘nearest’, ‘zero’, ‘slinear’, ‘quadratic’, ‘cubic’, ‘spline’, ‘barycentric’, ‘polynomial’: Passed to scipy.interpolate.interp1d. Both ‘polynomial’ and ‘spline’ require that you also specify an order (int), e.g. df.interpolate(method='polynomial', order=4). These use the numerical values of the index.
    # ‘krogh’, ‘piecewise_polynomial’, ‘spline’, ‘pchip’, ‘akima’: Wrappers around the SciPy interpolation methods of similar names. See Notes.
    # ‘from_derivatives’: Refers to scipy.interpolate.BPoly.from_derivatives which replaces ‘piecewise_polynomial’ interpolation method in scipy 0.18.
    # New in version 0.18.1: Added support for the ‘akima’ method. Added interpolate method ‘from_derivatives’ which replaces ‘piecewise_polynomial’ in SciPy 0.18; backwards-compatible with SciPy < 0.18
    # axis : {0 or ‘index’, 1 or ‘columns’, None}, default None
    # Axis to interpolate along.
    # limit : int, optional
    # Maximum number of consecutive NaNs to fill. Must be greater than 0.
    # inplace : bool, default False
    # Update the data in place if possible.
    # limit_direction : {‘forward’, ‘backward’, ‘both’}, default ‘forward’
    # If limit is specified, consecutive NaNs will be filled in this direction.
    # limit_area : {None, ‘inside’, ‘outside’}, default None
    # If limit is specified, consecutive NaNs will be filled with this restriction.
    # None: No fill restriction.
    # ‘inside’: Only fill NaNs surrounded by valid values (interpolate).
    # ‘outside’: Only fill NaNs outside valid values (extrapolate).
    # New in version 0.21.0.
    # downcast : optional, ‘infer’ or None, defaults to None
    # Downcast dtypes if possible.
    # **kwargs
    # Keyword arguments to pass on to the interpolating function.


######################################################################
########  处理后保存
######################################################################

# outfile = 'outfile.xlsx'
# df.to_excel(outfile, index=False)

