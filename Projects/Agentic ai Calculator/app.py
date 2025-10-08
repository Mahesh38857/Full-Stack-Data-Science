import streamlit as st
from calculator import add, subtract, multiply, divide

st.title("Simple Calculator")

# Input fields
num1 = st.number_input("Enter first number", value=0.0)
num2 = st.number_input("Enter second number", value=0.0)

# Operation buttons
col1, col2, col3, col4 = st.columns(4)
result = None

with col1:
    if st.button("Add"):
        result = add(num1, num2)
with col2:
    if st.button("Subtract"):
        result = subtract(num1, num2)
with col3:
    if st.button("Multiply"):
        result = multiply(num1, num2)
with col4:
    if st.button("Divide"):
        result = divide(num1, num2)

# Display result
if result is not None:
    st.success(f"Result: {result}")
