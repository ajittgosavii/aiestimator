#!/usr/bin/env python3
"""
Add intelligent guidance and cost estimation helpers to Cost Analysis tab
This helps enterprises who don't know how to estimate Gen AI costs
"""

# Cost Estimation Helper Module
COST_ESTIMATION_GUIDE = {
    'api_costs': {
        'factors': ['model_provider', 'use_case', 'org_size', 'expected_users'],
        'typical_ranges': {
            'small_pilot': {'requests_per_day': (100, 500), 'tokens_per_request': (1000, 2000)},
            'medium_deployment': {'requests_per_day': (500, 5000), 'tokens_per_request': (1500, 3000)},
            'large_production': {'requests_per_day': (5000, 50000), 'tokens_per_request': (2000, 5000)}
        },
        'provider_costs': {
            'OpenAI (GPT-4)': {'per_million': 30, 'description': 'Most capable, highest cost'},
            'Anthropic (Claude)': {'per_million': 15, 'description': 'Balanced performance and cost'},
            'AWS Bedrock': {'per_million': 12, 'description': 'Enterprise-focused, good value'},
            'Azure OpenAI': {'per_million': 28, 'description': 'Enterprise integration'},
            'Google Vertex AI': {'per_million': 10, 'description': 'Competitive pricing'}
        }
    },
    
    'infrastructure': {
        'by_maturity': {
            'Exploring': {'monthly_cost': (500, 2000), 'description': 'Minimal infrastructure, mostly SaaS'},
            'Pilot': {'monthly_cost': (2000, 8000), 'description': 'Dev/test environments, basic monitoring'},
            'Scaling': {'monthly_cost': (8000, 25000), 'description': 'Production infrastructure, scaling resources'},
            'Mature': {'monthly_cost': (25000, 100000), 'description': 'Full enterprise infrastructure, multi-region'}
        },
        'components': ['Vector databases', 'Caching layers', 'API gateways', 'Monitoring tools', 'Storage']
    },
    
    'development': {
        'by_size': {
            '<100': {'fte_count': (0.5, 2), 'avg_salary': 120000},
            '100-500': {'fte_count': (2, 5), 'avg_salary': 130000},
            '500-1000': {'fte_count': (3, 8), 'avg_salary': 140000},
            '1000-5000': {'fte_count': (5, 15), 'avg_salary': 145000},
            '5000+': {'fte_count': (10, 30), 'avg_salary': 150000}
        },
        'typical_timeline': 'Pilot: 3-6 months, Scaling: 6-12 months, Production: 12+ months'
    },
    
    'operations': {
        'by_maturity': {
            'Exploring': {'monthly_cost': (1000, 3000), 'fte': (0.25, 0.5)},
            'Pilot': {'monthly_cost': (3000, 10000), 'fte': (0.5, 2)},
            'Scaling': {'monthly_cost': (10000, 30000), 'fte': (2, 5)},
            'Mature': {'monthly_cost': (30000, 100000), 'fte': (5, 15)}
        }
    }
}

# Industry-specific multipliers
INDUSTRY_MULTIPLIERS = {
    'Financial Services': {'compliance': 1.3, 'security': 1.4, 'description': 'High compliance requirements'},
    'Healthcare': {'compliance': 1.4, 'security': 1.5, 'description': 'HIPAA compliance, high security'},
    'Government': {'compliance': 1.5, 'security': 1.6, 'description': 'Stringent regulations'},
    'Technology': {'compliance': 1.0, 'security': 1.1, 'description': 'Standard requirements'},
    'Retail': {'compliance': 1.1, 'security': 1.2, 'description': 'Moderate compliance'},
    'Manufacturing': {'compliance': 1.1, 'security': 1.2, 'description': 'Standard requirements'}
}

# Use case specific patterns
USE_CASE_PATTERNS = {
    'Customer Service/Chatbots': {
        'daily_requests_per_user': (20, 50),
        'avg_tokens': (1500, 2500),
        'description': 'High volume, shorter interactions',
        'typical_users': '10-20% of customer base'
    },
    'Content Generation': {
        'daily_requests_per_user': (5, 15),
        'avg_tokens': (3000, 6000),
        'description': 'Lower volume, longer outputs',
        'typical_users': 'Marketing/content teams (10-50 people)'
    },
    'Code Assistance': {
        'daily_requests_per_user': (15, 40),
        'avg_tokens': (2000, 4000),
        'description': 'Medium volume, code-heavy',
        'typical_users': 'Development teams (50-500 developers)'
    },
    'Data Analysis': {
        'daily_requests_per_user': (10, 30),
        'avg_tokens': (2500, 5000),
        'description': 'Medium volume, analytical outputs',
        'typical_users': 'Analytics teams (20-100 analysts)'
    },
    'Document Processing': {
        'daily_requests_per_user': (5, 20),
        'avg_tokens': (4000, 8000),
        'description': 'Lower volume, document-heavy',
        'typical_users': 'Document-intensive departments'
    }
}

def estimate_smart_defaults(org_profile):
    """
    Generate smart default values based on organization profile
    """
    industry = org_profile.get('industry', 'Technology')
    org_size = org_profile.get('org_size', '500-1000')
    maturity = org_profile.get('maturity', 'Pilot')
    use_case = org_profile.get('use_case', 'Customer Service/Chatbots')
    expected_users = org_profile.get('expected_users', 100)
    
    # Get multipliers
    industry_mult = INDUSTRY_MULTIPLIERS.get(industry, {'compliance': 1.0, 'security': 1.0})
    use_case_pattern = USE_CASE_PATTERNS.get(use_case, USE_CASE_PATTERNS['Customer Service/Chatbots'])
    
    # Estimate API costs
    requests_range = use_case_pattern['daily_requests_per_user']
    requests_per_day = int(expected_users * ((requests_range[0] + requests_range[1]) / 2))
    
    tokens_range = use_case_pattern['avg_tokens']
    avg_tokens = int((tokens_range[0] + tokens_range[1]) / 2)
    
    # Provider cost (use middle of the pack)
    cost_per_million = 15.0  # Claude/Bedrock range
    
    # Infrastructure
    infra_range = COST_ESTIMATION_GUIDE['infrastructure']['by_maturity'][maturity]['monthly_cost']
    monthly_infra = int((infra_range[0] + infra_range[1]) / 2)
    
    # Development
    dev_info = COST_ESTIMATION_GUIDE['development']['by_size'][org_size]
    dev_fte = (dev_info['fte_count'][0] + dev_info['fte_count'][1]) / 2
    dev_cost = int(dev_fte * dev_info['avg_salary'])
    
    # Operations
    ops_info = COST_ESTIMATION_GUIDE['operations']['by_maturity'][maturity]
    monthly_ops = int((ops_info['monthly_cost'][0] + ops_info['monthly_cost'][1]) / 2)
    
    # Apply industry multipliers
    monthly_infra = int(monthly_infra * industry_mult['security'])
    monthly_ops = int(monthly_ops * industry_mult['compliance'])
    
    return {
        'requests_per_day': requests_per_day,
        'avg_tokens_per_request': avg_tokens,
        'cost_per_million_tokens': cost_per_million,
        'monthly_infrastructure': monthly_infra,
        'annual_development': dev_cost,
        'monthly_operations': monthly_ops,
        'growth_rate': 25,  # Typical for scaling phase
        'contingency': 15,  # Standard project contingency
        'explanation': {
            'api': f"Based on {use_case}: {requests_range[0]}-{requests_range[1]} requests/user/day",
            'infrastructure': f"For {maturity} stage: ${infra_range[0]:,}-${infra_range[1]:,}/month",
            'development': f"For {org_size} org: {dev_info['fte_count'][0]}-{dev_info['fte_count'][1]} FTEs",
            'industry_note': f"{industry}: {industry_mult['compliance']}x compliance factor"
        }
    }

def generate_cost_guidance(field_name, org_profile):
    """
    Generate contextual guidance for each cost field
    """
    guidance = {
        'requests_per_day': {
            'tooltip': 'Total API requests across all users per day',
            'how_to_estimate': '1. Estimate requests per user per day\n2. Multiply by number of active users\n3. Add 20% buffer for peak usage',
            'example': 'Customer service chatbot: 100 users × 30 requests/day = 3,000 requests/day',
            'typical_range': 'Pilot: 100-1,000 | Production: 1,000-50,000',
            'red_flags': '• <10 requests/day: Too low for meaningful pilot\n• >100,000/day: Verify infrastructure can handle'
        },
        'avg_tokens_per_request': {
            'tooltip': 'Average combined input + output tokens per request',
            'how_to_estimate': '1. Input tokens: ~4 chars per token (e.g., 1000 chars = 250 tokens)\n2. Output tokens: depends on response length\n3. Add 20% buffer',
            'example': 'Chatbot: 500 input tokens + 1000 output tokens = 1,500 total',
            'typical_range': 'Short: 500-1,500 | Medium: 1,500-3,000 | Long: 3,000-8,000',
            'red_flags': '• <100 tokens: Likely underestimated\n• >10,000 tokens: Very expensive, consider optimization'
        },
        'cost_per_million_tokens': {
            'tooltip': 'Cost charged by your AI provider per 1 million tokens',
            'how_to_estimate': 'Check your provider\'s pricing page',
            'example': 'GPT-4: $30/M | Claude: $15/M | GPT-3.5: $2/M',
            'typical_range': 'Budget: $2-5/M | Standard: $10-20/M | Premium: $25-50/M',
            'providers': COST_ESTIMATION_GUIDE['api_costs']['provider_costs']
        },
        'monthly_infrastructure': {
            'tooltip': 'Hosting, databases, caching, monitoring, storage costs',
            'how_to_estimate': '1. List all infrastructure components\n2. Get quotes from AWS/Azure/GCP\n3. Add 30% for hidden costs',
            'example': 'Vector DB: $2K + Caching: $1K + Monitoring: $500 = $3,500/month',
            'by_maturity': COST_ESTIMATION_GUIDE['infrastructure']['by_maturity'],
            'components': COST_ESTIMATION_GUIDE['infrastructure']['components']
        },
        'annual_development': {
            'tooltip': 'Salaries for engineers, ML engineers, architects building the solution',
            'how_to_estimate': '1. List required roles and FTEs\n2. Use market salaries for your location\n3. Add benefits (30-40% of salary)',
            'example': '2 ML Engineers ($150K) + 1 Backend ($140K) = $440K',
            'by_org_size': COST_ESTIMATION_GUIDE['development']['by_size']
        }
    }
    
    return guidance.get(field_name, {})

print("Cost estimation helper module created!")
print(f"- Smart defaults for {len(INDUSTRY_MULTIPLIERS)} industries")
print(f"- Guidance for {len(USE_CASE_PATTERNS)} use cases")
print(f"- Detailed field-level help available")