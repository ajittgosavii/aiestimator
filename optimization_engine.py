"""
AI-Powered ROI Optimization Recommendations
Analyzes user's inputs and provides intelligent suggestions to improve ROI
"""

def generate_optimization_recommendations(cost_data, roi_data, org_profile, risks):
    """
    Generate intelligent recommendations to optimize costs and increase ROI
    
    Args:
        cost_data: Cost breakdown and projections
        roi_data: ROI calculations and benefits
        org_profile: Organization information
        risks: Risk assessment results
    
    Returns:
        dict: Categorized recommendations with priority and impact estimates
    """
    recommendations = {
        'cost_optimization': [],
        'revenue_enhancement': [],
        'risk_mitigation': [],
        'quick_wins': [],
        'strategic_initiatives': []
    }
    
    if not cost_data:
        return recommendations
    
    # Extract key metrics
    year1_cost = cost_data.get('year1_total', 0)
    breakdown = cost_data.get('year1_breakdown', {})
    three_year_tco = cost_data.get('three_year_tco', 0)
    
    api_costs = breakdown.get('API Costs', 0)
    infra_costs = breakdown.get('Infrastructure', 0)
    dev_costs = breakdown.get('Development', 0)
    data_costs = breakdown.get('Data Management', 0)
    ops_costs = breakdown.get('Operations', 0)
    
    api_pct = (api_costs / year1_cost * 100) if year1_cost > 0 else 0
    dev_pct = (dev_costs / year1_cost * 100) if year1_cost > 0 else 0
    data_pct = (data_costs / year1_cost * 100) if year1_cost > 0 else 0
    
    maturity = org_profile.get('maturity', 'Exploring')
    roi_pct = roi_data.get('roi_percentage', 0) if roi_data else 0
    
    # COST OPTIMIZATION RECOMMENDATIONS
    
    # API Cost Optimization
    if api_pct > 30:
        recommendations['cost_optimization'].append({
            'title': '🔴 Optimize API Costs (High Priority)',
            'priority': 'High',
            'estimated_savings': f'${api_costs * 0.3:,.0f}/year',
            'effort': 'Medium',
            'timeframe': '3-6 months',
            'description': f'Your API costs represent {api_pct:.0f}% of total budget ({api_costs:,.0f} annually).',
            'recommendations': [
                'Implement aggressive prompt caching (30-40% cost reduction)',
                'Use cheaper models for simple queries (GPT-3.5/Claude Haiku)',
                'Add request throttling and rate limiting',
                'Implement smart routing based on query complexity',
                'Consider reserved capacity pricing (20-30% discount)',
                'Audit and eliminate redundant API calls'
            ],
            'example': 'One customer reduced API costs by 45% by routing 60% of queries to cheaper models.'
        })
    elif api_pct > 15:
        recommendations['cost_optimization'].append({
            'title': '🟡 Moderate API Cost Optimization',
            'priority': 'Medium',
            'estimated_savings': f'${api_costs * 0.2:,.0f}/year',
            'effort': 'Low',
            'timeframe': '1-3 months',
            'description': f'API costs are {api_pct:.0f}% of budget - room for optimization.',
            'recommendations': [
                'Enable response caching for common queries',
                'Optimize prompt templates to reduce token usage',
                'Consider model fine-tuning to reduce prompt length',
                'Implement request batching where possible'
            ]
        })
    
    # Development Cost Optimization
    if dev_pct > 40:
        recommendations['cost_optimization'].append({
            'title': '🔴 Optimize Development Costs',
            'priority': 'High',
            'estimated_savings': f'${dev_costs * 0.25:,.0f}/year',
            'effort': 'High',
            'timeframe': '6-12 months',
            'description': f'Development costs are {dev_pct:.0f}% of budget - higher than typical 25-35%.',
            'recommendations': [
                'Leverage pre-built AI frameworks (LangChain, Semantic Kernel)',
                'Use no-code/low-code tools for rapid prototyping',
                'Consider offshore or nearshore development for non-core features',
                'Implement reusable component library',
                'Use AI coding assistants to boost productivity',
                'Transition to managed services to reduce maintenance'
            ]
        })
    
    # Infrastructure Optimization
    if infra_costs > 50000:
        recommendations['cost_optimization'].append({
            'title': '🟡 Optimize Infrastructure Spending',
            'priority': 'Medium',
            'estimated_savings': f'${infra_costs * 0.2:,.0f}/year',
            'effort': 'Medium',
            'timeframe': '2-4 months',
            'description': 'Significant infrastructure costs present optimization opportunities.',
            'recommendations': [
                'Use spot instances for dev/test environments (70% savings)',
                'Implement auto-scaling to match actual usage',
                'Right-size compute resources based on metrics',
                'Archive cold data to cheaper storage tiers',
                'Use CDN for static content delivery',
                'Consider reserved instances for predictable workloads (40% savings)'
            ]
        })
    
    # Data Management Optimization
    if data_pct < 8:
        recommendations['cost_optimization'].append({
            'title': '⚠️ Increase Data Quality Investment',
            'priority': 'Critical',
            'estimated_savings': 'N/A - Risk Mitigation',
            'effort': 'High',
            'timeframe': '3-6 months',
            'description': f'Data costs only {data_pct:.0f}% of budget. Insufficient investment in data quality is the #1 cause of AI project failure.',
            'recommendations': [
                'Increase data engineering resources immediately',
                'Implement comprehensive data quality framework',
                'Establish data validation and cleansing pipelines',
                'Invest in data labeling and annotation',
                'Create data governance policies',
                'Build continuous data quality monitoring'
            ],
            'warning': 'Underfunding data management typically leads to poor model performance and project failure.'
        })
    
    # REVENUE ENHANCEMENT RECOMMENDATIONS
    
    if roi_data:
        year1_benefits = roi_data.get('year1_benefits', 0)
        year3_benefits = roi_data.get('year3_benefits', 0)
        
        recommendations['revenue_enhancement'].append({
            'title': '📈 Accelerate Benefit Realization',
            'priority': 'High',
            'estimated_impact': f'${year1_benefits * 0.3:,.0f} additional Year 1 benefits',
            'effort': 'Medium',
            'timeframe': '3-6 months',
            'description': 'Strategies to realize benefits faster and increase adoption.',
            'recommendations': [
                'Launch aggressive change management program',
                'Identify and empower internal champions',
                'Create detailed user training program',
                'Implement gamification for adoption',
                'Showcase quick wins to build momentum',
                'Establish success metrics dashboard',
                'Conduct weekly adoption reviews'
            ]
        })
        
        recommendations['revenue_enhancement'].append({
            'title': '💰 Expand Use Cases',
            'priority': 'Medium',
            'estimated_impact': f'${year3_benefits * 0.5:,.0f} over 3 years',
            'effort': 'Medium',
            'timeframe': '6-12 months',
            'description': 'Identify adjacent use cases to maximize AI investment.',
            'recommendations': [
                'Survey users for additional pain points',
                'Analyze usage patterns for expansion opportunities',
                'Pilot 2-3 related use cases with existing infrastructure',
                'Create internal AI capabilities center',
                'Share learnings across organization',
                'Build platform approach for reusability'
            ]
        })
    
    # RISK MITIGATION FOR ROI PROTECTION
    
    if risks:
        critical_risks = [r for r, info in risks.items() if info.get('score', 0) >= 16]
        
        if critical_risks:
            recommendations['risk_mitigation'].append({
                'title': f'🔴 Mitigate {len(critical_risks)} Critical Risks',
                'priority': 'Critical',
                'estimated_impact': 'Protect projected ROI',
                'effort': 'High',
                'timeframe': '1-3 months',
                'description': f'You have {len(critical_risks)} critical risks that could derail ROI realization.',
                'critical_risks': critical_risks[:5],  # Top 5
                'recommendations': [
                    'Create dedicated risk mitigation task force',
                    'Assign owner for each critical risk',
                    'Establish weekly risk review cadence',
                    'Allocate contingency budget for mitigation',
                    'Implement early warning indicators'
                ]
            })
    
    # Vendor Lock-in Mitigation
    if api_pct > 35:
        recommendations['risk_mitigation'].append({
            'title': '🔒 Mitigate Vendor Lock-in Risk',
            'priority': 'High',
            'estimated_impact': 'Strategic flexibility',
            'effort': 'High',
            'timeframe': '4-6 months',
            'description': 'High API dependency creates vendor lock-in risk.',
            'recommendations': [
                'Implement abstraction layer for API calls',
                'Design for multi-provider capability',
                'Test with 2-3 different AI providers',
                'Maintain provider-agnostic data formats',
                'Build fallback mechanisms',
                'Negotiate favorable contract terms'
            ]
        })
    
    # Skills Gap Mitigation
    if maturity == 'Exploring':
        recommendations['risk_mitigation'].append({
            'title': '🎓 Address Skills Gap',
            'priority': 'High',
            'estimated_impact': 'Project success',
            'effort': 'Medium',
            'timeframe': '3-6 months',
            'description': 'Early-stage AI initiatives require specialized expertise.',
            'recommendations': [
                'Hire 1-2 experienced AI/ML engineers immediately',
                'Partner with AI consultancy for first 6 months',
                'Invest in comprehensive team training',
                'Send key staff to AI conferences/workshops',
                'Create internal AI learning program',
                'Join AI industry groups for knowledge sharing'
            ]
        })
    
    # QUICK WINS (High Impact, Low Effort)
    
    recommendations['quick_wins'].append({
        'title': '⚡ Implement Prompt Caching',
        'priority': 'High',
        'estimated_savings': f'${api_costs * 0.3:,.0f}/year',
        'effort': 'Low',
        'timeframe': '1-2 weeks',
        'description': 'Cache common queries to reduce API calls by 30-40%.',
        'implementation': [
            'Use Redis or similar caching layer',
            'Identify top 20% most common queries',
            'Implement 24-hour cache expiry',
            'Monitor cache hit rates'
        ],
        'roi': 'Payback in < 1 month'
    })
    
    recommendations['quick_wins'].append({
        'title': '⚡ Smart Model Routing',
        'priority': 'High',
        'estimated_savings': f'${api_costs * 0.25:,.0f}/year',
        'effort': 'Low',
        'timeframe': '2-4 weeks',
        'description': 'Route simple queries to cheaper models, complex ones to premium models.',
        'implementation': [
            'Classify queries by complexity',
            'Use GPT-3.5 or Claude Haiku for simple queries',
            'Reserve GPT-4/Claude Opus for complex queries',
            'Monitor quality metrics'
        ],
        'roi': 'Payback in < 2 months'
    })
    
    recommendations['quick_wins'].append({
        'title': '⚡ Usage Monitoring Dashboard',
        'priority': 'Medium',
        'estimated_savings': f'${year1_cost * 0.1:,.0f}/year',
        'effort': 'Low',
        'timeframe': '1 week',
        'description': 'Visibility into usage patterns enables optimization.',
        'implementation': [
            'Track API calls, costs, latency by user/feature',
            'Set up alerts for unusual usage',
            'Create daily cost reports',
            'Identify optimization opportunities'
        ],
        'roi': 'Enables all other optimizations'
    })
    
    # STRATEGIC INITIATIVES (Long-term Value)
    
    recommendations['strategic_initiatives'].append({
        'title': '🚀 Build AI Center of Excellence',
        'priority': 'Medium',
        'estimated_impact': '2-3x current ROI over 3 years',
        'effort': 'High',
        'timeframe': '12-18 months',
        'description': 'Establish centralized AI capability to scale across organization.',
        'components': [
            'Dedicated AI team (5-10 people)',
            'Reusable AI platform and components',
            'Governance framework and best practices',
            'Training and enablement programs',
            'Vendor management and optimization',
            'Innovation lab for experimentation'
        ],
        'benefits': [
            'Faster time-to-market for new AI use cases',
            'Shared infrastructure reduces costs',
            'Consistent quality and governance',
            'Knowledge sharing and collaboration',
            'Strategic vendor relationships'
        ]
    })
    
    recommendations['strategic_initiatives'].append({
        'title': '🚀 Model Fine-tuning Strategy',
        'priority': 'Medium',
        'estimated_savings': f'${api_costs * 0.5:,.0f}/year',
        'effort': 'High',
        'timeframe': '6-9 months',
        'description': 'Fine-tune models for your specific use case to reduce costs and improve quality.',
        'considerations': [
            'Requires significant labeled training data',
            'Upfront investment: $50K-$200K',
            'Ongoing retraining needed',
            'Can reduce API costs by 40-60%',
            'Improves response quality',
            'Reduces prompt token usage'
        ],
        'when_to_consider': 'If spending >$300K/year on API costs'
    })
    
    return recommendations

def calculate_optimization_roi(recommendations, current_roi_data):
    """
    Calculate potential ROI improvement from implementing recommendations
    """
    if not current_roi_data:
        return {}
    
    # Extract current metrics
    current_roi = current_roi_data.get('roi_percentage', 0)
    current_net_benefit = current_roi_data.get('net_benefit', 0)
    three_year_benefits = current_roi_data.get('three_year_benefits', 0)
    
    # Calculate potential improvements
    total_cost_savings = 0
    total_revenue_increase = 0
    
    for category, recs in recommendations.items():
        for rec in recs:
            # Parse savings/impact
            if 'estimated_savings' in rec and '$' in rec['estimated_savings']:
                try:
                    savings_str = rec['estimated_savings'].replace('$', '').replace(',', '').split('/')[0]
                    savings = float(savings_str)
                    if 'year' in rec['estimated_savings']:
                        total_cost_savings += savings * 3  # 3-year projection
                    else:
                        total_cost_savings += savings
                except:
                    pass
            
            if 'estimated_impact' in rec and '$' in rec['estimated_impact']:
                try:
                    impact_str = rec['estimated_impact'].replace('$', '').replace(',', '').split()[0]
                    impact = float(impact_str)
                    total_revenue_increase += impact
                except:
                    pass
    
    # Calculate optimized metrics
    optimized_costs = current_roi_data.get('three_year_tco', 0) - total_cost_savings if 'three_year_tco' in current_roi_data else 0
    optimized_benefits = three_year_benefits + total_revenue_increase
    optimized_net_benefit = optimized_benefits - optimized_costs if optimized_costs > 0 else 0
    optimized_roi = ((optimized_benefits - optimized_costs) / optimized_costs * 100) if optimized_costs > 0 else 0
    
    roi_improvement = optimized_roi - current_roi
    
    return {
        'total_cost_savings': total_cost_savings,
        'total_revenue_increase': total_revenue_increase,
        'optimized_roi': optimized_roi,
        'roi_improvement': roi_improvement,
        'optimized_net_benefit': optimized_net_benefit,
        'net_benefit_improvement': optimized_net_benefit - current_net_benefit
    }