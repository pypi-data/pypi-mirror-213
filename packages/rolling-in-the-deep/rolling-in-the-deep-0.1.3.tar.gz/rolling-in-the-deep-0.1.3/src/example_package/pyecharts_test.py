#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/5/26 11:34 上午
# @Author  : zhengyu.0985
# @FileName: pyecharts_test.py
# @Software: PyCharm
# from pyecharts.globals import CurrentConfig, NotebookType
# CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_LAB
# CurrentConfig.ONLINE_HOST

from pyecharts.charts import Bar, Line, Map, Page, Pie, Tree
from pyecharts import options
from pyecharts.options.global_options import AxisOpts, ToolBoxFeatureOpts, ToolBoxFeatureSaveAsImageOpts
from pyecharts.render import make_snapshot
# 内置主题类型可查看: pyecharts.globals.ThemeType
from pyecharts.globals import ThemeType


# 柱状图
def bar_func() -> Bar:
    x = ['餐饮', '娱乐', '交通', '保养', '衣服']
    y1 = [1000, 500, 100, 5000, 5000]
    y2 = [2000, 1000, 100, 20, 30]
    # bar = Bar()
    bar = Bar(init_opts=options.InitOpts(chart_id="bar", width='800px', height='600px',
                                         bg_color='#ADD8E7', theme=ThemeType.LIGHT,
                                         page_title='柱状图', animation_opts=options.global_options.AnimationOpts()))
    bar.add_xaxis(xaxis_data=x)
    # 第一个参数是图例的名称
    bar.add_yaxis(series_name='zhang某人', y_axis=y1)
    bar.add_yaxis(series_name='fan某人', y_axis=y2)
    # 添加options
    bar.set_global_opts(title_opts=options.TitleOpts(title='zhang某人和fan某人一月开支'))
    # 生成HTML文件
    bar.render('我的第一个echarts图.html')
    bar.render_notebook()
    # make_snapshot(engine=snapshot, file_name=bar.render(), output_name="bar.png")
    return bar


# 折线图
def line_func() -> Line:
    x = ['1月', '2月', '3月', '4月', '5月']
    y = [1000, 500, 100, 5000, 3500]
    z = [800, 600, 300, 2000, 3000]
    line = Line(init_opts=options.InitOpts(chart_id="line", width='800px', height='600px',
                                           bg_color='#ADD8E6', theme=ThemeType.LIGHT,
                                           page_title='我的折线图'))
    line.add_xaxis(xaxis_data=x)
    line.add_yaxis(series_name='Person_A', y_axis=y)
    line.add_yaxis(series_name='Person_B', y_axis=z)
    line.set_global_opts(title_opts=options.TitleOpts(title='幸福生活消费图',
                                                      title_link="http://www.baidu.com",
                                                      pos_left="center", pos_top="2px", padding=5))
    line.set_global_opts(legend_opts=options.LegendOpts(pos_bottom="2px", orient="horizontal"))  # 该行会导致Title不显示
    # line.set_global_opts(toolbox_opts=options.ToolboxOpts(is_show=True,
    #                                                       feature=ToolBoxFeatureOpts(
    #                                                           save_as_image=ToolBoxFeatureSaveAsImageOpts(pixel_ratio=2)
    #                                                       )))
    line.render('折线图.html')
    line.render_notebook()
    return line


# 中国地图
def map_func() -> Map:
    population = [["广东", 11169], ["山东", 10005.63], ["河南", 9559.13], ["四川", 8302]]
    map_obj = (Map(init_opts=options.InitOpts(chart_id="china_map", bg_color='#ADD8E5'))
               .add("省人口数量", population, "china")
               .set_global_opts(title_opts=options.TitleOpts(title='人口数量'),
                                visualmap_opts=options.VisualMapOpts(max_=12000)))
    map_obj.render('省人口数量.html')
    map_obj.render_notebook()
    return map_obj


color = {
       "type": 'linear',
       "x": 0,
       "y": 0,
       "x2": 0,
       "y2": 1,
       "colorStops": [{
           "offset": 0, "color": 'red'
       }, {
           "offset": 1, "color": 'blue'
       }],
       "global": False
    }


# 饼图
def pie_func() -> Pie:
    pie = Pie(init_opts=options.InitOpts(chart_id="pie", bg_color='#ADD8E4')).\
        add("", [['跳水', 12], ['游泳', 10],['居中', 8]], center=["50%", "60%"],).\
        set_series_opts(label_opts=options.LabelOpts(formatter="{b}:{c}"),
                        itemstyle_opts=options.ItemStyleOpts(opacity=0.85,
                                                             color=color  # 若需要每个扇叶不同颜色，可去掉该行。
                                                             ))
    pie.render('饼图.html')
    pie.render_notebook()
    return pie


data = [
    {
        "name": "TitleOpts:标题配置项"
    }
]


def title() -> Tree:
    tree = Tree(init_opts=options.InitOpts(width="1400px", height="100px", bg_color="#ADD8E3"))\
        .add("", data)\
        .set_global_opts(title_opts=options.TitleOpts(title="TitleOpts：标题配置项"))
    tree.render('Title.html')
    tree.render_notebook()
    return tree


data_list = [
    ["bar", bar_func()],
    ["line", line_func()],
    ["map", map_func()]
]


def map_world() -> Map:
    c = (
        Map(init_opts=options.InitOpts(chart_id="world_map", bg_color='#ADD8E4'))
        .add("", data_list, "world",
             is_map_symbol_show=False,
             )
        .set_series_opts(label_opts=options.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=options.TitleOpts(title="2022东京奥运会奖牌榜"),
            visualmap_opts=options.VisualMapOpts(max_=100)
        )
    )
    return c


page = Page(layout=Page.DraggablePageLayout, page_title="2022东京奥运会奖牌榜")
page.add(
    # title(),
    map_world(),
    bar_func(),
    line_func(),
    map_func(),
    pie_func()
)
page.render('composite.html')  # 当执行下面一行的时候需要保证composite.html不改变，所以要注释该行。
str_val = page.save_resize_html(source='composite.html', cfg_file='chart_config.json', dest='Final.html')

#config_dict = [{"cid":"2","width":"689.007812px","height":"421.007812px","top":"31.611328125px","left":"7.998046875px"},{"cid":"34882852ea034610852c8f313c500281","width":"728.007812px","height":"422.007812px","top":"31.103515625px","left":"701.9921875px"},{"cid":"35aa081744cd4a8eb25d73d0e8fa5889","width":"690.007812px","height":"411.007812px","top":"461.591796875px","left":"7.998046875px"},{"cid":"d4a5a178ca3e4da8960a0ba793a6d69f","width":"727.007812px","height":"412.007812px","top":"461.07421875px","left":"703.994140625px"}]
# str_val = page.save_resize_html(source='composite.html', cfg_dict=config_dict, dest='Final.html')
# print(str_val)
