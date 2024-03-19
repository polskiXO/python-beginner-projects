import google.generativeai as genai


class NatLang2Latext:
    def __init__(
        self, google_api_key: str | None = None, model_name: str = "gemini-pro"
    ):
        if google_api_key is None:
            raise ValueError(
                "Google API key is required, create .env file and add GOOGLE_API_KEY"
            )

        self.google_api_key = google_api_key
        self.model_name = model_name

    def convert(self, text: str) -> str:
        genai.configure(api_key=self.google_api_key)
        model = genai.GenerativeModel(model_name=self.model_name)
        # this prompt isn't great, but it's a start
        # TODO: prompt engineering later
        prompt = f"Convert the following natural language text to LaTeX:\n\n{text}"
        return model.generate_content(
            contents=prompt,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                max_output_tokens=50,
                temperature=0.5,
            ),
        )
