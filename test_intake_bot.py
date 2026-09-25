import json
from clinical_intake_bot import ClinicalIntakeSession

def test_emergency_interception_on_turn_one():
    """Verify emergency protocol halts immediately on acute chief complaints."""
    session = ClinicalIntakeSession()
    reply = session.process_turn("My chest feels like an elephant is sitting on it")
    
    assert session.state["status"] == "EMERGENCY_ESCALATED"
    assert session.state["slots"]["red_flags_present"] is True
    assert "EMERGENCY PROTOCOL TRIGGERED" in reply
    print("✅ Passed: Emergency interception on Turn 1.")

def test_vague_duration_recovery():
    """Verify ambiguity triggers conversational clarification instead of proceeding."""
    session = ClinicalIntakeSession()
    session.process_turn("severe joint stiffness")
    clarification_reply = session.process_turn("I don't know, a while")
    
    assert session.state["current_step"] == "DURATION"
    assert "hours, days, or weeks" in clarification_reply
    print("✅ Passed: Conversational error recovery for vague duration.")

def test_full_successful_intake_flow():
    """Verify normal 4-turn traversal results in clean JSON serialization."""
    session = ClinicalIntakeSession()
    session.process_turn("Persistent dull headache")
    session.process_turn("4 days")
    session.process_turn("Pain level 5")
    final_reply = session.process_turn("None")
    
    assert session.state["status"] == "COMPLETED"
    assert session.state["slots"]["chief_complaint"] == "Persistent dull headache"
    assert session.state["slots"]["duration"] == "4 days"
    assert session.state["slots"]["severity_score"] == 5
    assert session.state["slots"]["red_flags_present"] is False
    assert "INTAKE COMPLETED" in final_reply
    print("✅ Passed: Full successful intake flow and JSON serialization.")

if __name__ == "__main__":
    print("Running automated dialogue manager tests...\n")
    test_emergency_interception_on_turn_one()
    test_vague_duration_recovery()
    test_full_successful_intake_flow()
    print("\n🎉 All dialogue flow tests passed successfully!")