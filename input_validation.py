"""
Input Validation Module for Gen AI ROI Calculator
Validates all user inputs to prevent errors and provide helpful feedback
"""

import streamlit as st

class InputValidator:
    """Validates user inputs and provides helpful error messages"""
    
    # Validation thresholds
    THRESHOLDS = {
        'max_api_cost_pct': 70,  # API costs should typically be < 70% of total
        'max_dev_cost_pct': 60,  # Dev costs should typically be < 60% of total
        'min_data_cost_pct': 5,  # Data costs should be at least 5% of total
        'max_roi_pct': 500,  # ROI > 500% is highly unusual
        'min_payback_months': 3,  # Payback < 3 months is suspicious
        'max_payback_months': 60,  # Payback > 5 years is concerning
        'max_fte': 20,  # More than 20 FTE for one role is unusual
        'max_hourly_rate': 500,  # Hourly rate > $500 is very high
        'max_growth_rate': 200,  # Growth > 200% per year is aggressive
        'max_confidence': 100,  # Confidence can't exceed 100%
    }
    
    @staticmethod
    def validate_positive_number(value, field_name, allow_zero=False):
        """Validate that a number is positive"""
        if value is None:
            return False, f"{field_name} is required"
        
        if allow_zero:
            if value < 0:
                return False, f"{field_name} cannot be negative"
        else:
            if value <= 0:
                return False, f"{field_name} must be greater than zero"
        
        return True, ""
    
    @staticmethod
    def validate_percentage(value, field_name, min_val=0, max_val=100):
        """Validate that a percentage is within valid range"""
        valid, msg = InputValidator.validate_positive_number(value, field_name, allow_zero=True)
        if not valid:
            return False, msg
        
        if value < min_val or value > max_val:
            return False, f"{field_name} must be between {min_val}% and {max_val}%"
        
        return True, ""
    
    @staticmethod
    def validate_fte(value, field_name):
        """Validate FTE count"""
        valid, msg = InputValidator.validate_positive_number(value, field_name, allow_zero=True)
        if not valid:
            return False, msg
        
        if value > InputValidator.THRESHOLDS['max_fte']:
            return False, f"⚠️ {field_name}: {value} FTE is very high. Typical projects use fewer resources. Please verify."
        
        return True, ""
    
    @staticmethod
    def validate_cost(value, field_name, max_warning=None):
        """Validate cost input"""
        valid, msg = InputValidator.validate_positive_number(value, field_name, allow_zero=True)
        if not valid:
            return False, msg
        
        if max_warning and value > max_warning:
            return False, f"⚠️ {field_name}: ${value:,} seems very high. Please verify."
        
        return True, ""
    
    @staticmethod
    def validate_growth_rate(value):
        """Validate growth rate"""
        valid, msg = InputValidator.validate_positive_number(value, "Growth Rate", allow_zero=True)
        if not valid:
            return False, msg
        
        if value > InputValidator.THRESHOLDS['max_growth_rate']:
            return False, f"⚠️ Growth rate of {value}% per year is very aggressive. Typical AI projects see 20-80% annual growth. Please verify."
        
        return True, ""
    
    @staticmethod
    def validate_hourly_rate(value):
        """Validate hourly rate"""
        valid, msg = InputValidator.validate_positive_number(value, "Hourly Rate")
        if not valid:
            return False, msg
        
        if value > InputValidator.THRESHOLDS['max_hourly_rate']:
            return False, f"⚠️ Hourly rate of ${value} is very high. Typical rates are $50-$200/hour. Please verify."
        
        if value < 20:
            return False, f"⚠️ Hourly rate of ${value} is very low. Please verify."
        
        return True, ""
    
    @staticmethod
    def validate_cost_structure(cost_breakdown, total_cost):
        """Validate overall cost structure and provide warnings"""
        warnings = []
        errors = []
        
        if total_cost <= 0:
            errors.append("❌ Total cost must be greater than zero")
            return errors, warnings
        
        # Calculate percentages
        api_pct = (cost_breakdown.get('API Costs', 0) / total_cost * 100)
        dev_pct = (cost_breakdown.get('Development', 0) / total_cost * 100)
        data_pct = (cost_breakdown.get('Data Management', 0) / total_cost * 100)
        
        # Validate API costs
        if api_pct > InputValidator.THRESHOLDS['max_api_cost_pct']:
            warnings.append(f"⚠️ API costs are {api_pct:.0f}% of total budget. Typical range is 15-40%. Consider cost optimization strategies.")
        
        # Validate development costs
        if dev_pct > InputValidator.THRESHOLDS['max_dev_cost_pct']:
            warnings.append(f"⚠️ Development costs are {dev_pct:.0f}% of total budget. Typical range is 25-45%. Consider using pre-built frameworks or managed services.")
        
        # Validate data costs
        if data_pct < InputValidator.THRESHOLDS['min_data_cost_pct']:
            errors.append(f"❌ Data costs are only {data_pct:.1f}% of budget. This is dangerously low. Data quality is the #1 factor in AI success. Minimum 8-12% recommended.")
        
        return errors, warnings
    
    @staticmethod
    def validate_roi_projections(roi_data):
        """Validate ROI projections and provide warnings"""
        warnings = []
        errors = []
        
        roi_pct = roi_data.get('roi_percentage', 0)
        payback_months = roi_data.get('payback_months', 0)
        
        # Validate ROI percentage
        if roi_pct < 0:
            warnings.append(f"⚠️ Negative ROI of {roi_pct:.0f}% means the project will lose money. Are you sure you want to proceed?")
        elif roi_pct > InputValidator.THRESHOLDS['max_roi_pct']:
            warnings.append(f"⚠️ ROI of {roi_pct:.0f}% is extremely high. Typical AI projects see 100-200% ROI. Please verify your assumptions aren't overly optimistic.")
        
        # Validate payback period
        if payback_months > 0:
            if payback_months < InputValidator.THRESHOLDS['min_payback_months']:
                warnings.append(f"⚠️ Payback period of {payback_months:.0f} months is unusually short. Most AI projects take 12-36 months to break even. Please verify.")
            elif payback_months > InputValidator.THRESHOLDS['max_payback_months']:
                warnings.append(f"⚠️ Payback period of {payback_months:.0f} months (>{payback_months//12} years) is very long. Consider whether this investment is viable.")
        
        # Validate confidence levels
        confidence_issues = []
        if roi_data.get('productivity_pct', 0) < 50:
            confidence_issues.append("productivity gains")
        if roi_data.get('cost_reduction_confidence', 0) < 50:
            confidence_issues.append("cost reductions")
        if roi_data.get('revenue_confidence', 0) < 50:
            confidence_issues.append("revenue increases")
        
        if confidence_issues:
            warnings.append(f"⚠️ Low confidence in {', '.join(confidence_issues)}. Consider more conservative projections or pilot programs to validate assumptions.")
        
        return errors, warnings
    
    @staticmethod
    def validate_required_fields(data_dict, required_fields):
        """Validate that required fields are present and non-empty"""
        missing = []
        
        for field in required_fields:
            value = data_dict.get(field)
            if value is None or value == '' or value == 0:
                missing.append(field)
        
        if missing:
            return False, f"❌ Required fields missing: {', '.join(missing)}"
        
        return True, ""
    
    @staticmethod
    def show_validation_message(errors, warnings):
        """Display validation errors and warnings to user"""
        if errors:
            for error in errors:
                st.error(error)
            return False  # Has errors
        
        if warnings:
            for warning in warnings:
                st.warning(warning)
        
        return True  # No errors (warnings are OK)


def validate_cost_inputs(inputs):
    """Validate all cost-related inputs"""
    validator = InputValidator()
    errors = []
    warnings = []
    
    # Validate organization profile
    if not inputs.get('org_name'):
        errors.append("❌ Organization name is required")
    
    # Validate API costs
    valid, msg = validator.validate_positive_number(
        inputs.get('avg_tokens_per_request', 0),
        "Average Tokens per Request"
    )
    if not valid:
        errors.append(msg)
    
    valid, msg = validator.validate_positive_number(
        inputs.get('requests_per_day', 0),
        "Requests per Day"
    )
    if not valid:
        errors.append(msg)
    
    valid, msg = validator.validate_cost(
        inputs.get('cost_per_million_tokens', 0),
        "Cost per Million Tokens"
    )
    if not valid:
        errors.append(msg)
    
    valid, msg = validator.validate_growth_rate(
        inputs.get('growth_rate', 0)
    )
    if not valid:
        warnings.append(msg)
    
    # Validate FTE counts
    for field in ['ai_engineers', 'backend_devs', 'frontend_devs', 'qa_engineers', 
                  'data_engineers', 'ops_engineers', 'support_staff']:
        valid, msg = validator.validate_fte(
            inputs.get(field, 0),
            field.replace('_', ' ').title()
        )
        if not valid:
            warnings.append(msg)
    
    # Validate costs aren't unreasonably high
    if inputs.get('ai_engineer_cost', 0) > 300000:
        warnings.append(f"⚠️ AI Engineer annual cost of ${inputs['ai_engineer_cost']:,} is very high. Typical range is $150K-$250K.")
    
    # Validate contingency percentage
    contingency = inputs.get('contingency_pct', 0)
    if contingency < 10:
        warnings.append("⚠️ Contingency buffer < 10% is risky for AI projects. Recommend 15-25%.")
    elif contingency > 50:
        warnings.append("⚠️ Contingency buffer > 50% seems excessive. Typical range is 15-25%.")
    
    return errors, warnings


def validate_roi_inputs(inputs):
    """Validate all ROI-related inputs"""
    validator = InputValidator()
    errors = []
    warnings = []
    
    # Validate productivity inputs
    valid, msg = validator.validate_positive_number(
        inputs.get('time_saved_per_user', 0),
        "Time Saved per User",
        allow_zero=True
    )
    if not valid:
        errors.append(msg)
    
    if inputs.get('time_saved_per_user', 0) > 40:
        warnings.append("⚠️ Time saved > 40 hours/week is unrealistic (exceeds working hours). Please verify.")
    
    valid, msg = validator.validate_hourly_rate(
        inputs.get('hourly_rate', 75)
    )
    if not valid:
        warnings.append(msg)
    
    # Validate confidence percentages
    for field in ['productivity_pct', 'cost_reduction_confidence', 
                  'revenue_confidence', 'strategic_confidence']:
        valid, msg = validator.validate_percentage(
            inputs.get(field, 0),
            field.replace('_', ' ').title()
        )
        if not valid:
            errors.append(msg)
    
    return errors, warnings


def validate_before_calculation(cost_data_inputs, roi_data_inputs):
    """
    Comprehensive validation before running calculations
    Returns: (is_valid, errors, warnings)
    """
    all_errors = []
    all_warnings = []
    
    # Validate cost inputs
    cost_errors, cost_warnings = validate_cost_inputs(cost_data_inputs)
    all_errors.extend(cost_errors)
    all_warnings.extend(cost_warnings)
    
    # Validate ROI inputs
    roi_errors, roi_warnings = validate_roi_inputs(roi_data_inputs)
    all_errors.extend(roi_errors)
    all_warnings.extend(roi_warnings)
    
    is_valid = len(all_errors) == 0
    
    return is_valid, all_errors, all_warnings


def show_validation_summary(errors, warnings):
    """Show a summary of validation results"""
    if errors or warnings:
        st.markdown("---")
        st.subheader("⚠️ Validation Results")
    
    if errors:
        st.error(f"**{len(errors)} Error(s) Found - Please fix before proceeding:**")
        for error in errors:
            st.markdown(f"- {error}")
    
    if warnings:
        st.warning(f"**{len(warnings)} Warning(s):**")
        for warning in warnings:
            st.markdown(f"- {warning}")
        st.info("💡 Warnings don't prevent calculations but suggest reviewing your inputs for accuracy.")
    
    if not errors and not warnings:
        st.success("✅ All inputs validated successfully!")
    
    return len(errors) == 0  # Return True if no errors


def add_inline_validation_to_input(value, validation_func, *args):
    """
    Add inline validation to an input field
    Returns: (is_valid, value, error_message)
    """
    try:
        is_valid, message = validation_func(value, *args)
        return is_valid, value, message
    except Exception as e:
        return False, value, f"Validation error: {str(e)}"


# Quick validation helpers for common patterns
def validate_and_warn(value, min_val=None, max_val=None, field_name="Value", allow_zero=False):
    """
    Quick validation helper that can be used inline
    Returns True if valid, shows warning/error and returns False otherwise
    """
    if value is None:
        st.error(f"❌ {field_name} is required")
        return False
    
    if not allow_zero and value == 0:
        st.error(f"❌ {field_name} must be greater than zero")
        return False
    
    if allow_zero and value < 0:
        st.error(f"❌ {field_name} cannot be negative")
        return False
    
    if min_val is not None and value < min_val:
        st.warning(f"⚠️ {field_name} of {value} is below typical minimum of {min_val}")
    
    if max_val is not None and value > max_val:
        st.warning(f"⚠️ {field_name} of {value} exceeds typical maximum of {max_val}")
    
    return True