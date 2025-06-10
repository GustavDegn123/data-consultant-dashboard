import plotly.express as px

def plot_payment_sums(df):
    fig = px.pie(df, names="payment_type", values="payment_value",
                 title="Fordeling af betalingstyper")
    return fig

def plot_avg_installments(df):
    fig = px.bar(
        df,
        x="payment_type",
        y="avg_installments",  # <-- Dette skal matche df's kolonne
        title="Gennemsnitligt antal afbetalinger pr. betalingstype",
        labels={"avg_installments": "Antal afbetalinger", "payment_type": "Betalingstype"},
    )
    fig.update_layout(xaxis_title="Betalingstype", yaxis_title="Antal afbetalinger")
    return fig

