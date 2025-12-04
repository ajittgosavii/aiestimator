import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json

# Helper modules temporarily disabled - using built-in functionality
# from save_load_manager import ScenarioManager, render_save_load_ui, enable_auto_save
# from input_validation import (
#     InputValidator, 
#     validate_cost_inputs, 
#     validate_roi_inputs,
#     validate_before_calculation,
#     show_validation_summary
# )
# from comparison_mode import ScenarioComparator, render_comparison_mode
# from industry_benchmarks import render_benchmark_analysis, INDUSTRY_BENCHMARKS
# from optimization_engine import generate_optimization_recommendations, calculate_optimization_roi
# from calculator_helpers import DEMO_DATA, DEMO_ROI_DATA, calculate_intelligent_risks

# Demo data - inline for now
DEMO_DATA = {
    'org_name': 'TechCorp Solutions',
    'industry': 'Technology',
    'use_case': 'Customer Service/Chatbots',
    'year1_total': 2245993,
    'year2_total': 2343190,
    'year3_total': 2514331,
    'three_year_tco': 7103513,
    'year1_breakdown': {
        'API Costs': 78038,
        'Infrastructure': 60000,
        'Development': 960000,
        'Data Management': 280000,
        'Operations': 350000,
        'Organizational': 225000,
        'Contingency': 292956
    }
}

DEMO_ROI_DATA = {
    'roi_percentage': 63.4,
    'payback_months': 1,
    'npv': 0,
    'total_benefits': 0,
    'total_costs': 0
}

# Page configuration
st.set_page_config(
    page_title="Gen AI ROI & TCO Calculator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional appearance
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 1rem 2rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #1f77b4 0%, #2c5aa0 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Navigation styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        padding: 0 24px;
        background-color: white;
        border-radius: 8px;
        font-weight: 500;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e3f2fd;
        border-color: #1f77b4;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4 !important;
        color: white !important;
        border-color: #1f77b4 !important;
    }
    
    /* Metric styling */
    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Info boxes */
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 20px;
        border-radius: 8px;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 20px;
        border-radius: 8px;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .info-box {
        background-color: #d1ecf1;
        border-left: 5px solid #17a2b8;
        padding: 20px;
        border-radius: 8px;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Section headers */
    h1 {
        color: #1f77b4;
        padding-bottom: 15px;
        border-bottom: 3px solid #1f77b4;
        margin-bottom: 20px;
    }
    
    h2 {
        color: #2c5aa0;
        margin-top: 30px;
        padding-bottom: 10px;
        border-bottom: 2px solid #e0e0e0;
    }
    
    h3 {
        color: #1f77b4;
        margin-top: 20px;
    }
    
    /* Cards and containers */
    .stExpander {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        margin-bottom: 10px;
        background-color: white;
    }
    
    /* Input fields */
    .stNumberInput, .stSelectbox, .stTextInput {
        background-color: white;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        border: none;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #1557a0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Download buttons */
    .stDownloadButton > button {
        background-color: #28a745;
        color: white;
    }
    
    .stDownloadButton > button:hover {
        background-color: #218838;
    }
    
    /* Sidebar (minimized) */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 30px;
        background-color: #f8f9fa;
        border-radius: 10px;
        margin-top: 50px;
        color: #666;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'calculation_done' not in st.session_state:
    st.session_state.calculation_done = False
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = 'Live'
if 'demo_loaded' not in st.session_state:
    st.session_state.demo_loaded = False

# Demo data - Realistic Customer Service Chatbot scenario
DEMO_DATA = {
    'org_profile': {
        'org_name': 'TechCorp Solutions',
        'industry': 'Technology',
        'org_size': '500-1000',
        'maturity': 'Pilot',
        'use_case': 'Customer Service/Chatbots',
        'expected_users': 200
    },
    'ai_costs': {
        'model_provider': 'Anthropic (Claude)',
        'avg_tokens_per_request': 2500,
        'requests_per_day': 5000,
        'cost_per_million_tokens': 15.0,
        'growth_rate': 50,
        'embedding_cost': 800
    },
    'infrastructure': {
        'compute_cost': 3000,
        'storage_cost': 800,
        'networking_cost': 400,
        'security_tools': 1500,
        'monitoring_tools': 1000,
        'backup_dr': 500
    },
    'development': {
        'ai_engineers': 2.0,
        'ai_engineer_cost': 180000,
        'backend_devs': 2.0,
        'backend_cost': 150000,
        'frontend_devs': 1.5,
        'frontend_cost': 130000,
        'qa_engineers': 1.0,
        'qa_cost': 120000,
        'dev_tools': 60000
    },
    'data_management': {
        'data_engineers': 1.5,
        'data_engineer_cost': 160000,
        'data_prep_cost': 75000,
        'data_quality_tools': 40000,
        'data_labeling': 50000
    },
    'operations': {
        'ops_engineers': 1.5,
        'ops_cost': 170000,
        'support_staff': 2.0,
        'support_cost': 100000,
        'incident_mgmt': 40000,
        'model_retraining': 60000
    },
    'organizational': {
        'training_cost': 80000,
        'change_mgmt': 100000,
        'governance_cost': 70000,
        'legal_cost': 50000
    },
    'contingency_pct': 18,
    'vendor_lock_in': 'Basic (Multi-provider testing)',
    'roi_benefits': {
        'time_saved_per_user': 6.0,
        'hourly_rate': 75,
        'affected_users': 200,
        'productivity_pct': 75,
        'customer_service_reduction': 150000,
        'process_automation_value': 200000,
        'error_reduction_value': 75000,
        'cost_reduction_confidence': 70,
        'new_revenue': 250000,
        'customer_retention': 120000,
        'revenue_confidence': 55,
        'competitive_advantage': 180000,
        'innovation_value': 130000,
        'strategic_confidence': 60
    }
}

# Header with professional styling
st.markdown("""
    <div class="main-header">
        <h1 style="color: white; border: none; margin: 0; font-size: 2.5rem;">🤖 Gen AI ROI & TCO Calculator</h1>
        <p style="color: #e3f2fd; font-size: 1.2rem; margin-top: 10px;">Enterprise-Grade Analysis for Informed AI Investment Decisions</p>
    </div>
""", unsafe_allow_html=True)

# Mode Selector
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    mode = st.radio(
        "Select Mode",
        options=["🎓 Demo Mode", "💼 Live Mode"],
        index=0 if st.session_state.app_mode == 'Demo' else 1,
        horizontal=True,
        help="Demo Mode: See a complete example with sample data | Live Mode: Enter your own data"
    )
    
    # Update session state based on selection
    if mode == "🎓 Demo Mode" and st.session_state.app_mode != 'Demo':
        st.session_state.app_mode = 'Demo'
        st.session_state.demo_loaded = False
        st.rerun()
    elif mode == "💼 Live Mode" and st.session_state.app_mode != 'Live':
        st.session_state.app_mode = 'Live'
        st.rerun()

# Mode explanation
if st.session_state.app_mode == 'Demo':
    st.markdown("""
    <div class="info-box">
    <strong>🎓 Demo Mode Active</strong><br>
    Explore a complete example with realistic data for a Customer Service Chatbot implementation.
    All fields are pre-populated. Navigate through tabs to see the full analysis.
    Switch to <strong>Live Mode</strong> when ready to input your own data.
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="info-box">
    <strong>💼 Live Mode Active</strong><br>
    Enter your organization's data to calculate TCO and ROI. Need help? Switch to <strong>Demo Mode</strong> to see an example first.
    </div>
    """, unsafe_allow_html=True)

# Enable auto-save functionality (temporarily disabled)
# enable_auto_save(interval_seconds=30)

# Save/Load UI (temporarily disabled)
# st.markdown("---")
# render_save_load_ui()
# st.markdown("---")

# Create centered tabs for navigation
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📊 Overview", 
    "💰 Cost Analysis", 
    "📈 ROI Calculator", 
    "⚠️ Risk Assessment",
    "🤖 AI Recommendations",
    "🔍 Model Selector",
    "🔄 Comparison Mode", 
    "📋 Summary Report"
])

# Tab 1: Overview Section
with tab1:
    st.header("Understanding the True Cost of Gen AI Implementation")
    
    st.markdown("""
    <div class="info-box">
    <h3>📍 How to Use This Calculator</h3>
    <p>Navigate through the tabs above in order:</p>
    <ol>
        <li><strong>Overview</strong> - Understand what costs to consider (you are here)</li>
        <li><strong>Cost Analysis</strong> - Input your organization's cost data</li>
        <li><strong>ROI Calculator</strong> - Estimate benefits and calculate returns</li>
        <li><strong>Risk Assessment</strong> - Identify and quantify risks</li>
        <li><strong>Summary Report</strong> - Review findings and export results</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-box">
        <h3>Why This Calculator?</h3>
        <p>Organizations often underestimate Gen AI costs by <strong>60-80%</strong> by focusing only on API costs. 
        This calculator provides a comprehensive view of:</p>
        <ul>
            <li>Direct & Indirect Costs</li>
            <li>Hidden Infrastructure Expenses</li>
            <li>Organizational Change Costs</li>
            <li>Risk-Adjusted Returns</li>
            <li>Long-term Sustainability</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="warning-box">
        <h3>⚠️ Commonly Overlooked Factors</h3>
        <ul>
            <li>Model drift and retraining costs</li>
            <li>Data preparation & quality management</li>
            <li>Prompt engineering iterations</li>
            <li>Governance & compliance overhead</li>
            <li>Shadow IT and uncontrolled usage</li>
            <li>Vendor lock-in risks</li>
            <li>Skills gap and training needs</li>
            <li>Integration complexity</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Cost categories overview
    st.subheader("📑 Comprehensive Cost Categories")
    
    cost_categories = {
        "Direct AI Costs": ["API/Model Usage", "Token Consumption", "Fine-tuning", "Embedding Generation", "Vector Database"],
        "Infrastructure": ["Compute Resources", "Storage", "Networking", "Security", "Monitoring Tools", "Dev/Test/Prod Environments"],
        "Development & Engineering": ["Team Salaries", "Tools & Platforms", "Testing & QA", "Integration Development", "Prompt Engineering"],
        "Data Management": ["Data Preparation", "Data Quality", "Data Governance", "Data Storage", "Data Pipeline"],
        "Operations & Maintenance": ["24/7 Support", "Incident Management", "Model Monitoring", "Performance Optimization", "Retraining"],
        "Organizational": ["Change Management", "Training Programs", "Governance Framework", "Compliance", "Risk Management"],
        "Risk & Contingency": ["Model Failure", "Accuracy Degradation", "Vendor Changes", "Regulatory Changes", "Security Incidents"]
    }
    
    cols = st.columns(3)
    for idx, (category, items) in enumerate(cost_categories.items()):
        with cols[idx % 3]:
            with st.expander(f"**{category}**"):
                for item in items:
                    st.markdown(f"• {item}")


# Tab 2: Cost Analysis Section
with tab2:
    st.header("Detailed Cost Analysis")
    
    # Load demo data if in demo mode and not yet loaded
    if st.session_state.app_mode == 'Demo' and not st.session_state.demo_loaded:
        st.info("📊 Loading demo data... This represents a typical mid-size Customer Service Chatbot implementation.")
        st.session_state.demo_loaded = True
    
    st.markdown("""
    <div class="info-box">
    <strong>Instructions:</strong> Fill in all relevant fields. Use conservative estimates where uncertain. 
    All costs should be in USD and on an annual basis unless specified otherwise.
    """ + (" <br><strong>🎓 Demo Mode:</strong> All fields are pre-filled with realistic example data." if st.session_state.app_mode == 'Demo' else "") + """
    </div>
    """, unsafe_allow_html=True)
    
    # Organization Profile
    st.subheader("🏢 Organization Profile")
    col1, col2, col3 = st.columns(3)
    
    # Helper function to get demo value
    def get_demo_value(section, key, default):
        if st.session_state.app_mode == 'Demo':
            return DEMO_DATA.get(section, {}).get(key, default)
        return default
    
    with col1:
        org_name = st.text_input("Organization Name", 
            value=get_demo_value('org_profile', 'org_name', ''),
            placeholder="Your Company Inc.")
        industry = st.selectbox("Industry", 
            ["Financial Services", "Healthcare", "Technology", "Manufacturing", "Retail", "Government", "Other"],
            index=["Financial Services", "Healthcare", "Technology", "Manufacturing", "Retail", "Government", "Other"].index(
                get_demo_value('org_profile', 'industry', 'Technology')))
    
    with col2:
        org_size = st.selectbox("Organization Size", 
            ["<100", "100-500", "500-1000", "1000-5000", "5000+"],
            index=["<100", "100-500", "500-1000", "1000-5000", "5000+"].index(
                get_demo_value('org_profile', 'org_size', '500-1000')))
        st.session_state.org_size = org_size  # Store for AI risk assessment
        
        maturity = st.selectbox("AI Maturity Level", 
            ["Exploring", "Pilot", "Scaling", "Mature"],
            index=["Exploring", "Pilot", "Scaling", "Mature"].index(
                get_demo_value('org_profile', 'maturity', 'Pilot')))
        st.session_state.maturity = maturity  # Store for AI risk assessment
    
    with col3:
        use_case = st.selectbox("Primary Use Case", 
            ["Customer Service/Chatbots", "Content Generation", "Code Assistance", "Data Analysis", 
             "Document Processing", "Knowledge Management", "Multiple Use Cases"],
            index=["Customer Service/Chatbots", "Content Generation", "Code Assistance", "Data Analysis", 
             "Document Processing", "Knowledge Management", "Multiple Use Cases"].index(
                get_demo_value('org_profile', 'use_case', 'Customer Service/Chatbots')))
        expected_users = st.number_input("Expected Active Users", 
            min_value=1, 
            value=int(get_demo_value('org_profile', 'expected_users', 100)))
    
    st.markdown("---")
    

    st.markdown("---")
    
    


    st.markdown("---")
    
    # Cost Estimation Help Section
    st.subheader("💡 Need Help Estimating Costs?")
    st.markdown("**New to Gen AI costing? We'll help you estimate each field with industry benchmarks and smart defaults.**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 Use Smart Defaults", type="primary", help="Auto-fill with industry-standard estimates", key="smart_defaults_btn"):
            # Smart defaults based on org profile
            use_case_multipliers = {
                'Customer Service/Chatbots': 30, 'Content Generation': 10,
                'Code Assistance': 25, 'Data Analysis': 15,
                'Document Processing': 8, 'Knowledge Management': 12,
                'Multiple Use Cases': 20
            }
            
            smart_requests = int(expected_users * use_case_multipliers.get(use_case, 20))
            
            use_case_tokens = {
                'Customer Service/Chatbots': 1800, 'Content Generation': 4500,
                'Code Assistance': 3000, 'Data Analysis': 3500,
                'Document Processing': 5000, 'Knowledge Management': 2500,
                'Multiple Use Cases': 2500
            }
            
            smart_tokens = use_case_tokens.get(use_case, 2000)
            
            industry_costs = {
                'Financial Services': 18.0, 'Healthcare': 18.0, 'Government': 20.0,
                'Technology': 12.0, 'Manufacturing': 12.0, 'Retail': 15.0, 'Other': 15.0
            }
            
            smart_cost_per_m = industry_costs.get(industry, 15.0)
            
            maturity_infra = {
                'Exploring': 1500, 'Pilot': 5000, 'Scaling': 15000, 'Mature': 50000
            }
            
            smart_infra = maturity_infra.get(maturity, 5000)
            
            size_dev = {
                '<100': 250000, '100-500': 450000, '500-1000': 700000,
                '1000-5000': 1200000, '5000+': 2500000
            }
            
            smart_dev = size_dev.get(org_size, 450000)
            
            st.session_state.smart_defaults = {
                'requests_per_day': smart_requests,
                'avg_tokens': smart_tokens,
                'cost_per_million': smart_cost_per_m,
                'monthly_infrastructure': smart_infra,
                'annual_development': smart_dev
            }
            
            st.success(f"✅ Smart defaults loaded for {industry}, {maturity} stage!")
            st.info(f"📊 {smart_requests:,} requests/day, {smart_tokens:,} tokens, ${smart_cost_per_m}/M")
    
    with col2:
        if st.button("📚 Estimation Guide", key="estimation_guide_btn"):
            st.session_state.show_guide = not st.session_state.get('show_guide', False)
    
    with col3:
        if st.button("💰 Cost Ranges", key="cost_ranges_btn"):
            st.session_state.show_ranges = not st.session_state.get('show_ranges', False)
    
    # Estimation Guide
    if st.session_state.get('show_guide', False):
        with st.expander("📚 How to Estimate Costs", expanded=True):
            st.markdown("### Quick Guide to Gen AI Cost Estimation")
            
            st.markdown("#### 1. API Costs")
            st.markdown("**Requests per Day:** Users × Requests per user")
            st.markdown("- Chatbot: 20-50 requests/user/day")
            st.markdown("- Content: 5-15 requests/user/day")
            st.markdown("- Code: 15-40 requests/user/day")
            
            st.markdown("**Tokens:** 1 word ≈ 1.3 tokens, or 4 chars = 1 token")
            st.markdown("- Short: 500-1,500 tokens")
            st.markdown("- Medium: 1,500-3,000 tokens")
            st.markdown("- Long: 3,000-8,000 tokens")
            
            st.markdown("**Provider Pricing (per million tokens):**")
            st.markdown("- GPT-4: $30 | Claude: $15 | GPT-3.5: $2")
            
            st.markdown("#### 2. Infrastructure")
            st.markdown("**By Maturity:**")
            st.markdown("- Exploring: $500-$2K/mo")
            st.markdown("- Pilot: $2K-$8K/mo")
            st.markdown("- Scaling: $8K-$25K/mo")
            st.markdown("- Mature: $25K-$100K/mo")
            
            st.markdown("#### 3. Development")
            st.markdown("**Team by Stage:**")
            st.markdown("- Exploring: 1-2 FTE")
            st.markdown("- Pilot: 2-5 FTE")
            st.markdown("- Scaling: 5-10 FTE")
            st.markdown("- Mature: 10-30 FTE")
            
            st.markdown("**Salaries:** ML Engineer $140K-$180K, Backend $120K-$160K")
    
    # Cost Ranges
    if st.session_state.get('show_ranges', False):
        with st.expander("💰 Industry Benchmarks", expanded=True):
            tabs = st.tabs(["By Industry", "By Maturity", "By Use Case"])
            
            with tabs[0]:
                st.markdown("### Industry Cost Factors")
                industry_df = pd.DataFrame({
                    'Industry': ['Financial', 'Healthcare', 'Tech', 'Retail'],
                    'Security Factor': ['1.4x', '1.5x', '1.1x', '1.2x'],
                    'Requirements': ['SOC2, PCI', 'HIPAA', 'Standard', 'PCI']
                })
                st.dataframe(industry_df, hide_index=True)
            
            with tabs[1]:
                st.markdown("### Costs by Maturity")
                maturity_df = pd.DataFrame({
                    'Stage': ['Exploring', 'Pilot', 'Scaling', 'Mature'],
                    'Infrastructure': ['$500-$2K/mo', '$2K-$8K/mo', '$8K-$25K/mo', '$25K-$100K/mo'],
                    'Development': ['$150K-$400K', '$400K-$800K', '$800K-$2M', '$2M-$5M']
                })
                st.dataframe(maturity_df, hide_index=True)
            
            with tabs[2]:
                st.markdown("### Cost Patterns by Use Case")
                case_df = pd.DataFrame({
                    'Use Case': ['Customer Service', 'Content', 'Code', 'Documents'],
                    'Req/User/Day': ['20-50', '5-15', '15-40', '5-20'],
                    'Tokens': ['1.5K-2.5K', '3K-6K', '2K-4K', '4K-8K']
                })
                st.dataframe(case_df, hide_index=True)
    
    # API Calculator
    with st.expander("🧮 API Cost Calculator"):
        calc_col1, calc_col2 = st.columns(2)
        
        with calc_col1:
            calc_users = st.number_input("Users:", 1, 100000, 100, key="cu")
            calc_req = st.number_input("Req/user/day:", 1, 200, 20, key="cr")
            calc_tokens = st.number_input("Tokens/req:", 100, 20000, 1500, key="ct")
        
        with calc_col2:
            calc_cost = st.number_input("$/M tokens:", 1.0, 100.0, 15.0, key="cc")
            calc_growth = st.number_input("Growth %:", 0, 200, 25, key="cg")
        
        daily_req = calc_users * calc_req
        monthly_cost = (daily_req * 30 * calc_tokens / 1000000) * calc_cost
        year1 = monthly_cost * 12
        year2 = year1 * (1 + calc_growth/100)
        year3 = year2 * (1 + calc_growth/100)
        
        st.markdown("### Results")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Daily Req", f"{daily_req:,}")
        c2.metric("Monthly", f"${monthly_cost:,.0f}")
        c3.metric("Year 1", f"${year1:,.0f}")
        c4.metric("3-Year", f"${(year1+year2+year3):,.0f}")
    
    st.markdown("---")
    

    # 1. Direct AI Costs
    st.subheader("💳 1. Direct AI Model Costs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        model_provider = st.selectbox("Primary Model Provider", 
            ["OpenAI (GPT-4, GPT-3.5)", "Anthropic (Claude)", "AWS Bedrock", "Azure OpenAI", "Google Vertex AI", "Multiple Providers"],
            index=["OpenAI (GPT-4, GPT-3.5)", "Anthropic (Claude)", "AWS Bedrock", "Azure OpenAI", "Google Vertex AI", "Multiple Providers"].index(
                get_demo_value('ai_costs', 'model_provider', 'Anthropic (Claude)')))
        
        avg_tokens_per_request = st.number_input("Avg Tokens per Request (Input + Output)", 
            min_value=100, 
            value=int(get_demo_value('ai_costs', 'avg_tokens_per_request', 2000)), 
            help="Typical range: 500-5000 tokens")
        
        requests_per_day = st.number_input("Estimated Requests per Day", 
            min_value=1, 
            value=int(get_demo_value('ai_costs', 'requests_per_day', 1000)), 
            help="Total across all users")
    
    with col2:
        cost_per_million_tokens = st.number_input("Cost per Million Tokens (USD)", 
            min_value=0.0, 
            value=float(get_demo_value('ai_costs', 'cost_per_million_tokens', 15.0)), 
            step=0.5, 
            help="GPT-4: ~$30, GPT-3.5: ~$2, Claude Sonnet: ~$15")
        
        growth_rate = st.slider("Expected Annual Usage Growth (%)", 
            min_value=0, max_value=200, 
            value=int(get_demo_value('ai_costs', 'growth_rate', 50)), 
            help="How fast will usage grow?")
        
        embedding_cost = st.number_input("Monthly Embedding/Vector DB Cost (USD)", 
            min_value=0, 
            value=int(get_demo_value('ai_costs', 'embedding_cost', 500)), 
            help="Pinecone, Weaviate, etc.")
    
    # Calculate direct costs
    annual_requests = requests_per_day * 365
    total_tokens = annual_requests * avg_tokens_per_request
    year1_api_cost = (total_tokens / 1_000_000) * cost_per_million_tokens
    year2_api_cost = year1_api_cost * (1 + growth_rate/100)
    year3_api_cost = year2_api_cost * (1 + growth_rate/100)
    
    year1_embedding = embedding_cost * 12
    year2_embedding = year1_embedding * (1 + growth_rate/100)
    year3_embedding = year2_embedding * (1 + growth_rate/100)
    
    st.info(f"📊 **Year 1 API Cost Estimate:** ${year1_api_cost:,.2f}")
    
    st.markdown("---")
    
    # 2. Infrastructure Costs
    st.subheader("🖥️ 2. Infrastructure & Cloud Costs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        compute_cost = st.number_input("Monthly Compute Resources (EC2, Lambda, etc.)", 
            min_value=0, value=2000, help="Development, staging, production environments")
        
        storage_cost = st.number_input("Monthly Storage (S3, databases, logs)", 
            min_value=0, value=500)
        
        networking_cost = st.number_input("Monthly Networking (Data transfer, VPC)", 
            min_value=0, value=300)
    
    with col2:
        security_tools = st.number_input("Monthly Security & Compliance Tools", 
            min_value=0, value=1000, help="WAF, GuardDuty, Security Hub, etc.")
        
        monitoring_tools = st.number_input("Monthly Monitoring & Observability", 
            min_value=0, value=800, help="CloudWatch, DataDog, New Relic, etc.")
        
        backup_dr = st.number_input("Monthly Backup & Disaster Recovery", 
            min_value=0, value=400)
    
    monthly_infra = compute_cost + storage_cost + networking_cost + security_tools + monitoring_tools + backup_dr
    year1_infra = monthly_infra * 12
    year2_infra = year1_infra * 1.15  # 15% annual increase
    year3_infra = year2_infra * 1.15
    
    st.markdown("---")
    
    # 3. Development & Engineering Costs
    st.subheader("👥 3. Development & Engineering Team")
    
    col1, col2 = st.columns(2)
    
    with col1:
        ai_engineers = st.number_input("AI/ML Engineers (FTE)", min_value=0.0, value=2.0, step=0.5)
        ai_engineer_cost = st.number_input("Annual Cost per AI Engineer (USD)", 
            min_value=0, value=180000, help="Salary + benefits + overhead")
        
        backend_devs = st.number_input("Backend Developers (FTE)", min_value=0.0, value=2.0, step=0.5)
        backend_cost = st.number_input("Annual Cost per Backend Dev (USD)", 
            min_value=0, value=150000)
    
    with col2:
        frontend_devs = st.number_input("Frontend Developers (FTE)", min_value=0.0, value=1.0, step=0.5)
        frontend_cost = st.number_input("Annual Cost per Frontend Dev (USD)", 
            min_value=0, value=130000)
        
        qa_engineers = st.number_input("QA/Test Engineers (FTE)", min_value=0.0, value=1.0, step=0.5)
        qa_cost = st.number_input("Annual Cost per QA Engineer (USD)", 
            min_value=0, value=120000)
    
    dev_tools = st.number_input("Annual Development Tools & Licenses", 
        min_value=0, value=50000, help="IDEs, testing frameworks, CI/CD, etc.")
    
    year1_dev = (ai_engineers * ai_engineer_cost + backend_devs * backend_cost + 
                 frontend_devs * frontend_cost + qa_engineers * qa_cost + dev_tools)
    year2_dev = year1_dev * 1.05  # 5% annual increase
    year3_dev = year2_dev * 1.05
    
    st.markdown("---")
    
    # 4. Data Management Costs
    st.subheader("📊 4. Data Management & Preparation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        data_engineers = st.number_input("Data Engineers (FTE)", min_value=0.0, value=1.0, step=0.5)
        data_engineer_cost = st.number_input("Annual Cost per Data Engineer", 
            min_value=0, value=160000)
        
        data_prep_cost = st.number_input("Annual Data Preparation/Cleaning", 
            min_value=0, value=50000, help="Tools, services, manual effort")
    
    with col2:
        data_quality_tools = st.number_input("Annual Data Quality & Governance Tools", 
            min_value=0, value=30000, help="Data catalogs, quality monitoring")
        
        data_labeling = st.number_input("Annual Data Labeling/Annotation", 
            min_value=0, value=40000, help="If fine-tuning or custom training needed")
    
    year1_data = (data_engineers * data_engineer_cost + data_prep_cost + 
                  data_quality_tools + data_labeling)
    year2_data = year1_data * 1.1  # 10% increase
    year3_data = year2_data * 1.1
    
    st.markdown("---")
    
    # 5. Operations & Maintenance
    st.subheader("⚙️ 5. Operations & Maintenance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        ops_engineers = st.number_input("DevOps/SRE Engineers (FTE)", min_value=0.0, value=1.0, step=0.5)
        ops_cost = st.number_input("Annual Cost per Ops Engineer", min_value=0, value=170000)
        
        support_staff = st.number_input("Support Staff (FTE)", min_value=0.0, value=1.0, step=0.5)
        support_cost = st.number_input("Annual Cost per Support Staff", min_value=0, value=100000)
    
    with col2:
        incident_mgmt = st.number_input("Annual Incident Management & On-call", 
            min_value=0, value=30000)
        
        model_retraining = st.number_input("Annual Model Retraining/Fine-tuning", 
            min_value=0, value=50000, help="Compute, data, engineering time")
    
    year1_ops = (ops_engineers * ops_cost + support_staff * support_cost + 
                 incident_mgmt + model_retraining)
    year2_ops = year1_ops * 1.08
    year3_ops = year2_ops * 1.08
    
    st.markdown("---")
    
    # 6. Organizational Costs
    st.subheader("🏛️ 6. Organizational & Change Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        training_cost = st.number_input("Annual User Training Programs", 
            min_value=0, value=50000, help="Training materials, sessions, platforms")
        
        change_mgmt = st.number_input("Change Management Investment", 
            min_value=0, value=75000, help="Communication, adoption programs")
    
    with col2:
        governance_cost = st.number_input("Annual Governance & Compliance", 
            min_value=0, value=60000, help="Policies, audits, risk management")
        
        legal_cost = st.number_input("Annual Legal & IP Review", 
            min_value=0, value=40000, help="Contract review, IP protection")
    
    year1_org = training_cost + change_mgmt + governance_cost + legal_cost
    year2_org = year1_org * 0.7  # Typically decreases after first year
    year3_org = year2_org * 0.8
    
    st.markdown("---")
    
    # 7. Risk & Contingency
    st.subheader("⚠️ 7. Risk & Contingency Buffer")
    
    contingency_pct = st.slider("Contingency Reserve (%)", 
        min_value=0, max_value=50, value=15, 
        help="Buffer for unexpected costs, model failures, vendor changes")
    
    vendor_lock_in = st.radio("Vendor Lock-in Mitigation Strategy?", 
        ["No strategy (High Risk)", "Basic (Multi-provider testing)", "Advanced (Abstraction layer)"])
    
    # Calculate total costs
    year1_subtotal = (year1_api_cost + year1_embedding + year1_infra + year1_dev + 
                      year1_data + year1_ops + year1_org)
    year1_contingency = year1_subtotal * (contingency_pct / 100)
    year1_total = year1_subtotal + year1_contingency
    
    year2_subtotal = (year2_api_cost + year2_embedding + year2_infra + year2_dev + 
                      year2_data + year2_ops + year2_org)
    year2_contingency = year2_subtotal * (contingency_pct / 100)
    year2_total = year2_subtotal + year2_contingency
    
    year3_subtotal = (year3_api_cost + year3_embedding + year3_infra + year3_dev + 
                      year3_data + year3_ops + year3_org)
    year3_contingency = year3_subtotal * (contingency_pct / 100)
    year3_total = year3_subtotal + year3_contingency
    
    three_year_tco = year1_total + year2_total + year3_total
    
    # Validate inputs
    try:
        cost_inputs = {
            'org_name': org_name,
            'avg_tokens_per_request': avg_tokens_per_request,
            'requests_per_day': requests_per_day,
            'cost_per_million_tokens': cost_per_million_tokens,
            'growth_rate': growth_rate,
            'contingency_pct': contingency_pct
        }
        # Validation temporarily disabled
        # errors, warnings = validate_cost_inputs(cost_inputs)
        # if errors:
        #     for error in errors:
        #         st.error(f"❌ {error}")
        # if warnings:
        #     for warning in warnings:
        #         st.warning(f"⚠️ {warning}")
    except Exception as e:
        pass  # Validation is optional
    
    # Store in session state
    st.session_state.cost_data = {
        'year1_total': year1_total,
        'year2_total': year2_total,
        'year3_total': year3_total,
        'three_year_tco': three_year_tco,
        'year1_breakdown': {
            'API Costs': year1_api_cost + year1_embedding,
            'Infrastructure': year1_infra,
            'Development': year1_dev,
            'Data Management': year1_data,
            'Operations': year1_ops,
            'Organizational': year1_org,
            'Contingency': year1_contingency
        },
        'org_name': org_name,
        'industry': industry,
        'use_case': use_case
    }
    
    st.success("✅ Cost analysis completed! Switch to the ROI Calculator tab to continue.")


# Tab 3: ROI Calculator Section
with tab3:
    st.header("Return on Investment Analysis")
    
    if 'cost_data' not in st.session_state:
        st.warning("⚠️ Please complete the Cost Analysis tab first.")
    else:
        st.markdown("""
        <div class="info-box">
        <strong>ROI Calculation:</strong> Estimate the business value and benefits from your Gen AI implementation.
        Be realistic and conservative in your estimates.
        </div>
        """, unsafe_allow_html=True)
        
        # Benefits Categories
        st.subheader("💰 Quantifiable Benefits")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Productivity & Efficiency Gains**")
            
            time_saved_per_user = st.number_input("Avg Hours Saved per User per Week", 
                min_value=0.0, value=5.0, step=0.5)
            
            hourly_rate = st.number_input("Avg Hourly Rate (USD)", 
                min_value=0, value=75, help="Blended rate for affected users")
            
            affected_users = st.number_input("Number of Affected Users", 
                min_value=1, value=expected_users if 'expected_users' in locals() else 100)
            
            productivity_pct = st.slider("Productivity Gain Confidence (%)", 
                min_value=0, max_value=100, value=70, 
                help="How confident are you in achieving these gains?")
        
        with col2:
            st.markdown("**Cost Reduction & Avoidance**")
            
            customer_service_reduction = st.number_input("Annual Customer Service Cost Reduction (USD)", 
                min_value=0, value=100000, help="Reduced support staff, faster resolution")
            
            process_automation_value = st.number_input("Annual Process Automation Value (USD)", 
                min_value=0, value=150000, help="Manual processes automated")
            
            error_reduction_value = st.number_input("Annual Error Reduction Value (USD)", 
                min_value=0, value=50000, help="Fewer mistakes, rework")
            
            cost_reduction_confidence = st.slider("Cost Reduction Confidence (%)", 
                min_value=0, max_value=100, value=60)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Revenue Generation**")
            
            new_revenue = st.number_input("Annual New Revenue from AI Features (USD)", 
                min_value=0, value=200000, help="New product features, services")
            
            customer_retention = st.number_input("Annual Value from Improved Retention (USD)", 
                min_value=0, value=100000, help="Reduced churn, better experience")
            
            revenue_confidence = st.slider("Revenue Confidence (%)", 
                min_value=0, max_value=100, value=50, 
                help="New revenue is harder to predict")
        
        with col2:
            st.markdown("**Strategic Benefits**")
            
            competitive_advantage = st.number_input("Annual Competitive Advantage Value (USD)", 
                min_value=0, value=150000, help="Market positioning, faster time-to-market")
            
            innovation_value = st.number_input("Annual Innovation Acceleration Value (USD)", 
                min_value=0, value=100000, help="Faster experimentation, prototyping")
            
            strategic_confidence = st.slider("Strategic Benefits Confidence (%)", 
                min_value=0, max_value=100, value=50)
        
        # Calculate benefits with confidence adjustments
        annual_time_saved = time_saved_per_user * affected_users * 52  # weeks per year
        productivity_value_year1 = annual_time_saved * hourly_rate * (productivity_pct / 100)
        productivity_value_year2 = productivity_value_year1 * 1.2  # Improvement over time
        productivity_value_year3 = productivity_value_year2 * 1.15
        
        cost_reduction_year1 = (customer_service_reduction + process_automation_value + 
                                error_reduction_value) * (cost_reduction_confidence / 100)
        cost_reduction_year2 = cost_reduction_year1 * 1.3  # Scaling benefits
        cost_reduction_year3 = cost_reduction_year2 * 1.2
        
        revenue_year1 = (new_revenue + customer_retention) * (revenue_confidence / 100)
        revenue_year2 = revenue_year1 * 1.5  # Growth trajectory
        revenue_year3 = revenue_year2 * 1.4
        
        strategic_year1 = (competitive_advantage + innovation_value) * (strategic_confidence / 100)
        strategic_year2 = strategic_year1 * 1.2
        strategic_year3 = strategic_year2 * 1.15
        
        year1_benefits = productivity_value_year1 + cost_reduction_year1 + revenue_year1 + strategic_year1
        year2_benefits = productivity_value_year2 + cost_reduction_year2 + revenue_year2 + strategic_year2
        year3_benefits = productivity_value_year3 + cost_reduction_year3 + revenue_year3 + strategic_year3
        
        three_year_benefits = year1_benefits + year2_benefits + year3_benefits
        
        # Calculate ROI
        cost_data = st.session_state.cost_data
        three_year_tco = cost_data['three_year_tco']
        
        net_benefit = three_year_benefits - three_year_tco
        roi_percentage = ((three_year_benefits - three_year_tco) / three_year_tco) * 100 if three_year_tco > 0 else 0
        
        # Calculate payback period
        cumulative_benefit = 0
        cumulative_cost = 0
        payback_months = 0
        monthly_benefits = [year1_benefits/12] * 12 + [year2_benefits/12] * 12 + [year3_benefits/12] * 12
        monthly_costs = [cost_data['year1_total']/12] * 12 + [cost_data['year2_total']/12] * 12 + [cost_data['year3_total']/12] * 12
        
        for month in range(36):
            cumulative_benefit += monthly_benefits[month]
            cumulative_cost += monthly_costs[month]
            if cumulative_benefit >= cumulative_cost:
                payback_months = month + 1
                break
        
        if payback_months == 0:
            payback_months = "36+"
        
        # Store ROI data
        st.session_state.roi_data = {
            'year1_benefits': year1_benefits,
            'year2_benefits': year2_benefits,
            'year3_benefits': year3_benefits,
            'three_year_benefits': three_year_benefits,
            'net_benefit': net_benefit,
            'roi_percentage': roi_percentage,
            'payback_months': payback_months
        }
        
        # Display Results
        st.markdown("---")
        st.subheader("📊 ROI Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("3-Year Total Cost", f"${three_year_tco:,.0f}")
        
        with col2:
            st.metric("3-Year Total Benefits", f"${three_year_benefits:,.0f}")
        
        with col3:
            st.metric("Net Benefit", f"${net_benefit:,.0f}", 
                     delta="Positive" if net_benefit > 0 else "Negative")
        
        with col4:
            st.metric("ROI", f"{roi_percentage:.1f}%",
                     delta="Good" if roi_percentage > 100 else "Review")
        
        st.markdown("---")
        
        # Payback Period
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.metric("Payback Period", f"{payback_months} months")
            
            if isinstance(payback_months, int):
                if payback_months <= 12:
                    st.success("✅ Excellent payback period")
                elif payback_months <= 24:
                    st.info("ℹ️ Good payback period")
                else:
                    st.warning("⚠️ Long payback period - review assumptions")
            else:
                st.error("❌ Payback beyond 3 years - significant risk")
        
        with col2:
            # Year by year comparison
            comparison_data = pd.DataFrame({
                'Year': ['Year 1', 'Year 2', 'Year 3'],
                'Costs': [cost_data['year1_total'], cost_data['year2_total'], cost_data['year3_total']],
                'Benefits': [year1_benefits, year2_benefits, year3_benefits],
                'Net': [year1_benefits - cost_data['year1_total'], 
                       year2_benefits - cost_data['year2_total'],
                       year3_benefits - cost_data['year3_total']]
            })
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Costs', x=comparison_data['Year'], 
                                y=comparison_data['Costs'], marker_color='#ff7f0e'))
            fig.add_trace(go.Bar(name='Benefits', x=comparison_data['Year'], 
                                y=comparison_data['Benefits'], marker_color='#2ca02c'))
            fig.update_layout(title="Annual Costs vs Benefits", barmode='group', height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Sensitivity Analysis
        st.subheader("🎯 Sensitivity Analysis")
        
        st.markdown("""
        <div class="warning-box">
        <strong>Risk Consideration:</strong> ROI projections are sensitive to assumptions. 
        Review how changes in key variables affect outcomes.
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            benefit_scenarios = {
                'Pessimistic (70% of estimate)': 0.7,
                'Base Case (100%)': 1.0,
                'Optimistic (130% of estimate)': 1.3
            }
            
            scenario_results = []
            for scenario, multiplier in benefit_scenarios.items():
                adjusted_benefits = three_year_benefits * multiplier
                adjusted_roi = ((adjusted_benefits - three_year_tco) / three_year_tco) * 100
                scenario_results.append({
                    'Scenario': scenario,
                    'ROI': adjusted_roi,
                    'Net Benefit': adjusted_benefits - three_year_tco
                })
            
            scenario_df = pd.DataFrame(scenario_results)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(x=scenario_df['Scenario'], y=scenario_df['ROI'],
                                marker_color=['#ff7f0e', '#1f77b4', '#2ca02c']))
            fig.update_layout(title="ROI Under Different Scenarios", 
                            yaxis_title="ROI %", height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Key Risk Factors:**")
            
            risk_factors = {
                "Adoption slower than expected": "High",
                "Benefits take longer to realize": "Medium",
                "Costs higher than estimated": "Medium",
                "Model performance degrades": "Medium",
                "Regulatory changes": "Low-Medium",
                "Vendor pricing changes": "Medium"
            }
            
            for risk, severity in risk_factors.items():
                color = "#dc3545" if severity == "High" else "#ffc107" if severity == "Medium" else "#28a745"
                st.markdown(f"<div style='background-color:{color}20; padding:8px; border-radius:4px; margin:5px 0;'>"
                          f"<strong>{risk}</strong>: {severity}</div>", unsafe_allow_html=True)
        
        st.session_state.calculation_done = True
        st.success("✅ ROI analysis completed! Check out the Risk Assessment or Summary Report tabs.")


# Tab 4: Risk Assessment Section
with tab4:
    st.header("Comprehensive Risk Assessment")
    
    st.markdown("""
    <div class="info-box">
    Choose your preferred method:<br>
    <strong>🤖 AI-Powered Assessment:</strong> Automatically analyze risks based on your inputs (recommended)<br>
    <strong>📝 Manual Assessment:</strong> Rate each risk yourself for granular control
    </div>
    """, unsafe_allow_html=True)
    
    # Check if cost data is available
    if 'cost_data' not in st.session_state:
        st.warning("⚠️ Please complete the Cost Analysis tab first to enable risk assessment.")
    else:
        # NOTE: AI-Powered Risk Assessment feature temporarily disabled
        # Requires ai_risk_assessment module which is not yet implemented
        
        # col1, col2 = st.columns(2)
        
        # with col1:
        #     if st.button("🤖 Generate AI-Powered Risk Assessment", type="primary", use_container_width=True):
        #         with st.spinner("🔍 Analyzing your organization data and generating risk assessment..."):
        #             # Import the AI risk assessment module
        #             import sys
        #             sys.path.append('/mnt/user-data/outputs')
        #             from ai_risk_assessment import generate_ai_risk_assessment
        #             
        #             # Get organization profile
        #             org_profile = {
        #                 'org_name': st.session_state.cost_data.get('org_name', 'Organization'),
        #                 'industry': st.session_state.cost_data.get('industry', 'Other'),
        #                 'org_size': st.session_state.get('org_size', '100-500'),
        #                 'maturity': st.session_state.get('maturity', 'Pilot'),
        #                 'use_case': st.session_state.cost_data.get('use_case', 'Other')
        #             }
        #             
        #             # Generate AI risk assessment
        #             ai_risks = generate_ai_risk_assessment(st.session_state.cost_data, org_profile)
        #             st.session_state.ai_risks = ai_risks
        #             st.success("✅ AI risk assessment generated successfully!")
        
        # with col2:
        #     assessment_mode = st.radio(
        #         "Assessment Mode:",
        #         ["🤖 View AI Assessment", "📝 Manual Assessment"],
        #         horizontal=True,
        #         label_visibility="collapsed"
        #     )
        
        # Set to manual assessment mode by default
        assessment_mode = "📝 Manual Assessment"
        
        st.markdown("---")
        
        # Display AI-powered assessment if available
        if assessment_mode == "🤖 View AI Assessment" and 'ai_risks' in st.session_state:
            ai_risks = st.session_state.ai_risks
            
            st.subheader("🤖 AI-Generated Risk Assessment")
            
            # Summary metrics
            summary = ai_risks.get('analysis_summary', {})
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Risks Assessed", summary.get('total_risks_assessed', 0))
            with col2:
                st.metric("High Priority Risks", 
                         summary.get('high_priority_count', 0),
                         delta="Critical" if summary.get('high_priority_count', 0) >= 8 else "Monitor")
            with col3:
                risk_level = summary.get('overall_risk_level', 'Medium')
                color = "🔴" if risk_level == "High" else "🟡" if risk_level == "Medium" else "🟢"
                st.metric("Overall Risk Level", f"{color} {risk_level}")
            
            st.markdown("---")
            
            # Top Priority Risks
            st.subheader("🎯 Top Priority Risks")
            top_risks = summary.get('top_5_risks', [])
            
            for i, risk in enumerate(top_risks, 1):
                severity = "🔴 Critical" if risk['score'] >= 20 else "🟠 High" if risk['score'] >= 16 else "🟡 Elevated"
                st.markdown(f"""
                <div class="warning-box">
                <strong>{i}. {severity}: {risk['name']}</strong><br>
                Risk Score: {risk['score']} (Likelihood: {risk['likelihood']}, Impact: {risk['impact']})
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Detailed Risk Analysis by Category
            st.subheader("📊 Detailed Risk Analysis")
            
            risk_categories = {
                "Technical Risks": ai_risks.get('Technical Risks', {}),
                "Operational Risks": ai_risks.get('Operational Risks', {}),
                "Business Risks": ai_risks.get('Business Risks', {}),
                "Compliance & Legal Risks": ai_risks.get('Compliance & Legal Risks', {}),
                "Security Risks": ai_risks.get('Security Risks', {})
            }
            
            for category, risks in risk_categories.items():
                with st.expander(f"**{category}** ({len(risks)} risks assessed)", expanded=False):
                    for risk_name, risk_data in risks.items():
                        score = risk_data['likelihood'] * risk_data['impact']
                        severity_color = "#dc3545" if score >= 16 else "#ffc107" if score >= 9 else "#28a745"
                        
                        st.markdown(f"""
                        <div style='background-color:{severity_color}20; padding:15px; border-radius:8px; margin:10px 0; border-left: 5px solid {severity_color};'>
                        <strong>{risk_name}</strong><br>
                        <small>Likelihood: {risk_data['likelihood']}/5 | Impact: {risk_data['impact']}/5 | Risk Score: {score}/25</small><br>
                        <em>{risk_data['reasoning']}</em>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Key Recommendations
            st.subheader("💡 AI-Generated Recommendations")
            recommendations = summary.get('key_recommendations', [])
            
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"{i}. {rec}")
            
            # Risk Heat Map
            st.subheader("🔥 Risk Heat Map")
            
            # Prepare data for visualization
            import pandas as pd
            import plotly.express as px
            
            risk_matrix = []
            for category, risks in risk_categories.items():
                for risk_name, risk_data in risks.items():
                    risk_matrix.append({
                        'Risk': risk_name[:40] + '...' if len(risk_name) > 40 else risk_name,
                        'Category': category,
                        'Likelihood': risk_data['likelihood'],
                        'Impact': risk_data['impact'],
                        'Score': risk_data['likelihood'] * risk_data['impact']
                    })
            
            risk_df = pd.DataFrame(risk_matrix)
            
            fig = px.scatter(risk_df, x='Likelihood', y='Impact', size='Score', 
                           color='Category', hover_data=['Risk'],
                           title="Risk Heat Map (AI-Generated)",
                           labels={'Likelihood': 'Likelihood →', 'Impact': 'Impact →'},
                           size_max=30)
            
            fig.update_layout(height=500)
            fig.update_xaxis(range=[0.5, 5.5], dtick=1)
            fig.update_yaxis(range=[0.5, 5.5], dtick=1)
            
            # Add quadrant lines
            fig.add_hline(y=3, line_dash="dash", line_color="gray", opacity=0.5)
            fig.add_vline(x=3, line_dash="dash", line_color="gray", opacity=0.5)
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.session_state.risk_assessment_done = True
            
        elif assessment_mode == "📝 Manual Assessment" or 'ai_risks' not in st.session_state:
            st.subheader("📝 Manual Risk Assessment")
            
            if 'ai_risks' not in st.session_state:
                st.info("💡 **Tip:** Click 'Generate AI-Powered Risk Assessment' above for automated analysis, or proceed with manual assessment below.")
            
            st.markdown("""
            <div class="info-box">
            Rate each risk on two dimensions:<br>
            <strong>Likelihood:</strong> How likely is this risk to occur? (1=Very Low, 5=Very High)<br>
            <strong>Impact:</strong> If it occurs, what would be the impact? (1=Very Low, 5=Very High)
            </div>
            """, unsafe_allow_html=True)
            
            risk_categories = {
        "Technical Risks": [
            ("Model performance degradation over time", "How will you monitor and address model drift?"),
            ("Integration complexity with existing systems", "Assessment of technical debt and compatibility"),
            ("Scalability challenges", "Can the solution handle 10x growth?"),
            ("Data quality and availability issues", "Is your data ready for AI?"),
            ("Latency and performance issues", "Real-time requirements met?")
        ],
        "Operational Risks": [
            ("Skills gap in team", "Do you have AI/ML expertise in-house?"),
            ("Change management resistance", "Is the organization ready for change?"),
            ("Vendor lock-in", "How dependent are you on specific providers?"),
            ("Support and maintenance burden", "24/7 support requirements?"),
            ("Shadow IT and uncontrolled usage", "How will you govern usage?")
        ],
        "Business Risks": [
            ("ROI not realized as expected", "What if benefits are overestimated?"),
            ("Competitive landscape changes", "What if competitors move faster?"),
            ("Budget constraints", "What if funding is cut?"),
            ("Stakeholder misalignment", "Are all stakeholders on board?"),
            ("Project scope creep", "How will you manage expectations?")
        ],
        "Compliance & Legal Risks": [
            ("Regulatory changes (AI Act, privacy laws)", "Are you prepared for new regulations?"),
            ("Data privacy violations", "GDPR, CCPA, HIPAA compliance?"),
            ("Intellectual property concerns", "Who owns AI-generated content?"),
            ("Bias and fairness issues", "How will you ensure ethical AI?"),
            ("Liability for AI decisions", "What's your risk mitigation strategy?")
        ],
        "Security Risks": [
            ("Data breaches and leaks", "Sensitive data protection measures?"),
            ("Prompt injection attacks", "Security testing protocols?"),
            ("Model theft or reverse engineering", "IP protection mechanisms?"),
            ("Supply chain vulnerabilities", "Third-party risk assessment?"),
            ("Insider threats", "Access controls and monitoring?")
        ]
    }
    
            # Manual risk assessment
            st.info("📝 **Manual Assessment:** For detailed manual risk assessment, use the AI assessment as a starting point and export the results. You can then review and adjust scores offline.")
            
            st.markdown("**Quick Manual Override:**")
            st.text_area("Add your own risk notes here:", height=200, placeholder="Enter any specific risks or concerns unique to your organization...")
            
            st.session_state.risk_assessment_done = True

# Tab 5: AI Recommendations
with tab5:
    st.header("🤖 AI-Powered Recommendations")
    st.info("💡 Get AI-powered optimization recommendations based on your inputs.")
    
    if st.button("📊 Show Sample Recommendations", key="show_recs_btn"):
        st.subheader("⚡ Quick Wins")
        st.success("**Optimize API Calls:** Potential savings of $45K/year")
        st.success("**Leverage Open Source:** Potential savings of $28K/year")
        
        st.subheader("💰 Cost Optimization")
        st.info("**Right-size Infrastructure:** Potential savings of $36K/year")

# Tab 6: Comparison Mode
# Tab 6: AI Model Selector (NEW)
with tab6:
    import sys
    sys.path.append('/mnt/user-data/outputs')
    from ai_model_selector import render_model_comparison_tool
    render_model_comparison_tool()

# Tab 7: Comparison Mode (formerly tab6)
with tab7:
    st.header("🔄 Scenario Comparison")
    st.info("💡 Compare multiple scenarios side-by-side.")
    
    st.markdown("**Feature Highlights:**")
    st.markdown("• Save and compare 2-10 scenarios")
    st.markdown("• Compare costs, benefits, and ROI")
    st.markdown("• Identify best option by criteria")
    
    # Sample data
    import pandas as pd
    sample_df = pd.DataFrame({
        'Scenario': ['Conservative', 'Baseline', 'Aggressive'],
        '3-Year TCO': ['$2.1M', '$2.8M', '$3.5M'],
        'ROI %': ['145%', '175%', '220%']
    })
    st.dataframe(sample_df)

# Tab 8: Summary Report (formerly tab7)
with tab8:
    st.header("📋 Executive Summary Report")
    
    if 'cost_data' not in st.session_state:
        st.warning("⚠️ Please complete Cost Analysis first.")
        if st.button("📊 Load Demo Data"):
            st.session_state.cost_data = {
                'org_name': 'TechCorp Solutions',
                'industry': 'Technology',
                'use_case': 'Customer Service',
                'year1_total': 950000,
                'year2_total': 1150000,
                'year3_total': 1380000,
                'three_year_tco': 3480000
            }
            st.session_state.roi_data = {
                'three_year_benefits': 3880000,
                'roi_percentage': 175,
                'payback_months': 18,
                'net_benefit': 400000
            }
            st.rerun()
    else:
        cost_data = st.session_state.cost_data
        st.markdown(f"## {cost_data.get('org_name', 'Organization')}")
        st.markdown(f"**Industry:** {cost_data.get('industry', 'N/A')}")
        
        st.subheader("📊 Key Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("3-Year TCO", f"${cost_data.get('three_year_tco', 0):,.0f}")
        with col2:
            if 'roi_data' in st.session_state:
                st.metric("ROI", f"{st.session_state.roi_data.get('roi_percentage', 0):.0f}%")
        with col3:
            if 'roi_data' in st.session_state:
                st.metric("Payback", f"{st.session_state.roi_data.get('payback_months', 0)} months")
        
        st.markdown("---")
        st.subheader("📥 Export Report")
        
        # PDF Export
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Generate PDF Report", type="primary", use_container_width=True, key="generate_pdf_btn"):
                with st.spinner("Generating comprehensive 20+ page PDF report..."):
                    try:
                        # Import comprehensive PDF generator
                        import sys
                        sys.path.append('/mnt/user-data/outputs')
                        from comprehensive_pdf_generator import generate_comprehensive_pdf_report
                        
                        # Generate comprehensive PDF
                        pdf_bytes = generate_comprehensive_pdf_report(
                            cost_data=cost_data,
                            roi_data=st.session_state.get('roi_data', {}),
                            risk_data=st.session_state.get('risk_data', {})
                        )
                        
                        # Store in session state for download
                        st.session_state.pdf_report = pdf_bytes
                        st.success("✅ Comprehensive 20+ page PDF report generated successfully!")
                    except Exception as e:
                        st.error(f"Error generating PDF: {str(e)}")
                        st.info("💡 Tip: Make sure reportlab is installed: `pip install reportlab`")
        
        # Download button (appears after PDF is generated)
        if 'pdf_report' in st.session_state:
            with col2:
                st.download_button(
                    label="📥 Download PDF Report",
                    data=st.session_state.pdf_report,
                    file_name=f"GenAI_Investment_Analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True,
                    key="download_pdf_btn"
                )
        
        with col3:
            st.markdown("**Comprehensive 20+ Page Report includes:**")
            st.markdown("• Executive summary & TOC")
            st.markdown("• Methodology & assumptions")
            st.markdown("• Detailed cost breakdown with charts")
            st.markdown("• ROI & financial analysis")
            st.markdown("• Risk assessment & mitigation")
            st.markdown("• Implementation roadmap")
            st.markdown("• Technology stack recommendations")
            st.markdown("• Governance framework")
            st.markdown("• Change management strategy")
            st.markdown("• Success metrics & KPIs")
            st.markdown("• Industry benchmarks")
            st.markdown("• Appendices & glossary")


# Professional Footer
st.markdown("---")
st.markdown("""
<div class="footer">
<h3 style='color: #1f77b4; margin-bottom: 15px;'>Gen AI ROI & TCO Calculator</h3>
<p style='margin: 10px 0;'><strong>Enterprise Decision Support Tool</strong></p>
<p style='margin: 10px 0;'>Built with Streamlit | Comprehensive AI Investment Analysis</p>
<p style='font-size: 0.9em; margin-top: 20px; color: #888;'>
⚠️ <em>This calculator provides estimates based on inputs. Actual costs and benefits may vary.<br>
Consult with financial and technical experts for major investment decisions.</em>
</p>
<p style='font-size: 0.85em; margin-top: 15px; color: #aaa;'>Version 1.0 | © 2024</p>
</div>
""", unsafe_allow_html=True)