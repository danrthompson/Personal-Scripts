"""
Utils for the openai Python library. Helper functions for common tasks.
"""

import datetime
import os
from typing import cast, Any, Optional

from openai import ChatCompletion
from openai.openai_object import OpenAIObject


def set_openai_api_key(openai_module: Any) -> None:
    openai_module.api_key = os.getenv("OPENAI_API_KEY")


def get_openai_chat_completion(
    prompt: str,
    system_message: Optional[str] = None,
    completion_kwargs: Optional[dict] = None,
) -> OpenAIObject:
    """
    Get a completion from OpenAI's ChatGPT model.

    Completion kwargs can include:
        temperature
        top_p
        n
        max_tokens
        presence_penalty
        frequency_penalty
        stop
    """
    if not system_message:
        current_date = datetime.date.today().strftime("%Y-%m-%d")
        knowledge_cutoff = "2021-09-01"
        system_message = f"You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible. Knowledge cutoff: {knowledge_cutoff} Current date: {current_date}"

    if not completion_kwargs:
        completion_kwargs = {}

    completion_args = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
    }

    completion_kwargs.update(completion_args)

    completion = ChatCompletion.create(**completion_kwargs)
    return cast(OpenAIObject, completion)


def get_text_from_openai_chat_completion(
    completion: OpenAIObject,
    log_error_messages: bool = False,
    log_completion_details: bool = False,
) -> str:
    """
    Get the text from a completion object.
    """
    if log_completion_details:
        print(completion)

    if "choices" not in completion or not completion["choices"]:
        if log_error_messages:
            print("No choices in completion")
        return ""

    message = completion["choices"][0].get("message")
    if message is None:
        if log_error_messages:
            print("No message in completion")
        return ""

    content = message.get("content")
    if content is None:
        if log_error_messages:
            print("No content in completion")
        return ""

    return content
