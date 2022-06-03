import streamlit as st
import numpy as np
import pandas as pd
import time
from PIL import Image

st.title('Streamlit 超入門')
st.sidebar.write('Interactive Widgets')

"""
```python
    st.write('プログレスバーの表示')
    'Start!!'
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
        latest_iteration.text(f'Iteration {i+1}')
        bar.progress(i+1)
        time.sleep(0.05)
```
"""
st.write('プログレスバーの表示')
'Start!!'
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f'Iteration {i+1}')
    bar.progress(i+1)
    time.sleep(0.05)

st.write('DataFrame')

df = pd.DataFrame({
    '1列目': [1, 2, 3, 4],
    '2列目': [10, 20, 30, 40]
})
"""
```python
    st.write(df)
```
"""
st.write(df)
"""
```python
    st.dataframe(df.style.highlight_max(axis=0), width=400,
             height=400)  # 表を縦と横のピクセル数指定しつつ表示できる
```
"""
st.dataframe(df.style.highlight_max(axis=0), width=200,
             height=400)  # 表を縦と横のピクセル数指定しつつ表示できる
"""
```python
    st.table(df.style.highlight_max(axis=0))  # static静的なテーブルを表示できる
```
"""
st.table(df.style.highlight_max(axis=0))  # static静的なテーブルを表示できる


df2 = pd.DataFrame(
    np.random.rand(20, 3),
    columns=['a', 'b', 'c']
)
"""
```python
    st.line_chart(df2)
```
"""
st.line_chart(df2)
"""
```python
    st.area_chart(df2)
```
"""
st.area_chart(df2)
"""
```python
    st.bar_chart(df2)
```
"""
st.bar_chart(df2)

df3 = pd.DataFrame(
    np.random.rand(100, 2)/[50, 50]+[35.69, 139.7],
    columns=['lat', 'lon']
)
"""
```python
    df3 = pd.DataFrame(
        np.random.rand(100, 2)/[50, 50]+[35.69, 139.7],
    columns=['lat', 'lon']
)
    st.map(df3)
```
"""
st.map(df3)
"""
```python
    if st.checkbox('Show Image'):
        img = Image.open('CrckUZJUkAAohC3.jpg')
        st.image(img, caption='ruriruri', use_column_width=True)
```
"""
if st.checkbox('Show Image'):
    img = Image.open('CrckUZJUkAAohC3.jpg')
    st.image(img, caption='ruriruri', use_column_width=True)

"""
```python
    option = st.selectbox('好きなものを選んでください',
                      list(range(1, 11))
    )
    '選んだものは', option, 'です'
```
"""
option = st.selectbox('好きなものを選んでください',
                      list(range(1, 11))
                      )

'選んだものは', option, 'です'

"""
```python
    text = st.sidebar.text_input('好きなものを書き込んでください')
    '書き込んだものは', text
```
"""
text = st.sidebar.text_input('好きなものを書き込んでください')

'書き込んだものは', text
"""
```python
    cond = st.sidebar.slider('度数を選択してください', 0, 100, 50)  # 最小、最大、初期値
    '度数は', cond
```
"""
cond = st.sidebar.slider('度数を選択してください', 0, 100, 50)  # 最小、最大、初期値

'度数は', cond
"""
```python
    left_column, right_column = st.columns(2)
    button = left_column.button('右カラムに文字を表示')
    if button:
        right_column.write('右カラムです')

```
"""
left_column, right_column = st.columns(2)
button = left_column.button('右カラムに文字を表示')
if button:
    right_column.write('右カラムです')

expander = st.expander('Q&A：質問内容1')
expander.write('回答1')
expander = st.expander('Q&A：質問内容2')
expander.write('回答2')
expander = st.expander('Q&A：質問内容3')
expander.write('回答3')
