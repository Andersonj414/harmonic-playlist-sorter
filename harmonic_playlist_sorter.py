import streamlit as st
import pandas as pd

st.set_page_config(page_title="Harmonic Playlist Sorter", layout="wide")
st.title("🎧 Harmonic Flow Playlist Sorter")

st.markdown("Upload a CSV playlist to automatically sort it by harmonic flow.")

uploaded_file = st.file_uploader("📁 Upload your playlist CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    def camelot_sort(camelot_key):
        try:
            num = int(camelot_key[:-1])
            mode = 0 if camelot_key[-1].upper() == 'A' else 1
            return num * 2 + mode
        except:
            return 999

    df['Camelot Sort'] = df['Camelot'].apply(camelot_sort)
    df = df.dropna(subset=['BPM', 'Energy', 'Loud (Db)'])

    df['BPM'] = pd.to_numeric(df['BPM'], errors='coerce')
    df['Energy'] = pd.to_numeric(df['Energy'], errors='coerce')
    df['Loud (Db)'] = pd.to_numeric(df['Loud (Db)'], errors='coerce')

    sorted_df = df.sort_values(
        by=['Camelot Sort', 'BPM', 'Energy', 'Loud (Db)'],
        ascending=[True, True, True, True]
    ).reset_index(drop=True)

    st.success("✅ Playlist sorted successfully!")
    st.dataframe(sorted_df)

    csv = sorted_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Sorted CSV",
        data=csv,
        file_name="harmonically_sorted_playlist.csv",
        mime="text/csv"
    )
