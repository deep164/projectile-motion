import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import google.generativeai as genai

# પેજ સેટઅપ
st.set_page_config(page_title="AI Physics Agent", layout="wide")

st.title("🚀 AI-Powered Physics Simulator")
st.write("Streamlit અને Google Gemini AI સાથે બનાવેલ Customer-Facing Agent")

# ડાબી બાજુ (Sidebar) માં API Key નાખવા માટેની જગ્યા
api_key = st.sidebar.text_input("AQ.Ab8RN6IOQs6kJXsjqMc6RaKrNGiYO0SZ26_th4h5MvmoziD-zQ:", type="password")
st.sidebar.info("આ પ્રોજેક્ટને ચલાવવા માટે Google Gemini API કી જરૂરી છે.")

# યુઝર ઇનપુટ (Sliders)
col1, col2 = st.columns(2)
with col1:
    v0 = st.slider("શરૂઆતનો વેગ (Initial Velocity) [m/s]", 1, 100, 25)
with col2:
    angle = st.slider("ખૂણો (Angle) [degrees]", 1, 90, 45)

# ગણિત (Physics Math)
g = 9.81 
theta = math.radians(angle)
t_flight = (2 * v0 * math.sin(theta)) / g
max_height = (v0**2 * (math.sin(theta)**2)) / (2 * g)
range_x = (v0**2 * math.sin(2*theta)) / g

# પરિણામ દર્શાવવા
st.subheader("📊 ગણતરીના પરિણામો")
col3, col4, col5 = st.columns(3)
col3.metric("ઉડાનનો સમય (Time)", f"{t_flight:.2f} s")
col4.metric("મહત્તમ ઊંચાઈ (Height)", f"{max_height:.2f} m")
col5.metric("અંતર (Range)", f"{range_x:.2f} m")

# ગ્રાફ દોરવા માટે
t = np.linspace(0, t_flight, num=100)
x = v0 * np.cos(theta) * t
y = v0 * np.sin(theta) * t - 0.5 * g * t**2

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(x, y, color='blue', linewidth=2)
ax.fill_between(x, y, color='blue', alpha=0.1)
ax.set_title("પ્રોજેક્ટાઈલનો રસ્તો")
ax.set_xlabel("અંતર (X) [m]")
ax.set_ylabel("ઊંચાઈ (Y) [m]")
ax.set_ylim(bottom=0)
ax.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig)

st.markdown("---")

# ==========================================
# અસલી AI Agent (Gemini Integration)
# ==========================================
st.subheader("🤖 Physics AI Agent સાથે વાત કરો")
st.write("તમે ભૌતિકવિજ્ઞાન કે આ ગ્રાફને લગતો કોઈ પણ પ્રશ્ન પૂછી શકો છો. (ઉદાહરણ: જો પવન ફૂંકાતો હોય તો શું થાય?)")

# ચેટ હિસ્ટ્રી સેવ કરવા
if "messages" not in st.session_state:
    st.session_state.messages = []

# જૂના મેસેજ બતાવવા
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# નવો મેસેજ ઇનપુટ
if prompt := st.chat_input("અહીં તમારો પ્રશ્ન લખો..."):
    # યુઝરનો પ્રશ્ન સ્ક્રીન પર બતાવો
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    if api_key:
        try:
            # Gemini ને કન્ફિગર કરો
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # AI ને બેકગ્રાઉન્ડ માહિતી આપો (Prompt Engineering)
            system_context = f"""
            You are a helpful physics AI assistant. Please reply in Gujarati. 
            The user is running a projectile motion simulation with velocity {v0} m/s and angle {angle} degrees. 
            The max height is {max_height:.2f} m and range is {range_x:.2f} m. 
            Answer the user's question contextually based on these values.
            """
            full_prompt = f"{system_context}\n\nUser Question: {prompt}"
            
            # AI નો જવાબ મંગાવો
            response = model.generate_content(full_prompt)
            
            # જવાબ સ્ક્રીન પર બતાવો
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"Error: {e} (કૃપા કરીને ચેક કરો કે તમારી API Key સાચી છે કે નહીં)")
    else:
        st.warning("⚠️ કૃપા કરીને ડાબી બાજુ (Sidebar) માં તમારી Gemini API Key નાખો.")
