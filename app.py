import streamlit as st
import math

st.set_page_config(page_title='관류형증기보일러 수질 기준 확인', page_icon='💧')
CRITERIA = {'급수': (6.0, 9.0, 350.0), '관수': (10.5, 11.8, 4000.0)}
st.title('관류형증기보일러 수질 기준 확인')
st.write('급수 또는 관수를 선택하고 pH와 전기전도율을 입력하세요.')
sample = st.radio('시료 종류', list(CRITERIA), horizontal=True)
lo, hi, limit = CRITERIA[sample]
st.info(f'과제용 기준: pH {lo:g} ~ {hi:g} / 전기전도율 {limit:g} μS/cm 이하')
with st.form('water_check', clear_on_submit=False):
    ph = st.text_input('pH')
    ec = st.text_input('전기전도율 (μS/cm)')
    submitted = st.form_submit_button('기준 확인', use_container_width=True)
if submitted:
    try:
        p = float(ph.strip().replace(',', '.'))
        e = float(ec.strip().replace(',', '.'))
        if not math.isfinite(p) or not math.isfinite(e) or not 0 <= p <= 14 or e < 0:
            raise ValueError
    except ValueError:
        st.warning('pH는 0~14, 전기전도율은 0 이상의 숫자로 입력하세요.')
    else:
        st.subheader('판정 결과')
        p_ok = lo <= p <= hi
        e_ok = e <= limit
        (st.success if p_ok else st.error)(f'pH {p:g} → ' + ('기준 내' if p_ok else '기준 이탈'))
        (st.success if e_ok else st.error)(f'전기전도율 {e:g} μS/cm → ' + ('기준 내' if e_ok else '기준 초과'))
        (st.success if p_ok and e_ok else st.error)('두 항목 모두 기준 내입니다.' if p_ok and e_ok else '기준 이탈 항목이 있습니다. 원인을 확인해 주세요.')
st.caption('학습용 시제품입니다. 실제 운전 및 정비 판단은 해당 모델의 최신 취급설명서와 현장 승인 기준을 확인하세요.')
