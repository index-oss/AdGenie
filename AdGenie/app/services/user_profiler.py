import json
from pathlib import Path
from typing import Dict, Optional, List
from app.models.schemas import UserProfile
from app.config import DATA_DIR

class UserProfilerService:
    def __init__(self):
        self.users_file = DATA_DIR / "sample_users.json"
        self._users_cache: Dict[str, UserProfile] = {}
        self.reload_users()

    def reload_users(self):
        if self.users_file.exists():
            with open(self.users_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    self._users_cache[item["user_id"]] = UserProfile(**item)

    def get_user_profile(self, user_id: Optional[str]) -> Optional[UserProfile]:
        if not user_id:
            return None
        return self._users_cache.get(user_id)

    def list_sample_users(self) -> List[UserProfile]:
        return list(self._users_cache.values())

    @staticmethod
    def infer_age_group(age: int) -> str:
        if age <= 25:
            return "18-25"
        elif age <= 35:
            return "26-35"
        elif age <= 50:
            return "36-50"
        else:
            return "50+"

    @staticmethod
    def enrich_profile(profile: UserProfile) -> Dict[str, any]:
        """Calculates derived signals from user data for the recommendation model."""
        age_group = profile.age_group or UserProfilerService.infer_age_group(profile.age or 25)
        keywords = set()
        for s in profile.search_history:
            for w in s.lower().split():
                if len(w) > 2:
                    keywords.add(w)
        for interest in profile.interests:
            keywords.add(interest.lower())

        return {
            "user_id": profile.user_id,
            "name": profile.name,
            "age_group": age_group,
            "preferred_language": profile.preferred_language or "hinglish",
            "keywords": list(keywords),
            "recent_clicks": profile.recent_clicks,
            "intent_summary": f"{age_group} segment | interests: {', '.join(profile.interests) if profile.interests else 'general'}"
        }

user_profiler = UserProfilerService()
