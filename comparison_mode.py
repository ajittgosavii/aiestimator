"""
Scenario Comparison Module for Gen AI ROI Calculator
Allows side-by-side comparison of multiple scenarios
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

class ScenarioComparator:
    """Handles comparison of multiple scenarios"""
    
    def __init__(self):
        if 'comparison_scenarios' not in st.session_state:
            st.session_state.comparison_scenarios = {}
    
    def add_scenario_to_comparison(self, scenario_name, cost_data, roi_data, org_profile):
        """Add a scenario to the comparison set"""
        st.session_state.comparison_scenarios[scenario_name] = {
            'cost_data': cost_data,
            'roi_data': roi_data,
            'org_profile': org_profile,
            'added_date': pd.Timestamp.now()
        }
    
    def remove_scenario_from_comparison(self, scenario_name):
        """Remove a scenario from comparison"""
        if scenario_name in st.session_state.comparison_scenarios:
            del st.session_state.comparison_scenarios[scenario_name]
    
    def get_comparison_summary_table(self):
        """Generate summary comparison table"""
        if not st.session_state.comparison_scenarios:
            return None
        
        data = []
        for name, scenario in st.session_state.comparison_scenarios.items():
            cost_data = scenario['cost_data']
            roi_data = scenario['roi_data']
            
            row = {
                'Scenario': name,
                'Year 1 Cost': cost_data.get('year1_total', 0),
                'Year 2 Cost': cost_data.get('year2_total', 0),
                'Year 3 Cost': cost_data.get('year3_total', 0),
                '3-Year TCO': cost_data.get('three_year_tco', 0),
                'Year 1 Benefits': roi_data.get('year1_benefits', 0),
                'Year 2 Benefits': roi_data.get('year2_benefits', 0),
                'Year 3 Benefits': roi_data.get('year3_benefits', 0),
                '3-Year Benefits': roi_data.get('three_year_benefits', 0),
                'Net Benefit': roi_data.get('net_benefit', 0),
                'ROI %': roi_data.get('roi_percentage', 0),
                'Payback (months)': roi_data.get('payback_months', 0)
            }
            data.append(row)
        
        df = pd.DataFrame(data)
        return df
    
    def get_cost_breakdown_comparison(self):
        """Get cost breakdown comparison across scenarios"""
        if not st.session_state.comparison_scenarios:
            return None
        
        categories = ['API Costs', 'Infrastructure', 'Development', 'Data Management', 
                     'Operations', 'Organizational', 'Contingency']
        
        data = []
        for name, scenario in st.session_state.comparison_scenarios.items():
            breakdown = scenario['cost_data'].get('year1_breakdown', {})
            row = {'Scenario': name}
            row.update(breakdown)
            data.append(row)
        
        df = pd.DataFrame(data)
        return df
    
    def create_cost_comparison_chart(self):
        """Create grouped bar chart comparing costs"""
        df = self.get_comparison_summary_table()
        if df is None or df.empty:
            return None
        
        fig = go.Figure()
        
        years = ['Year 1 Cost', 'Year 2 Cost', 'Year 3 Cost']
        for year in years:
            fig.add_trace(go.Bar(
                name=year.replace(' Cost', ''),
                x=df['Scenario'],
                y=df[year],
                text=df[year].apply(lambda x: f'${x/1000:.0f}K'),
                textposition='auto'
            ))
        
        fig.update_layout(
            title='Cost Comparison by Year',
            xaxis_title='Scenario',
            yaxis_title='Cost (USD)',
            barmode='group',
            height=400
        )
        
        return fig
    
    def create_benefits_comparison_chart(self):
        """Create grouped bar chart comparing benefits"""
        df = self.get_comparison_summary_table()
        if df is None or df.empty:
            return None
        
        fig = go.Figure()
        
        years = ['Year 1 Benefits', 'Year 2 Benefits', 'Year 3 Benefits']
        for year in years:
            fig.add_trace(go.Bar(
                name=year.replace(' Benefits', ''),
                x=df['Scenario'],
                y=df[year],
                text=df[year].apply(lambda x: f'${x/1000:.0f}K'),
                textposition='auto'
            ))
        
        fig.update_layout(
            title='Benefits Comparison by Year',
            xaxis_title='Scenario',
            yaxis_title='Benefits (USD)',
            barmode='group',
            height=400
        )
        
        return fig
    
    def create_roi_comparison_chart(self):
        """Create comparison chart for ROI metrics"""
        df = self.get_comparison_summary_table()
        if df is None or df.empty:
            return None
        
        # Create subplots
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('ROI Comparison', 'Payback Period Comparison'),
            specs=[[{'type': 'bar'}, {'type': 'bar'}]]
        )
        
        # ROI chart
        fig.add_trace(
            go.Bar(
                x=df['Scenario'],
                y=df['ROI %'],
                text=df['ROI %'].apply(lambda x: f'{x:.0f}%'),
                textposition='auto',
                name='ROI %',
                marker_color='lightblue'
            ),
            row=1, col=1
        )
        
        # Payback chart
        fig.add_trace(
            go.Bar(
                x=df['Scenario'],
                y=df['Payback (months)'],
                text=df['Payback (months)'].apply(lambda x: f'{x:.0f}m'),
                textposition='auto',
                name='Payback (months)',
                marker_color='lightgreen'
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            height=400,
            showlegend=False
        )
        
        fig.update_yaxes(title_text="ROI %", row=1, col=1)
        fig.update_yaxes(title_text="Months", row=1, col=2)
        
        return fig
    
    def create_cost_breakdown_comparison_chart(self):
        """Create stacked bar chart comparing cost breakdowns"""
        df = self.get_cost_breakdown_comparison()
        if df is None or df.empty:
            return None
        
        categories = ['API Costs', 'Infrastructure', 'Development', 'Data Management', 
                     'Operations', 'Organizational', 'Contingency']
        
        fig = go.Figure()
        
        for category in categories:
            if category in df.columns:
                fig.add_trace(go.Bar(
                    name=category,
                    x=df['Scenario'],
                    y=df[category],
                    text=df[category].apply(lambda x: f'${x/1000:.0f}K' if x > 0 else ''),
                    textposition='inside'
                ))
        
        fig.update_layout(
            title='Cost Breakdown Comparison',
            xaxis_title='Scenario',
            yaxis_title='Cost (USD)',
            barmode='stack',
            height=500
        )
        
        return fig
    
    def create_waterfall_comparison(self):
        """Create waterfall chart showing net benefit buildup"""
        df = self.get_comparison_summary_table()
        if df is None or df.empty:
            return None
        
        # Create waterfall for first scenario as example
        scenario_name = df.iloc[0]['Scenario']
        scenario = st.session_state.comparison_scenarios[scenario_name]
        cost_data = scenario['cost_data']
        roi_data = scenario['roi_data']
        
        # Build waterfall data
        categories = ['Year 1<br>Benefits', 'Year 1<br>Costs', 'Year 1<br>Net',
                     'Year 2<br>Benefits', 'Year 2<br>Costs', 'Year 2<br>Net',
                     'Year 3<br>Benefits', 'Year 3<br>Costs', 'Total<br>Net Benefit']
        
        values = [
            roi_data.get('year1_benefits', 0),
            -cost_data.get('year1_total', 0),
            roi_data.get('year1_benefits', 0) - cost_data.get('year1_total', 0),
            roi_data.get('year2_benefits', 0),
            -cost_data.get('year2_total', 0),
            roi_data.get('year2_benefits', 0) - cost_data.get('year2_total', 0),
            roi_data.get('year3_benefits', 0),
            -cost_data.get('year3_total', 0),
            roi_data.get('net_benefit', 0)
        ]
        
        measures = ['relative', 'relative', 'relative',
                   'relative', 'relative', 'relative',
                   'relative', 'relative', 'total']
        
        fig = go.Figure(go.Waterfall(
            name=scenario_name,
            orientation='v',
            measure=measures,
            x=categories,
            y=values,
            text=[f'${v/1000:.0f}K' for v in values],
            textposition='outside',
            connector={'line': {'color': 'rgb(63, 63, 63)'}}
        ))
        
        fig.update_layout(
            title=f'Financial Waterfall: {scenario_name}',
            height=500,
            showlegend=False
        )
        
        return fig
    
    def create_spider_chart_comparison(self):
        """Create spider/radar chart comparing key metrics"""
        df = self.get_comparison_summary_table()
        if df is None or df.empty:
            return None
        
        # Normalize metrics to 0-100 scale for comparison
        metrics = ['ROI %', '3-Year Benefits', '3-Year TCO', 'Payback (months)']
        
        fig = go.Figure()
        
        for idx, row in df.iterrows():
            # Normalize values (higher is better for benefits/ROI, lower is better for costs/payback)
            normalized = []
            labels = []
            
            # ROI (higher is better) - scale to 0-100
            roi_val = min(100, row['ROI %'] / 5)  # 500% ROI = 100 points
            normalized.append(roi_val)
            labels.append(f"ROI<br>{row['ROI %']:.0f}%")
            
            # Benefits (higher is better) - scale to 0-100
            max_benefits = df['3-Year Benefits'].max()
            benefit_val = (row['3-Year Benefits'] / max_benefits * 100) if max_benefits > 0 else 0
            normalized.append(benefit_val)
            labels.append(f"Benefits<br>${row['3-Year Benefits']/1000:.0f}K")
            
            # Cost efficiency (lower cost is better) - invert scale
            max_cost = df['3-Year TCO'].max()
            cost_val = 100 - (row['3-Year TCO'] / max_cost * 100) if max_cost > 0 else 0
            normalized.append(cost_val)
            labels.append(f"Cost Efficiency<br>${row['3-Year TCO']/1000:.0f}K")
            
            # Payback speed (lower is better) - invert scale
            max_payback = df['Payback (months)'].max()
            payback_val = 100 - (row['Payback (months)'] / max_payback * 100) if max_payback > 0 else 0
            normalized.append(payback_val)
            labels.append(f"Payback Speed<br>{row['Payback (months)']:.0f}m")
            
            fig.add_trace(go.Scatterpolar(
                r=normalized,
                theta=['ROI', 'Benefits', 'Cost Efficiency', 'Payback Speed'],
                fill='toself',
                name=row['Scenario'],
                hovertext=labels,
                hoverinfo='text+name'
            ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            title='Multi-Dimensional Scenario Comparison',
            height=500
        )
        
        return fig
    
    def get_winner_analysis(self):
        """Determine which scenario is best on different criteria"""
        df = self.get_comparison_summary_table()
        if df is None or df.empty:
            return None
        
        analysis = {
            'highest_roi': df.loc[df['ROI %'].idxmax(), 'Scenario'],
            'lowest_cost': df.loc[df['3-Year TCO'].idxmin(), 'Scenario'],
            'highest_benefits': df.loc[df['3-Year Benefits'].idxmax(), 'Scenario'],
            'fastest_payback': df.loc[df['Payback (months)'].idxmin(), 'Scenario'],
            'best_year1': df.loc[(df['Year 1 Benefits'] - df['Year 1 Cost']).idxmax(), 'Scenario']
        }
        
        return analysis


def render_comparison_mode():
    """Render the comparison mode UI"""
    st.header("🔄 Scenario Comparison Mode")
    
    st.markdown("""
    <div class="info-box">
    <strong>Compare Multiple Scenarios Side-by-Side</strong><br>
    Add scenarios to compare different approaches, assumptions, or strategies.
    Analyze which option delivers the best ROI, lowest cost, or fastest payback.
    </div>
    """, unsafe_allow_html=True)
    
    comparator = ScenarioComparator()
    
    # Add current scenario to comparison
    st.markdown("---")
    st.subheader("➕ Add Scenario to Comparison")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        comparison_name = st.text_input(
            "Scenario Name for Comparison",
            value=st.session_state.get('current_scenario_name', 'Scenario 1'),
            key="comparison_scenario_name"
        )
    
    with col2:
        if st.button("➕ Add to Comparison", key="add_to_comparison_btn"):
            if not st.session_state.get('cost_data'):
                st.error("Please complete Cost Analysis first")
            elif not st.session_state.get('roi_data'):
                st.error("Please complete ROI Calculator first")
            else:
                comparator.add_scenario_to_comparison(
                    comparison_name,
                    st.session_state.cost_data,
                    st.session_state.roi_data,
                    st.session_state.get('org_profile', {})
                )
                st.success(f"✅ Added '{comparison_name}' to comparison")
                st.rerun()
    
    # Show current scenarios in comparison
    if st.session_state.comparison_scenarios:
        st.markdown("---")
        st.subheader(f"📊 Comparing {len(st.session_state.comparison_scenarios)} Scenarios")
        
        # Show scenario list with remove buttons
        for scenario_name in list(st.session_state.comparison_scenarios.keys()):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{scenario_name}**")
            with col2:
                if st.button("🗑️", key=f"remove_{scenario_name}"):
                    comparator.remove_scenario_from_comparison(scenario_name)
                    st.rerun()
        
        st.markdown("---")
        
        # Summary Table
        st.subheader("📋 Summary Comparison Table")
        df = comparator.get_comparison_summary_table()
        
        # Format currency columns
        currency_cols = [col for col in df.columns if 'Cost' in col or 'Benefit' in col or 'TCO' in col]
        styled_df = df.style.format({
            **{col: '${:,.0f}' for col in currency_cols},
            'ROI %': '{:.1f}%',
            'Payback (months)': '{:.1f}'
        })
        
        st.dataframe(styled_df, use_container_width=True)
        
        # Export comparison
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Comparison (CSV)",
            data=csv,
            file_name=f"scenario_comparison_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        st.markdown("---")
        
        # Winner Analysis
        st.subheader("🏆 Best Scenario by Criteria")
        winner_analysis = comparator.get_winner_analysis()
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Highest ROI", winner_analysis['highest_roi'])
        with col2:
            st.metric("Lowest Cost", winner_analysis['lowest_cost'])
        with col3:
            st.metric("Highest Benefits", winner_analysis['highest_benefits'])
        with col4:
            st.metric("Fastest Payback", winner_analysis['fastest_payback'])
        with col5:
            st.metric("Best Year 1", winner_analysis['best_year1'])
        
        st.markdown("---")
        
        # Visualizations
        st.subheader("📊 Visual Comparisons")
        
        # Cost comparison
        fig = comparator.create_cost_comparison_chart()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        # Benefits comparison
        fig = comparator.create_benefits_comparison_chart()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        # ROI metrics
        fig = comparator.create_roi_comparison_chart()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        # Cost breakdown
        fig = comparator.create_cost_breakdown_comparison_chart()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        # Spider chart
        fig = comparator.create_spider_chart_comparison()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        # Waterfall (for first scenario)
        if len(st.session_state.comparison_scenarios) > 0:
            fig = comparator.create_waterfall_comparison()
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.info("💡 No scenarios added yet. Complete Cost Analysis and ROI Calculator, then add your first scenario above.")