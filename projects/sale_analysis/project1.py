"""
Sales Analytics Dashboard
Comprehensive data analysis and visualization of synthetic sales data
using NumPy, Pandas, and Matplotlib
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# 1. DATA GENERATION - Create Synthetic Sales Dataset
# ============================================================================

def generate_synthetic_data(start_date='2023-01-01', num_days=365):
    """Generate synthetic sales dataset for three products across regions"""
    
    np.random.seed(42)
    
    # Define products, regions, and parameters
    products = ['Product_A', 'Product_B', 'Product_C']
    regions = ['North', 'South', 'East', 'West']
    
    # Generate date range
    dates = pd.date_range(start=start_date, periods=num_days, freq='D')
    
    # Generate synthetic data
    data = []
    for date in dates:
        for product in products:
            for region in regions:
                # Base units sold with seasonal variation
                base_units = np.random.randint(20, 100)
                seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * date.dayofyear / 365)
                units_sold = int(base_units * seasonal_factor)
                
                # Price per unit (varies by product)
                prices = {'Product_A': 50, 'Product_B': 75, 'Product_C': 100}
                price = prices[product]
                
                # Discount rate (0-20%)
                discount_rate = np.random.uniform(0, 0.20)
                
                # Cost per unit (60-70% of price)
                cost_per_unit = price * np.random.uniform(0.60, 0.70)
                
                data.append({
                    'Date': date,
                    'Product': product,
                    'Region': region,
                    'Units_Sold': units_sold,
                    'Price_Per_Unit': price,
                    'Discount_Rate': discount_rate,
                    'Cost_Per_Unit': cost_per_unit
                })
    
    df = pd.DataFrame(data)
    return df

# ============================================================================
# 2. DATA PROCESSING
# ============================================================================

def process_data(df):
    """Process raw data and calculate revenue, cost, and profit"""
    
    # Create a copy to avoid modifying original
    df = df.copy()
    
    # Calculate metrics
    df['Revenue_Before_Discount'] = df['Units_Sold'] * df['Price_Per_Unit']
    df['Discount_Amount'] = df['Revenue_Before_Discount'] * df['Discount_Rate']
    df['Revenue'] = df['Revenue_Before_Discount'] - df['Discount_Amount']
    df['Total_Cost'] = df['Units_Sold'] * df['Cost_Per_Unit']
    df['Profit'] = df['Revenue'] - df['Total_Cost']
    df['Profit_Margin'] = (df['Profit'] / df['Revenue'] * 100).round(2)
    
    return df

# ============================================================================
# 3. TIME-BASED ANALYSIS
# ============================================================================

def extract_time_features(df):
    """Extract month, day of week, quarter, and create time-based aggregations"""
    
    df = df.copy()
    
    # Extract time features
    df['Month'] = df['Date'].dt.month
    df['Month_Name'] = df['Date'].dt.strftime('%B')
    df['Day_Of_Week'] = df['Date'].dt.day_name()
    df['Quarter'] = df['Date'].dt.quarter
    df['Year_Month'] = df['Date'].dt.to_period('M')
    df['Week'] = df['Date'].dt.isocalendar().week
    
    return df

# ============================================================================
# 4. AGGREGATIONS
# ============================================================================

def create_aggregations(df):
    """Create various aggregations for analysis"""
    
    # Daily aggregation
    daily_sales = df.groupby('Date').agg({
        'Units_Sold': 'sum',
        'Revenue': 'sum',
        'Profit': 'sum'
    }).round(2)
    
    # Monthly aggregation
    monthly_sales = df.groupby('Year_Month').agg({
        'Units_Sold': 'sum',
        'Revenue': 'sum',
        'Total_Cost': 'sum',
        'Profit': 'sum',
        'Profit_Margin': 'mean'
    }).round(2)
    
    # Product-wise aggregation
    product_sales = df.groupby('Product').agg({
        'Units_Sold': 'sum',
        'Revenue': 'sum',
        'Profit': 'sum',
        'Profit_Margin': 'mean'
    }).round(2)
    
    # Region-wise aggregation
    region_sales = df.groupby('Region').agg({
        'Units_Sold': 'sum',
        'Revenue': 'sum',
        'Profit': 'sum',
        'Profit_Margin': 'mean'
    }).round(2)
    
    return daily_sales, monthly_sales, product_sales, region_sales

# ============================================================================
# 5. STATISTICAL ANALYSIS
# ============================================================================

def calculate_statistics(df, daily_sales, monthly_sales):
    """Calculate comprehensive statistics"""
    
    stats = {
        'Revenue': {
            'Total': df['Revenue'].sum(),
            'Average': df['Revenue'].mean(),
            'Std_Dev': df['Revenue'].std(),
            'Min': df['Revenue'].min(),
            'Max': df['Revenue'].max()
        },
        'Profit': {
            'Total': df['Profit'].sum(),
            'Average': df['Profit'].mean(),
            'Std_Dev': df['Profit'].std(),
            'Min': df['Profit'].min(),
            'Max': df['Profit'].max()
        },
        'Profit_Margin': {
            'Average': df['Profit_Margin'].mean(),
            'Std_Dev': df['Profit_Margin'].std(),
            'Min': df['Profit_Margin'].min(),
            'Max': df['Profit_Margin'].max()
        },
        'Units_Sold': {
            'Total': df['Units_Sold'].sum(),
            'Average': df['Units_Sold'].mean(),
            'Std_Dev': df['Units_Sold'].std()
        }
    }
    
    return stats

# ============================================================================
# 6. BUSINESS INSIGHTS
# ============================================================================

def generate_insights(df, monthly_sales):
    """Generate business insights from the data"""
    
    insights = {}
    
    # Best and worst performing months
    monthly_profit = monthly_sales['Profit']
    best_month = monthly_profit.idxmax()
    worst_month = monthly_profit.idxmin()
    
    insights['Best_Month'] = {
        'Month': str(best_month),
        'Profit': monthly_profit[best_month]
    }
    
    insights['Worst_Month'] = {
        'Month': str(worst_month),
        'Profit': monthly_profit[worst_month]
    }
    
    # Month-over-month growth
    monthly_profit_pct_change = monthly_profit.pct_change() * 100
    max_growth_month = monthly_profit_pct_change.idxmax()
    max_growth_rate = monthly_profit_pct_change[max_growth_month]
    
    insights['Highest_MoM_Growth'] = {
        'Month': str(max_growth_month),
        'Growth_Rate': f"{max_growth_rate:.2f}%"
    }
    
    # Product performance
    product_profit = df.groupby('Product')['Profit'].sum().sort_values(ascending=False)
    insights['Top_Product'] = {
        'Product': product_profit.idxmax(),
        'Profit': product_profit.max()
    }
    
    # Region performance
    region_profit = df.groupby('Region')['Profit'].sum().sort_values(ascending=False)
    insights['Top_Region'] = {
        'Region': region_profit.idxmax(),
        'Profit': region_profit.max()
    }
    
    # Discount impact
    avg_discount = df['Discount_Rate'].mean() * 100
    insights['Average_Discount'] = f"{avg_discount:.2f}%"
    
    # Profit margin trend
    monthly_margin = df.groupby('Year_Month')['Profit_Margin'].mean()
    margin_trend = 'Increasing' if monthly_margin.iloc[-1] > monthly_margin.iloc[0] else 'Decreasing'
    insights['Profit_Margin_Trend'] = margin_trend
    
    return insights

# ============================================================================
# 7. DATA VISUALIZATION - Dashboard
# ============================================================================

def create_dashboard(df, daily_sales, monthly_sales, product_sales, region_sales, stats, insights):
    """Create comprehensive dashboard with multiple visualizations"""
    
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle('Sales Analytics Dashboard', fontsize=20, fontweight='bold', y=0.995)
    
    # 1. Monthly Profit Bar Chart
    ax1 = plt.subplot(2, 3, 1)
    months = [str(m).split('-')[1] for m in monthly_sales.index]
    bars1 = ax1.bar(months, monthly_sales['Profit'], color='steelblue', alpha=0.8, edgecolor='navy')
    ax1.set_xlabel('Month', fontweight='bold')
    ax1.set_ylabel('Profit ($)', fontweight='bold')
    ax1.set_title('Monthly Profit Trend', fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:,.0f}', ha='center', va='bottom', fontsize=8)
    
    # 2. Revenue vs Profit Trend
    ax2 = plt.subplot(2, 3, 2)
    months_numeric = range(len(monthly_sales))
    ax2.plot(months_numeric, monthly_sales['Revenue'], marker='o', label='Revenue', 
             linewidth=2, color='green', markersize=6)
    ax2.plot(months_numeric, monthly_sales['Profit'], marker='s', label='Profit',
             linewidth=2, color='red', markersize=6)
    ax2.set_xlabel('Month', fontweight='bold')
    ax2.set_ylabel('Amount ($)', fontweight='bold')
    ax2.set_title('Revenue vs Profit Over Time', fontweight='bold')
    ax2.legend()
    ax2.grid(alpha=0.3)
    ax2.set_xticks(months_numeric[::2])
    
    # 3. Product Performance Pie Chart
    ax3 = plt.subplot(2, 3, 3)
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    wedges, texts, autotexts = ax3.pie(product_sales['Profit'], labels=product_sales.index,
                                        autopct='%1.1f%%', colors=colors, startangle=90)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    ax3.set_title('Profit Distribution by Product', fontweight='bold')
    
    # 4. Region Performance Comparison
    ax4 = plt.subplot(2, 3, 4)
    bars4 = ax4.barh(region_sales.index, region_sales['Profit'], color='coral', alpha=0.8, edgecolor='darkred')
    ax4.set_xlabel('Profit ($)', fontweight='bold')
    ax4.set_title('Regional Profit Comparison', fontweight='bold')
    ax4.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, bar in enumerate(bars4):
        width = bar.get_width()
        ax4.text(width, bar.get_y() + bar.get_height()/2.,
                f'${width:,.0f}', ha='left', va='center', fontsize=9, fontweight='bold')
    
    # 5. Monthly Units Sold vs Profit Margin
    ax5 = plt.subplot(2, 3, 5)
    ax5_twin = ax5.twinx()
    bars5 = ax5.bar(months_numeric, monthly_sales['Units_Sold'], alpha=0.6, color='skyblue', 
                    label='Units Sold', edgecolor='navy')
    line5 = ax5_twin.plot(months_numeric, monthly_sales['Profit_Margin'], color='darkred',
                          marker='D', linewidth=2, markersize=6, label='Profit Margin %')
    ax5.set_xlabel('Month', fontweight='bold')
    ax5.set_ylabel('Units Sold', fontweight='bold', color='skyblue')
    ax5_twin.set_ylabel('Profit Margin (%)', fontweight='bold', color='darkred')
    ax5.set_title('Units Sold vs Profit Margin', fontweight='bold')
    ax5.set_xticks(months_numeric[::2])
    ax5.tick_params(axis='y', labelcolor='skyblue')
    ax5_twin.tick_params(axis='y', labelcolor='darkred')
    ax5.grid(alpha=0.3)
    
    # 6. Daily Sales Distribution
    ax6 = plt.subplot(2, 3, 6)
    ax6.hist(daily_sales['Profit'], bins=30, color='mediumpurple', alpha=0.7, edgecolor='purple')
    ax6.axvline(daily_sales['Profit'].mean(), color='red', linestyle='--', linewidth=2, 
                label=f"Mean: ${daily_sales['Profit'].mean():,.0f}")
    ax6.set_xlabel('Daily Profit ($)', fontweight='bold')
    ax6.set_ylabel('Frequency', fontweight='bold')
    ax6.set_title('Distribution of Daily Profit', fontweight='bold')
    ax6.legend()
    ax6.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('sales_analytics_dashboard.png', dpi=300, bbox_inches='tight')
    print("\n[OK] Dashboard saved as 'sales_analytics_dashboard.png'")
    plt.close()  # Close instead of show() to allow execution to continue

# ============================================================================
# 8. PRINT STRUCTURED DASHBOARD SUMMARY
# ============================================================================

def print_dashboard_summary(df, daily_sales, monthly_sales, product_sales, region_sales, stats, insights):
    """Print a beautifully formatted dashboard summary"""
    
    print("\n" + "="*80)
    print(" "*20 + "SALES ANALYTICS DASHBOARD SUMMARY")
    print("="*80)
    
    # Executive Summary
    print("\n[EXECUTIVE SUMMARY]")
    print("-" * 80)
    print(f"Analysis Period: {df['Date'].min().date()} to {df['Date'].max().date()}")
    print(f"Total Days Analyzed: {len(daily_sales)}")
    print(f"Products Covered: {', '.join(df['Product'].unique())}")
    print(f"Regions Covered: {', '.join(df['Region'].unique())}")
    
    # Key Metrics
    print("\n[KEY METRICS]")
    print("-" * 80)
    print(f"Total Revenue:              ${stats['Revenue']['Total']:>15,.2f}")
    print(f"Total Profit:               ${stats['Profit']['Total']:>15,.2f}")
    print(f"Total Units Sold:           {stats['Units_Sold']['Total']:>15,.0f}")
    print(f"Average Daily Profit:       ${stats['Profit']['Average']:>15,.2f}")
    print(f"Average Profit Margin:      {stats['Profit_Margin']['Average']:>14.2f}%")
    print(f"Average Discount Rate:      {insights['Average_Discount']:>15}")
    
    # Revenue & Profit Statistics
    print("\n[REVENUE STATISTICS]")
    print("-" * 80)
    print(f"Average Daily Revenue:      ${stats['Revenue']['Average']:>15,.2f}")
    print(f"Std Dev (Revenue):          ${stats['Revenue']['Std_Dev']:>15,.2f}")
    print(f"Min Daily Revenue:          ${stats['Revenue']['Min']:>15,.2f}")
    print(f"Max Daily Revenue:          ${stats['Revenue']['Max']:>15,.2f}")
    
    print("\n[PROFIT STATISTICS]")
    print("-" * 80)
    print(f"Average Daily Profit:       ${stats['Profit']['Average']:>15,.2f}")
    print(f"Std Dev (Profit):           ${stats['Profit']['Std_Dev']:>15,.2f}")
    print(f"Min Daily Profit:           ${stats['Profit']['Min']:>15,.2f}")
    print(f"Max Daily Profit:           ${stats['Profit']['Max']:>15,.2f}")
    
    # Business Insights
    print("\n[BUSINESS INSIGHTS]")
    print("-" * 80)
    print(f"Best Performing Month:      {insights['Best_Month']['Month']:>15} (${insights['Best_Month']['Profit']:,.2f})")
    print(f"Worst Performing Month:     {insights['Worst_Month']['Month']:>15} (${insights['Worst_Month']['Profit']:,.2f})")
    print(f"Highest MoM Growth:         {insights['Highest_MoM_Growth']['Month']:>15} ({insights['Highest_MoM_Growth']['Growth_Rate']})")
    print(f"Top Performing Product:     {insights['Top_Product']['Product']:>15} (${insights['Top_Product']['Profit']:,.2f})")
    print(f"Top Performing Region:      {insights['Top_Region']['Region']:>15} (${insights['Top_Region']['Profit']:,.2f})")
    print(f"Profit Margin Trend:        {insights['Profit_Margin_Trend']:>15}")
    
    # Product Performance
    print("\n[PRODUCT PERFORMANCE BREAKDOWN]")
    print("-" * 80)
    print(f"{'Product':<20} {'Units Sold':<15} {'Revenue':<15} {'Profit':<15} {'Margin %':<10}")
    print("-" * 80)
    for product in product_sales.index:
        print(f"{product:<20} {product_sales.loc[product, 'Units_Sold']:>12,.0f}   "
              f"${product_sales.loc[product, 'Revenue']:>12,.2f}   "
              f"${product_sales.loc[product, 'Profit']:>12,.2f}   "
              f"{product_sales.loc[product, 'Profit_Margin']:>7.2f}%")
    
    # Regional Performance
    print("\n[REGIONAL PERFORMANCE BREAKDOWN]")
    print("-" * 80)
    print(f"{'Region':<20} {'Units Sold':<15} {'Revenue':<15} {'Profit':<15} {'Margin %':<10}")
    print("-" * 80)
    for region in region_sales.index:
        print(f"{region:<20} {region_sales.loc[region, 'Units_Sold']:>12,.0f}   "
              f"${region_sales.loc[region, 'Revenue']:>12,.2f}   "
              f"${region_sales.loc[region, 'Profit']:>12,.2f}   "
              f"{region_sales.loc[region, 'Profit_Margin']:>7.2f}%")
    
    # Monthly Performance Summary
    print("\n[MONTHLY PERFORMANCE SUMMARY]")
    print("-" * 80)
    print(f"{'Month':<15} {'Units':<12} {'Revenue':<15} {'Profit':<15} {'Margin %':<10}")
    print("-" * 80)
    for month in monthly_sales.index:
        month_str = str(month)
        print(f"{month_str:<15} {monthly_sales.loc[month, 'Units_Sold']:>10,.0f}   "
              f"${monthly_sales.loc[month, 'Revenue']:>12,.2f}   "
              f"${monthly_sales.loc[month, 'Profit']:>12,.2f}   "
              f"{monthly_sales.loc[month, 'Profit_Margin']:>7.2f}%")
    
    # Key Takeaways
    print("\n[KEY TAKEAWAYS]")
    print("-" * 80)
    
    top_month = insights['Best_Month']['Month']
    worst_month = insights['Worst_Month']['Month']
    top_product = insights['Top_Product']['Product']
    top_region = insights['Top_Region']['Region']
    
    print(f"[*] {top_month} was the most profitable month")
    print(f"[*] {worst_month} showed the lowest performance")
    print(f"[*] {top_product} contributed the highest profit")
    print(f"[*] {top_region} region led in revenue generation")
    print(f"[*] Profit margin averaged {stats['Profit_Margin']['Average']:.2f}% across all sales")
    print(f"[*] {insights['Profit_Margin_Trend']} trend in profit margins detected")
    
    print("\n" + "="*80)
    print(" "*25 + "END OF DASHBOARD SUMMARY")
    print("="*80 + "\n")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    
    print("\n[START] Starting Sales Analytics Dashboard Generation...\n")
    
    # Step 1: Generate synthetic data
    print("Step 1: Generating synthetic sales data...")
    df = generate_synthetic_data(start_date='2023-01-01', num_days=365)
    print(f"[OK] Generated {len(df)} records across {len(df['Date'].unique())} days")
    
    # Step 2: Process data
    print("\nStep 2: Processing data and calculating metrics...")
    df = process_data(df)
    print("[OK] Calculated revenue, cost, and profit metrics")
    
    # Step 3: Extract time features
    print("\nStep 3: Extracting time-based features...")
    df = extract_time_features(df)
    print("[OK] Added month, day of week, quarter, and other time features")
    
    # Step 4: Create aggregations
    print("\nStep 4: Creating data aggregations...")
    daily_sales, monthly_sales, product_sales, region_sales = create_aggregations(df)
    print("[OK] Generated daily, monthly, product, and regional aggregations")
    
    # Step 5: Calculate statistics
    print("\nStep 5: Calculating statistical metrics...")
    stats = calculate_statistics(df, daily_sales, monthly_sales)
    print("[OK] Computed revenue, profit, and margin statistics")
    
    # Step 6: Generate insights
    print("\nStep 6: Generating business insights...")
    insights = generate_insights(df, monthly_sales)
    print("[OK] Identified key performance indicators and trends")
    
    # Step 7: Create visualizations
    print("\nStep 7: Creating dashboard visualizations...")
    create_dashboard(df, daily_sales, monthly_sales, product_sales, region_sales, stats, insights)
    print("[OK] Dashboard visualization completed")
    
    # Step 8: Print summary
    print("\nStep 8: Printing structured dashboard summary...")
    print("[PROCESSING] This may take a moment...")
    print_dashboard_summary(df, daily_sales, monthly_sales, product_sales, region_sales, stats, insights)
    
    # Save processed data to CSV for reference
    print("\nStep 9: Saving processed data...")
    df.to_csv('sales_data_processed.csv', index=False)
    monthly_sales.to_csv('monthly_summary.csv')
    print("[OK] Data saved to 'sales_data_processed.csv' and 'monthly_summary.csv'")
    
    print("\n[COMPLETE] Sales Analytics Dashboard Generation Finished!\n")

if __name__ == "__main__":
    main()
