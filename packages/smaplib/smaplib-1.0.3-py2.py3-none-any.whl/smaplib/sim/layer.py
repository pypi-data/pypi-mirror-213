from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

import tensorflow as tf

from . import dataset as dat
from . import feature as fea


class ProductEmbeddingLayer(tf.keras.layers.Layer):
    def __init__(self, feature_set: fea.FeatureSet, **kwargs):
        super(tf.keras.layers.Layer, self).__init__(**kwargs)
        self.feature_set = feature_set

    def call(self, inputs: dat.ProductList) -> tf.Tensor:
        return tf.stack(inputs.get_embeddings(feature_set=self.feature_set), axis=0)

    def get_config(self):
        config = super().get_config()
        config.update({"feature_set": self.feature_set.get_config()})

        return config

    @classmethod
    def from_config(cls, config):
        feature_set = fea.FeatureSet.from_config(config["feature_set"])
        config_dict = {
            key: value for key, value in config.items() if key not in ["feature_set"]
        }

        return cls(feature_set=feature_set, **config_dict)
