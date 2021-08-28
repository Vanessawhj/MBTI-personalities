from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.sampledata.periodic_table import elements
from bokeh.transform import dodge, factor_cmap
import streamlit as st
from PIL import Image
import pandas as pd


# to remove duplicates!
from bokeh.io import curdoc
curdoc().clear()


st.beta_set_page_config(
page_title="The MBTI Consultant",
page_icon="🔍",
layout="wide",
initial_sidebar_state="collapsed")



df_all = pd.read_csv("/Users/huijee/Downloads/MBTI_data.csv")

# get the personality types
mbti_core = set()
def core(x):
    x = str(x)
    if len(x) == 4:
        mbti_core.add(x)

    
df_all.type.apply(lambda x: core(x))


def try_expander(expander_name, sidebar=False):
    if sidebar:
        try:
            return st.sidebar.expander(expander_name)
        except:
            return st.sidebar.beta_expander(expander_name)
    else:
        try:
            return st.expander(expander_name)
        except:
            return st.beta_expander(expander_name)


st.title('The MBTI Consultant')
with try_expander('About'):

    st.markdown('''This is a Periodic Table of the 16 MBTI personalities inspired by Rob van Zoest and his creation of the Periodic Table of NLP Tasks. \
    The motivation of this project is to help people understand their personality better. No doubt, identifying my personality type has helped me to put the \
    pieces of my personality puzzle together. Since then, the haze became clear, so much of my life started to make sense and I hope it would be the same for you.''')

    st.text(" \n")
    st.markdown("Do the test [here](https://www.16personalities.com/free-personality-test) to find out your personality type!" )


# set containers
c1, c2, c3, c4 = st.beta_columns((2,0.1,1,2))
with c1:
    base_price_unit = st.selectbox('Select MBTI type', list(mbti_core))

    title = f'{df_all[df_all["type"] == base_price_unit].category.values[0]} - {df_all[df_all["type"] == base_price_unit].personality.values[0]}'
    st.subheader(title)
    

with c3:
    plot_fonts = ['Helvetica','Times','Arial','century gothic','Bodoni MT']
    plot_font = st.selectbox('Font', plot_fonts, index=0)


path = f'/Users/huijee/Documents/MBTI_icons/{base_price_unit}.png'
image = Image.open(path)
st.image(image, width=300)


# callback
df = df_all[df_all["type"] == base_price_unit]

df = df.rename({"ï»¿atomicnumber":"atomicnumber"}, axis=1)
df["elementname"] = df["elementname"].str.replace('\\n', '\n', regex=False)
df["groupname"] = df["groupname"].str.replace('\\n', ' ', regex=False)
df["exercpt"] = df["excerpt"].str.replace('\\n', ' ', regex=False)

df_group = pd.pivot_table(df, values='atomicnumber', index=['group','groupname'], 
                        columns=[], aggfunc=pd.Series.nunique).reset_index()


periods = [str(x) for x in set(df.period.values.tolist())]
periods_bottomrow = str(len(periods)+1)
periods += [periods_bottomrow]

df["period"] = df.period.astype(str)

groups = [str(x) for x in df_group.group]
groupnames = [str(x) for x in df_group.groupname]


# define properties
title_color = '#3B3838'
text_color = '#3B3838'
groupname_color = '#757171'
trademark_color = '#757171'


plot_scale = 1
plot_width = round(len(groups) * 107 * plot_scale)
plot_height = round(len(periods) * 107 * plot_scale)
title_size = str(round(48 * plot_scale)) + 'px'
element_number_size = str(round(12 * plot_scale)) + 'px'
element_symbol_size = str(round(26 * plot_scale)) + 'px'
element_name_size = str(round(11 * plot_scale)) + 'px'
group_name_size = str(round(12 * plot_scale)) + 'px'
trademark_size = str(round(12 * plot_scale)) + 'px'
text_line_height = 0.6 if plot_scale <= 0.9 else 0.7 if plot_scale <=1.1 else 0.8 if plot_scale < 1.5 else 0.9
border_line_width = 2


# define tooltip
TOOLTIPS = """
    <div style="width:300px; padding:10px;background-color: @color;">
        <div>
            <span style="font-size: 36px; font-weight: bold;">@symbol</span>
        </div>
        <div>
            <span style="font-size: 14px; font-weight: bold; ">@groupname</span>
        </div>
        <br>
        <div>
            <span style="font-size: 20px; font-weight: bold; margin-bottom:20px">@atomicnumber - @elementname</span>
        </div>
        <div>
            <span style="font-size: 15px; ">@excerpt</span>
        </div>
        <br>
        <div>
            <span style="font-size: 10px; ">(@{group}, @{period})</span>
        </div>
"""

# periodic table
p = figure(plot_width=plot_width, plot_height=plot_height,
    x_range=groups,
    y_range=list(reversed(periods)),
    tools="hover",
    toolbar_location="below",
    toolbar_sticky=False,
    tooltips=TOOLTIPS)

# squares
r = p.rect("group", "period", 0.94, 0.94, 
    source=df,
    fill_alpha=0.7, 
    color="color", 
    line_width=border_line_width)

text_props = {"source": df, "text_baseline":"middle", "text_color":text_color}

# number
p.text(x=dodge("group", -0.4, range=p.x_range), 
    y=dodge("period", 0.3, range=p.y_range),
    text="atomicnumber",
    text_align="left",
    text_font=plot_font,
    text_font_style="italic",
    text_font_size=element_number_size,
    **text_props)

# symbol
p.text(x=dodge("group", -0.13, range=p.x_range),
    y=dodge("period", 0.07, range=p.y_range),
    text="symbol",
    text_font=plot_font,
    text_font_style="bold",
    text_font_size=element_symbol_size,
    **text_props)

# element name
p.text(x=dodge("group", 0.0, range=p.x_range),
    y=dodge("period", -0.25, range=p.y_range),
    text="elementname",
    text_align="center",
    text_line_height=text_line_height,
    text_font=plot_font,
    text_font_size=element_name_size,
    **text_props)

# axis 
p.text(x=groups,
    y=[periods_bottomrow for x in groups],
    text=[x.replace(u' ', u'\n') for x in groupnames],
    text_align="center", 
    text_line_height=text_line_height,
    text_baseline="middle",
    text_font=plot_font,
    text_font_size=group_name_size,
    text_color=groupname_color
    )

p.outline_line_color = None
p.grid.grid_line_color = None
p.axis.visible = False
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_standoff = 0
p.hover.renderers = [r] # only hover element boxes

# Allow autohide to true to only show the toolbar when mouse is over plot
p.toolbar.autohide = True


st.bokeh_chart(p)


st.markdown('***')
st.markdown("I hope you've enjoyed reading it as much as I did while working on this project. I'd love feedback on this, so if you want to reach out you can find me on [LinkedIn] (https://www.linkedin.com/in/huijeewong/) :)")