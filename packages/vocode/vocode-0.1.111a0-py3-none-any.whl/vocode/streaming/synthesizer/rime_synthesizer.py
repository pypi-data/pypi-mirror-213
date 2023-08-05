import audioop
import logging
import aiohttp
from pydub import AudioSegment
import base64
from vocode import getenv
from vocode.streaming.agent.bot_sentiment_analyser import BotSentiment
from vocode.streaming.models.audio_encoding import AudioEncoding
from vocode.streaming.models.message import BaseMessage

from vocode.streaming.synthesizer.base_synthesizer import (
    BaseSynthesizer,
    SynthesisResult,
    encode_as_wav,
    tracer,
)

from typing import Any, Optional
import io
import requests

from vocode.streaming.models.synthesizer import RimeSynthesizerConfig, SynthesizerType

from opentelemetry.context.context import Context

# https://rime.ai/docs/quickstart
RIME_SAMPLING_RATE = 22050
RIME_BASE_URL = "https://rjmopratfrdjgmfmaios.functions.supabase.co/rime-tts"


class RimeSynthesizer(BaseSynthesizer[RimeSynthesizerConfig]):
    def __init__(
        self,
        synthesizer_config: RimeSynthesizerConfig,
        logger: Optional[logging.Logger] = None,
    ):
        super().__init__(synthesizer_config)
        self.api_key = getenv("RIME_API_KEY")
        self.speaker = synthesizer_config.speaker

    async def create_speech(
        self,
        message: BaseMessage,
        chunk_size: int,
        bot_sentiment: Optional[BotSentiment] = None,
    ) -> SynthesisResult:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        body = {
            "text": message.text,
            "speaker": self.speaker,
        }
        create_speech_span = tracer.start_span(
            f"synthesizer.{SynthesizerType.RIME.value.split('_', 1)[-1]}.create_total",
        )
        async with aiohttp.ClientSession() as session:
            async with session.post(
                RIME_BASE_URL,
                headers=headers,
                json=body,
                timeout=aiohttp.ClientTimeout(total=15),
            ) as response:
                if not response.ok:
                    raise Exception(
                        f"Rime API error: {response.status}, {await response.text()}"
                    )
                data = await response.json()
                create_speech_span.end()
                convert_span = tracer.start_span(
                    f"synthesizer.{SynthesizerType.RIME.value.split('_', 1)[-1]}.convert",
                )

                audio_file = io.BytesIO(base64.b64decode(data.get("audioContent")))

                result = self.create_synthesis_result_from_wav(
                    file=audio_file, message=message, chunk_size=chunk_size
                )
                convert_span.end()
                return result
