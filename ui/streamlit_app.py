import os
import streamlit as st
import plotly.graph_objects as go
from simulation.journey_orchestrator import JourneyOrchestrator
from data.persistence import PersistenceManager


def main():
    st.set_page_config(page_title="Elyx Healthcare Journey", layout="wide")

    st.title("🏥 Elyx Healthcare Journey - Rohan Patel Simulation")

    st.sidebar.header("Control Panel")
    # Live LLM controls
    live_mode = st.sidebar.toggle("Use live LLM (OpenRouter)", value=os.getenv("USE_MOCK_RESPONSES", "1") not in {"1", "true", "True"})
    model_default = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-exp:free")
    model_input = st.sidebar.text_input("Model ID", value=model_default, help="e.g., google/gemini-2.0-flash-exp:free")
    if model_input:
        os.environ["OPENROUTER_MODEL"] = model_input
    os.environ["USE_MOCK_RESPONSES"] = "0" if live_mode else "1"
    api_key_present = bool(os.getenv("OPENROUTER_API_KEY"))
    if live_mode and not api_key_present:
        st.sidebar.error("OPENROUTER_API_KEY not set. Using mock responses.")
        os.environ["USE_MOCK_RESPONSES"] = "1"

    st.sidebar.write(":small_blue_diamond: Mode: {}".format("Live" if os.environ.get("USE_MOCK_RESPONSES") in {"0", "false", "False"} else "Mock"))
    st.sidebar.write(":small_blue_diamond: Model: {}".format(os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-exp:free")))

    st.sidebar.divider()
    if st.sidebar.button("Reset Chat History"):
        reset_chat_history()

    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat Interface", "📊 Analytics", "📋 Journey Timeline", "🔍 Agent Monitoring"])  # noqa: E501

    with tab1:
        render_chat_interface()

    with tab2:
        render_analytics()

    with tab3:
        render_timeline()

    with tab4:
        render_agent_monitoring()


def render_chat_interface():
    st.header("Real-time Chat with Elyx Agents")

    if "chat_system" not in st.session_state:
        from agents.group_chat import GroupChatSystem

        st.session_state.chat_system = GroupChatSystem()

    persistence = PersistenceManager()
    history = persistence.load_conversation_history()

    chat_container = st.container()
    with chat_container:
        for message in history[-20:]:
            if message["sender"] == "Rohan":
                st.write(f"🧑‍💼 **{message['sender']}**: {message['message']}")
            else:
                st.write(f"👩‍⚕️ **{message['sender']}**: {message['message']}")

    user_input = st.text_input("Send message as Rohan:", placeholder="Type your message here...")
    if st.button("Send"):
        if user_input:
            st.session_state.chat_system.send_message("Rohan", user_input)
            persistence.save_conversation_history(st.session_state.chat_system.conversation_history)
            st.rerun()


def render_analytics():
    st.header("Health Analytics Dashboard")

    weeks = list(range(1, 35))
    blood_sugar = [max(120, 180 - (week * 2)) for week in weeks]
    a1c_values = [max(5.5, 6.2 - (week * 0.02)) for week in weeks]

    col1, col2 = st.columns(2)

    with col1:
        fig_bs = go.Figure()
        fig_bs.add_trace(go.Scatter(x=weeks, y=blood_sugar, name="Blood Sugar"))
        fig_bs.update_layout(title="Blood Sugar Trend Over 8 Months")
        st.plotly_chart(fig_bs, use_container_width=True)

    with col2:
        fig_a1c = go.Figure()
        fig_a1c.add_trace(go.Scatter(x=weeks, y=a1c_values, name="A1C"))
        fig_a1c.update_layout(title="A1C Improvement Over Time")
        st.plotly_chart(fig_a1c, use_container_width=True)


def render_timeline():
    st.header("8-Month Journey Timeline")
    timeline_events = [
        {"week": 1, "event": "Onboarding & Initial Test", "type": "milestone"},
        {"week": 10, "event": "Leg Injury", "type": "incident"},
        {"week": 12, "event": "Second Test - Blood Sugar Better", "type": "milestone"},
        {"week": 24, "event": "Third Test - Overall Better", "type": "milestone"},
        {"week": 34, "event": "Journey Complete", "type": "milestone"},
    ]
    for event in timeline_events:
        if event["type"] == "milestone":
            st.success(f"**Week {event['week']}**: {event['event']}")
        else:
            st.warning(f"**Week {event['week']}**: {event['event']}")


def render_agent_monitoring():
    st.header("Agent Performance Monitoring")
    agent_metrics = {
        "Ruby": {"response_time": "2.3s", "interactions": 156, "satisfaction": "94%"},
        "Dr. Warren": {"response_time": "3.1s", "interactions": 89, "satisfaction": "97%"},
        "Carla": {"response_time": "2.8s", "interactions": 134, "satisfaction": "91%"},
        "Advik": {"response_time": "2.5s", "interactions": 112, "satisfaction": "93%"},
        "Rachel": {"response_time": "2.9s", "interactions": 67, "satisfaction": "96%"},
        "Neel": {"response_time": "3.4s", "interactions": 45, "satisfaction": "98%"},
    }
    for agent, metrics in agent_metrics.items():
        with st.expander(f"👩‍⚕️ {agent} - {metrics['satisfaction']} Satisfaction"):
            col1, col2, col3 = st.columns(3)
            col1.metric("Response Time", metrics["response_time"])
            col2.metric("Interactions", metrics["interactions"])
            col3.metric("Satisfaction", metrics["satisfaction"])


def start_new_journey():
    orchestrator = JourneyOrchestrator()
    with st.spinner("Starting new journey simulation..."):
        orchestrator.run_full_journey()
    st.success("Journey simulation completed!")


def continue_journey():
    st.info("Continuing from saved state...")


def reset_chat_history():
    pm = PersistenceManager()
    pm.save_conversation_history([])
    if "chat_system" in st.session_state:
        st.session_state.chat_system.conversation_history = []
    st.success("Chat history reset.")


if __name__ == "__main__":
    main()


