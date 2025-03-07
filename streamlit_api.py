import streamlit as st
from constants import MESSAGES, ACTUAL_CHAT, GPT_MODEL, GPT_API_KEY, API_KEY_FILE
from openai_api import openai_send_message
from utils_files import *


def init_session_state():
    if not MESSAGES in st.session_state:
        st.session_state[MESSAGES] = []
    if not ACTUAL_CHAT in st.session_state:
        st.session_state[ACTUAL_CHAT] = ''
    if not GPT_MODEL in st.session_state:
        st.session_state[GPT_MODEL] = 'gpt-4o'
    if not GPT_API_KEY in st.session_state:
        st.session_state[GPT_API_KEY] = ready_api_key()


def render_main_page():
    messages = ler_mensagens(st.session_state[MESSAGES])
    st.header('🤖 Chatbot', divider=True)

    for message in messages:
        chat = st.chat_message(message['role'])
        chat.markdown(message['content'])

    prompt = st.chat_input('Faça uma pergunta')
    if prompt:
        if st.session_state[GPT_API_KEY] == '':
            st.error('Adicone uma chave de api na aba config')
        else:
            nova_mensagem = {'role': 'user',
                             'content': prompt}
            chat = st.chat_message(nova_mensagem['role'])
            chat.markdown(nova_mensagem['content'])
            messages.append(nova_mensagem)

            chat = st.chat_message('assistant')
            placeholder = chat.empty()
            placeholder.markdown("▌")
            resposta_completa = ''
            respostas = openai_send_message(messages, stream=True)
            for resposta in respostas:
                resposta_completa += resposta.choices[0].delta.get('content', '')
                placeholder.markdown(resposta_completa + "▌")
            placeholder.markdown(resposta_completa)
            nova_mensagem = {'role': 'assistant',
                             'content': resposta_completa}
            messages.append(nova_mensagem)

            st.session_state[MESSAGES] = messages
            salvar_mensagens(messages)


def tab_chats(tab):
    tab.button('➕ Nova conversa',
               on_click=seleciona_conversa,
               args=('', ),
               use_container_width=True)
    tab.markdown('')
    conversas = listar_conversas()
    for nome_arquivo in conversas:
        nome_mensagem = desconverte_nome_mensagem(nome_arquivo).capitalize()
        if len(nome_mensagem) == 30:
            nome_mensagem += '...'
        tab.button(nome_mensagem,
                   on_click=seleciona_conversa,
                   args=(nome_arquivo, ),
                   disabled=nome_arquivo==st.session_state[ACTUAL_CHAT],
                   use_container_width=True)


def tab_config(tab):
    modelo_escolhido = tab.selectbox('Select model',
                                     ['gpt-3.5-turbo', 'gpt-4o-mini', 'gpt-4'])
    st.session_state[GPT_MODEL] = modelo_escolhido

    chave = tab.text_input('Adicione sua api key', value=st.session_state[GPT_API_KEY])
    if chave != st.session_state[GPT_API_KEY]:
        st.session_state[GPT_API_KEY] = chave
        salva_chave(chave)
        tab.success('Chave salva com sucesso')


def ready_api_key():
    if (CONFIG_PATH / API_KEY_FILE).exists():
        with open(CONFIG_PATH / API_KEY_FILE, 'rb') as f:
            return pickle.load(f)
    else:
        return ''


def seleciona_conversa(nome_arquivo):
    if nome_arquivo == '':
        st.session_state[MESSAGES] = []
    else:
        mensagem = ler_mensagem_por_nome_arquivo(nome_arquivo)
        st.session_state[MESSAGES] = mensagem
    st.session_state[ACTUAL_CHAT] = nome_arquivo