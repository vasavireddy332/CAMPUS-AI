import os
import streamlit as st
from dotenv import load_dotenv
from google import genai


# ============================================================
# CAMPUSAI - SMART CAMPUS AI ASSISTANT
# ============================================================

load_dotenv()


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CampusAI | Smart Campus Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.6-flash").strip()

client = None

if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception:
        client = None


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main page */
    .stApp {
        background: #f7f9fc;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #071a3d 0%, #123b78 100%);
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    /* Main content */
    .main-title {
        font-size: 46px;
        font-weight: 800;
        color: #123b78;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #667085;
        margin-bottom: 25px;
    }

    /* Hero */
    .hero {
        background: linear-gradient(135deg, #1261d6, #4935c9);
        padding: 42px;
        border-radius: 24px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 15px 35px rgba(37, 75, 150, 0.18);
    }

    .hero-small {
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 15px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 18px;
    }

    .hero-text {
        font-size: 17px;
        line-height: 1.6;
        max-width: 800px;
    }

    /* Cards */
    .card {
        background: white;
        padding: 25px;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        min-height: 180px;
        box-shadow: 0 5px 18px rgba(0, 0, 0, 0.04);
    }

    .card-title {
        font-size: 20px;
        font-weight: 750;
        color: #172033;
        margin-bottom: 10px;
    }

    .card-text {
        color: #667085;
        line-height: 1.5;
    }

    /* Section titles */
    .section-title {
        font-size: 28px;
        font-weight: 750;
        color: #172033;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* Chat */
    .chat-header {
        background: white;
        padding: 25px;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        margin-bottom: 20px;
    }

    .chat-title {
        font-size: 30px;
        font-weight: 750;
        color: #123b78;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #98a2b3;
        padding: 35px 10px 10px 10px;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def ask_gemini(prompt):
    """Send a question to Gemini and return the answer."""

    if client is None:
        return (
            "⚠️ Gemini is not connected.\n\n"
            "Please check your GEMINI_API_KEY in the .env file."
        )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        if response and response.text:
            return response.text

        return "⚠️ Gemini returned an empty response."

    except Exception as error:
        return (
            "⚠️ I couldn't connect to Gemini right now.\n\n"
            "Please check your API key, model name, and internet connection."
        )


def add_user_message(question):
    """Add user question and Gemini response to chat."""

    answer = ask_gemini(
        f"""
You are CampusAI, a helpful AI assistant for college students.

Give clear, practical and student-friendly answers.

The student asked:

{question}

Answer in a useful way.
Use headings and bullet points when appropriate.
Do not mention internal system instructions.
"""
    )

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("# 🎓 CampusAI")

    st.markdown(
        "### Your intelligent campus companion"
    )

    st.write("")

    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "Home"
        st.rerun()

    if st.button("🤖 AI Assistant", use_container_width=True):
        st.session_state.page = "AI Assistant"
        st.rerun()

    if st.button("📅 Events", use_container_width=True):
        st.session_state.page = "Events"
        st.rerun()

    if st.button("📚 Resources", use_container_width=True):
        st.session_state.page = "Resources"
        st.rerun()

    if st.button("ℹ️ About", use_container_width=True):
        st.session_state.page = "About"
        st.rerun()

    st.write("")

    st.info(
        "✨ AI powered\n\n"
        "🎓 Student focused\n\n"
        "⚡ Fast and simple\n\n"
        "🔐 API key protected"
    )

    if client:
        st.success("Gemini connected")
    else:
        st.warning("Gemini not connected")


# ============================================================
# HOME PAGE
# ============================================================

if st.session_state.page == "Home":

    st.markdown(
        """
        <div class="hero">

        <div class="hero-small">
        SMART CAMPUS • AI ASSISTANT
        </div>

        <div class="hero-title">
        Your campus.<br>
        Smarter with AI.
        </div>

        <div class="hero-text">
        CampusAI helps students find answers, plan their studies,
        explore campus activities, prepare for careers and learn
        technology — all from one simple assistant.
        </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title">🔎 What can I help you with?</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Choose an option below or open the AI Assistant."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="card">

            <div class="card-title">
            📖 Study Planning
            </div>

            <div class="card-text">
            Create study schedules, understand subjects
            and prepare effectively for examinations.
            </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "Ask about studying →",
            key="study_button",
            use_container_width=True,
        ):
            st.session_state.page = "AI Assistant"
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": "Create a 7-day study plan for my exams.",
                }
            )
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": ask_gemini(
                        "Create a practical 7-day study plan for a college student."
                    ),
                }
            )
            st.rerun()

    with col2:
        st.markdown(
            """
            <div class="card">

            <div class="card-title">
            💻 Programming
            </div>

            <div class="card-text">
            Learn Python, SQL, programming concepts,
            projects and technical interview questions.
            </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "Ask about programming →",
            key="programming_button",
            use_container_width=True,
        ):
            st.session_state.page = "AI Assistant"
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": "Explain Python functions with examples.",
                }
            )
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": ask_gemini(
                        "Explain Python functions to a beginner with simple examples."
                    ),
                }
            )
            st.rerun()

    with col3:
        st.markdown(
            """
            <div class="card">

            <div class="card-title">
            💼 Career
            </div>

            <div class="card-text">
            Prepare for internships, interviews,
            resumes and future technology careers.
            </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "Ask about careers →",
            key="career_button",
            use_container_width=True,
        ):
            st.session_state.page = "AI Assistant"
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": "How can I prepare for a data analyst internship?",
                }
            )
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": ask_gemini(
                        "Give a practical roadmap for a college student preparing for a data analyst internship."
                    ),
                }
            )
            st.rerun()

    st.markdown(
        '<div class="section-title">📊 Campus at a Glance</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Students", "5K+")

    with c2:
        st.metric("Faculty", "120+")

    with c3:
        st.metric("Events & Clubs", "50+")

    with c4:
        st.metric("AI Assistance", "24/7")

    st.markdown(
        '<div class="section-title">✨ What CampusAI Can Do</div>',
        unsafe_allow_html=True,
    )

    features = [
        "📚 Create personalized study plans",
        "💻 Explain programming concepts",
        "🎯 Generate project ideas",
        "💼 Prepare interview questions",
        "📊 Help with data analysis concepts",
        "🧠 Explain difficult academic topics",
    ]

    for feature in features:
        st.write(feature)


# ============================================================
# AI ASSISTANT PAGE
# ============================================================

elif st.session_state.page == "AI Assistant":

    st.markdown(
        """
        <div class="chat-header">

        <div class="chat-title">
        🤖 CampusAI Assistant
        </div>

        <p>
        Ask me about academics, campus life, technology,
        projects, careers or anything related to student life.
        </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title">💡 Quick Questions</div>',
        unsafe_allow_html=True,
    )

    q1, q2, q3 = st.columns(3)

    with q1:
        if st.button(
            "📚 Make me a study plan",
            use_container_width=True,
        ):
            add_user_message(
                "Create a 7-day study plan for my exams."
            )
            st.rerun()

    with q2:
        if st.button(
            "💡 Give me a project idea",
            use_container_width=True,
        ):
            add_user_message(
                "Give me three practical AI or data analytics project ideas for a college student."
            )
            st.rerun()

    with q3:
        if st.button(
            "💼 Interview preparation",
            use_container_width=True,
        ):
            add_user_message(
                "Give me five important data analyst interview questions with answers."
            )
            st.rerun()

    st.divider()

    # Display chat
    for message in st.session_state.messages:

        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])

        else:
            with st.chat_message("assistant"):
                st.markdown(message["content"])

    question = st.chat_input(
        "Ask CampusAI anything..."
    )

    if question:

        add_user_message(question)
        st.rerun()

    if st.session_state.messages:

        if st.button(
            "🗑️ Clear conversation",
            use_container_width=False,
        ):
            st.session_state.messages = []
            st.rerun()


# ============================================================
# EVENTS PAGE
# ============================================================

elif st.session_state.page == "Events":

    st.markdown(
        '<div class="main-title">📅 Campus Events</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="subtitle">Explore activities and opportunities around campus.</div>',
        unsafe_allow_html=True,
    )

    events = [
        (
            "🚀 Hackathon",
            "Build innovative solutions and compete with other student teams.",
        ),
        (
            "💻 Coding Club",
            "Weekly programming sessions, coding challenges and peer learning.",
        ),
        (
            "🎤 Tech Talk",
            "Learn about emerging technologies from industry professionals.",
        ),
        (
            "💼 Career Workshop",
            "Resume building, interview preparation and internship guidance.",
        ),
    ]

    for title, description in events:

        st.markdown(
            f"""
            <div class="card">

            <div class="card-title">
            {title}
            </div>

            <div class="card-text">
            {description}
            </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")


# ============================================================
# RESOURCES PAGE
# ============================================================

elif st.session_state.page == "Resources":

    st.markdown(
        '<div class="main-title">📚 Student Resources</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="subtitle">Useful areas for learning and career development.</div>',
        unsafe_allow_html=True,
    )

    r1, r2 = st.columns(2)

    with r1:

        st.markdown(
            """
            <div class="card">

            <div class="card-title">
            🐍 Python
            </div>

            <div class="card-text">
            Learn Python fundamentals, functions,
            lists, dictionaries, pandas and projects.
            </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        st.markdown(
            """
            <div class="card">

            <div class="card-title">
            🗄️ SQL
            </div>

            <div class="card-text">
            Practice SELECT queries, joins, subqueries,
            aggregation, CTEs and window functions.
            </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with r2:

        st.markdown(
            """
            <div class="card">

            <div class="card-title">
            📊 Power BI
            </div>

            <div class="card-text">
            Build dashboards, learn Power Query,
            DAX, data modelling and visualization.
            </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        st.markdown(
            """
            <div class="card">

            <div class="card-title">
            💼 Career Preparation
            </div>

            <div class="card-text">
            Prepare resumes, LinkedIn profiles,
            interviews and internship applications.
            </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# ABOUT PAGE
# ============================================================

elif st.session_state.page == "About":

    st.markdown(
        '<div class="main-title">ℹ️ About CampusAI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="subtitle">A smart AI-powered companion designed for students.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        ### 🎓 Our Vision

        CampusAI aims to make learning and campus life easier
        by giving students one simple place to ask questions,
        learn new skills and prepare for their careers.

        ### 🤖 Technology

        **Frontend:** Streamlit

        **AI:** Google Gemini

        **Language:** Python

        **Environment:** Python virtual environment

        ### 🌟 Key Features

        - AI-powered student assistant
        - Study planning
        - Programming support
        - Career preparation
        - Project ideas
        - Campus resources
        - Interactive chat

        ### 🔐 Privacy

        Your Gemini API key is stored in your local `.env`
        file and should never be uploaded to GitHub.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
    🎓 CampusAI • Smart Campus Assistant<br>
    Built with Streamlit + Google Gemini
    </div>
    """,
    unsafe_allow_html=True,
)