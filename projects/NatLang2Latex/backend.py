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
        self.prompt = "The following is a problem that involve converting natural language to its LaTeX representation.\n"
        self.prompt += "The text in between the <NATLANG></NATLANG> tags should be converted to LaTeX.\n"
        self.prompt += "The text in between the <LATEX></LATEX> tags should be the expected LaTeX representation of the text in between the <NATLANG></NATLANG> tags.\n\n"
        # n-shot example
        self.prompt += (
            "<NATLANG>The definite integral of x squared from 0 to 1.</NATLANG>\n"
        )
        self.prompt += "<LATEX>\\int_{0}^{1} x^2 dx</LATEX>\n\n"
        self.prompt += "<NATLANG>The derivative of x squared.</NATLANG>\n"
        self.prompt += "<LATEX>\\frac{d}{dx} x^2</LATEX>\n\n"
        self.prompt += "<NATLANG>The limit as x approaches 0 of x squared.</NATLANG>\n"
        self.prompt += "<LATEX>\\lim_{x \\to 0} x^2</LATEX>\n\n"
        # actual query
        self.prompt += "<NATLANG>"

    def convert(self, text: str) -> str:
        genai.configure(api_key=self.google_api_key)
        model = genai.GenerativeModel(model_name=self.model_name)
        # this prompt isn't great, but it's a start
        # TODO: prompt engineering later
        prompt = f"{self.prompt}{text}</NATLANG>\n<LATEX>"
        return model.generate_content(
            contents=prompt,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                max_output_tokens=200,
                temperature=0.5,
                stop_sequences=["</LATEX>"],
            ),
        ).text
