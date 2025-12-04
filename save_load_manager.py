"""
Save/Load Functionality for Gen AI ROI Calculator
Handles data persistence, scenario management, and import/export
"""

import streamlit as st
import json
from datetime import datetime
import base64

class ScenarioManager:
    """Manages saving, loading, and managing multiple scenarios"""
    
    def __init__(self):
        # Initialize session state for scenarios
        if 'scenarios' not in st.session_state:
            st.session_state.scenarios = {}
        if 'current_scenario_name' not in st.session_state:
            st.session_state.current_scenario_name = 'Default Scenario'
        if 'last_auto_save' not in st.session_state:
            st.session_state.last_auto_save = None
    
    def get_current_data(self):
        """Collect all current session state data into a single dictionary"""
        data = {
            'metadata': {
                'scenario_name': st.session_state.current_scenario_name,
                'created_date': datetime.now().isoformat(),
                'version': '2.2'
            },
            'cost_data': st.session_state.get('cost_data', {}),
            'roi_data': st.session_state.get('roi_data', {}),
            'risk_scores': st.session_state.get('risk_scores', {}),
            'org_profile': {
                'org_name': st.session_state.get('org_name', ''),
                'industry': st.session_state.get('industry', ''),
                'org_size': st.session_state.get('org_size', ''),
                'maturity': st.session_state.get('maturity', ''),
                'use_case': st.session_state.get('use_case', ''),
                'expected_users': st.session_state.get('expected_users', 0)
            },
            'inputs': {
                # Direct AI Costs
                'model_provider': st.session_state.get('model_provider', ''),
                'avg_tokens_per_request': st.session_state.get('avg_tokens_per_request', 0),
                'requests_per_day': st.session_state.get('requests_per_day', 0),
                'cost_per_million_tokens': st.session_state.get('cost_per_million_tokens', 0),
                'growth_rate': st.session_state.get('growth_rate', 0),
                'embedding_cost': st.session_state.get('embedding_cost', 0),
                
                # Infrastructure
                'compute_cost': st.session_state.get('compute_cost', 0),
                'storage_cost': st.session_state.get('storage_cost', 0),
                'networking_cost': st.session_state.get('networking_cost', 0),
                'security_tools': st.session_state.get('security_tools', 0),
                'monitoring_tools': st.session_state.get('monitoring_tools', 0),
                'backup_dr': st.session_state.get('backup_dr', 0),
                
                # Development
                'ai_engineers': st.session_state.get('ai_engineers', 0),
                'ai_engineer_cost': st.session_state.get('ai_engineer_cost', 0),
                'backend_devs': st.session_state.get('backend_devs', 0),
                'backend_cost': st.session_state.get('backend_cost', 0),
                'frontend_devs': st.session_state.get('frontend_devs', 0),
                'frontend_cost': st.session_state.get('frontend_cost', 0),
                'qa_engineers': st.session_state.get('qa_engineers', 0),
                'qa_cost': st.session_state.get('qa_cost', 0),
                'dev_tools': st.session_state.get('dev_tools', 0),
                
                # Data Management
                'data_engineers': st.session_state.get('data_engineers', 0),
                'data_engineer_cost': st.session_state.get('data_engineer_cost', 0),
                'data_prep_cost': st.session_state.get('data_prep_cost', 0),
                'data_quality_tools': st.session_state.get('data_quality_tools', 0),
                'data_labeling': st.session_state.get('data_labeling', 0),
                
                # Operations
                'ops_engineers': st.session_state.get('ops_engineers', 0),
                'ops_cost': st.session_state.get('ops_cost', 0),
                'support_staff': st.session_state.get('support_staff', 0),
                'support_cost': st.session_state.get('support_cost', 0),
                'incident_mgmt': st.session_state.get('incident_mgmt', 0),
                'model_retraining': st.session_state.get('model_retraining', 0),
                
                # Organizational
                'training_cost': st.session_state.get('training_cost', 0),
                'change_mgmt': st.session_state.get('change_mgmt', 0),
                'governance_cost': st.session_state.get('governance_cost', 0),
                'legal_cost': st.session_state.get('legal_cost', 0),
                
                # Contingency
                'contingency_pct': st.session_state.get('contingency_pct', 0),
                
                # ROI Inputs
                'time_saved_per_user': st.session_state.get('time_saved_per_user', 0),
                'hourly_rate': st.session_state.get('hourly_rate', 0),
                'affected_users': st.session_state.get('affected_users', 0),
                'productivity_pct': st.session_state.get('productivity_pct', 0),
                'customer_service_reduction': st.session_state.get('customer_service_reduction', 0),
                'process_automation_value': st.session_state.get('process_automation_value', 0),
                'error_reduction_value': st.session_state.get('error_reduction_value', 0),
                'cost_reduction_confidence': st.session_state.get('cost_reduction_confidence', 0),
                'new_revenue': st.session_state.get('new_revenue', 0),
                'customer_retention': st.session_state.get('customer_retention', 0),
                'revenue_confidence': st.session_state.get('revenue_confidence', 0),
                'competitive_advantage': st.session_state.get('competitive_advantage', 0),
                'innovation_value': st.session_state.get('innovation_value', 0),
                'strategic_confidence': st.session_state.get('strategic_confidence', 0)
            }
        }
        return data
    
    def save_scenario(self, scenario_name):
        """Save current data as a named scenario"""
        data = self.get_current_data()
        data['metadata']['scenario_name'] = scenario_name
        st.session_state.scenarios[scenario_name] = data
        st.session_state.current_scenario_name = scenario_name
        return True
    
    def load_scenario(self, scenario_name):
        """Load a saved scenario into session state"""
        if scenario_name not in st.session_state.scenarios:
            return False
        
        data = st.session_state.scenarios[scenario_name]
        
        # Load all data back into session state
        st.session_state.cost_data = data.get('cost_data', {})
        st.session_state.roi_data = data.get('roi_data', {})
        st.session_state.risk_scores = data.get('risk_scores', {})
        
        # Load org profile
        org_profile = data.get('org_profile', {})
        for key, value in org_profile.items():
            st.session_state[key] = value
        
        # Load all inputs
        inputs = data.get('inputs', {})
        for key, value in inputs.items():
            st.session_state[key] = value
        
        st.session_state.current_scenario_name = scenario_name
        return True
    
    def delete_scenario(self, scenario_name):
        """Delete a saved scenario"""
        if scenario_name in st.session_state.scenarios:
            del st.session_state.scenarios[scenario_name]
            return True
        return False
    
    def export_scenario_json(self, scenario_name=None):
        """Export scenario as JSON string"""
        if scenario_name and scenario_name in st.session_state.scenarios:
            data = st.session_state.scenarios[scenario_name]
        else:
            data = self.get_current_data()
        
        return json.dumps(data, indent=2)
    
    def import_scenario_json(self, json_str, scenario_name=None):
        """Import scenario from JSON string"""
        try:
            data = json.loads(json_str)
            
            # Validate basic structure
            if 'metadata' not in data:
                return False, "Invalid file format: missing metadata"
            
            # Generate scenario name if not provided
            if not scenario_name:
                scenario_name = data['metadata'].get('scenario_name', f"Imported_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            # Save to scenarios
            st.session_state.scenarios[scenario_name] = data
            
            return True, f"Successfully imported scenario: {scenario_name}"
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON file: {str(e)}"
        except Exception as e:
            return False, f"Error importing scenario: {str(e)}"
    
    def get_scenario_list(self):
        """Get list of saved scenario names"""
        return list(st.session_state.scenarios.keys())
    
    def auto_save(self):
        """Auto-save current scenario"""
        auto_save_name = f"_autosave_{st.session_state.current_scenario_name}"
        self.save_scenario(auto_save_name)
        st.session_state.last_auto_save = datetime.now()


def render_save_load_ui():
    """Render the save/load UI in the sidebar or main area"""
    
    st.markdown("---")
    st.subheader("💾 Scenario Management")
    
    manager = ScenarioManager()
    
    # Current scenario display
    st.markdown(f"**Current:** {st.session_state.current_scenario_name}")
    
    # Save current scenario
    col1, col2 = st.columns([3, 1])
    with col1:
        new_scenario_name = st.text_input(
            "Scenario Name",
            value=st.session_state.current_scenario_name,
            key="save_scenario_name"
        )
    with col2:
        if st.button("💾 Save", key="save_scenario_btn"):
            if new_scenario_name:
                manager.save_scenario(new_scenario_name)
                st.success(f"✅ Saved: {new_scenario_name}")
                st.rerun()
            else:
                st.error("Please enter a scenario name")
    
    # Load existing scenario
    scenarios = manager.get_scenario_list()
    if scenarios:
        # Filter out auto-save scenarios for display
        display_scenarios = [s for s in scenarios if not s.startswith('_autosave_')]
        
        if display_scenarios:
            st.markdown("**Load Saved Scenario:**")
            selected_scenario = st.selectbox(
                "Select scenario",
                display_scenarios,
                key="load_scenario_select"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📂 Load", key="load_scenario_btn"):
                    if manager.load_scenario(selected_scenario):
                        st.success(f"✅ Loaded: {selected_scenario}")
                        st.rerun()
                    else:
                        st.error("Failed to load scenario")
            
            with col2:
                if st.button("🗑️ Delete", key="delete_scenario_btn"):
                    if manager.delete_scenario(selected_scenario):
                        st.success(f"✅ Deleted: {selected_scenario}")
                        st.rerun()
                    else:
                        st.error("Failed to delete scenario")
    
    st.markdown("---")
    
    # Export/Import
    st.markdown("**📥 Import/Export**")
    
    # Export
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📤 Export Current", key="export_btn"):
            json_str = manager.export_scenario_json()
            filename = f"{st.session_state.current_scenario_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            st.download_button(
                label="⬇️ Download JSON",
                data=json_str,
                file_name=filename,
                mime="application/json",
                key="download_json_btn"
            )
    
    # Import
    with col2:
        uploaded_file = st.file_uploader(
            "📁 Import Scenario",
            type=['json'],
            key="import_file_uploader"
        )
        
        if uploaded_file is not None:
            try:
                json_str = uploaded_file.read().decode('utf-8')
                success, message = manager.import_scenario_json(json_str)
                
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
    
    # Auto-save indicator
    if st.session_state.last_auto_save:
        time_since_save = (datetime.now() - st.session_state.last_auto_save).seconds
        st.caption(f"Last auto-saved: {time_since_save}s ago")


def enable_auto_save(interval_seconds=30):
    """
    Enable auto-save functionality
    Call this in your main app to enable periodic auto-saving
    """
    manager = ScenarioManager()
    
    # Check if enough time has passed since last auto-save
    if st.session_state.last_auto_save:
        time_since_save = (datetime.now() - st.session_state.last_auto_save).seconds
        if time_since_save < interval_seconds:
            return
    
    # Perform auto-save
    try:
        manager.auto_save()
    except Exception as e:
        # Silent failure - don't disrupt user experience
        pass


def export_all_scenarios():
    """Export all scenarios as a single JSON file"""
    data = {
        'export_date': datetime.now().isoformat(),
        'version': '2.2',
        'scenarios': st.session_state.scenarios
    }
    return json.dumps(data, indent=2)


def import_all_scenarios(json_str):
    """Import multiple scenarios from a single JSON file"""
    try:
        data = json.loads(json_str)
        
        if 'scenarios' not in data:
            return False, "Invalid export file format"
        
        # Import all scenarios
        count = 0
        for scenario_name, scenario_data in data['scenarios'].items():
            st.session_state.scenarios[scenario_name] = scenario_data
            count += 1
        
        return True, f"Successfully imported {count} scenarios"
    except Exception as e:
        return False, f"Error importing scenarios: {str(e)}"