import streamlit as st
import pandas as pd
import joblib
import pickle
import numpy as np

st.set_page_config(
    page_title="Customer Churn Predictor", 
    layout="wide"
)P

st.title("Customer Churn Prediction Application")
st.markdown("#### Predict customer churn risk and get retention recommendations!")
st.markdown("---")

# navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Single Prediction", "Batch Prediction", "Retention Insights"])

# model and preprocessing objects
@st.cache_resource
def load_artifacts():
    try:
        model = joblib.load('churn_rf_model.pkl')
        scaler = joblib.load('scaler.pkl')
        with open('label_encoders.pkl', 'rb') as f:
            label_encoders = pickle.load(f)
        with open('feature_names.pkl', 'rb') as f:
            feature_names = pickle.load(f)
        return model, scaler, label_encoders, feature_names
    except Exception as e:
        st.error(f"Error loading artifacts: {e}")
        return None, None, None, None

model, scaler, label_encoders, feature_names = load_artifacts()

if model is None:
    st.stop()

# feature importance
feature_importance = pd.DataFrame({
    'feature': feature_names,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

st.sidebar.write("### Top 5 Important Features:")
counter = 1
for i, row in feature_importance.head(5).iterrows():
    st.sidebar.write(f"{counter}: {row['feature']}")
    counter += 1

# 1- Single Prediction Page
if page == "Single Prediction":
    st.header("1- Single Customer Prediction")
    
    # multiple columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Customer Demographics")
        gender = st.selectbox("Gender", ["Female", "Male"])
        senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
        partner = st.selectbox("Partner", ["No", "Yes"])
        dependents = st.selectbox("Dependents", ["No", "Yes"])
        
        st.subheader("Services")
        phone_service = st.selectbox("Phone Service", ["No", "Yes"])
        multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])
        internet_service = st.selectbox("Internet Service", ["No", "DSL", "Fiber optic"])
        online_security = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
        online_backup = st.selectbox("Online Backup", ["No", "Yes", "No internet service"])
        
    with col2:
        st.subheader("Additional Services")
        device_protection = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])
        tech_support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
        streaming_tv = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"])
        streaming_movies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])
        
        st.subheader("Billing & Contract")
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
        paperless_billing = st.selectbox("Paperless Billing", ["No", "Yes"])
        payment_method = st.selectbox("Payment Method", [
            "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"
        ])
        tenure_group = st.selectbox("Tenure Group", ["0-12 months", "13-24 months", "25-36 months", "37+ months"])
    
    # Numerical inputs
    st.subheader("Financial Information")
    col3, col4, col5 = st.columns(3)
    with col3:
        total_charges = st.number_input("Total Charges", min_value=0.0, value=1000.0, step=100.0)
    with col4:
        cltv = st.number_input("CLTV (Customer Lifetime Value)", min_value=0, value=3000, step=100)
    with col5:
        avg_monthly_charge = st.number_input("Average Monthly Charge", min_value=0.0, value=50.0, step=10.0)
    
    # Prediction button
    if st.button("Predict Churn Risk", type="primary"):
        try:
            # input data
            input_data = {
                'Gender': gender,
                'Senior Citizen': senior_citizen,
                'Partner': partner,
                'Dependents': dependents,
                'Phone Service': phone_service,
                'Multiple Lines': multiple_lines,
                'Internet Service': internet_service,
                'Online Security': online_security,
                'Online Backup': online_backup,
                'Device Protection': device_protection,
                'Tech Support': tech_support,
                'Streaming TV': streaming_tv,
                'Streaming Movies': streaming_movies,
                'Contract': contract,
                'Paperless Billing': paperless_billing,
                'Payment Method': payment_method,
                'Tenure Group': tenure_group,
                'Total Charges': total_charges,
                'CLTV': cltv,
                'Avg Monthly Charge': avg_monthly_charge
            }
            
            input_df = pd.DataFrame([input_data])
            
            # binary mapping
            binary_mapping = {'Yes': 1, 'No': 0, 'Male': 1, 'Female': 0}
            binary_columns = ['Gender', 'Senior Citizen', 'Partner', 'Dependents', 'Phone Service', 'Paperless Billing']
            
            for col in binary_columns:
                if col in input_df.columns:
                    input_df[col] = input_df[col].map(binary_mapping)
            
            # multi-category columns using label encoders
            multi_category_columns = [
                'Multiple Lines', 'Internet Service', 'Online Security', 
                'Online Backup', 'Device Protection', 'Tech Support',
                'Streaming TV', 'Streaming Movies', 'Contract', 
                'Payment Method', 'Tenure Group'
            ]
            
            encoding_successful = True
            for col in multi_category_columns:
                if col in input_df.columns and col in label_encoders:
                    try:
                        # Debug: Show what we're trying to encode
                        original_value = input_df[col].iloc[0]
                        available_classes = list(label_encoders[col].classes_)
                        
                        # Check if value exists in encoder classes
                        if original_value in available_classes:
                            input_df[col] = label_encoders[col].transform([original_value])[0]
                        else:
                            st.warning(f"Value '{original_value}' not found in {col} encoder. Using default encoding.")
                            input_df[col] = label_encoders[col].transform([available_classes[0]])[0]
                            
                    except Exception as e:
                        st.error(f"Error encoding {col}: {e}")
                        encoding_successful = False
                        break
            
            if not encoding_successful:
                st.error("Encoding failed. Please check the values and try again.")
            else:
                # Scale numerical features
                numerical_cols = ['Total Charges', 'CLTV', 'Avg Monthly Charge']
                input_df[numerical_cols] = scaler.transform(input_df[numerical_cols])
                
                input_df = input_df[feature_names]
                
                # Make prediction
                churn_probability = model.predict_proba(input_df)[0][1]
                churn_prediction = model.predict(input_df)[0]
                
                st.subheader("- Prediction Results")
                
                # Progress bar for churn probability
                st.write(f"**Churn Probability:** {churn_probability:.1%}")
                st.progress(float(churn_probability))
                
                # Risk level
                if churn_probability < 0.3:
                    risk_level = "Low Risk"
                    recommendation = "Standard monitoring recommended"
                elif churn_probability < 0.7:
                    risk_level = "Medium Risk" 
                    recommendation = "Proactive engagement needed"
                else:
                    risk_level = "High Risk"
                    recommendation = "Immediate retention action required"
                
                st.write(f"**Risk Level:** {risk_level}")
                st.write(f"**Recommendation:** {recommendation}")
                
                # Key factors contributing to churn risk
                st.subheader("- Key Risk Factors")
                top_factors = feature_importance.head(3)
                for _, row in top_factors.iterrows():
                    st.write(f"- {row['feature']} (Impact: {row['importance']:.3f})")
                
        except Exception as e:
            st.error(f"Prediction error: {e}")
            st.error("Please check the console for detailed error information")

# 2- Batch Prediction Page  
elif page == "Batch Prediction":
    st.header("2- Batch Prediction")
    st.write("Upload a CSV file with multiple customer records for batch churn prediction")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            # Read and display data
            batch_data = pd.read_csv(uploaded_file)
            st.write("**Uploaded Data Preview:**")
            st.dataframe(batch_data.head())
            
            if st.button("Predict Batch Churn", type="primary"):
                st.info("Batch prediction functionality would be implemented here")
                st.write("This would process all records and provide churn probabilities")
                
        except Exception as e:
            st.error(f"Error reading file: {e}")

# 3- Retention Insights Page
elif page == "Retention Insights":
    st.header("Retention Strategy Insights")
    
    st.subheader("Top Churn Drivers")
    st.dataframe(feature_importance.head(10).sort_values('importance', ascending=False))
    
    st.subheader("Data-Backed Retention Strategies")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("""
        **Immediate Actions (High-Risk Customers)**
        
        • **Personalized Outreach**: Contact customers with >70% churn probability
        • **Contract Incentives**: Offer discounts for switching to annual contracts  
        • **Payment Method Optimization**: Encourage automatic payment methods
        • **Service Bundles**: Create customized service packages
        
        **Service Improvements**
        
        • **Fiber Optic Enhancement**: Address service issues for fiber customers
        • **Tech Support Priority**: Expedited support for high-risk segments
        • **Security Features**: Promote online security package benefits
        """)
    
    with col2:
        st.write("""
        **Preventive Measures (All Customers)**
        
        • **Tenure Rewards**: Loyalty programs for long-term customers
        • **Proactive Monitoring**: Early warning system for at-risk behaviors
        • **Customer Education**: Resources on service optimization
        • **Regular Check-ins**: Quarterly satisfaction surveys
        
        **Financial Strategies**
        
        • **Flexible Billing**: Payment plan options for financial hardship
        • **Bundle Discounts**: Reduced rates for multiple services
        • **Loyalty Pricing**: Special rates for customers >24 months
        """)
    
    st.subheader("Implementation Plan")
    st.write("""
    1. **Week 1-2**: Identify top 10% high-risk customers
    2. **Week 3-4**: Deploy personalized retention offers  
    3. **Month 2**: Implement service improvement initiatives
    4. **Month 3**: Launch preventive programs for medium-risk segment
    5. **Ongoing**: Monitor effectiveness and adjust strategies
    """)