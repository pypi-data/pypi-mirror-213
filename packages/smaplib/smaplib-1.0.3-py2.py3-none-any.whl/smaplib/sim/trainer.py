from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

import numpy as np
import tensorflow as tf

from . import dataset as dat
from . import feature as fea
from . import model as mdl


class ProductSimilarityModelTrainer:
    def __init__(
        self,
        feature_set: fea.FeatureSet,
        num_heads: int,
        num_filters: int = 32,
        num_output_units: int = 512,
        dropout: float = 1e-2,
        batch_size: int = 32,
        distance_margin: float = 0.1,
        triplet_loss_weight: float = 0.5,
        metric_fct: Any = tf.keras.losses.CosineSimilarity(),
    ) -> None:
        # Initialize parameters
        self.feature_set = feature_set
        self.num_heads = num_heads
        self.num_filters = num_filters
        self.num_output_units = num_output_units
        self.dropout = dropout
        self.batch_size = batch_size
        self.distance_margin = distance_margin
        self.triplet_loss_weight = triplet_loss_weight
        self.metric_fct = metric_fct

        # Initialize model
        self.model = mdl.ProductSimilarityModel(
            feature_set=self.feature_set,
            num_heads=self.num_heads,
            num_filters=self.num_filters,
            num_output_units=self.num_output_units,
            dropout=self.dropout,
        )

        # Initialize optimizer
        self.optimizer = tf.keras.optimizers.Adam()

    def train(
        self,
        train_data: dat.TripletList,
        num_epochs: int,
    ) -> List[float]:
        loss_history = []

        for epoch in range(num_epochs):
            epoch_loss_history = []
            print("Starting epoch {0}/{1}".format(epoch + 1, num_epochs))

            for triplet_list in train_data.chunks(self.batch_size):
                # Get anchors, positives and negatives for the batch
                anchors = triplet_list.anchors()
                positives = triplet_list.positives()
                negatives = triplet_list.negatives()

                with tf.GradientTape() as tape:
                    # Forward pass for anchors, positives and negatives batch.
                    # The model expects inputs of type `ProductList`.
                    anchors_embeddings = self.model(anchors)
                    positives_embeddings = self.model(positives)
                    negatives_embeddings = self.model(negatives)

                    # Compute loss
                    loss = ProductSimilarityModelTrainer.combined_loss(
                        anchors=anchors_embeddings,
                        positives=positives_embeddings,
                        negatives=negatives_embeddings,
                        metric_fct=self.metric_fct,
                        distance_margin=self.distance_margin,
                        triplet_loss_weight=self.triplet_loss_weight,
                    )

                # Backward pass
                gradients = tape.gradient(
                    target=loss, sources=self.model.trainable_variables
                )

                self.optimizer.apply_gradients(
                    grads_and_vars=zip(gradients, self.model.trainable_variables)
                )

                epoch_loss_history.append(loss.numpy())

            # Compute average loss for this epoch
            epoch_loss = np.mean(epoch_loss_history)
            loss_history.append(epoch_loss)

            print("Epoch {0}/{1} loss: {2}".format(epoch + 1, num_epochs, epoch_loss))

        return loss_history

    @staticmethod
    def combined_loss(
        anchors, positives, negatives, metric_fct, distance_margin, triplet_loss_weight
    ):
        # Compute the triplet loss
        t_loss = ProductSimilarityModelTrainer.triplet_loss(
            anchors, positives, negatives, metric_fct, distance_margin
        )

        # Compute the contrastive loss
        c_loss = ProductSimilarityModelTrainer.contrastive_loss(
            anchors, positives, negatives, metric_fct, distance_margin
        )

        # Return the weighted sum of the triplet loss and the contrastive loss
        return triplet_loss_weight * t_loss + (1 - triplet_loss_weight) * c_loss

    @staticmethod
    def triplet_loss(anchors, positives, negatives, metric_fct, distance_margin):
        # Compute distance between anchors and positives
        positives_distance = metric_fct(anchors, positives)

        # Compute distance between anchors and negatives
        negatives_distance = metric_fct(anchors, negatives)

        # Compute the triplet loss
        return max(positives_distance - negatives_distance + distance_margin, 0)

    @staticmethod
    def contrastive_loss(anchors, positives, negatives, metric_fct, distance_margin):
        # Compute distance between anchors and positives
        positives_distance = metric_fct(anchors, positives)

        # Compute distance between anchors and negatives
        negatives_distance = metric_fct(anchors, negatives)

        # Compute the contrastive loss
        return positives_distance ^ 2 + max(distance_margin - negatives_distance, 0) ^ 2
