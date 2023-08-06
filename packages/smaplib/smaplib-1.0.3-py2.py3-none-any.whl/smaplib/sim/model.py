from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

import numpy as np
import tensorflow as tf

from . import feature as fea
from . import layer as lay


class ProductSimilarityModel(tf.keras.Model):
    def __init__(
        self,
        feature_set: fea.FeatureSet,
        num_heads: int,
        num_filters: int = 32,
        num_output_units: int = 512,
        dropout: float = 1e-2,
    ) -> None:
        super(ProductSimilarityModel, self).__init__()

        self.feature_set = feature_set
        self.num_heads = num_heads
        self.num_filters = num_filters
        self.num_output_units = num_output_units
        self.dropout = dropout
        self.key_dim = self.feature_set.token_size // self.num_heads

        if self.key_dim * self.num_heads != self.feature_set.token_size:
            raise Exception(
                "ERROR: `feature_set.token_size` should be divisible by `num_heads`!"
            )

        # Initialize layers
        self.embedding_layer = lay.ProductEmbeddingLayer(feature_set=self.feature_set)

        self.multihead_attention = tf.keras.layers.MultiHeadAttention(
            num_heads=self.num_heads, key_dim=self.key_dim, dropout=self.dropout
        )

        self.conv1d = tf.keras.layers.Conv1D(
            filters=self.num_filters,
            kernel_size=3,
            activation="relu",
            dropout=self.dropout,
        )

        self.maxpool = tf.keras.layers.MaxPooling1D(pool_size=2)

        self.flatten = tf.keras.layers.Flatten()

        self.dense = tf.keras.layers.Dense(
            units=self.num_output_units, activation="relu", dropout=self.dropout
        )

    def call(self, inputs):
        x = self.embedding_layer(inputs)
        x = self.multihead_attention(x, x, return_attention_scores=False)
        x = self.conv1d(x)
        x = self.maxpool(x)
        x = self.flatten(x)
        x = self.dense(x)
        return x
