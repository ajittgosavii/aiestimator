"""
Industry Benchmarks for Gen AI ROI Calculator
Provides context by comparing user inputs to industry standards
"""

import streamlit as st

# Industry benchmark data based on real-world Gen AI implementations
INDUSTRY_BENCHMARKS = {
    'Financial Services': {
        'cost_structure': {
            'api_pct': (18, 30),  # (min, max) typical range
            'infrastructure_pct': (10, 15),
            'development_pct': (30, 40),
            'data_pct': (12, 18),
            'operations_pct': (12, 18),
            'organizational_pct': (8, 12),
            'contingency_pct': (15, 25)
        },
        'roi_metrics': {
            'typical_roi': (120, 200),  # % range
            'payback_months': (18, 30),
            'year1_negative': True  # Typically negative in Year 1
        },
        'use_case_costs': {
            'chatbot': (800000, 2000000),  # 3-year TCO range
            'document_processing': (1200000, 3000000),
            'fraud_detection': (2000000, 5000000),
            'code_assistant': (600000, 1500000)
        },
        'notes': 'Financial services typically has higher compliance and security costs. Data quality is critical.'
    },
    
    'Healthcare': {
        'cost_structure': {
            'api_pct': (15, 25),
            'infrastructure_pct': (12, 18),
            'development_pct': (28, 38),
            'data_pct': (15, 22),  # Higher due to data sensitivity
            'operations_pct': (12, 18),
            'organizational_pct': (10, 15),  # Higher due to compliance
            'contingency_pct': (18, 28)  # Higher due to regulatory risk
        },
        'roi_metrics': {
            'typical_roi': (100, 180),
            'payback_months': (24, 40),
            'year1_negative': True
        },
        'use_case_costs': {
            'clinical_assistant': (1500000, 4000000),
            'document_processing': (1000000, 2500000),
            'patient_support': (800000, 2000000)
        },
        'notes': 'Healthcare has strict HIPAA compliance requirements. ROI often comes from quality improvements rather than pure cost reduction.'
    },
    
    'Technology': {
        'cost_structure': {
            'api_pct': (20, 35),
            'infrastructure_pct': (8, 12),
            'development_pct': (25, 35),
            'data_pct': (10, 15),
            'operations_pct': (10, 15),
            'organizational_pct': (6, 10),
            'contingency_pct': (12, 20)
        },
        'roi_metrics': {
            'typical_roi': (150, 250),
            'payback_months': (12, 24),
            'year1_negative': False  # Tech companies often break even in Year 1
        },
        'use_case_costs': {
            'code_assistant': (400000, 1000000),
            'chatbot': (500000, 1200000),
            'content_generation': (600000, 1500000)
        },
        'notes': 'Tech companies typically have faster adoption and lower change management costs.'
    },
    
    'Retail': {
        'cost_structure': {
            'api_pct': (22, 35),
            'infrastructure_pct': (10, 15),
            'development_pct': (28, 38),
            'data_pct': (8, 12),
            'operations_pct': (12, 18),
            'organizational_pct': (8, 12),
            'contingency_pct': (15, 25)
        },
        'roi_metrics': {
            'typical_roi': (130, 220),
            'payback_months': (15, 28),
            'year1_negative': True
        },
        'use_case_costs': {
            'customer_service': (600000, 1500000),
            'personalization': (1000000, 2500000),
            'inventory_optimization': (1200000, 3000000)
        },
        'notes': 'Retail focuses on customer experience and operational efficiency.'
    },
    
    'Manufacturing': {
        'cost_structure': {
            'api_pct': (15, 25),
            'infrastructure_pct': (12, 18),
            'development_pct': (30, 42),
            'data_pct': (12, 18),
            'operations_pct': (12, 18),
            'organizational_pct': (8, 12),
            'contingency_pct': (15, 25)
        },
        'roi_metrics': {
            'typical_roi': (110, 190),
            'payback_months': (20, 36),
            'year1_negative': True
        },
        'use_case_costs': {
            'quality_control': (1000000, 2500000),
            'predictive_maintenance': (1200000, 3000000),
            'supply_chain': (1500000, 3500000)
        },
        'notes': 'Manufacturing ROI often comes from defect reduction and operational efficiency.'
    },
    
    'Professional Services': {
        'cost_structure': {
            'api_pct': (25, 40),
            'infrastructure_pct': (8, 12),
            'development_pct': (25, 35),
            'data_pct': (8, 12),
            'operations_pct': (10, 15),
            'organizational_pct': (8, 12),
            'contingency_pct': (12, 20)
        },
        'roi_metrics': {
            'typical_roi': (140, 230),
            'payback_months': (14, 26),
            'year1_negative': False
        },
        'use_case_costs': {
            'document_analysis': (400000, 1000000),
            'research_assistant': (500000, 1200000),
            'proposal_generation': (600000, 1500000)
        },
        'notes': 'Professional services see quick ROI through productivity gains.'
    }
}

# General benchmarks across all industries
GENERAL_BENCHMARKS = {
    'maturity_impact': {
        'Exploring': {
            'typical_roi': (50, 120),
            'payback_months': (30, 48),
            'contingency_pct': (20, 35),
            'notes': 'Early stage projects have higher risk and longer payback'
        },
        'Pilot': {
            'typical_roi': (100, 180),
            'payback_months': (18, 32),
            'contingency_pct': (15, 25),
            'notes': 'Pilot projects balance risk with proven value'
        },
        'Production': {
            'typical_roi': (130, 220),
            'payback_months': (12, 24),
            'contingency_pct': (12, 20),
            'notes': 'Production systems deliver consistent ROI'
        },
        'Mature': {
            'typical_roi': (150, 280),
            'payback_months': (8, 18),
            'contingency_pct': (10, 18),
            'notes': 'Mature implementations maximize efficiency'
        }
    },
    
    'org_size_impact': {
        '<100': {
            'typical_cost_multiplier': 0.6,  # Smaller orgs spend less
            'typical_roi': (80, 150),  # But also see lower absolute ROI
            'notes': 'Small orgs have lower costs but face scaling challenges'
        },
        '100-500': {
            'typical_cost_multiplier': 1.0,
            'typical_roi': (120, 200),
            'notes': 'Mid-size orgs see best cost-to-value ratio'
        },
        '500-1000': {
            'typical_cost_multiplier': 1.3,
            'typical_roi': (110, 190),
            'notes': 'Larger orgs face more change management costs'
        },
        '1000-5000': {
            'typical_cost_multiplier': 1.8,
            'typical_roi': (100, 180),
            'notes': 'Enterprise scale brings complexity and higher costs'
        },
        '5000+': {
            'typical_cost_multiplier': 2.5,
            'typical_roi': (90, 170),
            'notes': 'Very large orgs have significant integration challenges'
        }
    }
}


def get_industry_benchmark(industry, category):
    """Get benchmark for specific industry and category"""
    if industry not in INDUSTRY_BENCHMARKS:
        return None
    return INDUSTRY_BENCHMARKS[industry].get(category)


def compare_to_benchmark(user_value, benchmark_range, metric_name, higher_is_better=True):
    """
    Compare user value to benchmark range
    Returns: (status, message, color)
    status: 'above', 'within', 'below'
    """
    min_val, max_val = benchmark_range
    
    if user_value < min_val:
        if higher_is_better:
            return 'below', f"{metric_name} is below typical range ({min_val}-{max_val})", '🔴'
        else:
            return 'above', f"{metric_name} is better than typical range ({min_val}-{max_val})", '🟢'
    elif user_value > max_val:
        if higher_is_better:
            return 'above', f"{metric_name} is above typical range ({min_val}-{max_val})", '🟢'
        else:
            return 'below', f"{metric_name} is above typical range ({min_val}-{max_val})", '🔴'
    else:
        return 'within', f"{metric_name} is within typical range ({min_val}-{max_val})", '🟡'


def analyze_cost_structure_vs_benchmark(cost_breakdown, total_cost, industry):
    """Analyze how user's cost structure compares to industry benchmarks"""
    benchmarks = get_industry_benchmark(industry, 'cost_structure')
    if not benchmarks:
        return []
    
    analysis = []
    
    categories = {
        'api_pct': ('API Costs', cost_breakdown.get('API Costs', 0)),
        'infrastructure_pct': ('Infrastructure', cost_breakdown.get('Infrastructure', 0)),
        'development_pct': ('Development', cost_breakdown.get('Development', 0)),
        'data_pct': ('Data Management', cost_breakdown.get('Data Management', 0)),
        'operations_pct': ('Operations', cost_breakdown.get('Operations', 0)),
        'organizational_pct': ('Organizational', cost_breakdown.get('Organizational', 0))
    }
    
    for key, (name, amount) in categories.items():
        if total_cost > 0:
            user_pct = (amount / total_cost * 100)
            benchmark_range = benchmarks.get(key)
            
            if benchmark_range:
                status, message, icon = compare_to_benchmark(
                    user_pct, benchmark_range, name, higher_is_better=False
                )
                
                analysis.append({
                    'category': name,
                    'user_value': user_pct,
                    'benchmark_range': benchmark_range,
                    'status': status,
                    'message': message,
                    'icon': icon
                })
    
    return analysis


def analyze_roi_vs_benchmark(roi_data, industry, maturity):
    """Analyze how user's ROI compares to benchmarks"""
    industry_benchmarks = get_industry_benchmark(industry, 'roi_metrics')
    maturity_benchmarks = GENERAL_BENCHMARKS['maturity_impact'].get(maturity, {})
    
    analysis = []
    
    if industry_benchmarks:
        user_roi = roi_data.get('roi_percentage', 0)
        benchmark_range = industry_benchmarks['typical_roi']
        status, message, icon = compare_to_benchmark(
            user_roi, benchmark_range, 'ROI', higher_is_better=True
        )
        analysis.append({
            'metric': 'ROI',
            'user_value': user_roi,
            'benchmark_range': benchmark_range,
            'status': status,
            'message': message,
            'icon': icon,
            'source': 'Industry Average'
        })
        
        user_payback = roi_data.get('payback_months', 0)
        benchmark_range = industry_benchmarks['payback_months']
        status, message, icon = compare_to_benchmark(
            user_payback, benchmark_range, 'Payback Period', higher_is_better=False
        )
        analysis.append({
            'metric': 'Payback Period',
            'user_value': user_payback,
            'benchmark_range': benchmark_range,
            'status': status,
            'message': message,
            'icon': icon,
            'source': 'Industry Average'
        })
    
    if maturity_benchmarks:
        user_roi = roi_data.get('roi_percentage', 0)
        benchmark_range = maturity_benchmarks.get('typical_roi')
        if benchmark_range:
            status, message, icon = compare_to_benchmark(
                user_roi, benchmark_range, 'ROI', higher_is_better=True
            )
            analysis.append({
                'metric': 'ROI',
                'user_value': user_roi,
                'benchmark_range': benchmark_range,
                'status': status,
                'message': message,
                'icon': icon,
                'source': f'{maturity} Maturity Average'
            })
    
    return analysis


def render_benchmark_analysis(cost_data, roi_data, org_profile):
    """Render benchmark comparison in the UI"""
    st.markdown("---")
    st.subheader("📊 Industry Benchmark Comparison")
    
    industry = org_profile.get('industry', '')
    maturity = org_profile.get('maturity', '')
    
    if not industry or industry not in INDUSTRY_BENCHMARKS:
        st.info("💡 Select an industry in Organization Profile to see benchmark comparisons.")
        return
    
    # Cost Structure Comparison
    st.markdown("**Cost Structure vs Industry Benchmarks:**")
    
    cost_analysis = analyze_cost_structure_vs_benchmark(
        cost_data.get('year1_breakdown', {}),
        cost_data.get('year1_total', 0),
        industry
    )
    
    if cost_analysis:
        for item in cost_analysis:
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.markdown(f"**{item['category']}**")
            with col2:
                min_val, max_val = item['benchmark_range']
                st.caption(f"Your: {item['user_value']:.1f}% | Industry: {min_val}-{max_val}%")
            with col3:
                st.markdown(item['icon'])
    
    # ROI Comparison
    st.markdown("---")
    st.markdown("**ROI Metrics vs Benchmarks:**")
    
    roi_analysis = analyze_roi_vs_benchmark(roi_data, industry, maturity)
    
    if roi_analysis:
        for item in roi_analysis:
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.markdown(f"**{item['metric']}** ({item['source']})")
            with col2:
                min_val, max_val = item['benchmark_range']
                if 'ROI' in item['metric']:
                    st.caption(f"Your: {item['user_value']:.0f}% | Benchmark: {min_val}-{max_val}%")
                else:
                    st.caption(f"Your: {item['user_value']:.0f}m | Benchmark: {min_val}-{max_val}m")
            with col3:
                st.markdown(item['icon'])
    
    # Industry notes
    st.markdown("---")
    industry_data = INDUSTRY_BENCHMARKS[industry]
    st.info(f"**{industry} Notes:** {industry_data['notes']}")
    
    if maturity in GENERAL_BENCHMARKS['maturity_impact']:
        maturity_notes = GENERAL_BENCHMARKS['maturity_impact'][maturity]['notes']
        st.info(f"**{maturity} Maturity Notes:** {maturity_notes}")