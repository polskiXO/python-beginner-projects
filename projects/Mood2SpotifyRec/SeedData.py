class SeedData:
    def __init__(
        self,
        seed_genres=None,
        seed_artists=None,
        target_valence=None,
        target_energy=None,
        target_danceability=None,
        target_acousticness=None,
    ):
        self.seed_genres = seed_genres if seed_genres is not None else []
        self.seed_artists = seed_artists if seed_artists is not None else []
        self.target_valence = target_valence
        self.target_energy = target_energy
        self.target_danceability = target_danceability
        self.target_acousticness = target_acousticness

    def get_test_seed_data(self):
        return SeedData(
            seed_genres=["indie", "rock"],
            seed_artists=[
                "4NHQUGzhtTLFvgF5SZesLK"
            ],  # Example artist ID for Tame Impala
            # seed_tracks=["0c6xIDDpzE81m2q797ordA"],  # Example track ID
            target_valence=0.5,
            target_energy=0.8,
            target_danceability=0.7,
            target_acousticness=0.3,
        )
