import pandas as pd
import numpy as np
import gradio as gr
import matplotlib.pyplot as plt

# Simple DCF Calculator Setup
def discounted_cash_flow(fcf, growth_rate, discount_rate, terminal_growth_rate, forecast_years=5):
    fcf_forecast = []
    present_values = []

    for year in range(1, forecast_years + 1):
        fcf_year = fcf * ((1 + growth_rate) ** year)
        discount_factor = (1 + discount_rate) ** year
        present_value = fcf_year / discount_factor

        fcf_forecast.append(fcf_year)
        present_values.append(present_value)

    # Terminal Value Calculation (after final year)
    terminal_value = (fcf_forecast[-1] * (1 + terminal_growth_rate)) / (discount_rate - terminal_growth_rate)
    terminal_value_pv = terminal_value / ((1 + discount_rate) ** forecast_years)

    total_value = sum(present_values) + terminal_value_pv

    return fcf_forecast, present_values, terminal_value, terminal_value_pv, total_value

def dcf_interface(fcf, growth_rate, discount_rate, terminal_growth_rate, forecast_years):
    fcf_forecast, present_values, terminal_value, terminal_value_pv, total_intrinsic_value = discounted_cash_flow(
        fcf, growth_rate, discount_rate, terminal_growth_rate, forecast_years
    )
    df = pd.DataFrame({
        'Year': list(range(1, forecast_years + 1)),
        'Forecasted FCF ($)': fcf_forecast,
        'Present Value of FCF ($)': present_values
    })

    # Plot FCF
    fig, ax = plt.subplots()
    ax.plot(df['Year'], df['Forecasted FCF ($)'], marker='o')
    ax.set_title('Forecasted Free Cash Flow Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Free Cash Flow ($)')
    ax.grid(True)

    summary = f"""
🏦 Total Intrinsic Value Estimate: ${total_intrinsic_value:,.2f}
Terminal Value (undiscounted): ${terminal_value:,.2f}
Present Value of Terminal Value: ${terminal_value_pv:,.2f}
"""
    return df, fig, summary

iface = gr.Interface(
    fn=dcf_interface,
    inputs=[
        gr.Number(label="Initial Free Cash Flow ($)"),
        gr.Number(label="Annual Growth Rate (e.g., 0.06 for 6%)"),
        gr.Number(label="Discount Rate (e.g., 0.08 for 8%)"),
        gr.Number(label="Terminal Growth Rate (e.g., 0.025 for 2.5%)"),
        gr.Number(label="Forecast Years (e.g., 5 or 10)")
    ],
    outputs=[
        gr.Dataframe(label="DCF Forecast Table"),
        gr.Plot(label="Free Cash Flow Forecast Chart"),
        gr.Textbox(label="Summary")
    ],
    examples=[
        [100_560_000_000, 0.06, 0.08, 0.025, 5]  # Example: Apple
    ],
    title="DCF Valuation Calculator",
    description="Estimate a company's intrinsic value using Discounted Cash Flow (DCF) analysis. Adjust inputs or run a preset example."
)

if __name__ == "__main__":
    iface.launch()
