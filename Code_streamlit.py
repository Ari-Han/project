import streamlit as st
import pandas as pd
import plotly.express as px
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.by import By

st.title("Title")
if st.button("Recruit Searching"):
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    #잡코리아

    url1 ='https://www.jobkorea.co.kr/'
    driver.get(url1)

    search_box = driver.find_element(By.CSS_SELECTOR, 'div.smKey')
    search_box.click()

    element = driver.find_element(By.CSS_SELECTOR, 'input#stext')
    element.send_keys('데이터분석')

    search_button = driver.find_element(By.CSS_SELECTOR, 'input[id = "common_search_btn"]')
    search_button.click()

    time.sleep(5)

    contents = []
    articles = driver.find_elements(By.CSS_SELECTOR, 'article.list-item')

    for article in articles:
        if not article.is_displayed():
            continue

        data = {}
        
        # Site
        data['Site'] = 'Job_Korea'

        # Col_Company
        try:
            company = article.find_element(By.CSS_SELECTOR, 'div.list-section-corp a.corp-name-link').text.strip()
            data['Col_Company'] = company
        except:
            data['Col_Company'] = ' '
        
        # Col_Recruit
        try:
            recruit = article.find_element(By.CSS_SELECTOR, 'div.list-section-information')
            recruittext = recruit.find_element(By.CSS_SELECTOR, 'a.information-title-link.dev-view').text.strip()
            data['Col_Recruit'] = recruittext
        except:
            data['Col_Recruit'] = ' '

        # Col_detail
        try:
            detail = []
            detail_list = article.find_elements(By.CSS_SELECTOR, 'ul.chip-information-group > li')
            for item in detail_list :
                detailtext = item.text.strip()
                detail.append(detailtext)
            data['Col_detail'] = detail
        except:
            data['Col_detail'] = ' '
        
        # Col_url
        try:
            url = article.find_element(By.CSS_SELECTOR, 'div.list-section-corp a.corp-name-link').get_attribute('href')
            url = url.replace("https://", "") if url else ' '
            data['Col_url'] = url
        except:
            data['Col_url'] = ' '
        
        contents.append(data)

    #사람인

    url2 ='https://www.saramin.co.kr/'
    driver.get(url2)

    search_box = driver.find_element(By.CSS_SELECTOR, 'button#btn_search')
    search_box.click()

    element = driver.find_element(By.CSS_SELECTOR, 'input#ipt_keyword_recruit')
    element.send_keys('데이터분석')

    search_button = driver.find_element(By.CSS_SELECTOR, 'button#btn_search_recruit')
    search_button.click()

    time.sleep(5)

    articles = driver.find_elements(By.CSS_SELECTOR, 'div.content div.item_recruit')

    for article in articles:
        if not article.is_displayed():
            continue

        data = {}
        
        # Site
        data['Site'] = 'Saramin'

        # Col_Company
        try:
            company = article.find_element(By.CSS_SELECTOR, 'strong.corp_name a').text.strip()
            data['Col_Company'] = company
        except:
            data['Col_Company'] = ' '
        
        # Col_Recruit
        try:
            recruittext = article.find_element(By.CSS_SELECTOR, 'h2.job_tit').text.strip()
            data['Col_Recruit'] = recruittext
        except:
            data['Col_Recruit'] = ' '

        # Col_detail
        try:
            detail = []
            spans = article.find_elements(By.CSS_SELECTOR, 'div.job_condition span')
            for span in spans :
                locations = span.find_elements(By.TAG_NAME, 'a')
                if locations :
                    locationtext = ' '.join([location.text.strip() for location in locations])
                    detail.append(locationtext)
                else : 
                    text = span.text.strip()
                    detail.append(text)
            data['Col_detail'] = detail
        except:
            data['Col_detail'] = ' '
        
        # Col_url
        try:
            url = article.find_element(By.CSS_SELECTOR, 'h2.job_tit a').get_attribute('href')
            url = url.replace("https://", "") if url else ' '
            data['Col_url'] = url
        except:
            data['Col_url'] = ' '
        
        contents.append(data)


    df1 = pd.DataFrame(contents)
    df2 = df1.groupby('Site').size().reset_index(name='Count')
    df2 = df2.sort_values(by='Count', ascending = False).reset_index(drop=True)
    df2['Ratio'] = (df2['Count'] / df2['Count'].sum() * 100).round(2)
    st.dataframe(df1)
    st.dataframe(df2)
    fig = px.pie(df2, names='Site', values='Count', title='Recruitment Ratio')
    fig.update_traces(textinfo='percent')
    st.plotly_chart(fig)

