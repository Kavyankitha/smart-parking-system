import streamlit as st
import random
import cv2
import numpy as np
st.title("Smart Public Parking System")
st.subheader("Live Parking Availability")
slots_status = []
for i in range(8):
    slots_status.append(random.choice(["Available", "Occupied"]))
cols = st.columns(4)
for i, slot in enumerate(slots_status):
    if slot == "Available":
        cols[i % 4].success(f"Slot {i+1} 🟢 Available")
    else:
        cols[i % 4].error(f"Slot {i+1} 🔴 Occupied")
st.subheader("Dynamic Parking Fee")
available = slots_status.count("Available")
if available < 3:
    fee = 80
elif available < 6:
    fee = 50
else:
    fee = 30
st.write(f"Current Parking Fee: ₹{fee} per hour")
st.subheader("Find Parking Slot")
if st.button("Find Available Slot"):
    for i, slot in enumerate(slots_status):
        if slot == "Available":
            st.success(f"You can park at Slot {i+1}")
            break
st.subheader("Parking Layout with Virtual Slots")
image = cv2.imread("parking2.jpg")
image = cv2.resize(image, (900, 500))
cars = [
    (150, 140, 80, 120),
    (350, 140, 80, 120),
    (750, 140, 80, 120),
    (350, 300, 80, 120),
    (550, 300, 80, 120)
]
for (x, y, w, h) in cars:
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
slots = [
    (120,120,260,240),
    (300,120,440,240),
    (480,120,620,240),
    (660,120,800,240),

    (120,260,260,380),
    (300,260,440,380),
    (480,260,620,380),
    (660,260,800,380)
]
occupied_count = 0
for (x1, y1, x2, y2) in slots:

    occupied = False

    for (x, y, w, h) in cars:

        cx = x + w // 2
        cy = y + h // 2

        if x1 < cx < x2 and y1 < cy < y2:
            occupied = True

    if occupied:
        color = (0, 0, 255)  # red
        occupied_count += 1
    else:
        color = (0, 255, 0)  # green

    cv2.rectangle(image, (x1, y1), (x2, y2), color, 3)


st.image(image, channels="BGR")
# OCCUPANCY METRICS

total_slots = len(slots)
occupancy = (occupied_count / total_slots) * 100

st.write(f"Total Slots: {total_slots}")
st.write(f"Occupied Slots: {occupied_count}")
st.write(f"Parking Occupancy: {occupancy:.1f}%")