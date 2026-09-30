import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="HealthPulse AI", page_icon="🩺", layout="centered")

st.title("🩺 HealthPulse AI")
st.subheader("Community Health & First-Line Wellness Assistant")
st.caption("Track 3: Smart Health & Supply Chain Resilience")

# Sidebar for API Key & Configuration
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter your Gemini API Key", type="password")
    st.info("Get a free key from Google AI Studio (aistudio.google.com).")
    st.markdown("---")
    st.markdown("**Disclaimer:** This tool provides general guidance and is not a substitute for professional medical care.")

# User Inputs
st.write("### Describe Your Concern")
user_input = st.text_area(
    "Enter your symptoms, health questions, or current stress levels:",
    placeholder="e.g., I've had a persistent dry cough and mild fever for two days, feeling fatigued..."
)

urgency = st.select_slider(
    "How severe does your discomfort feel right now?",
    options=["Mild", "Moderate", "Significant", "Severe"]
)

# AI Analysis
if st.button("Analyze & Get Guidance", type="primary"):
    if not api_key:
        st.error("Please provide a Gemini API Key in the sidebar to proceed.")
    elif not user_input.strip():
        st.warning("Please enter your symptoms or health query first.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-pro")

            system_prompt = f"""
            You are HealthPulse, an empathetic, certified first-line healthcare triage assistant.
            A user reports the following concern:
            "{user_input}"
            Perceived severity: {urgency}

            Provide a clear, structured response with:
            1. **Potential Explanations**: Common benign causes (state clearly this is not a diagnosis).
            2. **Immediate Home Care / Self-Care Steps**: Practical, safe comfort measures.
            3. **Red Flags & Warning Signs**: Specific symptoms that mean they should visit an emergency clinic immediately.
            4. **Relevant Questions for a Doctor**: What questions they should bring to their healthcare provider.
            Keep the tone calm, structured, and easy to read.
            """

            with st.spinner("Analyzing guidance..."):
                response = model.generate_content(system_prompt)
                st.success("Analysis Complete")
                st.markdown(response.text)

        except Exception as e:
            st.error(f"Error communicating with Gemini: {e}")
