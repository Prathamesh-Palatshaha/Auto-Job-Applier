from dotenv import load_dotenv
load_dotenv()
from graph import build_graph

if __name__ == "__main__":
    try:
        app = build_graph()
        
        initial_state = {
            "resume_paths": [
                r"resume\Prathamesh_Palatshaha_AIML.pdf",
                r"resume\Prathamesh_Palatshaha_BA_ROLE.pdf"
            ],
            "resumes": [],
            "jobs": [],
            "selected_job": {},
            "selected_resume": {},
            "match_score": 0.0,
            "decision": "",
            "evaluation_reasoning": "", 
            "human_approval": ""
        }
        
        print("🚀 Starting Job Application Agent...\n")
        result = app.invoke(initial_state)
        
        print("\n✅ Workflow completed!")
        print(f"Final decision: {result.get('decision')}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Workflow interrupted by user")
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        import traceback
        traceback.print_exc()