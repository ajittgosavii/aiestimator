"""
Helper functions and data for Gen AI ROI Calculator
Includes demo data and intelligent risk assessment logic
"""

# Demo Data - Realistic Customer Service Chatbot Implementation
DEMO_DATA = {
    'org_profile': {
        'org_name': 'TechCorp Industries',
        'industry': 'Technology',
        'org_size': '500-1000',
        'maturity': 'Pilot',
        'use_case': 'Customer Service/Chatbots',
        'expected_users': 250
    },
    'direct_ai': {
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
        'networking_cost': 500,
        'security_tools': 1500,
        'monitoring_tools': 1000,
        'backup_dr': 600
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
    'data': {
        'data_engineers': 1.5,
        'data_engineer_cost': 160000,
        'data_prep_cost': 75000,
        'data_quality_tools': 40000,
        'data_labeling': 50000
    },
    'operations': {
        'ops_engineers': 1.5,
        'ops_cost': 170000,
        'support_staff': 1.0,
        'support_cost': 100000,
        'incident_mgmt': 40000,
        'model_retraining': 60000
    },
    'organizational': {
        'training_cost': 80000,
        'change_mgmt': 100000,
        'governance_cost': 75000,
        'legal_cost': 50000
    },
    'contingency_pct': 18,
    'vendor_lock_in': 'Basic (Multi-provider testing)'
}

DEMO_ROI_DATA = {
    'productivity': {
        'time_saved_per_user': 6.0,
        'hourly_rate': 75,
        'affected_users': 200,
        'productivity_pct': 75
    },
    'cost_reduction': {
        'customer_service_reduction': 180000,
        'process_automation_value': 200000,
        'error_reduction_value': 80000,
        'cost_reduction_confidence': 70
    },
    'revenue': {
        'new_revenue': 250000,
        'customer_retention': 150000,
        'revenue_confidence': 55
    },
    'strategic': {
        'competitive_advantage': 200000,
        'innovation_value': 120000,
        'strategic_confidence': 60
    }
}

def calculate_intelligent_risks(cost_data=None, roi_data=None, org_profile=None):
    """
    Intelligently assess risks based on organization profile and financial data
    
    Returns:
        dict: Risk assessments with likelihood, impact, and reasoning
    """
    risks = {}
    
    if not cost_data or not org_profile:
        # Return default medium risks if no data
        return get_default_risks()
    
    # Extract key metrics
    total_cost = cost_data.get('three_year_tco', 0)
    year1_cost = cost_data.get('year1_total', 0)
    breakdown = cost_data.get('year1_breakdown', {})
    
    api_costs = breakdown.get('API Costs', 0)
    dev_costs = breakdown.get('Development', 0)
    data_costs = breakdown.get('Data Management', 0)
    
    api_pct = (api_costs / year1_cost * 100) if year1_cost > 0 else 0
    dev_pct = (dev_costs / year1_cost * 100) if year1_cost > 0 else 0
    data_pct = (data_costs / year1_cost * 100) if year1_cost > 0 else 0
    
    maturity = org_profile.get('maturity', 'Exploring')
    org_size = org_profile.get('org_size', '<100')
    use_case = org_profile.get('use_case', '')
    
    roi_pct = roi_data.get('roi_percentage', 0) if roi_data else 0
    
    # Risk categories with intelligent assessment
    risk_categories = {
        "Technical Risks": [
            assess_model_drift_risk(maturity, use_case),
            assess_integration_risk(dev_pct, maturity),
            assess_scalability_risk(org_size, total_cost),
            assess_data_quality_risk(data_pct, maturity),
            assess_performance_risk(use_case)
        ],
        "Operational Risks": [
            assess_skills_gap_risk(maturity, org_size),
            assess_change_management_risk(org_size, maturity),
            assess_vendor_lockin_risk(api_pct),
            assess_maintenance_risk(maturity),
            assess_shadow_it_risk(maturity, org_size)
        ],
        "Business Risks": [
            assess_roi_risk(roi_pct, maturity),
            assess_competitive_risk(use_case),
            assess_budget_risk(total_cost, org_size),
            assess_stakeholder_risk(maturity),
            assess_scope_creep_risk(maturity)
        ],
        "Compliance & Legal Risks": [
            assess_regulatory_risk(org_size, use_case),
            assess_privacy_risk(use_case),
            assess_ip_risk(use_case),
            assess_bias_risk(use_case),
            assess_liability_risk(use_case, maturity)
        ],
        "Security Risks": [
            assess_breach_risk(org_size, use_case),
            assess_injection_risk(use_case),
            assess_model_theft_risk(api_pct),
            assess_supply_chain_risk(api_pct),
            assess_insider_risk(org_size)
        ]
    }
    
    # Flatten into single dict
    for category, risk_list in risk_categories.items():
        for risk in risk_list:
            risks[risk['name']] = {
                'category': category,
                'likelihood': risk['likelihood'],
                'impact': risk['impact'],
                'score': risk['likelihood'] * risk['impact'],
                'reasoning': risk['reasoning']
            }
    
    return risks

# Individual risk assessment functions
def assess_model_drift_risk(maturity, use_case):
    likelihood = 4 if maturity in ['Exploring', 'Pilot'] else 3
    impact = 4
    reasoning = "Model drift is common in early deployments and requires ongoing monitoring"
    return {'name': 'Model performance degradation over time', 'likelihood': likelihood, 'impact': impact, 'reasoning': reasoning}

def assess_integration_risk(dev_pct, maturity):
    likelihood = 4 if dev_pct > 35 else 3
    impact = 4 if maturity == 'Exploring' else 3
    reasoning = f"High development costs ({dev_pct:.0f}%) indicate complex integration" if dev_pct > 35 else "Moderate integration complexity expected"
    return {'name': 'Integration complexity with existing systems', 'likelihood': likelihood, 'impact': impact, 'reasoning': reasoning}

def assess_scalability_risk(org_size, total_cost):
    likelihood = 4 if '5000+' in org_size or '1000-5000' in org_size else 3
    impact = 4 if total_cost > 2000000 else 3
    reasoning = "Large-scale deployments face scalability challenges"
    return {'name': 'Scalability challenges', 'likelihood': likelihood, 'impact': impact, 'reasoning': reasoning}

def assess_data_quality_risk(data_pct, maturity):
    likelihood = 5 if data_pct < 8 and maturity == 'Exploring' else 4
    impact = 5
    reasoning = "Data quality issues are the #1 cause of AI project failure" if data_pct < 8 else "Data challenges common but manageable"
    return {'name': 'Data quality and availability issues', 'likelihood': likelihood, 'impact': impact, 'reasoning': reasoning}

def assess_performance_risk(use_case):
    likelihood = 4 if 'Chatbot' in use_case or 'Customer Service' in use_case else 3
    impact = 4
    reasoning = "Real-time applications require careful performance optimization"
    return {'name': 'Latency and performance issues', 'likelihood': likelihood, 'impact': impact, 'reasoning': reasoning}

def assess_skills_gap_risk(maturity, org_size):
    likelihood = 5 if maturity == 'Exploring' else 3 if maturity == 'Pilot' else 2
    impact = 4
    reasoning = "AI/ML expertise is scarce; critical for early-stage projects"
    return {'name': 'Skills gap in team', 'likelihood': likelihood, 'impact': impact, 'reasoning': reasoning}

def assess_change_management_risk(org_size, maturity):
    likelihood = 4 if '1000+' in org_size or '5000+' in org_size else 3
    impact = 4
    reasoning = "Large organizations face significant change resistance"
    return {'name': 'Change management resistance', 'likelihood': likelihood, 'impact': impact, 'reasoning': reasoning}

def assess_vendor_lockin_risk(api_pct):
    likelihood = 5 if api_pct > 40 else 4 if api_pct > 25 else 2
    impact = 4
    reasoning = f"High API dependency ({api_pct:.0f}% of costs) creates significant vendor lock-in" if api_pct > 25 else "Diversified costs reduce vendor lock-in risk"
    return {'name': 'Vendor lock-in', 'likelihood': likelihood, 'impact': impact, 'reasoning': reasoning}

def assess_maintenance_risk(maturity):
    likelihood = 4
    impact = 3
    reasoning = "AI systems require continuous monitoring, retraining, and updates"
    return {'name': 'Support and maintenance burden', 'likelihood': likelihood, 'impact': impact, 'reasoning': reasoning}

def assess_shadow_it_risk(maturity, org_size):
    likelihood = 4 if maturity == 'Exploring' else 2
    impact = 3
    reasoning = "Uncontrolled AI usage common without established governance"
    return {'name': 'Shadow IT and uncontrolled usage', 'likelihood': likelihood, 'impact': impact, 'reasoning': reasoning}

def assess_roi_risk(roi_pct, maturity):
    likelihood = 5 if roi_pct > 300 else 4 if roi_pct > 200 else 3
    impact = 5
    reasoning = f"Very high ROI projection ({roi_pct:.0f}%) indicates over-optimism" if roi_pct > 200 else "ROI realization depends on execution and adoption"
    return {'name': 'ROI not realized as expected', 'likelihood': likelihood, 'impact': impact, 'reasoning': reasoning}

def assess_competitive_risk(use_case):
    likelihood = 4
    impact = 3
    reasoning = "AI landscape evolves rapidly; competitors may leapfrog"
    return {'name': 'Competitive landscape changes', 'likelihood': likelihood, 'impact': impact, 'reasoning': reasoning}

def assess_budget_risk(total_cost, org_size):
    likelihood = 4 if total_cost > 3000000 else 3 if total_cost > 1000000 else 2
    impact = 4
    reasoning = "Large investments face budget scrutiny and potential cuts"
    return {'name': 'Budget constraints', 'likelihood': likelihood, 'impact': impact, 'reasoning': reasoning}

def assess_stakeholder_risk(maturity):
    likelihood = 4 if maturity == 'Exploring' else 2
    impact = 4
    reasoning = "Early projects need strong executive sponsorship and alignment"
    return {'name': 'Stakeholder misalignment', 'likelihood': likelihood, 'impact': impact, 'reasoning': reasoning}

def assess_scope_creep_risk(maturity):
    likelihood = 4
    impact = 3
    reasoning = "AI projects often expand as teams discover new possibilities"
    return {'name': 'Project scope creep', 'likelihood': likelihood, 'impact': impact, 'reasoning': reasoning}

def assess_regulatory_risk(org_size, use_case):
    likelihood = 5 if 'Healthcare' in use_case or 'Financial' in use_case else 4
    impact = 4
    reasoning = "AI regulations (EU AI Act, etc.) evolving rapidly worldwide"
    return {'name': 'Regulatory changes (AI Act, privacy laws)', 'likelihood': likelihood, 'impact': impact, 'reasoning': reasoning}

def assess_privacy_risk(use_case):
    likelihood = 4 if 'Customer' in use_case or 'Service' in use_case else 3
    impact = 5
    reasoning = "Customer-facing applications process sensitive personal data"
    return {'name': 'Data privacy violations', 'likelihood': likelihood, 'impact': impact, 'reasoning': reasoning}

def assess_ip_risk(use_case):
    likelihood = 3
    impact = 4
    reasoning = "AI-generated content ownership and IP rights still evolving"
    return {'name': 'Intellectual property concerns', 'likelihood': likelihood, 'impact': impact, 'reasoning': reasoning}

def assess_bias_risk(use_case):
    likelihood = 4
    impact = 4
    reasoning = "AI bias is a known issue requiring active monitoring and mitigation"
    return {'name': 'Bias and fairness issues', 'likelihood': likelihood, 'impact': impact, 'reasoning': reasoning}

def assess_liability_risk(use_case, maturity):
    likelihood = 3
    impact = 4
    reasoning = "Legal framework for AI liability and accountability still developing"
    return {'name': 'Liability for AI decisions', 'likelihood': likelihood, 'impact': impact, 'reasoning': reasoning}

def assess_breach_risk(org_size, use_case):
    likelihood = 3
    impact = 5
    reasoning = "AI systems processing sensitive data are high-value targets"
    return {'name': 'Data breaches and leaks', 'likelihood': likelihood, 'impact': impact, 'reasoning': reasoning}

def assess_injection_risk(use_case):
    likelihood = 4 if 'Chatbot' in use_case or 'Customer Service' in use_case else 3
    impact = 3
    reasoning = "Prompt injection is an emerging threat for LLM applications"
    return {'name': 'Prompt injection attacks', 'likelihood': likelihood, 'impact': impact, 'reasoning': reasoning}

def assess_model_theft_risk(api_pct):
    likelihood = 2 if api_pct > 20 else 3
    impact = 3
    reasoning = "Using third-party APIs reduces model theft risk"
    return {'name': 'Model theft or reverse engineering', 'likelihood': likelihood, 'impact': impact, 'reasoning': reasoning}

def assess_supply_chain_risk(api_pct):
    likelihood = 3 if api_pct > 20 else 2
    impact = 3
    reasoning = "Dependencies on third-party AI services create supply chain risks"
    return {'name': 'Supply chain vulnerabilities', 'likelihood': likelihood, 'impact': impact, 'reasoning': reasoning}

def assess_insider_risk(org_size):
    likelihood = 2
    impact = 4
    reasoning = "Standard insider threat concern for any sensitive system"
    return {'name': 'Insider threats', 'likelihood': likelihood, 'impact': impact, 'reasoning': reasoning}

def get_default_risks():
    """Return default medium-risk assessments"""
    default_risks = [
        'Model performance degradation over time',
        'Integration complexity with existing systems',
        'Scalability challenges',
        'Data quality and availability issues',
        'Latency and performance issues',
        'Skills gap in team',
        'Change management resistance',
        'Vendor lock-in',
        'Support and maintenance burden',
        'Shadow IT and uncontrolled usage',
        'ROI not realized as expected',
        'Competitive landscape changes',
        'Budget constraints',
        'Stakeholder misalignment',
        'Project scope creep',
        'Regulatory changes (AI Act, privacy laws)',
        'Data privacy violations',
        'Intellectual property concerns',
        'Bias and fairness issues',
        'Liability for AI decisions',
        'Data breaches and leaks',
        'Prompt injection attacks',
        'Model theft or reverse engineering',
        'Supply chain vulnerabilities',
        'Insider threats'
    ]
    
    risks = {}
    categories = {
        0: "Technical Risks", 1: "Technical Risks", 2: "Technical Risks", 3: "Technical Risks", 4: "Technical Risks",
        5: "Operational Risks", 6: "Operational Risks", 7: "Operational Risks", 8: "Operational Risks", 9: "Operational Risks",
        10: "Business Risks", 11: "Business Risks", 12: "Business Risks", 13: "Business Risks", 14: "Business Risks",
        15: "Compliance & Legal Risks", 16: "Compliance & Legal Risks", 17: "Compliance & Legal Risks", 
        18: "Compliance & Legal Risks", 19: "Compliance & Legal Risks",
        20: "Security Risks", 21: "Security Risks", 22: "Security Risks", 23: "Security Risks", 24: "Security Risks"
    }
    
    for idx, risk in enumerate(default_risks):
        risks[risk] = {
            'category': categories.get(idx, "Other"),
            'likelihood': 3,
            'impact': 3,
            'score': 9,
            'reasoning': 'Complete Cost Analysis for intelligent risk assessment'
        }
    
    return risks