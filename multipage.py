import streamlit as st

import profit_calculator
import price_comparison
import volatility



PAGES = {
    "Crypto vs Stock Index Price": price_comparison,
    "Price Volatility": volatility,
    "Profit Calculator": profit_calculator
}


def main():
    """Main function of the App"""
    st.set_page_config(layout='wide')
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        page.write()


if __name__ == "__main__":
    main()