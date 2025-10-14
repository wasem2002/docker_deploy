import pickle
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse import save_npz, load_npz


with open("recommend/models/als_model.pkl", "rb") as f:
    als_model = pickle.load(f)

with open("recommend/models/item_mappings.pkl", "rb") as f:
    i2idx = pickle.load(f)   # product_id -> idx

with open("recommend/models/user_mappings.pkl", "rb") as f:
    u2idx = pickle.load(f)   # customer_id -> idx

with open("recommend/models/popularity.pkl", "rb") as f:
    global_pop_rank = pickle.load(f)

with open("recommend/models/recent_popularity.pkl", "rb") as f:
    recent30_pop_rank = pickle.load(f)

with open("recommend/models/train_user_items.pkl", "rb") as f:
    train_user_items = pickle.load(f)  # dict: user_idx -> set(item_idx)

with open("recommend/models/idx2item.pkl", "rb") as f:
    idx2i = pickle.load(f)   # idx -> product_id

def popularity_get_recs(user_idx, pop_rank, train_user_items, K=10):
    seen = train_user_items.get(user_idx, set())
    recs = [it for it in pop_rank if it not in seen][:K]
    return [idx2i[i] for i in recs]

train_mat = load_npz("recommend/models/train_mat.npz")

def als_get_recs(user_idx, K=10):
    ids, scores = als_model.recommend(
        user_idx,
        train_mat[user_idx],   # directly use sparse row
        N=K,
        filter_already_liked_items=True
    )
    return [idx2i[i] for i in ids]   # map to product_id


def hybrid_get_recs(user_id, K=10):
    if user_id in u2idx:   # known user
        user_idx = u2idx[user_id]
        return als_get_recs(user_idx, K)
    else:   # cold-start fallback
        return popularity_get_recs(-1, global_pop_rank, train_user_items, K)  


def recommend(user_id, method="hybrid", K=10):
    if method == "hybrid":
        return hybrid_get_recs(user_id, K)
    elif method == "als":
        return als_get_recs(u2idx[user_id], K)
    elif method == "popularity":
        return popularity_get_recs(u2idx.get(user_id, -1), global_pop_rank, train_user_items, K)
    else:
        raise ValueError("Unknown method")


# if __name__ == "__main__":
#     test_user = "12"
#     print("Hybrid:", recommend(test_user, method="hybrid", K=10))
#     print("ALS:", recommend(test_user, method="als", K=10))
#     print("Popularity:", recommend(test_user, method="popularity", K=10))