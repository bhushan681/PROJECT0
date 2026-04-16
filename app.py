import google.generativeai as genai
import streamlit as st

# --- 1. CONFIGURATION ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("Missing API Key in Secrets!")

# --- 2. UI SETUP ---
st.set_page_config(page_title="ELI5 Decipherer", page_icon="👶")
st.title("👶 ELI: Complexity Decipherer")

# NEW: Difficulty Slider
level = st.select_slider(
    "Select Complexity Level:",
    options=["Child", "Student", "Expert"],
    value="Child"
)

user_topic = st.text_input("Enter a complex topic:", placeholder="e.g. Backpropagation, Black Holes...")

if st.button("Decipher Topic", type="primary"):
    if user_topic:
        with st.spinner(f"Explaining for a {level}..."):
            try:
                # Dynamic Prompt based on selection
                prompts = {
                    "Child": f"Explain {user_topic} to a 5-year-old using a simple analogy. No big words.",
                    "Student": f"Explain {user_topic} to a college student. Use technical terms but explain them clearly with examples.",
                    "Expert": f"Provide a high-level, technical summary of {user_topic} for a researcher. Focus on core mechanics and efficiency."
                }

                # Model selection logic (keeping our "bulletproof" version)
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                selected_model = next((m for m in available_models if '1.5-flash' in m), available_models[0])
                
                model = genai.GenerativeModel(selected_model)
                response = model.generate_content(prompts[level])
                
                st.subheader(f"Level: {level}")
                st.success(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a topic first!")

st.divider()
st.markdown("**Developed by:** Fuled by caffien | Vishwanova Hackathon 🚀")
