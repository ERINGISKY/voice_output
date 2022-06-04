import datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
import altair as alt

# スクレイピングの関数定義ーEc
url_ec = 'https://scraping.official.ec/'
soup_ec = BeautifulSoup(requests.get(url_ec).text, 'html.parser')

item_list = soup_ec.find('ul', {'id': 'itemList'})
items = item_list.find_all('li')
data_ec = []


def get_ec():
    for item in items:
        datum_ec = {}
        datum_ec['title'] = item.find(
            'p', {'class': 'items-grid_itemTitleText_5a0255a1'}).text
        price = item.find('p', {'class': 'items-grid_price_5a0255a1'}).text
        datum_ec['price'] = int(price.replace('¥', '').replace(',', ''))
        datum_ec['link'] = item.find('a')['href']
        is_stock = item.find(
            'p', {'class': 'items-grid_infoItem_5a0255a1 items-grid_status_5a0255a1 items-grid_soldOut_5a0255a1'}) == None
        datum_ec['is_stock'] = '在庫あり' if is_stock == True else '在庫なし'
        data_ec.append(datum_ec)
    df_ec = pd.DataFrame(data_ec)
    return df_ec


def get_worksheet():
    # スプレッドシートの取得
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    credentials = Credentials.from_service_account_file(
        'udemy-scraping.json',
        scopes=scopes
    )

    gc = gspread.authorize(credentials)

    SP_SHEET_KEY = '1Q-lOqjp-_H02vfRRviBOCNrpfta2Dcus-K3DZuGJVdw'
    sh = gc.open_by_key(SP_SHEET_KEY)
    SP_SHEET = 'db'
    worksheet = sh.worksheet(SP_SHEET)
    return worksheet


def get_chart():
    worksheet = get_worksheet()
    data = worksheet.get_all_values()
    df_sp_new = pd.DataFrame(data[1:], columns=data[0])

    # グラフ作成
    df_sp_new = df_sp_new.astype({
        'n_subscriber': int,
        'n_review': int
    })
    ymin1 = df_sp_new['n_subscriber'].min()-10
    ymax1 = df_sp_new['n_subscriber'].max()+10
    ymin2 = df_sp_new['n_review'].min()-10
    ymax2 = df_sp_new['n_review'].max()+10

    source = df_sp_new

    base = alt.Chart(source).encode(
        alt.X('date:T', axis=alt.Axis(title=None))
    )
    line1 = base.mark_line(opacity=0.3, color='#57A44C').encode(
        alt.Y('n_subscriber',
              axis=alt.Axis(title='受講生数', titleColor='#57A44C'), scale=alt.Scale(domain=[ymin1, ymax1]))
    )
    line2 = base.mark_line(stroke='#5276A7', interpolate='monotone').encode(
        alt.Y('n_review',
              axis=alt.Axis(title='レビュー数', titleColor='#5276A7'), scale=alt.Scale(domain=[ymin2, ymax2]))
    )
    chart = alt.layer(line1, line2).resolve_scale(
        y='independent'
    )
    return chart


chart = get_chart()
ec_scraping = get_ec()

# Streamlit書き込み
st.title('Webスクレイピング活用アプリ')


st.altair_chart(chart, use_container_width=True)
# EC情報取得

st.markdown('### EC在庫情報')
st.dataframe(ec_scraping)
