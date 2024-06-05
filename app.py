import os
import streamlit as st
from openai import AzureOpenAI

#ページタイトルとアイコンを設定する。
st.set_page_config(page_title="Custom ChatGPT", page_icon="💬",layout="wide")

#タイトルを表示する。
st.markdown("# Azure OpenAI ChatGPT サンプルアプリケーション")

#サイドバーに説明を表示する。
st.sidebar.header("ChatGPT Demo")
st.sidebar.markdown("Azure OpenAIのChatGPT APIを使ったWebアプリケーションのサンプル画面です。")

#Azure OpenAIへの接続情報を設定する。※適宜編集してください
deployment = os.getenv('OPENAI_DPLOYMENT')
apikey = os.getenv('OPENAI_API_KEY')
base = os.getenv('OPENAI_API_ENDPOINT')
api_version = os.getenv('OPENAI_API_VERSION')#"2023-03-15-preview"

st.sidebar.text("Endpoint："+base)
st.sidebar.text("API Ver："+api_version)
st.sidebar.text("Deployment："+deployment)


client = AzureOpenAI(
  azure_endpoint = base, 
  api_key=apikey,  
  api_version=api_version
)

# チャットの吹き出しスタイル、マークダウンのCSS
CSS = """
<style>
 /* チャットの吹き出しスタイル */ 
 .chat-bubble {
    display: inline-block;
    margin-bottom: 5px; padding: 5px 10px; 
    border-radius: 25px; clear: both; }

.user { background-color: #DCF8C6; float: right; color: black; } 

.assistant { background-color: #E5E5EA; float: left; color: black;} 

code {
  background-color: black;
  color: white;
  display: block;
  padding: 0.5rem;
  overflow-x: auto;
  font-family: monospace, monospace;
  font-size: 0.9rem;
  line-height: 1.2;
  border-radius: 0.25rem;
}

pre code {
  background-color: black;
  color: white;
  padding: 0;
  overflow: visible;
  overflow-x: auto;
  font-size: inherit;
  line-height: inherit;
}

pre {
  background-color: black;
  color: white;
  padding: 0;
  overflow: visible;
  overflow-x: auto;
  font-size: inherit;
  line-height: inherit;
}

@media (prefers-color-scheme: dark) {
  code {
    color: white;
  }
  pre code {
    color: white;
  }
  pre {
    color: white;
  }
}
 </style>
"""

# CSSをStreamlitに適用
st.markdown(CSS, unsafe_allow_html=True)


# 3つのセッションステートを作成する。
if 'generated' not in st.session_state:
  st.session_state['generated'] = []

if 'past' not in st.session_state:
  st.session_state['past'] = []

if 'conversation' not in st.session_state:
  st.session_state['conversation'] = []

# クリアボタンを押した場合、チャットをクリアする。
if st.sidebar.button("Clear Chat"):
  st.session_state['generated'] = []
  st.session_state['past'] = []
  st.session_state['conversation'] = []
  st.session_state["input"] = ""  

# サイドバーでパラメータを設定する
st.sidebar.markdown("ChatGPTのパラメータ設定")
Temperature_temp = st.sidebar.slider("Temperature(温度)", 0.0, 1.0, 0.7, 0.01)
MaxTokens_temp = st.sidebar.slider("Max_Tokens(最大応答トークン数)", 0, 2048, 500, 1)
top_p_temp = st.sidebar.slider("Top_p(上位P)", 0.0, 1.0, 0.9, 0.01)

# Systemの役割を定義する。入力ボックスで指定する
SystemRole = st.sidebar.text_area("System Role(システムの役割)", "あなたは優秀な助手です。丁寧に質問や相談に回答してください")

# Systemの役割をsession_stateに追加する
if SystemRole:
  st.session_state.conversation.append({"role": "system", "content": SystemRole})

# ユーザの入力ボックス
user_input = st.text_area("You: ","", key="input")

# 入力ボックスのクリア
def clear_text():
  st.session_state.input = ""

st.button("Clear text input", on_click=clear_text)
st.write("")

# ユーザの入力があった場合、conversationに追加する。
st.session_state.conversation.append({"role": "user", "content": user_input})

# ユーザの入力があった場合、ChatGPT APIを呼び出す。
if user_input:
  output = client.chat.completions.create(
    model=deployment,
    messages=st.session_state.conversation,
    temperature=Temperature_temp,
    max_tokens=MaxTokens_temp,
    top_p=top_p_temp,
    frequency_penalty=0,
    presence_penalty=0,
  )

  # ChatGPTからの返答をconversationに追加する。
  st.session_state.conversation.append({"role": "assistant", "content":output.choices[0].message.content})
  # ユーザからの入力をpastに追加する。
  st.session_state.past.append(user_input)
  # ChatGPTからの返答をgeneratedに追加する。
  st.session_state.generated.append(output.choices[0].message.content)

# generatedが存在する場合、メッセージを表示する。
if st.session_state['generated']:
  for i in range(len(st.session_state['generated'])-1, -1, -1):
    if st.session_state['past'][i]:
      st.markdown(f'<div class="chat-bubble assistant">{st.session_state["generated"][i]} </div>', unsafe_allow_html=True)
      st.markdown(f'<div class="chat-bubble user">{st.session_state["past"][i]} </div>', unsafe_allow_html=True)