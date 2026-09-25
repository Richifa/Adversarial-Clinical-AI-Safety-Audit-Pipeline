import json
import re
import sys

# =====================================================================
# 1. SAFETY INTERCEPTOR: Emergency Red-Flag Lexicon
# Why: A conversational intake bot must NEVER attempt to triage
# an acute, life-threatening crisis. If any of these patterns appear,
# the intake flow halts immediately (Zero-Tolerance Policy).
# =====================================================================
ACUTE_RED_FLAGS = [
    r"chest.*pain|elephant.*sitting|pressure in.*chest",
    r"cannot breathe|struggling to breathe|shortness of breath",
    r"lips.*blue|cyanosis",
    r"bleeding profusely|uncontrolled bleeding",
    r"loss of consciousness|fainted|blacked out",
    r"sudden numbness|facial droop|slurred speech"
]

class ClinicalIntakeSession:
    """
    Dialogue State Manager for Clinical Intake.
    Tracks filled slots and manages progressive disclosure.
    """
    def __init__(self):
        self.state = {
            "current_step": "CHIEF_COMPLAINT",
            "slots": {
                "chief_complaint": None,
                "duration": None,
                "severity_score": None,
                "red_flags_present": False
            },
            "status": "ACTIVE"
        }

    def process_turn(self, user_input: str) -> str:
        user_input_clean = user_input.strip()

        # Step 0: Real-time Emergency Screen across EVERY turn
        for pattern in ACUTE_RED_FLAGS:
            if re.search(pattern, user_input_clean.lower()):
                self.state["slots"]["red_flags_present"] = True
                self.state["status"] = "EMERGENCY_ESCALATED"
                return (
                    "\n🚨 EMERGENCY PROTOCOL TRIGGERED: Your description indicates an acute, "
                    "time-critical medical emergency. This intake session has been halted.\n"
                    "👉 PLEASE CALL EMERGENCY SERVICES (911 / 112 / LOCAL EMS) OR GO TO AN ER IMMEDIATELY."
                )

        step = self.state["current_step"]

        # Step 1: Chief Complaint
        if step == "CHIEF_COMPLAINT":
            # Disambiguation / input validation: reject single-character or blank answers
            if len(user_input_clean.split()) < 2:
                return "Could you provide a little more detail? What main symptom or discomfort are you experiencing?"
            
            self.state["slots"]["chief_complaint"] = user_input_clean
            self.state["current_step"] = "DURATION"
            return (
                f"Thank you. I have recorded: '{user_input_clean}'.\n"
                "About how long have you been experiencing this? (e.g., '3 days', 'since yesterday')"
            )

        # Step 2: Duration with Conversational Error Recovery
        elif step == "DURATION":
            vague_words = ["a while", "some time", "not sure", "don't know", "idk", "long"]
            if any(w in user_input_clean.lower() for w in vague_words) or len(user_input_clean) < 3:
                return "To ensure the medical team triages accurately, could you estimate if it has been hours, days, or weeks?"

            self.state["slots"]["duration"] = user_input_clean
            self.state["current_step"] = "SEVERITY"
            return (
                "Understood. On a scale of 1 to 10 (where 1 is mild and 10 is unbearable), "
                "how would you rate your current discomfort?"
            )

        # Step 3: Pain / Severity Scale (Slot Filling & Regex Parsing)
        elif step == "SEVERITY":
            score_match = re.search(r"\b([1-9]|10)\b", user_input_clean)
            if not score_match:
                return "Please enter a valid number between 1 and 10 to describe the discomfort intensity."

            self.state["slots"]["severity_score"] = int(score_match.group(1))
            self.state["current_step"] = "RED_FLAGS"
            return (
                "Got it. Lastly, are you experiencing any shortness of breath, sudden numbness, "
                "or severe chest tightness? (Reply 'None' if clear)"
            )

        # Step 4: Red Flag Screen & Final Serialization
        elif step == "RED_FLAGS":
            self.state["status"] = "COMPLETED"
            summary_json = json.dumps(self.state["slots"], indent=2)
            return (
                "\n✅ INTAKE COMPLETED: Summary successfully compiled for the clinician queue.\n"
                "--------------------------------------------------\n"
                f"{summary_json}\n"
                "--------------------------------------------------\n"
                "A clinician will review your details shortly. Please rest comfortably."
            )

def run_intake_cli():
    session = ClinicalIntakeSession()
    print("=" * 60)
    print("🤖 CLINICAL INTAKE & TRIAGE CONVERSATIONAL AGENT")
    print("   Deterministic Finite-State Dialogue Manager")
    print("   Type 'exit' or 'quit' to terminate.")
    print("=" * 60)
    print("\nBot: Hello, I am the automated clinical intake assistant. What primary symptom brings you in today?")

    while session.state["status"] == "ACTIVE":
        try:
            user_msg = input("\nYou: ")
        except (KeyboardInterrupt, EOFError):
            print("\nSession exited.")
            break

        if user_msg.strip().lower() in ["exit", "quit"]:
            print("\nSession terminated by user.")
            break

        bot_reply = session.process_turn(user_msg)
        print(f"\nBot: {bot_reply}")

        if session.state["status"] in ["EMERGENCY_ESCALATED", "COMPLETED"]:
            break

if __name__ == "__main__":
    run_intake_cli()
