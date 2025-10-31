import boto3
import json
import streamlit as st

region = 'us-east-1'
# Initialize Bedrock client
bedrock_client = boto3.client(
    service_name='bedrock-runtime', 
    region_name=region)

modelId = 'amazon.titan-text-express-v1'
accept = 'application/json'
contentType = 'application/json'

# --- Streamlit UI ---
st.set_page_config(page_title="Ask titan", page_icon="🤖")
st.title("Ask titan (via Amazon Bedrock)")
user_input = st.text_area("Enter your question:", placeholder="e.g., Explain quantum computing")
submit = st.button("Ask")

if submit and user_input.strip():
    with st.spinner("Thinking..."):
        body = {
                "inputText":  user_input,
                "textGenerationConfig": {
                "temperature": 0.6,
                "topP": 0.9,
            } # required version header
                
        }

        # Convert the body to json
        request_body = json.dumps(body)

        # Invoke the Claude model
        response = bedrock_client.invoke_model(
        body=request_body, # This accepts json string
        modelId=modelId, 
        accept=accept, 
        contentType=contentType)

        # Parse the response body
        resp_body = json.loads(response["body"].read())

        # Extract the assistant’s text reply
        answer = (resp_body["results"][0]["outputText"])
        st.markdown("### 💬 Titan's Response")
        st.write(answer)