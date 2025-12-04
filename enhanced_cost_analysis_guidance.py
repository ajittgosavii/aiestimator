"""
Enhanced Cost Analysis Section with Intelligent Guidance
This makes it MUCH easier for enterprises to estimate costs
"""

# Add this to the Cost Analysis tab (Tab 2) section

# After the organization profile section, add this helper:

st.markdown("---")
st.subheader("💡 Need Help Estimating Costs?")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🎯 Use Smart Defaults", type="primary", help="Auto-fill with industry-standard estimates"):
        # Generate smart defaults based on profile
        st.session_state.use_smart_defaults = True
        st.success("✅ Smart defaults loaded! Review and adjust as needed.")

with col2:
    if st.button("📚 Show Estimation Guide", help="Learn how to estimate each cost"):
        st.session_state.show_guide = True

with col3:
    if st.button("💰 View Cost Ranges", help="See typical cost ranges by industry"):
        st.session_state.show_ranges = True

# Show estimation guide
if st.session_state.get('show_guide', False):
    with st.expander("📚 Cost Estimation Guide - How to Fill This Form", expanded=True):
        st.markdown("""
        ### 🎯 Don't Know Where to Start? Here's How to Estimate Each Cost:
        
        #### 1️⃣ **API Costs (AI Model Usage)**
        **What it is:** The cost charged by OpenAI, Anthropic, AWS, etc. for API calls
        
        **How to estimate:**
        1. **Requests per day:** 
           - Think: How many times will users interact with AI daily?
           - Example: 100 users × 30 questions/day = 3,000 requests
        
        2. **Tokens per request:**
           - Input: Count characters in typical question, divide by 4
           - Output: Estimate response length, divide by 4
           - Example: 500-word question (2,000 chars) + 1,000-word response (4,000 chars) = 1,500 tokens
        
        3. **Cost per million tokens:**
           - Check your provider's website
           - GPT-4: ~$30/M | Claude: ~$15/M | GPT-3.5: ~$2/M
        
        **Typical ranges by use case:**
        - Customer Service Chatbot: 1,000-10,000 requests/day, 1,500-2,500 tokens
        - Content Generation: 100-1,000 requests/day, 3,000-6,000 tokens
        - Code Assistant: 500-5,000 requests/day, 2,000-4,000 tokens
        
        ---
        
        #### 2️⃣ **Infrastructure Costs**
        **What it is:** Hosting, databases, storage, monitoring
        
        **Components to include:**
        - Vector database (Pinecone, Weaviate): $500-$5,000/month
        - Caching layer (Redis): $200-$2,000/month
        - API gateway (Kong, AWS): $100-$1,000/month
        - Monitoring (Datadog, New Relic): $500-$3,000/month
        - Storage (S3, Azure Blob): $100-$1,000/month
        
        **By maturity stage:**
        - Exploring: $500-$2,000/month (minimal setup)
        - Pilot: $2,000-$8,000/month (dev + test environments)
        - Scaling: $8,000-$25,000/month (production infrastructure)
        - Mature: $25,000-$100,000/month (enterprise-grade)
        
        ---
        
        #### 3️⃣ **Development Costs**
        **What it is:** Salaries for people building the solution
        
        **How to estimate:**
        1. List required roles:
           - ML Engineer: $140K-$180K/year
           - Backend Engineer: $120K-$160K/year
           - Frontend Engineer: $110K-$150K/year
           - Solutions Architect: $150K-$200K/year
        
        2. Estimate FTEs needed:
           - Pilot (3-6 months): 1-3 people
           - Scaling (6-12 months): 3-8 people
           - Production (12+ months): 5-15 people
        
        3. Add benefits: Salary × 1.3 (for healthcare, 401k, etc.)
        
        **Example:**
        2 ML Engineers ($150K each) + 1 Backend ($130K) = $430K
        With benefits: $430K × 1.3 = $559K/year
        
        ---
        
        #### 4️⃣ **Operations Costs**
        **What it is:** Ongoing maintenance, monitoring, support
        
        **Includes:**
        - DevOps/SRE team: $100K-$150K per person
        - Support staff: $60K-$90K per person
        - Tools (PagerDuty, etc.): $500-$2,000/month
        - Training and upskilling: $5K-$20K/person/year
        
        **Rule of thumb:** 15-30% of development costs
        
        ---
        
        #### 5️⃣ **Data Management**
        **What it is:** Preparing, cleaning, storing training data
        
        **Typical activities:**
        - Data labeling: $20-$100 per hour (outsourced)
        - Data engineering: $120K-$160K per engineer
        - Storage: $0.02-$0.10 per GB/month
        - ETL tools: $1,000-$10,000/month
        
        **Budget:** 10-20% of total AI project cost
        
        ---
        
        #### 6️⃣ **Organizational Change**
        **What it is:** Training, change management, governance
        
        **Includes:**
        - Training programs: $500-$2,000 per employee
        - Change management consultant: $150-$300/hour
        - Governance frameworks: $50K-$200K setup
        - Communication campaigns: $10K-$50K
        
        **Rule of thumb:** 5-15% of total project cost
        """)

# Show cost ranges by industry
if st.session_state.get('show_ranges', False):
    with st.expander("💰 Typical Cost Ranges by Industry & Maturity", expanded=True):
        st.markdown("### Cost Ranges Help You Validate Your Estimates")
        
        tabs = st.tabs(["By Industry", "By Maturity", "By Organization Size", "By Use Case"])
        
        with tabs[0]:
            st.markdown("#### 📊 Industry-Specific Multipliers")
            st.markdown("""
            Different industries have different cost profiles due to compliance and security needs:
            
            | Industry | Compliance Factor | Security Factor | Notes |
            |----------|------------------|-----------------|-------|
            | **Financial Services** | 1.3x | 1.4x | SOC2, PCI-DSS requirements |
            | **Healthcare** | 1.4x | 1.5x | HIPAA compliance, PHI protection |
            | **Government** | 1.5x | 1.6x | FedRAMP, FISMA requirements |
            | **Technology** | 1.0x | 1.1x | Standard requirements |
            | **Retail** | 1.1x | 1.2x | PCI for payments |
            | **Manufacturing** | 1.1x | 1.2x | IP protection |
            
            **How to use:** Multiply your base estimates by these factors
            """)
        
        with tabs[1]:
            st.markdown("#### 🎯 Costs by Maturity Stage")
            
            maturity_data = {
                'Stage': ['Exploring', 'Pilot', 'Scaling', 'Mature'],
                'Monthly Infrastructure': ['$500-$2K', '$2K-$8K', '$8K-$25K', '$25K-$100K'],
                'Annual Development': ['$150K-$400K', '$400K-$800K', '$800K-$2M', '$2M-$5M'],
                'Monthly Operations': ['$1K-$3K', '$3K-$10K', '$10K-$30K', '$30K-$100K'],
                'Timeline': ['1-3 months', '3-6 months', '6-12 months', '12+ months']
            }
            
            import pandas as pd
            df = pd.DataFrame(maturity_data)
            st.dataframe(df, use_container_width=True)
            
            st.info("""
            💡 **Where are you?**
            - **Exploring:** Just investigating AI, no commitment yet
            - **Pilot:** Testing with small team, proving concept
            - **Scaling:** Rolling out to more users, refining
            - **Mature:** Production-ready, enterprise-wide
            """)
        
        with tabs[2]:
            st.markdown("#### 👥 Costs by Organization Size")
            
            size_data = {
                'Org Size': ['<100', '100-500', '500-1000', '1000-5000', '5000+'],
                'Dev Team Size': ['0.5-2 FTE', '2-5 FTE', '3-8 FTE', '5-15 FTE', '10-30 FTE'],
                'Avg Salary': ['$120K', '$130K', '$140K', '$145K', '$150K'],
                'Annual Dev Cost': ['$60K-$240K', '$260K-$650K', '$420K-$1.1M', '$725K-$2.2M', '$1.5M-$4.5M']
            }
            
            df = pd.DataFrame(size_data)
            st.dataframe(df, use_container_width=True)
            
            st.info("💡 **Tip:** Larger orgs have higher salaries but more resources to share costs")
        
        with tabs[3]:
            st.markdown("#### 🎯 Costs by Use Case")
            
            use_case_data = {
                'Use Case': ['Customer Service', 'Content Gen', 'Code Assistant', 'Data Analysis', 'Document Processing'],
                'Daily Requests/User': ['20-50', '5-15', '15-40', '10-30', '5-20'],
                'Avg Tokens/Request': ['1.5K-2.5K', '3K-6K', '2K-4K', '2.5K-5K', '4K-8K'],
                'Cost Profile': ['High volume, lower tokens', 'Low volume, high tokens', 'Medium volume', 'Medium volume', 'Low volume, very high tokens']
            }
            
            df = pd.DataFrame(use_case_data)
            st.dataframe(df, use_container_width=True)

# Now enhance each input field with contextual help

# Example for API costs section:
st.markdown("---")
st.subheader("💳 1. Direct AI Model Costs")

# Add a help section
with st.expander("❓ How do I estimate API costs?", expanded=False):
    st.markdown("""
    ### Step-by-Step Guide to Estimating API Costs
    
    **Step 1: Estimate Daily Requests**
    - Think about your use case: How often will each user interact with AI?
    - Customer service chatbot: 20-50 requests/user/day
    - Content writer: 5-15 requests/user/day
    - Developer using code assistant: 15-40 requests/user/day
    
    **Formula:** (Number of users) × (Requests per user per day) = Total daily requests
    
    **Step 2: Estimate Tokens per Request**
    - **Quick estimate:** 1 word ≈ 1.3 tokens, or 4 characters ≈ 1 token
    - Count typical input length + expected output length
    - Add 20% buffer for variation
    
    **Example:**
    - Input: "Summarize this 500-word document" (100 words ≈ 130 tokens)
    - Output: A 300-word summary (300 words ≈ 390 tokens)
    - Total: 520 tokens, round up to 600 with buffer
    
    **Step 3: Find Your Provider's Pricing**
    - OpenAI GPT-4: $30 per million tokens (most capable, expensive)
    - Anthropic Claude: $15 per million tokens (balanced)
    - OpenAI GPT-3.5: $2 per million tokens (fast, cheaper)
    - AWS Bedrock Claude: $12 per million tokens (enterprise)
    """)
    
    # Add a calculator
    st.markdown("### 🧮 Quick Calculator")
    calc_users = st.number_input("Number of users:", 1, 10000, 100, key="calc_users")
    calc_req_per_user = st.number_input("Requests per user per day:", 1, 100, 20, key="calc_req")
    calc_tokens = st.number_input("Tokens per request:", 100, 10000, 1500, key="calc_tokens")
    calc_cost_per_m = st.number_input("Cost per million tokens ($):", 1.0, 100.0, 15.0, key="calc_cost")
    
    daily_requests = calc_users * calc_req_per_user
    monthly_requests = daily_requests * 30
    monthly_tokens = monthly_requests * calc_tokens
    monthly_cost = (monthly_tokens / 1_000_000) * calc_cost_per_m
    annual_cost = monthly_cost * 12
    
    st.success(f"""
    **Estimated API Costs:**
    - Daily requests: {daily_requests:,}
    - Monthly cost: ${monthly_cost:,.2f}
    - Annual cost: ${annual_cost:,.2f}
    """)

print("Enhanced Cost Analysis guidance created!")
print("Features:")
print("- Smart Defaults button")
print("- Comprehensive estimation guide")
print("- Cost ranges by industry, maturity, size, use case")
print("- Quick calculator for API costs")
print("- Step-by-step instructions for each cost category")