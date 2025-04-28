import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import datetime

# Define current_year at the module level
current_year = datetime.datetime.now().year
# Function to calculate heat index
def calculate_heat_index(temp_celsius, humidity):
    temp_fahrenheit = (1.8 * temp_celsius) + 32
    heat_index = temp_fahrenheit + humidity
    return heat_index

def get_impact(heat_index):
    if heat_index < 150:
        return "Tidak menyebabkan permasalahan performa"
    elif heat_index < 155:
        return "Mulai terjadi gangguan performance ayam"
    elif heat_index < 160:
        return "Penurunan feed intake, peningkatan water intake, dan penurunan performa"
    elif heat_index < 165:
        return "Awal kejadian kematian"
    else:
        return "Dapat menyebabkan tingginya kematian"

# Add favicon to the Streamlit app
st.set_page_config(page_title="Kalkulator Heat Stress Index Ayam Broiler", page_icon="🐔")

st.title("Kalkulator Heat Stress Index Ayam Broiler")

st.write("""
Program ini menghitung Heat Stress Index pada ayam broiler berdasarkan suhu dan kelembaban.
""")

# Input fields
temp = st.number_input("Masukkan Suhu (°C)", min_value=0.0, max_value=50.0, value=31.0)
humidity = st.number_input("Masukkan Kelembaban (%)", min_value=0.0, max_value=100.0, value=70.0)

if st.button("Hitung Heat Stress Index"):
    # Calculate Heat Index
    heat_index = calculate_heat_index(temp, humidity)
    
    # Display results
    st.write("### Hasil Perhitungan:")
    st.write(f"Suhu (°F) = {temp} × 1.8 + 32 = {(1.8 * temp) + 32:.1f}")
    st.write(f"Heat Stress Index = {heat_index:.1f}")
    st.write(f"**Interpretasi:** {get_impact(heat_index)}")
    
    # Add Gauge Chart", ">170"],
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = heat_index,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Heat Stress Index"},
        gauge = {
            'axis': {'range': [None, 170]},
            'steps': [
                {'range': [0, 150], 'color': "lightgreen"},
                {'range': [150, 155], 'color': "yellow"},
                {'range': [155, 160], 'color': "orange"},
                {'range': [160, 165], 'color': "red"},
                {'range': [165, 170], 'color': "darkred"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': heat_index
            }
        }
    ))
    st.plotly_chart(fig_gauge)

    # Add Temperature vs Heat Index Line Chart
    temps = np.linspace(20, 40, 100)
    heat_indices = [calculate_heat_index(t, humidity) for t in temps]
    
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=temps,
        y=heat_indices,
        mode='lines',
        name='Heat Index'
    ))
    fig_line.add_vline(x=temp, line_dash="dash", line_color="red")
    fig_line.add_hline(y=heat_index, line_dash="dash", line_color="red")
    
    # Add the relationship between temperature, heat stress index, and performance impact
    fig_line.add_trace(go.Scatter(
        x=temps,
        y=[get_impact(calculate_heat_index(t, humidity)) for t in temps],
        mode='lines',
        name='Pengaruh Terhadap Performa',
        line=dict(dash='dot')
    ))

    fig_line.update_layout(
        title="Hubungan Suhu dan Heat Stress Index",
        xaxis_title="Suhu (°C)",
        yaxis_title="Heat Stress Index",
        hovermode='x'
    )
    st.plotly_chart(fig_line)

    # Add Additional Insights
    st.write("### Insight Tambahan")
    
    with st.expander("📊 Dampak Heat Stress pada Produktivitas"):
        st.write("""
        - Penurunan konsumsi pakan hingga 20-40%
        - Penurunan Feed Conversion Ratio (FCR)
        - Penurunan berat badan hingga 15-25%
        - Peningkatan mortalitas 2-3x lipat
        """)
    
    with st.expander("🌡️ Zona Suhu Optimal"):
        st.write("""
        - Minggu 1: 31-33°C
        - Minggu 2: 28-30°C
        - Minggu 3: 26-28°C
        - Minggu 4+: 24-26°C
        """)
    
    with st.expander("💡 Tips Pencegahan Heat Stress"):
        st.write("""
        1. Pengaturan ventilasi yang baik
        2. Pemberian air minum yang cukup dan sejuk
        3. Pengaturan kepadatan kandang (<8 ekor/m²)
        4. Pemberian elektrolit tambahan
        5. Penggunaan atap dengan insulasi yang baik
        """)

# Display reference table
st.write("### Tabel Referensi Heat Stress Index")
data = {
    "Heat Index": ["kurang dari 150", "155", "160", "165", "lebih dari 170"],
    "Pengaruh Terhadap Performa": [
        "Tidak menyebabkan permasalahan performa",
        "Mulai terjadi gangguan performance ayam",
        "Penurunan feed intake, peningkatan water intake, dan penurunan performa",
        "Awal kejadian kematian",
        "Dapat menyebabkan tingginya kematian"
    ]
}

df = pd.DataFrame(data)
st.table(df)

# Add source citation with smaller font and italics
st.markdown("""
<div style='font-size: 12px; font-style: italic;'>
Sumber: Fadilah R. 2007. Beternak Unggas Bebas Flu Burung. Agromedia. Jakarta.
</div>
""", unsafe_allow_html=True)

# Footer with LinkedIn profile link and improved styling
st.markdown("""
<hr style="height:1px;border:none;color:#333;background-color:#333;margin-top:30px;margin-bottom:20px">
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align:center; padding:15px; margin-top:10px; margin-bottom:20px">
    <p style="font-size:16px; color:#555">
        © {current_year} Developed by: 
        <a href="https://www.linkedin.com/in/galuh-adi-insani-1aa0a5105/" target="_blank" 
           style="text-decoration:none; color:#0077B5; font-weight:bold">
            <img src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" 
                 width="16" height="16" style="vertical-align:middle; margin-right:5px">
            Galuh Adi Insani
        </a> 
        with <span style="color:#e25555">❤️</span>
    </p>
    <p style="font-size:12px; color:#777">All rights reserved.</p>
</div>
""", unsafe_allow_html=True)

# Hide Streamlit style
hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_st_style, unsafe_allow_html=True)