import json
import os
from simulation.complete_journey import CompleteJourney

def main():
    # Set a dummy API key for simulation purposes
    os.environ["OPENAI_API_KEY"] = "dummy_key"
    """
    Main function to run the complete journey simulation.
    """
    print("🎬 Starting Complete Journey Simulation...")

    # A chronological list of main messages from the user
    rohan_messages = [
        "I'm ready to start my health journey. What's the first step?",
        "I've completed the onboarding. What's next?",
        "I'm feeling a bit tired this week. Any suggestions?",
        "How can I improve my sleep quality?",
        "I'm traveling for work next week. How should I adjust my routine?",
        "I'm back from my trip. Let's get back on track.",
        "What are some healthy snack options?",
        "I'm feeling stressed from work. Any tips to manage stress?",
        "I've been consistent with my workouts. What's the next level?",
        "How can I optimize my diet for better energy levels?",
        "I'm having trouble with my knee. Should I see a specialist?",
        "My knee is feeling better now. Thanks for the advice.",
        "I'm going on vacation next month. How can I stay healthy?",
        "I'm back from vacation. Let's review my progress.",
        "I'm feeling great! What's the plan for the next few months?",
    ]

    # Initialize the CompleteJourney with the user's messages
    complete_journey = CompleteJourney(messages=rohan_messages, num_months=8)

    # Run the simulation
    results = complete_journey.run()

    # Print the results in a structured format
    print("\n\n--- Simulation Results ---")
    print("\n--- Conversation History ---")
    print(json.dumps(results["conversation_history"], indent=2))

    print("\n--- Journey Data ---")
    print(json.dumps(results["journey_data"], indent=2))

    print("\n🎉 Simulation Finished!")

if __name__ == "__main__":
    main()
