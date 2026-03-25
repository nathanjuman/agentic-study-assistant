# Versions:
V1
- VoiceAgent
- RAGAgent
V2
- Add Dialogue Manager
- Add Memory Store
V3: 
- Add Study Strategy Agent (quiz, spacing, testing)


# File Structure:
backend/
├── app/
│   ├── main.py
│   ├── config/
│   │   ├── settings.py
│   │   └── logging.py
│   ├── api/
│   │   ├── routes/
│   │   │   ├── health.py
│   │   │   ├── files.py
│   │   │   ├── rag.py
│   │   │   └── voice.py
│   │   ├── schemas/
│   │   │   ├── files.py
│   │   │   ├── rag.py
│   │   │   └── voice.py
│   │   └── deps.py
│   ├── agents/
│   │   ├── rag_agent/
│   │   │   ├── orchestrator.py
│   │   │   └── prompt.py
│   │   ├── voice_agent/
│   │   │   ├── pipeline.py
│   │   │   ├── agent_stage.py
│   │   │   ├── session.py
│   │   │   └── prompt.py
│   │   └── shared/
│   │       ├── types.py
│   │       ├── events.py
│   │       └── context_builder.py
│   ├── rag/
│   │   ├── loaders/
│   │   ├── chunking/
│   │   ├── embeddings/
│   │   ├── vectorstore/
│   │   ├── retrieval/
│   │   ├── ingestion/
│   │   └── citations.py
│   ├── voice/
│   │   ├── stt/
│   │   │   ├── assemblyai_client.py
│   │   │   └── stt_stage.py
│   │   ├── tts/
│   │   │   ├── cartesia_client.py
│   │   │   └── tts_stage.py
│   │   ├── transport/
│   │   │   ├── websocket_manager.py
│   │   │   └── audio_stream.py
│   │   └── codecs/
│   │       └── pcm16.py
│   ├── services/
│   │   ├── file_service.py
│   │   ├── storage_service.py
│   │   └── conversation_service.py
│   ├── db/
│   │   ├── models/
│   │   │   ├── uploaded_file.py
│   │   │   ├── document_chunk.py
│   │   │   └── study_session.py
│   │   └── client.py
│   ├── prompts/
│   │   ├── rag/
│   │   │   └── answer_prompt.txt
│   │   └── voice/
│   │       └── tutor_prompt.txt
│   └── utils/
│       ├── ids.py
│       └── timers.py
├── tests/
│   ├── api/
│   ├── agents/
│   ├── rag/
│   └── voice/
├── requirements.txt
├── .env
└── README.md



---
# Packages & Libraries
  