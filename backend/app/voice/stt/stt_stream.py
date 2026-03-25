import asyncio
import contextlib
from typing import AsyncIterator
from assemblyai_client import AssemblyAISTT


async def _stt_stream(audio_stream: AsyncIterator[bytes]) -> AsyncIterator[VoiceAgentEvent]:
    """Comment"""
    stt = AssemblyAISTT(sample_rate=16000)

    async def send_audio():
        """
        Background task that pumps audio chunks to Assembly (Producer).
        """
        try:
            # Stream each audio chunk to Assembly as it arrives
            async for audio_chunk in audio_stream:
                await stt.send_audio(audio_chunk)
        finally:
            await stt.close()

    # Launch audio sending task in background to simultaneously receive transcripts in main coroutine
    send_task = asyncio.create_task(send_audio())

    # Consumer loop: receive and yield transcription events as they arrive from AssemblyAI.
    try:
        # listens on the WebSocket for transcript events and yields them as they become available.
        async for event in stt.receive_events():
            yield event
    finally:
            # Cleanup: ensure background task is cancelled and awaited
            with contextlib.suppress(asyncio.CancelledError):
                send_task.cancel()
                await send_task
            # ensure ws connection is closed
            await stt.close()
