import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="AI Physics Assistant", layout="centered")

st.title("🚀 Projectile Motion Simulator")
st.write("રોજબરોજના ભૌતિકવિજ્ઞાનનો ઉપયોગ - ગણિત અને AI સાથે")

# યુઝર ઇનપુટ (Sliders)
col1, col2 = st.columns(2)
with col1:
    v0 = st.slider("શરૂઆતનો વેગ (Initial Velocity) [m/s]", 1, 100, 25)
with col2:
    angle = st.slider("ખૂણો (Angle) [degrees]", 1, 90, 45)

g = 9.81 # ગુરુત્વાકર્ષણ પ્રવેગ

# ગણિત (Math Calculations)
theta = math.radians(angle)
t_flight = (2 * v0 * math.sin(theta)) / g
max_height = (v0**2 * (math.sin(theta)**2)) / (2 * g)
range_x = (v0**2 * math.sin(2*theta)) / g

# પરિણામ દર્શાવવા
st.subheader("📊 ગણતરીના પરિણામો (Calculations)")
col3, col4, col5 = st.columns(3)
col3.metric("ઉડાનનો સમય (Time)", f"{t_flight:.2f} s")
col4.metric("મહત્તમ ઊંચાઈ (Height)", f"{max_height:.2f} m")
col5.metric("અંતર (Range)", f"{range_x:.2f} m")

# ગ્રાફ દોરવા માટે (Trajectory Path)
t = np.linspace(0, t_flight, num=100)
x = v0 * np.cos(theta) * t
y = v0 * np.sin(theta) * t - 0.5 * g * t**2

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y, color='blue', linewidth=2)
ax.fill_between(x, y, color='blue', alpha=0.1)
ax.set_title("પ્રોજેક્ટાઈલનો રસ્તો (Trajectory Path)")
ax.set_xlabel("અંતર (Distance in X) [m]")
ax.set_ylabel("ઊંચાઈ (Height in Y) [m]")
ax.set_ylim(bottom=0)
ax.grid(True, linestyle='--', alpha=0.6)

st.pyplot(fig)

# AI Assistant જેવો મેસેજ
st.info(f"💡 **Physics Assistant Note:** જો તમે {angle} ડિગ્રીના ખૂણે અને {v0} m/s ની ઝડપે વસ્તુ ફેંકશો, તો તે બરાબર {range_x:.2f} મીટર દૂર જઈને પડશે!")
