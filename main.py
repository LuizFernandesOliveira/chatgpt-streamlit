import streamlit as st
from streamlit_api import init_session_state, render_main_page, tab_chats, tab_config


# MAIN ==================================================
def main():
    init_session_state()
    render_main_page()
    tab1, tab2 = st.sidebar.tabs(['💬 Chats', '🔗 Config'])
    tab_chats(tab1)
    tab_config(tab2)


if __name__ == '__main__':
    main()
