import json
import math
from pathlib import Path
from typing import List, Optional, Tuple, Dict
import numpy as np

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

from app.models.schemas import Product, ScoredProduct, UserProfile
from app.config import DATA_DIR
from app.services.user_profiler import user_profiler

class FallbackTfidf:
    """Lightweight pure-python TF-IDF and cosine similarity fallback if scikit-learn is loading."""
    def __init__(self):
        self.vocabulary: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}

    def fit_transform(self, docs: List[str]):
        tokenized_docs = [doc.lower().split() for doc in docs]
        N = len(tokenized_docs)
        df = {}
        for tokens in tokenized_docs:
            for term in set(tokens):
                df[term] = df.get(term, 0) + 1
        
        self.vocabulary = {term: idx for idx, term in enumerate(df.keys())}
        self.idf = {term: math.log((1 + N) / (1 + count)) + 1 for term, count in df.items()}

        vectors = []
        for tokens in tokenized_docs:
            vec = np.zeros(len(self.vocabulary))
            for t in tokens:
                if t in self.vocabulary:
                    vec[self.vocabulary[t]] += 1
            # tf * idf
            for t, idx in self.vocabulary.items():
                if vec[idx] > 0:
                    vec[idx] = vec[idx] * self.idf[t]
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
            vectors.append(vec)
        return np.array(vectors)

    def transform(self, queries: List[str]):
        vectors = []
        for q in queries:
            tokens = q.lower().split()
            vec = np.zeros(len(self.vocabulary))
            for t in tokens:
                if t in self.vocabulary:
                    vec[self.vocabulary[t]] += 1 * self.idf[t]
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
            vectors.append(vec)
        return np.array(vectors)

class RecommendationEngine:
    def __init__(self):
        self.products_file = DATA_DIR / "products.json"
        self.products: List[Product] = []
        self.product_map = {}
        self.tfidf_matrix = None
        self.product_corpus = []
        
        if SKLEARN_AVAILABLE:
            self.tfidf_vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        else:
            self.tfidf_vectorizer = FallbackTfidf()
            
        self.reload_products()

    def reload_products(self):
        if not self.products_file.exists():
            return
        with open(self.products_file, "r", encoding="utf-8") as f:
            raw = json.load(f)
            self.products = [Product(**p) for p in raw]
            self.product_map = {p.id: p for p in self.products}

        # Build TF-IDF document representation
        self.product_corpus = []
        for p in self.products:
            combined = f"{p.name} {p.category} {p.sub_category} {' '.join(p.tags)} {p.description}"
            self.product_corpus.append(combined)

        if self.product_corpus:
            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.product_corpus)

    def get_product(self, product_id: str) -> Optional[Product]:
        return self.product_map.get(product_id)

    def list_all_products(self) -> List[Product]:
        return self.products

    def _calc_cosine_similarity(self, query_vec, matrix):
        if SKLEARN_AVAILABLE:
            return cosine_similarity(query_vec, matrix)[0]
        else:
            # Query vector dot matrix transpose
            return np.dot(matrix, query_vec[0])

    def recommend(
        self,
        user_id: Optional[str] = None,
        user_profile: Optional[UserProfile] = None,
        search_query: Optional[str] = None,
        current_product_id: Optional[str] = None,
        top_k: int = 4
    ) -> Tuple[List[ScoredProduct], str, str]:
        """
        Hybrid recommendation pipeline:
        1. Query / Keyword relevance (TF-IDF Cosine Similarity)
        2. Demographic affinity boosting (Age group filter & affinity)
        3. Item-to-item similarity (if looking at a specific product)
        4. Cold-start fallback (Rating & popularity ranking)
        """
        profile = user_profile or user_profiler.get_user_profile(user_id)
        user_age_group = profile.age_group if profile else "18-25"
        user_segment = f"{user_age_group} | {profile.preferred_language if profile else 'general'}"

        if not self.products:
            return [], "None", user_segment

        n_items = len(self.products)
        scores = np.zeros(n_items)
        reasons = ["Popular item"] * n_items

        # Component 1: Search Query Relevance (Real-time intent)
        if search_query and search_query.strip():
            query_vec = self.tfidf_vectorizer.transform([search_query])
            sim = self._calc_cosine_similarity(query_vec, self.tfidf_matrix)
            scores += sim * 0.45
            for idx, s in enumerate(sim):
                if s > 0.15:
                    reasons[idx] = f"Matches search: '{search_query.strip()}'"

        # Component 2: User Search History & Interest Tokens (Historical intent)
        if profile and (profile.search_history or profile.interests):
            combined_history = " ".join(profile.search_history + profile.interests)
            if combined_history.strip():
                hist_vec = self.tfidf_vectorizer.transform([combined_history])
                sim = self._calc_cosine_similarity(hist_vec, self.tfidf_matrix)
                scores += sim * 0.35
                for idx, s in enumerate(sim):
                    if s > 0.12 and reasons[idx] == "Popular item":
                        reasons[idx] = f"Based on your interest in {profile.interests[0] if profile.interests else 'recent searches'}"

        # Component 3: Demographic Alignment (Age-group booster)
        if profile and profile.age_group:
            for idx, p in enumerate(self.products):
                if profile.age_group in p.age_groups:
                    scores[idx] += 0.25
                    if reasons[idx] == "Popular item":
                        reasons[idx] = f"Popular among age {profile.age_group} in {profile.city or 'your region'}"

        # Component 4: Item-to-Item Similarity (Related products context)
        if current_product_id and current_product_id in self.product_map:
            curr_idx = next((i for i, p in enumerate(self.products) if p.id == current_product_id), None)
            if curr_idx is not None:
                if SKLEARN_AVAILABLE:
                    item_sim = cosine_similarity(self.tfidf_matrix[curr_idx], self.tfidf_matrix)[0]
                else:
                    item_sim = np.dot(self.tfidf_matrix, self.tfidf_matrix[curr_idx])
                scores += item_sim * 0.30
                scores[curr_idx] = -1.0  # Do not recommend same item
                for idx, s in enumerate(item_sim):
                    if s > 0.20 and idx != curr_idx:
                        reasons[idx] = f"Frequently bought with {self.product_map[current_product_id].name[:20]}..."

        # Component 5: Product Quality Base (Rating / 5.0)
        for idx, p in enumerate(self.products):
            scores[idx] += (p.rating / 5.0) * 0.10

        # Rank indices
        ranked_indices = np.argsort(scores)[::-1]
        
        result: List[ScoredProduct] = []
        for idx in ranked_indices:
            if len(result) >= top_k:
                break
            p = self.products[idx]
            final_score = float(np.clip(scores[idx], 0.05, 0.99))
            scored_item = ScoredProduct(
                **p.model_dump(),
                score=round(final_score, 2),
                match_reason=reasons[idx]
            )
            result.append(scored_item)

        engine_name = "Scikit-learn TF-IDF + Cosine Similarity" if SKLEARN_AVAILABLE else "NumPy TF-IDF + Cosine Similarity"
        algorithm_used = f"Hybrid {engine_name} + Demographic Weighting"
        return result, algorithm_used, user_segment

recommender = RecommendationEngine()
