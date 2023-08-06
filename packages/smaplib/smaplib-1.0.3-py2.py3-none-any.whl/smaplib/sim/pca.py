from __future__ import annotations

import pickle

from sklearn.decomposition import PCA


class PCA_Saver:
    @staticmethod
    def save_pca(pca, filename):
        """Saves a fitted PCA model to a pickle file"""
        pca_parameters = {
            "components": pca.components_,
            "explained_variance": pca.explained_variance_,
            "mean": pca.mean_,
            "n_components": pca.n_components_,
        }

        with open(filename, "wb") as handle:
            pickle.dump(pca_parameters, handle, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_pca(filename):
        """Loads a fitted PCA model from a pickle file"""
        with open(filename, "rb") as handle:
            loaded_pca_parameters = pickle.load(handle)

        loaded_pca = PCA(n_components=int(loaded_pca_parameters["n_components"]))
        loaded_pca.components_ = loaded_pca_parameters["components"]
        loaded_pca.explained_variance_ = loaded_pca_parameters["explained_variance"]
        loaded_pca.mean_ = loaded_pca_parameters["mean"]

        return loaded_pca
