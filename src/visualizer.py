"""
AetherNova – Kerala Rainfall Trend Detective
NASA Space Apps Challenge 2026: Be an Earth System Trend Detective

Module: src/visualizer.py
Description: Interactive Plotly scientific visualizer for rainfall time-series,
seasonal distributions, spatial maps, and anomaly indicators.
"""

from typing import Dict, Optional
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_annual_rainfall(
    annual_df: pd.DataFrame,
    title_suffix: str = "",
    trend_slope: Optional[float] = None,
    trend_intercept: Optional[float] = None,
) -> go.Figure:
    """Builds interactive annual rainfall bar chart with rolling average and trendline."""
    fig = go.Figure()

    if (
        annual_df is None
        or annual_df.empty
        or "year" not in annual_df.columns
        or "annual_rainfall_mm" not in annual_df.columns
        or len(annual_df) == 0
    ):
        fig.update_layout(
            title=dict(
                text=f"Kerala Annual Rainfall Exploration {title_suffix}".strip(),
                font=dict(size=17, color="#F8FAFC", family="sans-serif"),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#111A33",
            annotations=[
                dict(
                    text="No annual rainfall observations available for the selected criteria.<br>Complete 12-month calendar year observations are required for full annual totals.",
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(size=13, color="#94A3B8"),
                    align="center",
                )
            ],
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False),
            height=420,
            margin=dict(l=40, r=40, t=70, b=40),
        )
        return fig

    # Annual rainfall bars
    fig.add_trace(
        go.Bar(
            x=annual_df["year"],
            y=annual_df["annual_rainfall_mm"],
            name="Annual Total",
            marker=dict(
                color="rgba(0, 240, 255, 0.65)",
                line=dict(color="#00F0FF", width=1.2),
            ),
            hovertemplate="<b>Year %{x}</b><br>Rainfall: %{y:.1f} mm<extra></extra>",
        )
    )

    # Rolling average line
    if "rolling_avg_3yr" in annual_df.columns:
        fig.add_trace(
            go.Scatter(
                x=annual_df["year"],
                y=annual_df["rolling_avg_3yr"],
                mode="lines+markers",
                name="3-Yr Rolling Mean",
                line=dict(color="#38BDF8", width=2.5),
                marker=dict(size=6, color="#00F0FF"),
                hovertemplate="<b>Year %{x}</b><br>3-Yr Mean: %{y:.1f} mm<extra></extra>",
            )
        )

    # Baseline reference line
    if "baseline_mean_mm" in annual_df.columns and len(annual_df) > 0:
        base_val = annual_df["baseline_mean_mm"].iloc[0]
        fig.add_hline(
            y=base_val,
            line_dash="dot",
            line_color="#94A3B8",
            line_width=1.5,
            annotation_text=f"Baseline Mean ({base_val:.0f} mm)",
            annotation_position="bottom right",
            annotation_font_color="#94A3B8",
        )

    # Optional Sen's Slope / Trend Line
    if trend_slope is not None and trend_intercept is not None and len(annual_df) > 1:
        years = annual_df["year"].values
        x_norm = np.arange(len(years))
        trend_y = trend_intercept + trend_slope * x_norm
        fig.add_trace(
            go.Scatter(
                x=years,
                y=trend_y,
                mode="lines",
                name=f"Sen's Slope ({trend_slope:+.1f} mm/yr)",
                line=dict(color="#FBBF24", width=2, dash="dash"),
                hovertemplate="Trend: %{y:.1f} mm<extra></extra>",
            )
        )

    fig.update_layout(
        title=dict(
            text=f"Kerala Annual Rainfall Exploration {title_suffix}".strip(),
            font=dict(size=17, color="#F8FAFC", family="sans-serif"),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#111A33",
        xaxis=dict(
            title=dict(text="Calendar Year", font=dict(color="#94A3B8")),
            tickfont=dict(color="#94A3B8"),
            gridcolor="rgba(255, 255, 255, 0.06)",
            dtick=1 if len(annual_df) <= 10 else 2,
        ),
        yaxis=dict(
            title=dict(text="Total Precipitation (mm)", font=dict(color="#94A3B8")),
            tickfont=dict(color="#94A3B8"),
            gridcolor="rgba(255, 255, 255, 0.06)",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#F1F5F9", size=11),
        ),
        margin=dict(l=40, r=40, t=70, b=40),
        height=420,
    )
    return fig


def plot_rainfall_anomalies(annual_df: pd.DataFrame, title_suffix: str = "") -> go.Figure:
    """Builds interactive anomaly departure chart (surplus vs deficit)."""
    fig = go.Figure()

    if (
        annual_df is None
        or annual_df.empty
        or "year" not in annual_df.columns
        or "anomaly_pct" not in annual_df.columns
        or len(annual_df) == 0
    ):
        fig.update_layout(
            title=dict(
                text=f"Annual Rainfall Anomalies (% Departure from Baseline) {title_suffix}".strip(),
                font=dict(size=16, color="#F8FAFC", family="sans-serif"),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#111A33",
            annotations=[
                dict(
                    text="No annual anomaly records available for the selected criteria.",
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(size=13, color="#94A3B8"),
                    align="center",
                )
            ],
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False),
            height=360,
            margin=dict(l=40, r=40, t=60, b=40),
        )
        return fig

    colors = ["#10B981" if x >= 0 else "#EF4444" for x in annual_df["anomaly_pct"]]

    fig.add_trace(
        go.Bar(
            x=annual_df["year"],
            y=annual_df["anomaly_pct"],
            marker_color=colors,
            name="Anomaly (%)",
            hovertemplate="<b>Year %{x}</b><br>Anomaly: %{y:+.1f}%<extra></extra>",
        )
    )

    fig.add_hline(y=0, line_color="#94A3B8", line_width=1.5)

    fig.update_layout(
        title=dict(
            text=f"Annual Rainfall Anomalies (% Departure from Baseline) {title_suffix}".strip(),
            font=dict(size=16, color="#F8FAFC", family="sans-serif"),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#111A33",
        xaxis=dict(
            title=dict(text="Year", font=dict(color="#94A3B8")),
            tickfont=dict(color="#94A3B8"),
            gridcolor="rgba(255, 255, 255, 0.06)",
        ),
        yaxis=dict(
            title=dict(text="Anomaly (%)", font=dict(color="#94A3B8")),
            tickfont=dict(color="#94A3B8"),
            gridcolor="rgba(255, 255, 255, 0.06)",
            ticksuffix="%",
        ),
        margin=dict(l=40, r=40, t=60, b=40),
        height=360,
    )
    return fig


def plot_seasonal_distribution(seasonal_df: pd.DataFrame, title_suffix: str = "") -> go.Figure:
    """Creates a grouped bar chart showing rainfall contribution across Kerala's 4 seasons."""
    if (
        seasonal_df is None
        or seasonal_df.empty
        or "year" not in seasonal_df.columns
        or "seasonal_rainfall_mm" not in seasonal_df.columns
        or "season" not in seasonal_df.columns
        or len(seasonal_df) == 0
    ):
        fig = go.Figure()
        fig.update_layout(
            title=dict(
                text=f"Seasonal Rainfall Decomposition {title_suffix}".strip(),
                font=dict(size=16, color="#F8FAFC"),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#111A33",
            annotations=[
                dict(
                    text="No seasonal rainfall observations available for the selected criteria.",
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(size=13, color="#94A3B8"),
                    align="center",
                )
            ],
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False),
            height=400,
            margin=dict(l=40, r=40, t=70, b=40),
        )
        return fig

    season_colors = {
        "Southwest Monsoon (Edavappathi)": "#00F0FF",
        "Northeast Monsoon (Thulavarsham)": "#38BDF8",
        "Summer / Pre-Monsoon": "#F59E0B",
        "Winter": "#A855F7",
    }

    fig = px.bar(
        seasonal_df,
        x="year",
        y="seasonal_rainfall_mm",
        color="season",
        color_discrete_map=season_colors,
        barmode="stack",
        title=f"Seasonal Rainfall Decomposition {title_suffix}".strip(),
        labels={"seasonal_rainfall_mm": "Rainfall (mm)", "season": "Season", "year": "Year"},
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#111A33",
        font=dict(color="#F1F5F9"),
        xaxis=dict(
            tickfont=dict(color="#94A3B8"),
            gridcolor="rgba(255, 255, 255, 0.06)",
        ),
        yaxis=dict(
            tickfont=dict(color="#94A3B8"),
            gridcolor="rgba(255, 255, 255, 0.06)",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=10),
        ),
        margin=dict(l=40, r=40, t=70, b=40),
        height=400,
    )
    return fig


def plot_monthly_climatology_chart(climatology_df: pd.DataFrame, title_suffix: str = "") -> go.Figure:
    """Plots monthly mean rainfall curve with min-max variability bands."""
    fig = go.Figure()

    if (
        climatology_df is None
        or climatology_df.empty
        or "month_name" not in climatology_df.columns
        or "mean_mm" not in climatology_df.columns
        or len(climatology_df) == 0
    ):
        fig.update_layout(
            title=dict(
                text=f"Kerala Monthly Precipitation Climatology {title_suffix}".strip(),
                font=dict(size=16, color="#F8FAFC"),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#111A33",
            annotations=[
                dict(
                    text="No monthly climatology observations available for the selected criteria.",
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(size=13, color="#94A3B8"),
                    align="center",
                )
            ],
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False),
            height=380,
            margin=dict(l=40, r=40, t=70, b=40),
        )
        return fig

    # Max band
    fig.add_trace(
        go.Scatter(
            x=climatology_df["month_name"],
            y=climatology_df["max_mm"],
            mode="lines",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip",
        )
    )

    # Min band with fill
    fig.add_trace(
        go.Scatter(
            x=climatology_df["month_name"],
            y=climatology_df["min_mm"],
            mode="lines",
            line=dict(width=0),
            fill="tonexty",
            fillcolor="rgba(0, 240, 255, 0.12)",
            name="Historical Range [Min-Max]",
            hovertemplate="Range Min: %{y:.1f} mm<extra></extra>",
        )
    )

    # Mean line
    fig.add_trace(
        go.Scatter(
            x=climatology_df["month_name"],
            y=climatology_df["mean_mm"],
            mode="lines+markers",
            line=dict(color="#00F0FF", width=3),
            marker=dict(size=7, color="#FFFFFF"),
            name="Mean Rainfall",
            hovertemplate="<b>%{x}</b><br>Mean: %{y:.1f} mm<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(
            text=f"Kerala Monthly Precipitation Climatology {title_suffix}",
            font=dict(size=16, color="#F8FAFC"),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#111A33",
        xaxis=dict(
            tickfont=dict(color="#94A3B8"),
            gridcolor="rgba(255, 255, 255, 0.06)",
        ),
        yaxis=dict(
            title="Monthly Rainfall (mm)",
            tickfont=dict(color="#94A3B8"),
            gridcolor="rgba(255, 255, 255, 0.06)",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11),
        ),
        margin=dict(l=40, r=40, t=70, b=40),
        height=380,
    )
    return fig


def plot_kerala_spatial_map(pixel_df: pd.DataFrame, month_label: str = "June 2024") -> go.Figure:
    """Renders 320 terrestrial satellite pixels on Kerala's base map."""
    if (
        pixel_df is None
        or pixel_df.empty
        or "lat" not in pixel_df.columns
        or "lon" not in pixel_df.columns
        or "rainfall_mm" not in pixel_df.columns
        or len(pixel_df) == 0
    ):
        fig = go.Figure()
        fig.update_layout(
            title=dict(
                text=f"NASA GPM IMERG V07 Terrestrial Spatial Distribution: {month_label}",
                font=dict(size=16, color="#F8FAFC"),
            ),
            paper_bgcolor="#0A0F1D",
            plot_bgcolor="#111A33",
            annotations=[
                dict(
                    text="No spatial pixel validation observations available.",
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(size=13, color="#94A3B8"),
                    align="center",
                )
            ],
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False),
            height=520,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        return fig

    fig = px.scatter_map(
        pixel_df,
        lat="lat",
        lon="lon",
        color="rainfall_mm",
        size=[9] * len(pixel_df),
        color_continuous_scale="Viridis",
        labels={"rainfall_mm": "Rainfall (mm)"},
        title=f"NASA GPM IMERG V07 Terrestrial Spatial Distribution: {month_label}",
        hover_data={"lon": ":.2f", "lat": ":.2f", "rainfall_mm": ":.1f", "rate_mm_hr": ":.3f"},
    )

    fig.update_layout(
        map=dict(
            style="carto-darkmatter",
            center=dict(lat=10.5, lon=76.2),
            zoom=6.6,
        ),
        paper_bgcolor="#0A0F1D",
        font=dict(color="#F1F5F9"),
        margin=dict(l=20, r=20, t=50, b=20),
        coloraxis_colorbar=dict(
            title="Rainfall (mm)",
            tickfont=dict(color="#F1F5F9"),
            title_font=dict(color="#00F0FF"),
        ),
        height=520,
    )
    return fig
