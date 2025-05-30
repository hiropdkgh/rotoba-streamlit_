
import streamlit as st
import streamlit.components.v1 as components

# تحميل واجهة HTML من ملف خارجي
with open('custom_ui.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# عرض الواجهة
components.html(html_content, height=1000, scrolling=True)
