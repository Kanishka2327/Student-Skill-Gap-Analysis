import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Hugging Face API Key (Replace with yours)
HF_API_KEY = "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"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

# Load dataset dynamically
file_path = r"C:\Users\Hp\Downloads\DMA_DATASET_Indian_Names.csv"
df = pd.read_csv(file_path)

# Store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to get chatbot response
def chatbot_response(prompt):
    url = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
    data = {"inputs": f"Provide a clear, structured response without repeating the question: {prompt}"}

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            response_json = response.json()

            if isinstance(response_json, list) and response_json:
                raw_text = response_json[0].get("generated_text", "").strip()
            else:
                raw_text = response_json.get("generated_text", "").strip()

            cleaned_text = raw_text.replace(prompt, "").strip()
            formatted_text = cleaned_text.replace(". ", ".\n\n")  

            return formatted_text if formatted_text else "⚠️ No meaningful response generated. Try rephrasing."
        else:
            return f"⚠️ AI service unavailable (Error {response.status_code}). Please try again later."

    except Exception as e:
        return f"⚠️ An error occurred: {str(e)}"

# Apply Custom Neon Sidebar Styling
st.sidebar.markdown(
    """
    <style>
        .sidebar-box {
            background-color: #111;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #0FF;
            box-shadow: 0px 0px 10px #0FF;
            text-align: center;
        }
        .sidebar-box h2 {
            color: #00FFFF;
            text-shadow: 0px 0px 5px #00FFFF, 0px 0px 10px #00FFFF;
        }
        .stTextInput input {
            border: 2px solid #FF00FF !important;
            background-color: black !important;
            color: white !important;
        }
    </style>
    <div class="sidebar-box">
        <h2>📌 Navigation</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar Navigation
page = st.sidebar.radio("Go to", ["Home", "Skill Analysis", "Internship Listings", "Career Chatbot", "Challenges & Support"])

# 📊 Skill Analysis Page
if page == "Skill Analysis":
    st.title("📊 Skill Analysis & Tech Trends")

    # Display top technical skills
    st.subheader("🔥 Top Technical Skills")
    top_skills = df["technical_skills"].value_counts().head(10)
    st.bar_chart(top_skills)

    # *🔵 Updated Pie Chart for Skill Distribution*
    st.subheader("🎯 Skill Distribution")

    # Split multi-skill entries into separate skills
    all_skills = df["technical_skills"].dropna().str.split(", ").explode()

    # Count occurrences of each individual skill
    skill_counts = all_skills.value_counts()

    # Take the top 6 most frequent skills
    top_skills = skill_counts.head(6)

    # Calculate percentage for each skill
    top_skills_percentage = (top_skills / top_skills.sum()) * 100  

    # Plot pie chart
    fig, ax = plt.subplots()
    ax.pie(top_skills_percentage, labels=top_skills.index, autopct='%1.1f%%', 
           colors=sns.color_palette("coolwarm", len(top_skills)))
    ax.set_title("Distribution of Technical Skills")
    st.pyplot(fig)

    # Trending Tech Stacks
    tech_trends = pd.DataFrame({
        "Technology": ["AI", "Cloud Computing", "Cybersecurity", "Blockchain", "Data Science", "Web Development"],
        "Popularity": [90, 85, 80, 75, 95, 88]
    })
    st.subheader("📈 Trending Tech Stacks")
    fig, ax = plt.subplots()
    sns.barplot(x="Technology", y="Popularity", data=tech_trends, palette="coolwarm", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# 🏠 Home Page
elif page == "Home":
    st.title("🏠 Welcome to Your Dashboard")
    st.write("Explore the latest trends and skills in the tech world.")

    selected_user = st.selectbox("Select a user to view details:", df["name"].tolist())
    user_details = df[df["name"] == selected_user].iloc[0]

    st.write(f"📌 *Name:* {user_details['name']}")
    st.write(f"📚 *Current Course:* {user_details['current_course']}")
    st.write(f"🛠 *Technical Skills:* {user_details['technical_skills']}")
    st.write(f"💡 *Career Aspiration:* {user_details['job_role_aspiration']}")
    st.write(f"🔍 *Challenges Faced:* {user_details['challenges_faced']}")
    st.write(f"📖 *Preferred Learning Method:* {user_details['preferred_learning_method']}")

# 💼 Internship Listings
elif page == "Internship Listings":
    st.title("💼 Internship Opportunities")
    internships = [
        "🔹 Google India - Software Engineer Intern ([Apply](https://careers.google.com))",
        "🔹 TCS - Data Analyst Intern ([Apply](https://www.tcs.com/careers))",
        "🔹 Infosys - Cloud Engineer Intern ([Apply](https://careers.infosys.com))",
    ]
    st.subheader("📢 Latest Openings")
    for internship in internships:
        st.markdown(internship)

# 🤖 AI Career Chatbot with Chat History
elif page == "Career Chatbot":
    st.title("🤖 AI Career Chatbot")
    st.write("💡 *Ask your career-related questions!*")

    user_input = st.text_input("Ask me anything:")

    if user_input:
        with st.spinner("Thinking... 🤔"):
            response = chatbot_response(user_input)

        # Store in chat history
        st.session_state.chat_history.append(f"*You:* {user_input}")
        st.session_state.chat_history.append(f"*AI:* {response}")

    # Display chat history
    for chat in st.session_state.chat_history:
        st.markdown(chat)

# ⚡ Challenges & Support Page
elif page == "Challenges & Support":
    st.title("⚡ Challenges & Support System")
    st.subheader("📢 Frequently Asked Questions (FAQs)")
    faqs = [
        "✅ *How can I improve my resume?* - Use templates from [Zety](https://zety.com/resume-builder).",
        "✅ *Where can I find free coding courses?* - Explore [Harvard CS50](https://cs50.harvard.edu/).",
        "✅ *How do I prepare for technical interviews?* - Use [GeeksforGeeks](https://www.geeksforgeeks.org/) for coding questions."
    ]
    for faq in faqs:
        st.markdown(faq)

    st.subheader("📞 Contact Us")
    st.write("📧 *Email:* support@skillgapanalysis.com")
    st.write("📞 *Phone:* +91 9876543210")