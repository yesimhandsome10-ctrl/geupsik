import streamlit as st
import pandas as pd
import re
from itertools import permutations
from collections import defaultdict
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="급식 규칙 찾기", layout="wide")

@st.cache_data
def load_and_process_data():
    url = "https://raw.githubusercontent.com/it-teacher-go/data-share-/main/songtan_meals_184.csv"
    df = pd.read_csv(url, encoding='utf-8')
    
    # 괄호 및 괄호 안 내용 제거 함수
    def clean_menu(menu_str):
        if pd.isna(menu_str):
            return []
        cleaned = re.sub(r'\(.*?\)', '', str(menu_str))
        items = [item.strip() for item in cleaned.split('|') if item.strip()]
        return items

    transactions = df['메뉴'].apply(clean_menu).tolist()
    
    item_counts = defaultdict(int)
    pair_counts = defaultdict(int)
    
    for t in transactions:
        t_set = set(t)
        for item in t_set:
            item_counts[item] += 1
        # 조건과 결과를 바꾼 규칙(순열) 모두 포함
        for item1, item2 in permutations(t_set, 2):
            pair_counts[(item1, item2)] += 1
            
    total_days = len(transactions)
    unique_items = len(item_counts)
    
    rules = []
    for (item1, item2), co_occurrence in pair_counts.items():
        support = co_occurrence / total_days
        confidence = co_occurrence / item_counts[item1]
        lift = confidence / (item_counts[item2] / total_days)
        
        rules.append({
            '조건': item1,
            '결과': item2,
            '동시': co_occurrence,
            '지지도': support,
            '신뢰도': confidence,
            '향상도': lift
        })
        
    rules_df = pd.DataFrame(rules)
    unique_pairs_
