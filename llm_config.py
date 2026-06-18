import os
from crewai import LLM


class LLMConfig:
    """
    Manages LLM provider configuration using CrewAI's native LLM class.
    Supports OpenAI, Groq, and Gemini.
    """

    @staticmethod
    def get_llm(
        provider: str = "groq",
        model: str = None,
        temperature: float = 0.7
    ):
        provider = provider.lower()

        if provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")

            if not api_key:
                raise ValueError(
                    "OPENAI_API_KEY not found in environment variables"
                )

            return LLM(
                model=model or "gpt-4o",
                api_key=api_key,
                temperature=temperature
            )

        elif provider == "groq":
            api_key = os.getenv("GROQ_API_KEY")

            if not api_key:
                raise ValueError(
                    "GROQ_API_KEY not found in environment variables"
                )

            return LLM(
                model=f"groq/{model or 'llama-3.3-70b-versatile'}",
                api_key=api_key,
                temperature=temperature
            )

        elif provider == "gemini":
            api_key = os.getenv("GOOGLE_API_KEY")

            if not api_key:
                raise ValueError(
                    "GOOGLE_API_KEY not found in environment variables"
                )

            return LLM(
                model=f"gemini/{model or 'gemini-1.5-pro'}",
                api_key=api_key,
                temperature=temperature
            )

        else:
            raise ValueError(f"Unsupported provider: {provider}")

    @staticmethod
    def get_available_models(provider: str):
        models = {
            "openai": [
                "gpt-4o",
                "gpt-4-turbo",
                "gpt-3.5-turbo"
            ],

            "groq": [
                "llama-3.3-70b-versatile",
                "llama-3.1-70b-versatile",
                "llama-3.1-8b-instant"
            ],

            "gemini": [
                "gemini-1.5-pro",
                "gemini-1.5-flash"
            ]
        }

        return models.get(provider.lower(), [])