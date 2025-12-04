import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Gen AI ROI & TCO Calculator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional appearance
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #1f77b4;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border-left: 5px solid #17a2b8;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 10px;
        border-bottom: 3px solid #1f77b4;
    }
    h2 {
        color: #2c5aa0;
        margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'calculation_done' not in st.session_state:
    st.session_state.calculation_done = False

# Header
st.title("🤖 Gen AI ROI & Total Cost of Ownership Calculator")
st.markdown("### *Enterprise-Grade Analysis for Informed AI Investment Decisions*")
st.markdown("---")

# Sidebar for navigation
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/1f77b4/ffffff?text=Gen+AI+ROI", use_container_width=True)
    st.markdown("### Navigation")
    section = st.radio(
        "Select Section:",
        ["📊 Overview", "💰 Cost Analysis", "📈 ROI Calculator", "⚠️ Risk Assessment", "📋 Summary Report"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### About")
    st.info("""
    This calculator helps you understand:
    - **Total Cost of Ownership** (3-year projection)
    - **Hidden & Often-Overlooked Costs**
    - **ROI with Risk Adjustments**
    - **Break-even Analysis**
    - **Comparative Scenarios**
    """)

# Overview Section
if section == "📊 Overview":
    st.header("Understanding the True Cost of Gen AI Implementation")
    
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

# Cost Analysis Section
elif section == "💰 Cost Analysis":
    st.header("Detailed Cost Analysis")
    
    st.markdown("""
    <div class="info-box">
    <strong>Instructions:</strong> Fill in all relevant fields. Use conservative estimates where uncertain. 
    All costs should be in USD and on an annual basis unless specified otherwise.
    </div>
    """, unsafe_allow_html=True)
    
    # Organization Profile
    st.subheader("🏢 Organization Profile")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        org_name = st.text_input("Organization Name", placeholder="Your Company Inc.")
        industry = st.selectbox("Industry", ["Financial Services", "Healthcare", "Technology", "Manufacturing", "Retail", "Government", "Other"])
    
    with col2:
        org_size = st.selectbox("Organization Size", ["<100", "100-500", "500-1000", "1000-5000", "5000+"])
        maturity = st.selectbox("AI Maturity Level", ["Exploring", "Pilot", "Scaling", "Mature"])
    
    with col3:
        use_case = st.selectbox("Primary Use Case", 
            ["Customer Service/Chatbots", "Content Generation", "Code Assistance", "Data Analysis", 
             "Document Processing", "Knowledge Management", "Multiple Use Cases"])
        expected_users = st.number_input("Expected Active Users", min_value=1, value=100)
    
    st.markdown("---")
    
    # 1. Direct AI Costs
    st.subheader("💳 1. Direct AI Model Costs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        model_provider = st.selectbox("Primary Model Provider", 
            ["OpenAI (GPT-4, GPT-3.5)", "Anthropic (Claude)", "AWS Bedrock", "Azure OpenAI", "Google Vertex AI", "Multiple Providers"])
        
        avg_tokens_per_request = st.number_input("Avg Tokens per Request (Input + Output)", 
            min_value=100, value=2000, help="Typical range: 500-5000 tokens")
        
        requests_per_day = st.number_input("Estimated Requests per Day", 
            min_value=1, value=1000, help="Total across all users")
    
    with col2:
        cost_per_million_tokens = st.number_input("Cost per Million Tokens (USD)", 
            min_value=0.0, value=15.0, step=0.5, 
            help="GPT-4: ~$30, GPT-3.5: ~$2, Claude Sonnet: ~$15")
        
        growth_rate = st.slider("Expected Annual Usage Growth (%)", 
            min_value=0, max_value=200, value=50, 
            help="How fast will usage grow?")
        
        embedding_cost = st.number_input("Monthly Embedding/Vector DB Cost (USD)", 
            min_value=0, value=500, help="Pinecone, Weaviate, etc.")
    
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
    
    st.success("✅ Cost analysis completed! Navigate to ROI Calculator to continue.")

# ROI Calculator Section
elif section == "📈 ROI Calculator":
    st.header("Return on Investment Analysis")
    
    if 'cost_data' not in st.session_state:
        st.warning("⚠️ Please complete the Cost Analysis section first.")
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
        st.success("✅ ROI analysis completed! Navigate to Risk Assessment or Summary Report.")

# Risk Assessment Section
elif section == "⚠️ Risk Assessment":
    st.header("Comprehensive Risk Assessment")
    
    st.markdown("""
    <div class="info-box">
    Identify and quantify risks that could impact your Gen AI investment. 
    This assessment helps in risk mitigation planning and contingency budgeting.
    </div>
    """, unsafe_allow_html=True)
    
    # Risk Categories
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
    
    # Risk assessment
    risk_scores = {}
    
    for category, risks in risk_categories.items():
        st.subheader(f"📋 {category}")
        
        for risk, question in risks:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"**{risk}**")
                st.caption(question)
            
            with col2:
                likelihood = st.select_slider(
                    f"Likelihood###{risk}",
                    options=["Very Low", "Low", "Medium", "High", "Very High"],
                    value="Medium",
                    key=f"likelihood_{risk}",
                    label_visibility="collapsed"
                )
            
            with col3:
                impact = st.select_slider(
                    f"Impact###{risk}",
                    options=["Very Low", "Low", "Medium", "High", "Very High"],
                    value="Medium",
                    key=f"impact_{risk}",
                    label_visibility="collapsed"
                )
            
            # Calculate risk score
            likelihood_score = {"Very Low": 1, "Low": 2, "Medium": 3, "High": 4, "Very High": 5}[likelihood]
            impact_score = {"Very Low": 1, "Low": 2, "Medium": 3, "High": 4, "Very High": 5}[impact]
            risk_score = likelihood_score * impact_score
            
            risk_scores[risk] = {
                'category': category,
                'likelihood': likelihood_score,
                'impact': impact_score,
                'score': risk_score
            }
        
        st.markdown("---")
    
    # Risk Heat Map
    st.subheader("🔥 Risk Heat Map")
    
    # Prepare data for heat map
    risk_matrix = []
    for risk, data in risk_scores.items():
        risk_matrix.append({
            'Risk': risk[:40] + '...' if len(risk) > 40 else risk,
            'Category': data['category'],
            'Likelihood': data['likelihood'],
            'Impact': data['impact'],
            'Score': data['score']
        })
    
    risk_df = pd.DataFrame(risk_matrix)
    
    # Create scatter plot for risk visualization
    fig = px.scatter(risk_df, x='Likelihood', y='Impact', size='Score', 
                     color='Category', hover_data=['Risk'],
                     title="Risk Heat Map (Likelihood vs Impact)",
                     labels={'Likelihood': 'Likelihood →', 'Impact': 'Impact →'},
                     size_max=30)
    
    fig.update_layout(height=500)
    fig.update_xaxis(range=[0.5, 5.5], dtick=1)
    fig.update_yaxis(range=[0.5, 5.5], dtick=1)
    
    # Add quadrant lines
    fig.add_hline(y=3, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=3, line_dash="dash", line_color="gray", opacity=0.5)
    
    # Add quadrant labels
    fig.add_annotation(x=1.5, y=4.5, text="High Impact<br>Low Likelihood", 
                      showarrow=False, opacity=0.5)
    fig.add_annotation(x=4.5, y=4.5, text="High Impact<br>High Likelihood<br>(CRITICAL)", 
                      showarrow=False, opacity=0.5, font=dict(color="red"))
    fig.add_annotation(x=1.5, y=1.5, text="Low Impact<br>Low Likelihood", 
                      showarrow=False, opacity=0.5)
    fig.add_annotation(x=4.5, y=1.5, text="Low Impact<br>High Likelihood", 
                      showarrow=False, opacity=0.5)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Top Risks
    st.subheader("🎯 Top Risks Requiring Immediate Attention")
    
    top_risks = risk_df.nlargest(5, 'Score')[['Risk', 'Category', 'Score', 'Likelihood', 'Impact']]
    
    for idx, row in top_risks.iterrows():
        severity = "🔴 Critical" if row['Score'] >= 16 else "🟡 High" if row['Score'] >= 9 else "🟢 Medium"
        st.markdown(f"""
        <div class="warning-box">
        <strong>{severity}: {row['Risk']}</strong><br>
        Category: {row['Category']}<br>
        Risk Score: {row['Score']} (Likelihood: {row['Likelihood']}, Impact: {row['Impact']})
        </div>
        """, unsafe_allow_html=True)
    
    # Mitigation Recommendations
    st.subheader("🛡️ Risk Mitigation Recommendations")
    
    st.markdown("""
    **For High-Priority Risks, Consider:**
    
    1. **Technical Risks:**
       - Implement continuous model monitoring and automated retraining pipelines
       - Establish comprehensive testing frameworks including adversarial testing
       - Design with provider abstraction to avoid vendor lock-in
       - Invest in data quality frameworks from day one
    
    2. **Operational Risks:**
       - Create a formal AI Center of Excellence with clear governance
       - Implement comprehensive training and change management programs
       - Establish usage policies and monitoring to prevent shadow IT
       - Hire or train specialized AI/ML talent
    
    3. **Business Risks:**
       - Set realistic, phased rollout plans with measurable milestones
       - Establish executive sponsorship and regular stakeholder communication
       - Create contingency plans for budget constraints
       - Conduct regular business value assessments
    
    4. **Compliance & Legal:**
       - Engage legal counsel early for AI-specific contract reviews
       - Implement privacy by design and conduct regular audits
       - Establish AI ethics guidelines and review boards
       - Stay updated on emerging AI regulations (EU AI Act, etc.)
    
    5. **Security Risks:**
       - Implement zero-trust architecture for AI systems
       - Conduct regular security assessments and penetration testing
       - Establish data classification and access controls
       - Create incident response plans specific to AI systems
    """)
    
    st.session_state.risk_assessment_done = True

# Summary Report Section
elif section == "📋 Summary Report":
    st.header("Executive Summary Report")
    
    if 'cost_data' not in st.session_state:
        st.warning("⚠️ Please complete the Cost Analysis section first.")
    else:
        cost_data = st.session_state.cost_data
        
        # Header
        st.markdown(f"""
        # Gen AI Investment Analysis
        ## {cost_data.get('org_name', 'Your Organization')}
        **Industry:** {cost_data.get('industry', 'N/A')} | **Use Case:** {cost_data.get('use_case', 'N/A')}  
        **Report Generated:** {datetime.now().strftime('%B %d, %Y')}
        
        ---
        """)
        
        # Executive Summary
        st.subheader("📊 Executive Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("3-Year Total Cost of Ownership", 
                     f"${cost_data['three_year_tco']:,.0f}",
                     help="Comprehensive cost including all direct, indirect, and hidden costs")
        
        with col2:
            if 'roi_data' in st.session_state:
                roi_data = st.session_state.roi_data
                st.metric("3-Year ROI", f"{roi_data['roi_percentage']:.1f}%",
                         delta="Positive" if roi_data['roi_percentage'] > 0 else "Negative")
        
        with col3:
            if 'roi_data' in st.session_state:
                payback = roi_data['payback_months']
                st.metric("Payback Period", f"{payback} months" if isinstance(payback, int) else payback)
        
        st.markdown("---")
        
        # Cost Breakdown
        st.subheader("💰 3-Year Cost Breakdown")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Year-over-year costs
            year_data = pd.DataFrame({
                'Year': ['Year 1', 'Year 2', 'Year 3'],
                'Cost': [cost_data['year1_total'], cost_data['year2_total'], cost_data['year3_total']]
            })
            
            fig = px.bar(year_data, x='Year', y='Cost', 
                        title="Annual Costs",
                        labels={'Cost': 'Cost (USD)'},
                        color_discrete_sequence=['#1f77b4'])
            fig.update_traces(text=year_data['Cost'].apply(lambda x: f'${x:,.0f}'), textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Cost category breakdown (Year 1)
            breakdown = cost_data['year1_breakdown']
            
            fig = go.Figure(data=[go.Pie(
                labels=list(breakdown.keys()),
                values=list(breakdown.values()),
                hole=.4
            )])
            fig.update_layout(title="Year 1 Cost Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed breakdown table
        st.subheader("📑 Detailed Cost Breakdown")
        
        breakdown_df = pd.DataFrame({
            'Category': list(cost_data['year1_breakdown'].keys()),
            'Year 1': [f"${v:,.0f}" for v in cost_data['year1_breakdown'].values()],
            'Percentage': [f"{(v/cost_data['year1_total']*100):.1f}%" 
                          for v in cost_data['year1_breakdown'].values()]
        })
        
        st.dataframe(breakdown_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # ROI Analysis (if completed)
        if 'roi_data' in st.session_state:
            roi_data = st.session_state.roi_data
            
            st.subheader("📈 ROI & Benefits Analysis")
            
            # Benefits vs Costs over 3 years
            timeline_data = pd.DataFrame({
                'Year': ['Year 1', 'Year 2', 'Year 3'],
                'Costs': [cost_data['year1_total'], cost_data['year2_total'], cost_data['year3_total']],
                'Benefits': [roi_data['year1_benefits'], roi_data['year2_benefits'], roi_data['year3_benefits']],
                'Cumulative Net': [
                    roi_data['year1_benefits'] - cost_data['year1_total'],
                    (roi_data['year1_benefits'] + roi_data['year2_benefits']) - 
                    (cost_data['year1_total'] + cost_data['year2_total']),
                    roi_data['net_benefit']
                ]
            })
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Costs', x=timeline_data['Year'], y=timeline_data['Costs'],
                                marker_color='#ff7f0e'))
            fig.add_trace(go.Bar(name='Benefits', x=timeline_data['Year'], y=timeline_data['Benefits'],
                                marker_color='#2ca02c'))
            fig.add_trace(go.Scatter(name='Cumulative Net', x=timeline_data['Year'], 
                                    y=timeline_data['Cumulative Net'], mode='lines+markers',
                                    line=dict(color='#d62728', width=3), marker=dict(size=10)))
            
            fig.update_layout(title="3-Year Financial Projection", barmode='group', height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Benefits", f"${roi_data['three_year_benefits']:,.0f}")
            
            with col2:
                st.metric("Net Benefit", f"${roi_data['net_benefit']:,.0f}",
                         delta="Positive" if roi_data['net_benefit'] > 0 else "Negative")
            
            with col3:
                benefit_cost_ratio = roi_data['three_year_benefits'] / cost_data['three_year_tco']
                st.metric("Benefit-Cost Ratio", f"{benefit_cost_ratio:.2f}:1")
            
            with col4:
                annual_roi = ((benefit_cost_ratio - 1) / 3) * 100
                st.metric("Annualized ROI", f"{annual_roi:.1f}%")
        
        st.markdown("---")
        
        # Key Findings
        st.subheader("🔍 Key Findings & Recommendations")
        
        # Calculate some insights
        total_cost = cost_data['three_year_tco']
        year1_cost = cost_data['year1_total']
        api_pct = (cost_data['year1_breakdown']['API Costs'] / year1_cost) * 100
        dev_pct = (cost_data['year1_breakdown']['Development'] / year1_cost) * 100
        
        findings = []
        
        # Cost structure findings
        if api_pct < 20:
            findings.append(("⚠️ Low API Cost Ratio", 
                           f"API costs are only {api_pct:.1f}% of total costs. The majority of costs are in infrastructure, development, and operations. This is typical for enterprise implementations."))
        
        if dev_pct > 40:
            findings.append(("👥 Development-Heavy Investment", 
                           f"Development costs represent {dev_pct:.1f}% of total investment. Consider strategies to reduce time-to-value and optimize team size."))
        
        if 'roi_data' in st.session_state:
            roi_pct = roi_data['roi_percentage']
            
            if roi_pct > 200:
                findings.append(("✅ Strong ROI Potential", 
                               f"Projected ROI of {roi_pct:.1f}% is excellent. Focus on execution and risk mitigation to realize these benefits."))
            elif roi_pct > 100:
                findings.append(("✅ Positive ROI Expected", 
                               f"Projected ROI of {roi_pct:.1f}% is good. Ensure realistic expectations and phased rollout."))
            elif roi_pct > 0:
                findings.append(("⚠️ Modest ROI", 
                               f"Projected ROI of {roi_pct:.1f}% is modest. Consider optimizing costs or increasing benefit capture."))
            else:
                findings.append(("❌ Negative ROI", 
                               f"Current projections show negative ROI. Significant revisions needed to business case or implementation approach."))
            
            payback = roi_data['payback_months']
            if isinstance(payback, int):
                if payback <= 18:
                    findings.append(("✅ Fast Payback", 
                                   f"Payback period of {payback} months is excellent for enterprise AI investments."))
                elif payback <= 30:
                    findings.append(("ℹ️ Moderate Payback", 
                                   f"Payback period of {payback} months is acceptable but consider acceleration strategies."))
                else:
                    findings.append(("⚠️ Long Payback", 
                                   f"Payback beyond {payback} months increases risk. Consider phased approach or benefit optimization."))
        
        # Display findings
        for title, description in findings:
            st.markdown(f"""
            <div class="info-box">
            <strong>{title}</strong><br>
            {description}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Recommendations
        st.subheader("💡 Strategic Recommendations")
        
        recommendations = """
        **1. Start with Clear Use Case & Metrics**
        - Define specific, measurable success criteria before implementation
        - Establish baseline metrics for comparison
        - Set realistic timelines for benefit realization
        
        **2. Phased Rollout Approach**
        - Begin with pilot projects in contained environments
        - Prove value before scaling to enterprise-wide deployment
        - Iterate based on lessons learned
        
        **3. Invest in Foundational Capabilities**
        - Data quality and governance infrastructure
        - AI literacy and training programs
        - Monitoring and observability platforms
        - Security and compliance frameworks
        
        **4. Cost Optimization Strategies**
        - Implement usage monitoring and cost allocation from day one
        - Consider reserved capacity for predictable workloads
        - Evaluate build vs. buy tradeoffs for components
        - Establish FinOps practices for AI spending
        
        **5. Risk Mitigation**
        - Avoid vendor lock-in through abstraction layers
        - Implement comprehensive testing and validation
        - Establish governance for AI usage and ethics
        - Create contingency plans for model performance issues
        
        **6. Organizational Readiness**
        - Secure executive sponsorship and ongoing commitment
        - Address change management proactively
        - Build or acquire necessary AI/ML talent
        - Establish cross-functional collaboration models
        
        **7. Continuous Monitoring**
        - Track actual costs vs. projections monthly
        - Measure realized benefits against targets
        - Monitor model performance and user adoption
        - Adjust strategy based on data
        """
        
        st.markdown(recommendations)
        
        st.markdown("---")
        
        # Export options
        st.subheader("📥 Export Report")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Prepare JSON export
            export_data = {
                'metadata': {
                    'organization': cost_data.get('org_name', 'N/A'),
                    'industry': cost_data.get('industry', 'N/A'),
                    'use_case': cost_data.get('use_case', 'N/A'),
                    'report_date': datetime.now().isoformat()
                },
                'costs': {
                    'year1': cost_data['year1_total'],
                    'year2': cost_data['year2_total'],
                    'year3': cost_data['year3_total'],
                    'total_3year': cost_data['three_year_tco'],
                    'breakdown': cost_data['year1_breakdown']
                },
                'roi': st.session_state.get('roi_data', {})
            }
            
            json_str = json.dumps(export_data, indent=2)
            st.download_button(
                label="📄 Download JSON",
                data=json_str,
                file_name=f"genai_roi_analysis_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
        
        with col2:
            # Prepare CSV export
            summary_data = {
                'Metric': ['Year 1 Cost', 'Year 2 Cost', 'Year 3 Cost', '3-Year TCO'],
                'Value': [cost_data['year1_total'], cost_data['year2_total'], 
                         cost_data['year3_total'], cost_data['three_year_tco']]
            }
            
            if 'roi_data' in st.session_state:
                summary_data['Metric'].extend(['Year 1 Benefits', 'Year 2 Benefits', 
                                              'Year 3 Benefits', '3-Year Benefits', 
                                              'Net Benefit', 'ROI %', 'Payback Months'])
                summary_data['Value'].extend([roi_data['year1_benefits'], 
                                             roi_data['year2_benefits'],
                                             roi_data['year3_benefits'],
                                             roi_data['three_year_benefits'],
                                             roi_data['net_benefit'],
                                             roi_data['roi_percentage'],
                                             roi_data['payback_months']])
            
            summary_df = pd.DataFrame(summary_data)
            csv = summary_df.to_csv(index=False)
            
            st.download_button(
                label="📊 Download CSV",
                data=csv,
                file_name=f"genai_roi_summary_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col3:
            st.markdown("**Share this analysis** with stakeholders to facilitate informed decision-making.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
<p><strong>Gen AI ROI & TCO Calculator</strong> | Enterprise Decision Support Tool</p>
<p>Built with Streamlit | For enterprise AI investment analysis</p>
<p style='font-size: 0.8em;'>⚠️ This calculator provides estimates based on inputs. Actual costs and benefits may vary. 
Consult with financial and technical experts for major investment decisions.</p>
</div>
""", unsafe_allow_html=True)