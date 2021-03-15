import streamlit as st 
import numpy as np
import pandas as pd
import requests
import base64

#------------------------------------------------#

#title
st.title("🌐 HTML Table Scraper 🕸️")
st.markdown(" A simple HTML table scraper made in Python 🐍 & the amazing [Streamlit!](https://www.streamlit.io/) ")

st.markdown('### **1️⃣ Enter a URL to scrape **')

#------------------------------------------------------------------#
#main
url = st.text_input("", value='https://stackexchange.com/leagues/1/alltime/stackoverflow', max_chars=None, key=None, type='default')
if url:
	arr= ['https://', 'http://']
	if any(c in url for c in arr):
		header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36","X-Requested-With": "XMLHttpRequest"}

		
		@st.cache(persist = True, show_spinner=False)
		def load_data():
			r = requests.get(url, headers=header)
			return pd.read_html(r.text)


df = load_data()
length = len(df)
if length ==1:
	st.write('This webpage contains 1 table')
else:
	st.write('This webpage contains 1 table', str(length) + 'tables')
if st.button('Show Scraped Tables'):
	st.table(df)
else:
	st.empty()


def createlist(r1,r2):
	return[item for item in range(r1,r2+1)]
r1,r2 = 1, length

funct = createlist(r1,r2)
st.markdown('### **2️⃣ Select a table to export **')

value_selected = st.selectbox('', funct)
df1 = df[value_selected-1]

if df1.empty:
	st.warning('ℹ️ - This DataFrame is empty!')
else:
	df1 = df1.replace(np.nan,'empty cell', regex = True )
	st.dataframe(df1)

##Download the file
csv = df1.to_csv(index = False)
b64 = base64.b64encode(csv.encode()).decode()
st.markdown('### ** ⬇️ Download the selected table to CSV **')
href = f'<a href= "data:file/csv;base64,{b64}" download="filtered_table.csv"> **Click Here**</a>'
st.markdown(href, unsafe_allow_html=True)