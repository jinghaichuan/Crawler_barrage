import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnarDataSource

import warnings
warnings.filterwarnings('ignore')


'''
①加载数据
'''
data = pd.read_excel('上海餐饮数据.xlsx', sheet_name=0)


'''
②计算口味、客单价、性价比指标
'''
df1 = data[['类别', '口味', '环境', '服务', '人均消费']]
data1 = df1.dropna()
data1['性价比'] = (data1['口味'] + data1['环境'] + data1['服务']) / data1['人均消费']
# 数据清洗 + 性价比计算


def f1():
    fig, axes = plt.subplots(1, 3, figsize=(10, 4))
    data1.boxplot(column=['口味'], ax=axes[0])
    data1.boxplot(column=['人均消费'], ax=axes[1])
    data1.boxplot(column=['性价比'], ax=axes[2])
# 创建函数1：制作箱型图，查看异常值

def f2(data, col):
    q1 = data[col].quantile(q=0.25)
    q3 = data[col].quantile(q=0.75)
    iqr = q3 - q1
    t1 = q1 - 3 * iqr
    t2 = q3 + 3 * iqr
    return data[(data[col] > t1) & (data[col] < t2)][['类别', col]]
# 创建函数2：清除异常值


data_kw = f2(data1,'口味')
data_rj = f2(data1,'人均消费')
data_xjb = f2(data1,'性价比')


def f3(data,col):
	col_name = col + '_norm'
	data_gp = data.groupby('类别').mean()
	data_gp[col_name] = (data_gp[col] - data_gp[col].min()) / (data_gp[col].max() - data_gp[col].min())
	data_gp.sort_values(by = col_name,inplace = True,ascending=False)
	return data_gp
# 创建函数3：标准化指标并排序

data_kw_score = f3(data_kw,'口味')
data_rj_score = f3(data_rj,'人均消费')
data_xjb_score = f3(data_xjb,'性价比')
# 指标标准化得分

data_final_q1 = pd.merge(data_kw_score,data_rj_score,left_index = True,right_index = True)
data_final_q1 = pd.merge(data_final_q1,data_xjb_score,left_index = True,right_index = True)
# 数据合并


'''
③绘制图表辅助分析
'''
import bokeh.layouts
import gridplot

data_final_q1['size'] =data_final_q1['口味_norm'] * 40
data_final_q1.index.name = 'type'
data_final_q1.columns = ['kw','kw_norm','price','price_norm','xjb','xjb_norm','size']
# 将列名改为英文

source = ColumnarDataSource(data_final_q1)
#创建数据

result = figure(plot_width = 800,plot_height = 300,title = '餐饮类型得分',
				x_axis_lable = '人均消费' ,y_axis_lable = '性价比得分')
result.circle(x = 'price',y = 'xjb_norm',source = source,line_color = 'black',
			  line_dash = [6,4],fill_alpha = 0.6,size = 'size')
# 散点图

data_type = data_final_q1.index.tolist()

kw = figure(plot_width = 800,plot_heght = 300 ,title = '口味得分', x_range = data_type)
kw.vbar(x='type')
