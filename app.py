import pandas as pd
import numpy as np
import streamlit as st
import tensorflow as tf
from sklearn.preprocessing import StandardScaler,LabelBinarizer,OneHotEncoder
import pickle

model=tf.keras.models.load_model('model.h5')

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)
with open('encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)
with open('geo_encoder.pkl', 'rb') as f:
    geo_encoder = pickle.load(f)

st.title('Customer Churn Prediction')

geography = st.selectbox('Geography', geo_encoder.categories_[0])
gender=st.selectbox('Gender',encoder.classes_)
age=st.slider('Age', 18, 92)
balance=st.number_input('Balance')
credit_score=st.number_input('Credit Score')
estimated_salary=st.number_input('Estimated Salary')
tenure=st.slider('Tenure', 0, 10)
num_of_products=st.slider('Number of Products', 1, 4)
has_cr_card=st.selectbox('Has Credit Card', [0,1])
is_active_member=st.selectbox('Is Active Member', [0,1])

input_data={
    'CreditScore': [credit_score],
    'Gender':[encoder.transform([gender])[0]],
    'Age': [age],
    'Tenure': [tenure],
    'Balance': [balance],
    'NumOfProducts': [num_of_products],
     'HasCrCard': [has_cr_card],
     'IsActiveMember': [is_active_member],
     'EstimatedSalary': [estimated_salary],
}

geo_encoded=geo_encoder.transform([[geography]]).toarray()
geo_encoded_df=pd.DataFrame(geo_encoded,columns=geo_encoder.get_feature_names_out(['Geography']))

input_df = pd.DataFrame(input_data)
input_df = pd.concat([input_df.reset_index(drop=True), geo_encoded_df], axis=1)


input_data_scaled = scaler.transform(input_df)


prediction=model.predict(input_data_scaled)
prediction_prob=prediction[0][0]

if prediction_prob>0.5:
    st.write('Customer is likely to churn')
else:
    st.write('Customer is not likely to churn') 