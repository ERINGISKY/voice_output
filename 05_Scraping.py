import datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
import altair as alt


def get_udemy():
    url = 'https://scraping-for-beginner.herokuapp.com/udemy'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    n_subscriber = soup.find('p', {'class': 'subscribers'}).text
    n_subscriber = int(n_subscriber.split('：')[1])

    n_review = soup.find('p', {'class': 'reviews'}).text
    n_review = int(n_review.split('：')[1])
    return {
        'n_subscriber': n_subscriber,
        'n_review': n_review
    }


def main():
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
    data = worksheet.get_all_values()
    df_sp = pd.DataFrame(data[1:], columns=data[0])
    # udemyの関数を使用して今日の情報を取り出し、スプレッドシートを更新
    udemy_scraping = get_udemy()

    today = datetime.date.today().strftime('%Y/%m/%d')
    udemy_scraping['date'] = today

    df_sp2 = df_sp.append(udemy_scraping, ignore_index=True)

    set_with_dataframe(worksheet, df_sp2, row=1, col=1)


if __name__ == '__main__':
    main()
