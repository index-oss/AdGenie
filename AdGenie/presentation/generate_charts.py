import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

CHARTS_DIR = Path(__file__).resolve().parent / "assets"
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

# Set global styles
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 1.2

def generate_ctr_comparison():
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#f8fafc')

    categories = ['Traditional Static Ads\n(Generic / English)', 'AdGenie AI Ads\n(Personalized & Regional)']
    ctrs = [1.80, 7.42]
    colors = ['#94a3b8', '#10b981']

    bars = ax.bar(categories, ctrs, color=colors, width=0.45, edgecolor='#334155', linewidth=1.5, zorder=3)

    # Grid
    ax.grid(axis='y', linestyle='--', alpha=0.5, zorder=0, color='#94a3b8')

    # Value Labels
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}% CTR',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 6),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=14, fontweight='bold',
                    color='#0f172a')

    # Lift annotation
    ax.annotate('⚡ +312% Click-Through Lift!\n(4.1x Higher Conversions)',
                xy=(1, 5.2), xytext=(0.4, 6.2),
                arrowprops=dict(facecolor='#4f46e5', shrink=0.08, width=2, headwidth=8),
                fontsize=11, fontweight='bold', color='#4f46e5',
                bbox=dict(boxstyle="round,pad=0.5", fc="#eef2ff", ec="#6366f1", lw=1.5))

    ax.set_ylabel('Click-Through Rate (%)', fontsize=12, fontweight='bold', color='#1e293b')
    ax.set_title('Click-Through Rate (CTR) Benchmark Comparison', fontsize=14, fontweight='bold', pad=15, color='#0f172a')
    ax.set_ylim(0, 9.5)

    out_path = CHARTS_DIR / "chart_ctr_comparison.png"
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")

def generate_regional_engagement():
    fig, ax = plt.subplots(figsize=(8.5, 5), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#f8fafc')

    languages = ['English\n(Generic)', 'Marathi', 'Punjabi', 'Hindi', 'Hinglish\n(Pop-Culture)']
    rates = [2.10, 5.85, 6.20, 6.95, 8.40]
    colors = ['#94a3b8', '#38bdf8', '#fbbf24', '#f97316', '#6366f1']

    bars = ax.barh(languages, rates, color=colors, height=0.55, edgecolor='#1e293b', linewidth=1.2, zorder=3)
    ax.grid(axis='x', linestyle='--', alpha=0.5, zorder=0, color='#94a3b8')

    for bar in bars:
        width = bar.get_width()
        ax.annotate(f' {width:.2f}%',
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0),
                    textcoords="offset points",
                    ha='left', va='center',
                    fontsize=12, fontweight='bold', color='#0f172a')

    ax.set_xlabel('Conversion Rate (%)', fontsize=12, fontweight='bold', color='#1e293b')
    ax.set_title('Conversion Rate by Ad Language & Tone', fontsize=14, fontweight='bold', pad=15, color='#0f172a')
    ax.set_xlim(0, 10.0)

    out_path = CHARTS_DIR / "chart_regional_engagement.png"
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")

def generate_revenue_growth():
    fig, ax = plt.subplots(figsize=(8.5, 5), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#f8fafc')

    months = ['Month 1', 'Month 2\n(Static)', 'Month 3\n(AdGenie Launch)', 'Month 4', 'Month 5', 'Month 6']
    revenue = [12000, 14200, 38500, 54200, 73000, 96400]

    ax.plot(months, revenue, marker='o', markersize=8, color='#4f46e5', linewidth=3, zorder=4, label='E-Commerce Platform Revenue (INR)')
    ax.fill_between(months, revenue, color='#6366f1', alpha=0.15, zorder=2)
    ax.grid(axis='y', linestyle='--', alpha=0.5, zorder=0, color='#94a3b8')

    # Annotate launch
    ax.annotate('🚀 AdGenie API Integrated\n(+171% instant jump)',
                xy=('Month 3\n(AdGenie Launch)', 38500),
                xytext=('Month 1', 65000),
                arrowprops=dict(facecolor='#10b981', shrink=0.08, width=2, headwidth=8),
                fontsize=11, fontweight='bold', color='#047857',
                bbox=dict(boxstyle="round,pad=0.5", fc="#ecfdf5", ec="#10b981", lw=1.5))

    for m, rev in zip(months, revenue):
        ax.annotate(f'₹{rev:,}',
                    xy=(m, rev),
                    xytext=(0, 9),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=10, fontweight='bold', color='#1e293b')

    ax.set_ylabel('Monthly Ad & Affiliate Revenue (₹)', fontsize=12, fontweight='bold', color='#1e293b')
    ax.set_title('E-Commerce Revenue Growth Post AdGenie API Adoption', fontsize=14, fontweight='bold', pad=15, color='#0f172a')
    ax.set_ylim(0, 115000)

    out_path = CHARTS_DIR / "chart_revenue_growth.png"
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    generate_ctr_comparison()
    generate_regional_engagement()
    generate_revenue_growth()
    print("All presentation charts generated successfully!")
