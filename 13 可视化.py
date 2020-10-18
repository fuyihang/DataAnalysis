#-*- coding: utf-8 -*- 

########  本文件实现matplotlib可视化功能
# 1.中文显示问题
# 2.简单柱状图
# 3.直方图
# 4.箱图
# 5.饼图
# 6.散点图
# 7.折线图
# 8.复式柱状图、堆积柱状图、百分比堆积柱状图
# 9.桑基图（Sankey）
######################################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

###########方法一：一次性解决中文显示问题
# 1、查看字体所在目录
# import matplotlib
# print(matplotlib.matplotlib_fname())
# 2、下载simhei.ttf字体，复制到上述目录的fonts/ttf/目录中
# 
# 3、修改matplotlibrc文档
# 1)去掉前面注释#，加上simhei字体，形如
#       font.sans-serif: simhei,DejaVu Sans,...
# 2)去掉前面注释#，并修改为False，以便显示坐标轴的负号
#       axes.unicode_minus: False
# 4、清除matplotlib缓存
#   在MacOS中，使用命令 rm -rf ~/.matplotlib/*, 重启python即可
#   在window中，使用命令 cd .matplotlib, 然后del *, 重启python即可


############方法二：也可以使用代码来解决，每次在绘制图形前，采用如下代码来修改画图的字体
# plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
# plt.rcParams['font.family']='sans-serif'
# plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号


################简单柱状图###############################

def plotBar(df, indexCol, valCol, aggfunc=np.sum, title='柱状图', dataLabel=True):
    """\
    画柱状图
    """
    # 统计
    groups = df.groupby(indexCol)
    sr = groups[valCol].agg(aggfunc)

    # 画图
    rects = plt.bar(sr.index, sr.values, 
            # align='center', 
            edgecolor='k', 
            linewidth=1)

    # 添加数据标签
    if dataLabel==True:
        for rect in rects:
            x = rect.get_x() + rect.get_width()/2
            y = rect.get_height()*1.01
            s = '{:.1f}'.format(rect.get_height())
            plt.text(x, y, s, ha='center')      #ha表示字符串与位置的水平对齐方式
        # plt.axes().get_yaxis().set_visible(False)
        plt.yticks([])  # 隐藏坐标轴刻度值
    
    plt.ylabel(valCol)
    plt.xlabel(indexCol)
    plt.title(title)
    plt.show()


################直方图###############################

def plotHist(df, valCol, bins=10, range=None, title='直方图', dataLabel=True):
    """\
    画直方图
    """
    vals = plt.hist(df[valCol], bins, range=range, edgecolor='k')
    # 返回三元组列表(高，分割点，矩阵)
    heights = vals[0]
    bins = vals[1]
    plt.xticks(bins)

    if dataLabel:
        rects = vals[2]
        for rect in rects:
            x = rect.get_x() + rect.get_width()/2
            y = rect.get_height()*1.01
            s = '{}'.format(rect.get_height())
            plt.text(x, y, s, ha='center')

    plt.xlabel(valCol)
    plt.title(title)
    plt.show()


################箱图###############################

def plotBox(df, valCol, indexCol=None, title='箱图', dataLabel=True):
    """\
    画箱图
    """
    ltdf = []
    cols = []
    if indexCol != None:
        grouped = df.groupby(indexCol)

        for name, grp in grouped:
            cols.append(name)
            ltdf.append(grp[valCol])
    else:
        ltdf.append( df[valCol] )
        cols = [valCol]
    plt.boxplot(ltdf, labels=cols)

    if dataLabel:
        for pos in range(len(ltdf)):
            des = ltdf[pos].describe()
            Q1 = np.round(des['25%'])
            Q2 = np.round(des['50%'])
            Q3 = np.round(des['75%'])

            Q0 = np.max([des['min'], Q1 - 1.5*(Q3-Q1)])
            Q4 = np.min([des['max'], Q3 + 1.5*(Q3-Q1)])
            
            vals = [Q0, Q1, Q2, Q3, Q4]
            for val in vals:
                x = pos + 1.1
                y = val
                s = '{}'.format(val)
                plt.text(x, y, s)
                # plt.text(pos+1.1, val, val, fontsize=11.1)
    else:
        plt.grid()
    
    plt.title(title)
    plt.show()

################饼图###############################

def plotPie(df, indexCol, valCol, aggfunc=np.sum, title='饼图',dataLabel=True):
    """\
    画饼图
    """
    group = df.groupby(indexCol)
    sr = group[valCol].agg(aggfunc)

    # 按值升序
    sr.sort_values(ascending=True,inplace=True)

    # # 自定义显示格式,传入的pct是百分比值
    # def myLable(pct, vals):
    #     if dataLabel==True:
    #         lbl = "{0:.1f}%\n{1:.0f}".format(pct, pct*np.sum(vals))
    #     else:
    #         lbl = "{0:.1f}%".format(pct)
    #     return lbl

    # 默认从3点钟方向、逆时针排列
    # startangle=90表示从12点钟方向开始
    plt.pie(sr, labels=sr.index, 
            autopct='%.2f%%', 
            startangle=90)
    # plt.pie(sr, labels=sr.index, 
    #         autopct=lambda x: myLable(x, sr.values), 
    #         startangle=90)

    plt.ylabel(valCol)
    plt.xlabel(indexCol)
    plt.title(title)
    plt.show()

# 重要参数说明
    # explode=[0,0,0.2,0] 表示对应的饼块被拖出

    # import matplotlib.colors as pltclrs
    # colors = list(pltclrs.TABLEAU_COLORS.keys()) #生成10个颜色列表

    # colors = ['b','g','r','c','m','y','k','w']  #手工定义颜色
    # linestype:
    # 颜色控制参数
    # b - blue
    # g - green
    # r - red
    # c - cyan
    # m - magenta
    # y - yellow
    # k - black
    # w - white

################散点图、气泡图###############################

def plotScatter(df, xCol, yCol, colorCol=None, sizeCol=None, title='散点图'):
    """\
    画散点图
    """
    s = None
    if sizeCol != None:
        s = df[sizeCol]

    if colorCol != None:
        clrVals = df[colorCol].unique().tolist()

        for val in clrVals:
            cond = df[colorCol]==val
            df2 = df[cond]

            x = df2[xCol]
            y = df2[yCol]
            if sizeCol != None:
                s = df2[sizeCol]
            plt.scatter(x, y, s=s, alpha=0.8, label=val)
        plt.legend()
    else:
        x = df[xCol]
        y = df[yCol]
        plt.scatter(x, y, s=s, alpha=0.8)

    plt.xlabel(xCol)
    plt.ylabel(yCol)
    plt.title(title)
    plt.show()

################折线图###############################

def plotLine(df, dateCol, valCols, datePeriod='M', aggfunc=np.size, title='折线图'):
    """\
    画折线图
    """
    df = df.set_index(dateCol)

    for col in valCols:
        sr = df[col].resample(datePeriod).agg(aggfunc).to_period(datePeriod)

        plt.plot(range(len(sr)), sr, 'o-',label=col)

    if (len(valCols)==1):
        plt.ylabel(valCols[0])
    else:
        plt.legend()

    plt.title(title)
    plt.xlabel(dateCol)

    if len(sr.index) < 10:
        plt.xticks(ticks=range(len(sr)), labels=sr.index)

    plt.show()

    return None


################交叉分析的复式柱状图###############################

def plotBar2(df, indexCol, typeCol, valCol, aggfunc=np.sum, 
        stacked=False, percentage=False,
        title='柱状图',dataLabel=True):
    """\
    画复式/堆积柱状图
    """

    # 透视表
    df2 = pd.pivot_table(df, index=indexCol, 
                columns=typeCol, values=valCol,
                aggfunc= aggfunc)

    df2['Total'] = df2.sum(axis=1)  #行汇总：按列汇总
    
    # 加上这段，就是百分比
    if percentage:
        for i in range(len(df2.columns)-1):
            df2.iloc[:,i] = df2.iloc[:,i ] /df2.iloc[:, -1]
    
    # 若横坐标不是有序字符串变量，则按值排序
    if not pd.api.types.is_categorical_dtype(df[indexCol]):
        df2.sort_values(by='Total', ascending=False, inplace=True)
    df2.drop('Total', axis=1,inplace=True)
    
    if stacked:
        btm = pd.Series([0]*df2.shape[0], index=df2.index)
        for col in df2.columns:
            sr = df2[col]
            rects = plt.bar(sr.index, sr.values, label=col, bottom=btm)
            
            if dataLabel==True:
                for j, rect in enumerate(rects):
                    x = rect.get_x() + rect.get_width()/2
                    y = rect.get_height()/2 + btm[j]
                    if percentage:
                        s = '{:.0%}'.format(rect.get_height())
                    else:
                        s = '{}'.format(rect.get_height())
                    plt.text(x,y,s,ha='center')
                # plt.axes().get_yaxis().set_visible(False)
                plt.yticks([])  # 隐藏坐标轴刻度值
            btm += df2[col]

    else:   #复式柱状图
        n, m = df2.shape
        width = 0.8/m
        xpos = np.linspace(0, n, n, endpoint=False)
        for col in df2.columns:
            sr = df2[col]
            rects = plt.bar(xpos, sr.values, width=width, label=col)
            if dataLabel==True:
                for rect in rects:
                    x = rect.get_x() + rect.get_width()/2
                    y = rect.get_height()*1.01
                    if percentage:
                        s = '{:.0%}'.format(rect.get_height())
                    else:
                        s = '{}'.format(rect.get_height())
                    plt.text(x, y, s, ha='center')
                plt.yticks([])  # 隐藏坐标轴刻度值
            xpos += width
        
        # 在最后一个图下标注索引
        xpos -= width
        plt.xticks(ticks=xpos, labels=df2.index)

    plt.xlabel(indexCol)
    plt.ylabel(valCol)
    plt.title(title)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    filename = 'Telephone.csv'
    df = pd.read_csv(filename, encoding='gbk')
    col = '教育水平'
    eduLevel = ['初中','高中','大专','本科','研究生']
    df[col] = df[col].astype('category').cat.set_categories(eduLevel)

    plotBar(df, '居住地', '消费金额', np.mean)
    plotBar(df, '婚姻状况', '消费金额', np.mean)
    plotBar(df, '教育水平', '消费金额', np.mean)

    plotHist(df, '年龄')
    plotHist(df, '收入', dataLabel=False)
    plotHist(df, '收入',range=(9,200))

    plotBox(df, '年龄')
    plotBox(df, '收入')
    plotBox(df, '年龄', indexCol='居住地')

    plotPie(df, '教育水平','消费金额',title='收入结构')
    plotPie(df, '教育水平','UID',np.size, title='学历结构')

    plotScatter(df, '开通月数','消费金额')
    plotScatter(df.iloc[:10,:], '开通月数','消费金额', colorCol='性别')
    plotScatter(df.iloc[:10,:], '年龄','收入', sizeCol='消费金额')
    plotScatter(df.iloc[:10,:], '年龄','收入', colorCol='性别', sizeCol='消费金额')

    plotBar2(df, '教育水平','套餐类型','UID','count')
    plotBar2(df, '教育水平','套餐类型','UID','count',stacked=True)
    plotBar2(df, '教育水平','套餐类型','UID','count', percentage=True)
    plotBar2(df, '教育水平','套餐类型','UID','count',stacked=True, percentage=True)

    plotBar2(df, '套餐类型','流失','UID','count')
    plotBar2(df, '套餐类型','流失','UID','count',stacked=True)
    plotBar2(df, '套餐类型','流失','UID','count',percentage=True)
    plotBar2(df, '套餐类型','流失','UID','count',stacked=True, percentage=True)


# ################桑基图Sankey###############################
# # conda install pyecharts
# from pyecharts.charts import Sankey
# from pyecharts import options as opts

# # from matplotlib.sankey import Sankey

# def plotSankey(df, catCols, valCol, aggfunc=np.sum, 
#         title='桑基图'):
#     """\
#     画桑基图
#     """
#     # 先构造结点
#     nodes = []
#     for col in catCols:
#         labels = df[col].unique()
#         for lbl in labels:
#             node = {}
#             node['name'] = lbl
#             nodes.append(node)

#     # 再构造流向
#     links = []

#     for i in range(len(catCols)-1):
#         col1 = catCols[i]
#         col2 = catCols[i+1]

#         group = df.groupby([col1, col2])
#         sr = group[valCol].agg(aggfunc)
#         for (src, tgt), val in sr.items():
#             dic = {}
#             dic['source'] = src
#             dic['target'] = tgt
#             dic['value'] = np.round(val)
#             links.append(dic)
#     # print(links)

#     # # 画图
#     sankey = Sankey()
#     sankey.add(title,nodes,links,
#             linestyle_opt=opts.LineStyleOpts(opacity = 0.3, curve = 0.5, color = 'source'),
#             label_opts=opts.LabelOpts(position = 'top'),
#             node_gap= 30
#             )
#     sankey.render('sankey.html')
