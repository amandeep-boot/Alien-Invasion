class GameStats:
    """Track statistics for alien invasion """
    def __init__(self,ai_game):
        """Initialize statistics"""
        self.score = None
        self.ships_left = None
        self.settings = ai_game.settings
        self.reset_stats()
        # High score should never be reset
        self.high_score=0
        self.level =1

    def reset_stats(self):
        """Initialize statistics that can change during the game """
        self.ships_left = self.settings.ship_limit
        self.score = 0