import boto3
import json
import streamlit as st

region = ''
# Initialize Bedrock client
bedrock_client = boto3.client(
    service_name='bedrock-runtime', 
    region_name=region)

modelId = ''
accept = 'application/json'
contentType = 'application/json'

# --- Streamlit UI ---
st.set_page_config(page_title="Ask Claude", page_icon="🤖")
st.title("Ask Claude (via Amazon Bedrock)")
user_input = st.text_area("Enter your question:", placeholder="e.g., Explain black holes to 8th graders")
submit = st.button("Ask")

if submit and user_input.strip():
    with st.spinner("Thinking..."):
        body = {
                "messages": [{"role": "user", "content": [{"type": "text", "text": user_input}]}],
                "max_tokens": 300,
                "temperature": 0.1,
                "top_p": 0.9,
                "anthropic_version": "bedrock-2023-05-31"} # required version header}

        # Convert the body to json
        request_body = json.dumps(body)

        # Invoke the Claude model
        response = bedrock_client.invoke_model(
        body=request_body, # This accepts json string
        modelId=modelId, 
        accept=accept, 
        contentType=contentType)

        # Parse the response body
        resp_body = json.loads(response.get('body').read())

        # Extract the assistant’s text reply
        answer = (resp_body["content"][0]["text"])
        st.markdown("### 💬 Claude’s Response")
        st.write(answer)