import plotly.graph_objs as go
from django.db.models import Count
from plotly.offline import plot
from .models import Straight, Action, Parlay3, Parlay4


def generate_bets_bar_graph():
    # Query the number of bets for each type
    straight_count = Straight.objects.count()
    action_count = Action.objects.count()
    parlay3_count = Parlay3.objects.count()
    parlay4_count = Parlay4.objects.count()
    total_count = straight_count + action_count + parlay3_count + parlay4_count

    # Prepare data for the bar graph
    x = ["Straight", "Action", "Parlay3", "Parlay4"]
    y = [straight_count, action_count, parlay3_count, parlay4_count]

    # Create the bar graph
    fig = go.Figure(
        data=[
            go.Bar(
                x=x,
                y=y,
                marker=dict(color=["#636EFA", "#EF553B", "#00CC96", "#AB63FA"]),
            )
        ]
    )

    graph_title = f"Number of Bets by Type (Total Bets = {total_count})"

    fig.update_layout(
        title=graph_title,
        xaxis_title="Bet Type",
        yaxis_title="Number of Bets",
    )

    # Render the graph as an HTML div
    graph_div = plot(fig, auto_open=False, output_type="div")
    return graph_div
