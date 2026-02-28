from dotenv import load_dotenv
load_dotenv()
from graph import build_graph

if __name__ == "__main__":

    app = build_graph()

    initial_state = {
        "resume_paths": ["resume\Prathamesh_Palatshaha_AIML.pdf", "resume\Prathamesh_Palatshaha_BA_ROLE.pdf"],
        "resumes": [],
        "jobs": [],
        "selected_job": {},
        "selected_resume": {},
        "match_score": 0.0,
        "decision": "",
        "human_approval": ""
    }

    app.invoke(initial_state)