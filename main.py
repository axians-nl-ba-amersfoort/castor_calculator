import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Castor App", page_icon='logo-castor-inter.png', layout="wide")

col1, col2 = st.columns([3, 1])
with col2:
    st.image("logo-castor-inter.png", width=200)
    st.markdown(
        """
        <style>
        .css-1aumxhk {
            background-color: #f0f2f5;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
with col1:
    st.title("Castor App")
    st.subheader("Calculate your profit with Castor")
    st.write("This app calculates the profit you can make with Castor based on the number of paid stocks you buy.")

st.markdown("---")


# --- Sidebar Inputs ---
st.sidebar.title("Investment Details")
AMOUNT = st.sidebar.number_input("Enter the amount you want to invest", min_value=0, step=1, value=1000)
stock_price = 112.37

# --- Bonus Calculation ---
def calculate_free_stocks_from_paid(paid_stocks):
    if paid_stocks <= 10:
        return paid_stocks * 2
    elif 10 < paid_stocks <= 40:
        return 10 * 2 + (paid_stocks - 10) * 1
    elif 40 < paid_stocks <= 100:
        return 10 * 2 + 30 * 1 + (paid_stocks - 40) * 0.5
    else:
        return 10 * 2 + 30 * 1 + 60 * 0.5

# --- Interpolated Bonus ---
def calculate_interpolated_bonus(paid_stocks):
    lower = int(paid_stocks)
    upper = lower + 1
    frac = paid_stocks - lower
    lower_bonus = calculate_free_stocks_from_paid(lower)
    upper_bonus = calculate_free_stocks_from_paid(upper)
    return lower_bonus * (1 - frac) + upper_bonus * frac

# --- Main Calculation ---
paid_stocks = round(AMOUNT / stock_price, 2)
bonus_stocks = int(calculate_free_stocks_from_paid(int(paid_stocks)))
total_stocks = paid_stocks + bonus_stocks
total_value = total_stocks * stock_price
total_profit = total_value - AMOUNT
profit_percentage = (total_profit / AMOUNT) * 100 if AMOUNT > 0 else 0

# --- Display Results ---

col1, col2 = st.columns([1, 3])
with col1:
    st.write("### Result")
    st.write(f"Paid Stocks: {round(paid_stocks, 1)}")
    st.write(f"Free Stocks: {bonus_stocks}")
    st.write(f"Total Stocks: {round(total_stocks, 1)}")
    st.write(f"Total Investment: €{AMOUNT:.2f}")
    st.write(f"Total Profit: €{total_profit:.2f}")
    st.write(f"Total Profit Percentage: {profit_percentage:.2f}%")

# --- Data for Altair Plot ---
max_paid_stocks = int(AMOUNT // stock_price) + 10
x_vals = [x / 2 for x in range(2, max(301, max_paid_stocks * 2 + 1))]  # 1.0 to ~300
profit_euros = []

for x in x_vals:
    investment = x * stock_price
    bonus = calculate_interpolated_bonus(x)
    total = x + bonus
    total_value = total * stock_price
    profit = total_value - investment
    profit_euros.append(profit)

df = pd.DataFrame({
    'Paid Stocks': x_vals,
    'Profit (€)': profit_euros
})

highlight_df = pd.DataFrame({
    'Paid Stocks': [round(paid_stocks, 2)],
    'Profit (€)': [total_profit]
})

st.markdown("---")

# --- Altair Chart ---
with col2:
    st.write("### Profit (in €) vs. Paid Stocks (Altair Interactive)")

    line = alt.Chart(df).mark_line(color='steelblue').encode(
        x=alt.X('Paid Stocks', title='Number of Paid Stocks'),
        y=alt.Y('Profit (€)', title='Profit (€)'),
        tooltip=['Paid Stocks', 'Profit (€)']
    ).properties(width=700, height=400)

    point = alt.Chart(highlight_df).mark_point(color='red', size=100).encode(
        x='Paid Stocks',
        y='Profit (€)',
        tooltip=['Paid Stocks', 'Profit (€)']
    )


    st.altair_chart(line + point)
