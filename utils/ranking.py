from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def rank_resumes(resumes, job_description):
    """
    Rank resumes based on similarity to the job description.

    Parameters
    ----------
    resumes : list[str]
        List of cleaned resume texts.

    job_description : str
        Cleaned job description.

    Returns
    -------
    list[float]
        Similarity scores.
    """

    documents = resumes.copy()
    documents.append(job_description)

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity_scores = cosine_similarity(
        tfidf_matrix[-1],
        tfidf_matrix[:-1]
    )

    return similarity_scores.flatten()