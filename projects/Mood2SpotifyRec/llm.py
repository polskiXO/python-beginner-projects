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
        self.prompt = "The following is a problem that involve converting natural language of someone's mood to the correct Spotify metrics threshold.\n"
        self.prompt += (
            "The text in between the <MOOD></MOOD> is the user's current mood.\n"
        )
        self.prompt += "The text in between the <METRICS></METRICS> should be the range of metrics specific to Spotify. Those metrics are:\n"
        self.prompt += "- valence, ranging from 0 to 1, describes the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).\n"
        self.prompt += "- energy, ranging from 0 to 1, represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale.\n"
        self.prompt += "- danceability, ranging from 0 to 1, describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.\n"
        self.prompt += "- acousticness, ranging from 0 to 1, is a confidence measure of whether the track is acoustic. A score of 1.0 indicates high confidence the track is acoustic.\n"
        # n-shot example
        self.prompt += "<MOOD>I am feeling happy</MOOD>\n"
        self.prompt += "<METRICS>\n"
        self.prompt += "valence: 0.8-1.0\n"
        self.prompt += "energy: 0.6-1.0\n"
        self.prompt += "danceability: 0.6-1.0\n"
        self.prompt += "acousticness: 0.0-0.4\n"
        self.prompt += "</METRICS>\n"
        self.prompt += "<MOOD>I am feeling sad</MOOD>\n"
        self.prompt += "<METRICS>\n"
        self.prompt += "valence: 0.0-0.4\n"
        self.prompt += "energy: 0.0-0.4\n"
        self.prompt += "danceability: 0.0-0.4\n"
        self.prompt += "acousticness: 0.6-1.0\n"
        self.prompt += "</METRICS>\n"
        self.prompt += "<MOOD>I am feeling energetic</MOOD>\n"
        self.prompt += "<METRICS>\n"
        self.prompt += "valence: 0.6-1.0\n"
        self.prompt += "energy: 0.6-1.0\n"
        self.prompt += "danceability: 0.6-1.0\n"
        self.prompt += "acousticness: 0.0-0.4\n"
        self.prompt += "</METRICS>\n"

    def convert(self, text: str) -> dict[str, float]:
        """
        Convert natural language to Spotify metrics
        Args:
            text (str): natural language text
        Returns:
            dict[str, float]: Spotify metrics
        """
        genai.configure(api_key=self.google_api_key)
        model = genai.GenerativeModel(model_name=self.model_name)
        prompt = f"<MOOD>{self.prompt}{text}</MOOD>\n<METRICS>\n"
        raw_ouput = model.generate_content(
            contents=prompt,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                max_output_tokens=200,
                temperature=0.5,
                stop_sequences=["</METRICS>"],
            ),
        ).text

        metrics = {}
        for line in raw_ouput.split("\n"):
            if ":" in line:
                key, value = line.split(":")
                metrics[key.strip()] = float(value.strip())

        return metrics
