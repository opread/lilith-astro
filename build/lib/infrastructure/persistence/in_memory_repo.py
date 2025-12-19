"""In-memory repository for storing UserProfile and NatalChart."""

from typing import Dict, Optional

from src.core.domain.models import NatalChart, UserProfile


class InMemoryRepository:
    """In-memory repository implementation."""

    def __init__(self):
        """Initialize the repository."""
        self._profiles: Dict[str, UserProfile] = {}
        self._charts: Dict[str, NatalChart] = {}

    def save_profile(self, profile: UserProfile) -> None:
        """Save a user profile.

        Args:
            profile: The user profile to save.
        """
        self._profiles[profile.user_id] = profile

    def get_profile(self, user_id: str) -> Optional[UserProfile]:
        """Get a user profile by user ID.

        Args:
            user_id: The user ID.

        Returns:
            The user profile if found, None otherwise.
        """
        return self._profiles.get(user_id)

    def save_chart(self, user_id: str, chart: NatalChart) -> None:
        """Save a natal chart for a user.

        Args:
            user_id: The user ID.
            chart: The natal chart to save.
        """
        self._charts[user_id] = chart

    def get_chart(self, user_id: str) -> Optional[NatalChart]:
        """Get a natal chart by user ID.

        Args:
            user_id: The user ID.

        Returns:
            The natal chart if found, None otherwise.
        """
        return self._charts.get(user_id)