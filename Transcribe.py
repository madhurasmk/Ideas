import os
import whisper
import ffmpeg
from langgraph.graph import StateGraph, END
# from video_agent_state import VideoAgentState
from video_agent_state import VideoAgentState
VIDEO_FOLDER = "C:/Users/Sangmesh/Desktop/CSR"
VIDEO_EXTENSIONS = (".mp4", ".mov", ".avi", ".mkv", ".mpg", ".mpeg")

# Node 1: Fetch latest video
def get_latest_video(state: VideoAgentState):
    folder = state["video_folder"]

    videos = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(VIDEO_EXTENSIONS)
    ]

    if not videos:
        raise FileNotFoundError("No video files found")

    latest_video = max(videos, key=os.path.getmtime)

    return {
        **state,
        "video_path": latest_video,
        "audio_path": "audio.wav",
        "output_file": "transcript.txt"
    }

# Node 2: Extract audio
def extract_audio(state: VideoAgentState):
    ffmpeg.input(state["video_path"]).output(
        state["audio_path"],
        format="wav",
        acodec="pcm_s16le",
        ac=1,
        ar="16000"
    ).overwrite_output().run(quiet=True)

    return state

# Node 3: Transcribe audio
def transcribe_audio(state: VideoAgentState):
    model = whisper.load_model("base")
    result = model.transcribe(state["audio_path"])

    return {
        **state,
        "transcript": result["text"]
    }

# Node 4: Save transcript
def save_transcript(state: VideoAgentState):
    with open(state["output_file"], "w", encoding="utf-8") as f:
        f.write(state["transcript"])

    return state

# Build LangGraph
def build_video_agent():
    graph = StateGraph(VideoAgentState)

    graph.add_node("get_latest_video", get_latest_video)
    graph.add_node("extract_audio", extract_audio)
    graph.add_node("transcribe_audio", transcribe_audio)
    graph.add_node("save_transcript", save_transcript)

    graph.set_entry_point("get_latest_video")

    graph.add_edge("get_latest_video", "extract_audio")
    graph.add_edge("extract_audio", "transcribe_audio")
    graph.add_edge("transcribe_audio", "save_transcript")
    graph.add_edge("save_transcript", END)

    return graph.compile()

# Run Agent
if __name__ == "__main__":
    agent = build_video_agent()

    result = agent.invoke({
        "video_folder": VIDEO_FOLDER,
        "video_path": None,
        "audio_path": None,
        "transcript": None,
        "output_file": None
    })

    print("Transcript saved:", result["output_file"])
