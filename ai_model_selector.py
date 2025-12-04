"""
AI Model Comparison & Selection Tool
Helps organizations choose the best AI model based on cost, performance, and use case
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# AI Model Database with current pricing (as of Dec 2024)
AI_MODELS = {
    'GPT-4 Turbo': {
        'provider': 'OpenAI',
        'input_cost_per_1m': 10.00,  # $10 per 1M input tokens
        'output_cost_per_1m': 30.00,  # $30 per 1M output tokens
        'context_window': 128000,
        'speed': 'Fast',
        'quality': 'Excellent',
        'use_cases': ['Complex reasoning', 'Code generation', 'Analysis', 'Creative writing'],
        'strengths': ['Strong reasoning', 'Large context', 'Fast', 'Reliable'],
        'weaknesses': ['Higher output cost', 'Rate limits'],
        'best_for': 'Complex tasks requiring strong reasoning'
    },
    'GPT-4o': {
        'provider': 'OpenAI',
        'input_cost_per_1m': 2.50,
        'output_cost_per_1m': 10.00,
        'context_window': 128000,
        'speed': 'Very Fast',
        'quality': 'Excellent',
        'use_cases': ['Real-time chat', 'Customer service', 'Analysis', 'Multimodal'],
        'strengths': ['Fastest GPT-4', 'Multimodal', 'Cost-effective', 'Large context'],
        'weaknesses': ['Slightly less accurate than GPT-4 Turbo on complex tasks'],
        'best_for': 'High-volume applications needing speed and quality'
    },
    'GPT-3.5 Turbo': {
        'provider': 'OpenAI',
        'input_cost_per_1m': 0.50,
        'output_cost_per_1m': 1.50,
        'context_window': 16385,
        'speed': 'Very Fast',
        'quality': 'Good',
        'use_cases': ['Chatbots', 'Simple Q&A', 'Summarization', 'Translation'],
        'strengths': ['Very low cost', 'Fast', 'Good for simple tasks'],
        'weaknesses': ['Limited reasoning', 'Smaller context', 'Less accurate'],
        'best_for': 'High-volume, cost-sensitive applications'
    },
    'Claude 3.5 Sonnet': {
        'provider': 'Anthropic',
        'input_cost_per_1m': 3.00,
        'output_cost_per_1m': 15.00,
        'context_window': 200000,
        'speed': 'Fast',
        'quality': 'Excellent',
        'use_cases': ['Complex analysis', 'Code generation', 'Research', 'Long documents'],
        'strengths': ['Largest context', 'Strong reasoning', 'Excellent at following instructions', 'Safe outputs'],
        'weaknesses': ['Higher cost than some alternatives'],
        'best_for': 'Complex tasks with large context requirements'
    },
    'Claude 3 Opus': {
        'provider': 'Anthropic',
        'input_cost_per_1m': 15.00,
        'output_cost_per_1m': 75.00,
        'context_window': 200000,
        'speed': 'Moderate',
        'quality': 'Best-in-class',
        'use_cases': ['Complex reasoning', 'Research', 'Creative tasks', 'Expert-level work'],
        'strengths': ['Highest quality', 'Exceptional reasoning', 'Huge context', 'Very safe'],
        'weaknesses': ['Most expensive', 'Slower than alternatives'],
        'best_for': 'Mission-critical tasks requiring highest quality'
    },
    'Claude 3 Haiku': {
        'provider': 'Anthropic',
        'input_cost_per_1m': 0.25,
        'output_cost_per_1m': 1.25,
        'context_window': 200000,
        'speed': 'Very Fast',
        'quality': 'Good',
        'use_cases': ['Customer support', 'Simple tasks', 'High-volume processing'],
        'strengths': ['Lowest cost', 'Very fast', 'Large context', 'Good quality for price'],
        'weaknesses': ['Less capable than Sonnet/Opus'],
        'best_for': 'Cost-sensitive, high-volume applications'
    },
    'Gemini 1.5 Pro': {
        'provider': 'Google',
        'input_cost_per_1m': 1.25,
        'output_cost_per_1m': 5.00,
        'context_window': 2000000,
        'speed': 'Fast',
        'quality': 'Excellent',
        'use_cases': ['Multimodal', 'Video analysis', 'Large documents', 'Research'],
        'strengths': ['Largest context (2M)', 'Multimodal', 'Cost-effective', 'Strong performance'],
        'weaknesses': ['Less proven in production', 'Availability'],
        'best_for': 'Applications requiring massive context or multimodal'
    },
    'Gemini 1.5 Flash': {
        'provider': 'Google',
        'input_cost_per_1m': 0.075,
        'output_cost_per_1m': 0.30,
        'context_window': 1000000,
        'speed': 'Very Fast',
        'quality': 'Good',
        'use_cases': ['High-volume tasks', 'Real-time applications', 'Chatbots'],
        'strengths': ['Lowest cost', 'Very fast', 'Large context', 'Multimodal'],
        'weaknesses': ['Lower quality than Pro'],
        'best_for': 'Extreme high-volume, cost-sensitive applications'
    },
    'Llama 3.1 (70B)': {
        'provider': 'Meta (Open Source)',
        'input_cost_per_1m': 0.60,  # Approximate self-hosting cost
        'output_cost_per_1m': 0.60,
        'context_window': 128000,
        'speed': 'Moderate',
        'quality': 'Good',
        'use_cases': ['On-premise', 'Privacy-sensitive', 'Custom fine-tuning'],
        'strengths': ['Open source', 'Full control', 'No API costs', 'Privacy'],
        'weaknesses': ['Requires infrastructure', 'Lower quality', 'Maintenance burden'],
        'best_for': 'Organizations needing data privacy or custom models'
    }
}

def calculate_monthly_cost(model_name, monthly_input_tokens, monthly_output_tokens):
    """Calculate monthly cost for a specific model"""
    model = AI_MODELS[model_name]
    input_cost = (monthly_input_tokens / 1_000_000) * model['input_cost_per_1m']
    output_cost = (monthly_output_tokens / 1_000_000) * model['output_cost_per_1m']
    return input_cost + output_cost

def estimate_tokens_from_usage(requests_per_day, avg_input_words, avg_output_words):
    """Estimate token usage from daily requests and word counts"""
    # Approximate: 1 token ≈ 0.75 words (or 1.33 words per token)
    monthly_requests = requests_per_day * 30
    monthly_input_tokens = monthly_requests * (avg_input_words / 0.75)
    monthly_output_tokens = monthly_requests * (avg_output_words / 0.75)
    return monthly_input_tokens, monthly_output_tokens

def recommend_model_by_use_case(use_case, budget_level='medium'):
    """Recommend models based on use case and budget"""
    recommendations = {
        'Customer Service/Chatbots': {
            'budget': ['Gemini 1.5 Flash', 'Claude 3 Haiku', 'GPT-3.5 Turbo'],
            'balanced': ['GPT-4o', 'Claude 3.5 Sonnet', 'GPT-4 Turbo'],
            'premium': ['Claude 3.5 Sonnet', 'GPT-4 Turbo', 'Claude 3 Opus']
        },
        'Content Generation': {
            'budget': ['GPT-3.5 Turbo', 'Claude 3 Haiku', 'Gemini 1.5 Flash'],
            'balanced': ['GPT-4o', 'Claude 3.5 Sonnet', 'GPT-4 Turbo'],
            'premium': ['Claude 3 Opus', 'GPT-4 Turbo', 'Claude 3.5 Sonnet']
        },
        'Code Generation': {
            'budget': ['GPT-3.5 Turbo', 'Claude 3 Haiku'],
            'balanced': ['GPT-4 Turbo', 'Claude 3.5 Sonnet', 'GPT-4o'],
            'premium': ['Claude 3.5 Sonnet', 'GPT-4 Turbo', 'Claude 3 Opus']
        },
        'Data Analysis': {
            'budget': ['GPT-3.5 Turbo', 'Gemini 1.5 Flash'],
            'balanced': ['GPT-4o', 'Claude 3.5 Sonnet', 'Gemini 1.5 Pro'],
            'premium': ['Claude 3 Opus', 'GPT-4 Turbo', 'Claude 3.5 Sonnet']
        },
        'Document Processing': {
            'budget': ['Claude 3 Haiku', 'Gemini 1.5 Flash'],
            'balanced': ['Claude 3.5 Sonnet', 'Gemini 1.5 Pro', 'GPT-4o'],
            'premium': ['Claude 3 Opus', 'Claude 3.5 Sonnet', 'Gemini 1.5 Pro']
        },
        'Research/Complex Reasoning': {
            'budget': ['Claude 3.5 Sonnet', 'GPT-4o'],
            'balanced': ['Claude 3.5 Sonnet', 'GPT-4 Turbo', 'Claude 3 Opus'],
            'premium': ['Claude 3 Opus', 'Claude 3.5 Sonnet', 'GPT-4 Turbo']
        }
    }
    
    budget_map = {'low': 'budget', 'medium': 'balanced', 'high': 'premium'}
    budget_key = budget_map.get(budget_level, 'balanced')
    
    return recommendations.get(use_case, recommendations['Customer Service/Chatbots'])[budget_key]

def create_cost_comparison_chart(selected_models, monthly_input_tokens, monthly_output_tokens):
    """Create cost comparison bar chart"""
    costs = []
    models = []
    
    for model_name in selected_models:
        cost = calculate_monthly_cost(model_name, monthly_input_tokens, monthly_output_tokens)
        costs.append(cost)
        models.append(model_name)
    
    fig = go.Figure(data=[
        go.Bar(
            x=models,
            y=costs,
            text=[f'${c:,.2f}' for c in costs],
            textposition='outside',
            marker_color='#1f77b4'
        )
    ])
    
    fig.update_layout(
        title='Monthly Cost Comparison',
        xaxis_title='AI Model',
        yaxis_title='Monthly Cost ($)',
        height=400,
        showlegend=False
    )
    
    return fig

def create_cost_breakdown_chart(model_name, monthly_input_tokens, monthly_output_tokens):
    """Create pie chart showing input vs output costs"""
    model = AI_MODELS[model_name]
    input_cost = (monthly_input_tokens / 1_000_000) * model['input_cost_per_1m']
    output_cost = (monthly_output_tokens / 1_000_000) * model['output_cost_per_1m']
    
    fig = go.Figure(data=[go.Pie(
        labels=['Input Tokens', 'Output Tokens'],
        values=[input_cost, output_cost],
        marker_colors=['#1f77b4', '#ff7f0e'],
        hole=0.3
    )])
    
    fig.update_layout(
        title=f'Cost Breakdown: {model_name}',
        height=300
    )
    
    return fig

def render_model_comparison_tool():
    """Render the AI Model Comparison & Selection Tool"""
    
    st.markdown("## 🤖 AI Model Comparison & Selection Tool")
    st.markdown("Compare AI models to find the best fit for your organization based on cost, performance, and use case.")
    
    # Step 1: Define Your Use Case
    st.markdown("---")
    st.markdown("### Step 1: Define Your Use Case")
    
    col1, col2 = st.columns(2)
    
    with col1:
        use_case = st.selectbox(
            "Primary Use Case:",
            [
                'Customer Service/Chatbots',
                'Content Generation',
                'Code Generation',
                'Data Analysis',
                'Document Processing',
                'Research/Complex Reasoning'
            ]
        )
        
        budget_level = st.select_slider(
            "Budget Level:",
            options=['low', 'medium', 'high'],
            value='medium',
            help="Low: Minimize costs | Medium: Balance cost & quality | High: Maximize quality"
        )
    
    with col2:
        requests_per_day = st.number_input(
            "Expected Requests per Day:",
            min_value=10,
            max_value=10000000,
            value=1000,
            step=100,
            help="How many API calls will you make daily?"
        )
        
        avg_input_words = st.number_input(
            "Average Input Length (words):",
            min_value=10,
            max_value=100000,
            value=200,
            step=50,
            help="Average number of words in each prompt"
        )
        
        avg_output_words = st.number_input(
            "Average Output Length (words):",
            min_value=10,
            max_value=100000,
            value=300,
            step=50,
            help="Average number of words in each response"
        )
    
    # Calculate token usage
    monthly_input_tokens, monthly_output_tokens = estimate_tokens_from_usage(
        requests_per_day, avg_input_words, avg_output_words
    )
    
    st.info(f"📊 Estimated Monthly Usage: **{monthly_input_tokens/1_000_000:.2f}M input tokens** | **{monthly_output_tokens/1_000_000:.2f}M output tokens**")
    
    # Step 2: Get Recommendations
    st.markdown("---")
    st.markdown("### Step 2: Recommended Models for Your Use Case")
    
    recommended_models = recommend_model_by_use_case(use_case, budget_level)
    
    st.success(f"🎯 **Top 3 Recommended Models for {use_case}:**")
    
    cols = st.columns(3)
    for idx, model_name in enumerate(recommended_models[:3]):
        model = AI_MODELS[model_name]
        monthly_cost = calculate_monthly_cost(model_name, monthly_input_tokens, monthly_output_tokens)
        
        with cols[idx]:
            st.markdown(f"**#{idx+1}: {model_name}**")
            st.markdown(f"*{model['provider']}*")
            st.metric("Monthly Cost", f"${monthly_cost:,.2f}")
            st.markdown(f"**Quality:** {model['quality']}")
            st.markdown(f"**Speed:** {model['speed']}")
            st.markdown(f"✨ *{model['best_for']}*")
    
    # Step 3: Detailed Comparison
    st.markdown("---")
    st.markdown("### Step 3: Detailed Model Comparison")
    
    st.markdown("Select models to compare:")
    
    # Allow selection of multiple models
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_models = st.multiselect(
            "Choose Models:",
            options=list(AI_MODELS.keys()),
            default=recommended_models[:3] if len(recommended_models) >= 3 else list(AI_MODELS.keys())[:3]
        )
    
    with col2:
        comparison_view = st.radio(
            "View:",
            ["Cost Analysis", "Feature Comparison", "Detailed Specs"]
        )
    
    if selected_models:
        if comparison_view == "Cost Analysis":
            # Cost comparison chart
            st.plotly_chart(
                create_cost_comparison_chart(selected_models, monthly_input_tokens, monthly_output_tokens),
                use_container_width=True
            )
            
            # Cost breakdown table
            st.markdown("#### Monthly Cost Breakdown")
            
            cost_data = []
            for model_name in selected_models:
                model = AI_MODELS[model_name]
                monthly_cost = calculate_monthly_cost(model_name, monthly_input_tokens, monthly_output_tokens)
                input_cost = (monthly_input_tokens / 1_000_000) * model['input_cost_per_1m']
                output_cost = (monthly_output_tokens / 1_000_000) * model['output_cost_per_1m']
                cost_per_request = monthly_cost / (requests_per_day * 30)
                
                cost_data.append({
                    'Model': model_name,
                    'Provider': model['provider'],
                    'Input Cost': f"${input_cost:,.2f}",
                    'Output Cost': f"${output_cost:,.2f}",
                    'Total Monthly': f"${monthly_cost:,.2f}",
                    'Cost/Request': f"${cost_per_request:.4f}"
                })
            
            df_costs = pd.DataFrame(cost_data)
            st.dataframe(df_costs, use_container_width=True)
            
            # Annual projection
            st.markdown("#### Annual Cost Projection")
            annual_costs = []
            for model_name in selected_models:
                monthly_cost = calculate_monthly_cost(model_name, monthly_input_tokens, monthly_output_tokens)
                annual_cost = monthly_cost * 12
                annual_costs.append({
                    'Model': model_name,
                    'Year 1': f"${annual_cost:,.0f}",
                    'Year 2 (+25% usage)': f"${annual_cost * 1.25:,.0f}",
                    'Year 3 (+56% usage)': f"${annual_cost * 1.56:,.0f}",
                    '3-Year Total': f"${annual_cost * 3.81:,.0f}"
                })
            
            df_annual = pd.DataFrame(annual_costs)
            st.dataframe(df_annual, use_container_width=True)
        
        elif comparison_view == "Feature Comparison":
            # Feature comparison table
            st.markdown("#### Model Features & Capabilities")
            
            feature_data = []
            for model_name in selected_models:
                model = AI_MODELS[model_name]
                feature_data.append({
                    'Model': model_name,
                    'Provider': model['provider'],
                    'Quality': model['quality'],
                    'Speed': model['speed'],
                    'Context Window': f"{model['context_window']:,} tokens",
                    'Primary Strengths': ', '.join(model['strengths'][:2])
                })
            
            df_features = pd.DataFrame(feature_data)
            st.dataframe(df_features, use_container_width=True)
            
            # Strengths and weaknesses
            st.markdown("#### Detailed Analysis")
            for model_name in selected_models:
                model = AI_MODELS[model_name]
                with st.expander(f"📊 {model_name} - Detailed Analysis"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**✅ Strengths:**")
                        for strength in model['strengths']:
                            st.markdown(f"• {strength}")
                    
                    with col2:
                        st.markdown("**⚠️ Considerations:**")
                        for weakness in model['weaknesses']:
                            st.markdown(f"• {weakness}")
                    
                    st.markdown(f"**🎯 Best For:** {model['best_for']}")
                    st.markdown(f"**💡 Use Cases:** {', '.join(model['use_cases'])}")
        
        else:  # Detailed Specs
            # Detailed specifications
            st.markdown("#### Technical Specifications")
            
            spec_data = []
            for model_name in selected_models:
                model = AI_MODELS[model_name]
                spec_data.append({
                    'Model': model_name,
                    'Provider': model['provider'],
                    'Input Cost (per 1M)': f"${model['input_cost_per_1m']:.2f}",
                    'Output Cost (per 1M)': f"${model['output_cost_per_1m']:.2f}",
                    'Context Window': f"{model['context_window']:,}",
                    'Quality Rating': model['quality'],
                    'Speed': model['speed']
                })
            
            df_specs = pd.DataFrame(spec_data)
            st.dataframe(df_specs, use_container_width=True)
    
    # Step 4: Optimization Tips
    st.markdown("---")
    st.markdown("### Step 4: Cost Optimization Strategies")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💡 General Optimization Tips")
        st.markdown("""
        **Reduce Token Usage:**
        • Use shorter, more concise prompts
        • Implement response length limits
        • Cache common responses
        • Use prompt engineering to minimize tokens
        
        **Model Selection:**
        • Use cheaper models for simple tasks
        • Reserve premium models for complex queries
        • Implement tiered routing (route by complexity)
        • Consider open-source models for sensitive data
        """)
    
    with col2:
        st.markdown("#### 🎯 Use Case-Specific Tips")
        
        if use_case == 'Customer Service/Chatbots':
            st.markdown("""
            • Use GPT-3.5/Haiku for FAQs (90% of queries)
            • Route complex issues to GPT-4/Sonnet
            • Implement caching for common questions
            • Use fine-tuned models for specific domains
            """)
        elif use_case == 'Content Generation':
            st.markdown("""
            • Batch generate content to reduce API calls
            • Use templates to reduce prompt size
            • Consider GPT-4o for high-volume needs
            • Implement quality thresholds
            """)
        elif use_case == 'Code Generation':
            st.markdown("""
            • Use Claude 3.5 Sonnet for complex code
            • Cache generated code snippets
            • Implement code review layer
            • Use context caching for large codebases
            """)
        else:
            st.markdown("""
            • Analyze usage patterns monthly
            • Implement prompt optimization
            • Use tiered model routing
            • Monitor quality vs cost metrics
            """)
    
    # Step 5: ROI Comparison
    st.markdown("---")
    st.markdown("### Step 5: ROI Analysis")
    
    if selected_models:
        st.markdown("Compare potential ROI across selected models:")
        
        # Assume productivity benefit of $50k/year baseline
        baseline_benefit = 50000
        
        roi_data = []
        for model_name in selected_models:
            model = AI_MODELS[model_name]
            monthly_cost = calculate_monthly_cost(model_name, monthly_input_tokens, monthly_output_tokens)
            annual_cost = monthly_cost * 12
            
            # Quality multiplier affects benefit
            quality_multipliers = {'Best-in-class': 1.3, 'Excellent': 1.15, 'Good': 1.0}
            quality_mult = quality_multipliers.get(model['quality'], 1.0)
            
            annual_benefit = baseline_benefit * quality_mult
            net_benefit = annual_benefit - annual_cost
            roi = ((net_benefit) / annual_cost * 100) if annual_cost > 0 else 0
            
            roi_data.append({
                'Model': model_name,
                'Annual Cost': f"${annual_cost:,.0f}",
                'Estimated Benefit': f"${annual_benefit:,.0f}",
                'Net Benefit': f"${net_benefit:,.0f}",
                'ROI': f"{roi:.0f}%"
            })
        
        df_roi = pd.DataFrame(roi_data)
        st.dataframe(df_roi, use_container_width=True)
        
        st.info("💡 **Note:** Benefit estimates assume baseline productivity improvements. Actual benefits vary by implementation quality and use case.")
    
    # Final Recommendation Summary
    st.markdown("---")
    st.markdown("### 🎯 Final Recommendation")
    
    if selected_models:
        cheapest_model = min(selected_models, 
                            key=lambda m: calculate_monthly_cost(m, monthly_input_tokens, monthly_output_tokens))
        cheapest_cost = calculate_monthly_cost(cheapest_model, monthly_input_tokens, monthly_output_tokens)
        
        # Find highest quality model
        quality_order = {'Best-in-class': 3, 'Excellent': 2, 'Good': 1}
        best_quality_model = max(selected_models,
                                key=lambda m: quality_order.get(AI_MODELS[m]['quality'], 0))
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.success(f"**💰 Most Cost-Effective:**\n\n{cheapest_model}\n\n${cheapest_cost:,.2f}/month")
        
        with col2:
            st.info(f"**🎯 Recommended:**\n\n{recommended_models[0]}\n\n{AI_MODELS[recommended_models[0]]['best_for']}")
        
        with col3:
            st.warning(f"**⭐ Highest Quality:**\n\n{best_quality_model}\n\n{AI_MODELS[best_quality_model]['quality']} rating")
    
    st.markdown("---")
    st.markdown("""
    <div style='background-color: #f0f8ff; padding: 15px; border-radius: 5px; border-left: 4px solid #1f77b4;'>
    <b>💡 Pro Tip:</b> Start with a mid-tier model (GPT-4o or Claude 3.5 Sonnet) and optimize based on actual usage patterns. 
    Many organizations save 40-60% by implementing tiered routing after the first month of data collection.
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    # For testing standalone
    st.set_page_config(page_title="AI Model Comparison", page_icon="🤖", layout="wide")
    render_model_comparison_tool()