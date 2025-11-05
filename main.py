import streamlit as st
import datetime
import google.genai as genai
import os
from dotenv import load_dotenv

# ---------------------------
# LOAD .env
# ---------------------------
load_dotenv()
API_KEY = os.getenv("GENAI_API_KEY")
client = None
if API_KEY:
    client = genai.Client(api_key=API_KEY)

# ---------------------------
# PAGE TITLE
# ---------------------------
st.title("🌍 Trip With Friend - AI Travel Planner ✈️")

st.sidebar.header("🧭 Quick Options")
st.sidebar.info(
    """
    💡 *Plan your dream trip in seconds!*  
    - Enter your starting city 🏙️  
    - Add destinations 🌆  
    - Choose your budget 💰  
    - Pick a travel style 🎒  
    """
)
st.sidebar.success("✨ Powered by Gemini AI")

# ---------------------------
# MAIN FORM
# ---------------------------
with st.form("travel_form"):
    st.subheader("🧳 Trip Details")
    starting_point = st.text_input("📍 Starting Point (City, Country)", placeholder="e.g., Karachi")
    destinations = st.text_input("🗺️ Destination(s) (comma separated)", placeholder="e.g., Paris, Tokyo, Lahore")
    starting_date = st.date_input("🗓️ Starting Date", min_value=datetime.date.today())
    ending_date = st.date_input("📅 Ending Date", min_value=starting_date)
    num_travelers = st.number_input("👨‍👩‍👧 Number of Travelers", min_value=1, value=1)
    currency = st.selectbox("💱 Preferred Currency", options=["USD", "EUR", "GBP", "PKR", "INR", "JPY"])
    budget = st.number_input("💰 Budget")
    trip_type = st.selectbox("🎯 Trip Type", options=["Leisure", "Adventure", "Cultural", "Romantic", "Family", "Solo"])
    
    submit_btn = st.form_submit_button("🚀 Plan My Trip")

# ---------------------------
# RESPONSE
# ---------------------------
if submit_btn:
    if not all([starting_point, destinations, starting_date, ending_date, currency, budget, trip_type]):
        st.error("⚠️ Please fill in all the fields before continuing!")
    else:
        with st.spinner("🧠 Planning your trip... This may take a few seconds ⏳"):
            prompt = f"""
            Create a detailed daily travel itinerary with the following information:
            
            Starting From: {starting_point}
            Destinations to visit: {destinations}
            Trip Duration: {starting_date} to {ending_date}
            Number of Travelers: {num_travelers}
            Budget: {budget} {currency}
            Travel Style: {trip_type}
            
            Please provide a day-by-day itinerary including:
            1. Transportation options between destinations
            2. Recommended accommodations
            3. Key attractions and activities
            4. Estimated costs for each major activity
            5. Local cuisine recommendations
            6. Any practical travel tips
            
            Format the response clearly with a separate section for each day.
            """
            response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            st.success("🎉 Your AI-generated travel plan is ready!")
            st.write(response.text)
