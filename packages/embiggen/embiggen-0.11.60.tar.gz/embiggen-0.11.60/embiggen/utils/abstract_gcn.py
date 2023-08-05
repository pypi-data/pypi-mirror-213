"""Kipf GCN model for node-label prediction."""
from typing import List, Union, Optional, Dict, Any, Type, Tuple

import compress_pickle
import numpy as np
import pandas as pd
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau  # pylint: disable=import-error,no-name-in-module
from tensorflow.keras.models import Model  # pylint: disable=import-error,no-name-in-module
from tensorflow.keras.optimizers import \
    Optimizer  # pylint: disable=import-error,no-name-in-module

from ensmallen import Graph
import tensorflow as tf
from keras_mixed_sequence import Sequence
from embiggen.utils import AbstractEdgeFeature
from embiggen.utils.abstract_models import AbstractClassifierModel, abstract_class
from embiggen.utils.number_to_ordinal import number_to_ordinal
from embiggen.layers.tensorflow import GraphConvolution, FlatEmbedding, EmbeddingLookup, L2Norm
from tensorflow.keras.layers import Input, Concatenate
import warnings
from embiggen.utils.normalize_model_structural_parameters import normalize_model_list_parameter
import copy


def graph_to_sparse_tensor(
    graph: Graph,
    use_weights: bool,
    use_simmetric_normalized_laplacian: bool,
    handling_multi_graph: str = "warn",
) -> tf.SparseTensor:
    """Returns provided graph as sparse Tensor.

    Parameters
    -------------------
    graph: Graph,
        The graph to convert.
    use_weights: bool,
        Whether to load the graph weights.
    use_simmetric_normalized_laplacian: bool
        Whether to use the symmetrically normalized laplacian 
    handling_multi_graph: str = "warn"
        How to behave when dealing with multigraphs.
        Possible behaviours are:
        - "warn", which warns the user and drops the multi-edges.
        - "raise"
        - "drop"

    Raises
    -------------------
    ValueError,
        If the weights are requested but the graph does not contain any.
    ValueError,
        If the graph contains singletons.
    ValueError,
        If the graph is a multigraph.

    Returns
    -------------------
    SparseTensor with (weighted) adjacency matrix.
    """
    if use_weights and not graph.has_edge_weights():
        raise ValueError(
            "Edge weights were requested but the provided graph "
            "does not contain any edge weight."
        )

    if graph.has_singleton_nodes():
        raise ValueError(
            f"In the provided {graph.get_name()} graph there are "
            f"{graph.get_number_of_singleton_nodes()} singleton nodes."
            "The GCN model does not support operations on graph containing "
            "singletons. You can either choose to drop singletons from "
            "the graph by using the `graph.remove_singleton_nodes()` "
            "method or alternatively you can add selfloops to them by "
            "using the `graph.add_selfloops()` method."
        )

    if graph.is_multigraph():
        message = (
            "The GCN model does not currently support convolutions on a multigraph. "
            "We are dropping the parallel edges before computing the adjacency matrix."
        )
        if handling_multi_graph == "warn":
            warnings.warn(message)
        elif handling_multi_graph == "raise":
            raise ValueError(message)

        graph = graph.remove_parallel_edges()

    if use_simmetric_normalized_laplacian:
        edge_node_ids, weights = graph.get_symmetric_normalized_laplacian_coo_matrix()
        return tf.sparse.reorder(tf.SparseTensor(
            edge_node_ids,
            np.abs(weights),
            (graph.get_number_of_nodes(), graph.get_number_of_nodes())
        ))

    return tf.SparseTensor(
        graph.get_directed_edge_node_ids(),
        (
            graph.get_directed_edge_weights()
            if use_weights
            else tf.ones(graph.get_number_of_directed_edges())
        ),
        (graph.get_number_of_nodes(), graph.get_number_of_nodes())
    )


@abstract_class
class AbstractGCN(AbstractClassifierModel):
    """Kipf GCN model for node-label prediction."""

    def __init__(
        self,
        epochs: int = 1000,
        number_of_graph_convolution_layers: int = 2,
        number_of_units_per_graph_convolution_layers: Union[int, List[int]] = 128,
        dropout_rate: float = 0.5,
        apply_norm: bool = False,
        combiner: str = "mean",
        optimizer: Union[str, Optimizer] = "adam",
        early_stopping_min_delta: float = 0.001,
        early_stopping_patience: int = 10,
        reduce_lr_min_delta: float = 0.001,
        reduce_lr_patience: int = 5,
        early_stopping_monitor: str = "loss",
        early_stopping_mode: str = "min",
        reduce_lr_monitor: str = "loss",
        reduce_lr_mode: str = "min",
        reduce_lr_factor: float = 0.9,
        use_class_weights: bool = True,
        random_state: int = 42,
        use_simmetric_normalized_laplacian: bool = True,
        use_node_embedding: bool = False,
        node_embedding_size: int = 50,
        use_node_type_embedding: bool = False,
        node_type_embedding_size: int = 50,
        handling_multi_graph: str = "warn",
        node_feature_names: Optional[Union[str, List[str]]] = None,
        node_type_feature_names: Optional[Union[str, List[str]]] = None,
        verbose: bool = True
    ):
        """Create new Kipf GCN object.

        Parameters
        -------------------------------
        epochs: int = 1000
            Epochs to train the model for.
        number_of_graph_convolution_layers: int = 3
            Number of graph convolution layer.
        number_of_units_per_graph_convolution_layers: Union[int, List[int]] = 128
            Number of units per hidden layer.
        dropout_rate: float = 0.3
            Float between 0 and 1.
            Fraction of the input units to dropout.
        apply_norm: bool = False
            Whether to normalize the output of the convolution operations,
            after applying the level activations.
        combiner: str = "mean"
            A string specifying the reduction op.
            Currently "mean", "sqrtn" and "sum" are supported. 
            "sum" computes the weighted sum of the embedding results for each row.
            "mean" is the weighted sum divided by the total weight.
            "sqrtn" is the weighted sum divided by the square root of the sum of the squares of the weights.
            Defaults to mean.
        optimizer: str = "Adam"
            The optimizer to use while training the model.
        early_stopping_min_delta: float
            Minimum delta of metric to stop the training.
        early_stopping_patience: int
            Number of epochs to wait for when the given minimum delta is not
            achieved after which trigger early stopping.
        reduce_lr_min_delta: float
            Minimum delta of metric to reduce learning rate.
        reduce_lr_patience: int
            Number of epochs to wait for when the given minimum delta is not
            achieved after which reducing learning rate.
        early_stopping_monitor: str = "loss",
            Metric to monitor for early stopping.
        early_stopping_mode: str = "min",
            Direction of the variation of the monitored metric for early stopping.
        reduce_lr_monitor: str = "loss",
            Metric to monitor for reducing learning rate.
        reduce_lr_mode: str = "min",
            Direction of the variation of the monitored metric for learning rate.
        reduce_lr_factor: float = 0.9,
            Factor for reduction of learning rate.
        use_class_weights: bool = True
            Whether to use class weights to rebalance the loss relative to unbalanced classes.
            Learn more about class weights here: https://www.tensorflow.org/tutorials/structured_data/imbalanced_data
        random_state: int = 42
            Random state to reproduce the training samples.
        use_simmetric_normalized_laplacian: bool = True
            Whether to use laplacian transform before training on the graph.
        use_node_embedding: bool = False
            Whether to use a node embedding layer that is automatically learned
            by the model while it trains. Please do be advised that by using
            a node embedding layer you are making a closed-world assumption,
            and this model will not work on graphs with a different node vocabulary.
        node_embedding_size: int = 50
            Dimension of the node embedding.
        use_node_type_embedding: bool = False
            Whether to use a node type embedding layer that is automatically learned
            by the model while it trains. Please do be advised that by using
            a node type embedding layer you are making a closed-world assumption,
            and this model will not work on graphs with a different node vocabulary.
        node_type_embedding_size: int = 50
            Dimension of the node type embedding.
        handling_multi_graph: str = "warn"
            How to behave when dealing with multigraphs.
            Possible behaviours are:
            - "warn"
            - "raise"
            - "drop"
        node_feature_names: Optional[Union[str, List[str]]] = None
            Names of the node features.
            This is used as the layer names.
        node_type_feature_names: Optional[Union[str, List[str]]] = None
            Names of the node type features.
            This is used as the layer names.
        verbose: bool = True
            Whether to show loading bars.
        """
        self._number_of_graph_convolution_layers = number_of_graph_convolution_layers
        self._number_of_units_per_graph_convolution_layers = normalize_model_list_parameter(
            number_of_units_per_graph_convolution_layers,
            number_of_graph_convolution_layers,
            object_type=int,
            can_be_empty=True
        )

        self._combiner = combiner
        self._epochs = epochs
        self._use_class_weights = use_class_weights
        self._dropout_rate = dropout_rate
        self._optimizer = optimizer
        self._use_simmetric_normalized_laplacian = use_simmetric_normalized_laplacian
        self._apply_norm = apply_norm
        self._handling_multi_graph = handling_multi_graph
        self._use_node_embedding = use_node_embedding
        self._node_embedding_size = node_embedding_size
        self._use_node_type_embedding = use_node_type_embedding
        self._node_type_embedding_size = node_type_embedding_size

        if isinstance(node_feature_names, str):
            node_feature_names = [node_feature_names]

        if isinstance(node_type_feature_names, str):
            node_type_feature_names = [node_type_feature_names]

        self._node_feature_names = node_feature_names
        self._node_type_feature_names = node_type_feature_names

        self._early_stopping_min_delta = early_stopping_min_delta
        self._early_stopping_patience = early_stopping_patience
        self._reduce_lr_min_delta = reduce_lr_min_delta
        self._reduce_lr_patience = reduce_lr_patience
        self._early_stopping_monitor = early_stopping_monitor
        self._early_stopping_mode = early_stopping_mode
        self._reduce_lr_monitor = reduce_lr_monitor
        self._reduce_lr_mode = reduce_lr_mode
        self._reduce_lr_factor = reduce_lr_factor

        self._verbose = verbose
        self._model = None
        self.history = None

        super().__init__(random_state=random_state)

    @classmethod
    def smoke_test_parameters(cls) -> Dict[str, Any]:
        """Returns parameters for smoke test."""
        return dict(
            epochs=1,
            number_of_units_per_graph_convolution_layers=2,
            handling_multi_graph="drop"
        )

    def clone(self) -> Type["AbstractGCN"]:
        """Return copy of self."""
        return copy.deepcopy(self)

    def parameters(self) -> Dict[str, Any]:
        """Returns parameters used for this model."""
        return dict(
            number_of_units_per_graph_convolution_layers=self._number_of_units_per_graph_convolution_layers,
            epochs=self._epochs,
            apply_norm=self._apply_norm,
            combiner=self._combiner,
            use_class_weights=self._use_class_weights,
            dropout_rate=self._dropout_rate,
            optimizer=self._optimizer,
            early_stopping_min_delta=self._early_stopping_min_delta,
            early_stopping_patience=self._early_stopping_patience,
            reduce_lr_min_delta=self._reduce_lr_min_delta,
            reduce_lr_patience=self._reduce_lr_patience,
            early_stopping_monitor=self._early_stopping_monitor,
            early_stopping_mode=self._early_stopping_mode,
            reduce_lr_monitor=self._reduce_lr_monitor,
            reduce_lr_mode=self._reduce_lr_mode,
            reduce_lr_factor=self._reduce_lr_factor,
            use_node_embedding=self._use_node_embedding,
            node_embedding_size=self._node_embedding_size,
            use_node_type_embedding=self._use_node_type_embedding,
            node_type_embedding_size=self._node_type_embedding_size
        )

    def plot(
        self,
        show_shapes: bool = True,
        **kwargs: Dict
    ):
        return tf.keras.utils.plot_model(
            self._model,
            show_layer_names=True,
            expand_nested=True,
            show_layer_activations=True,
            show_shapes=show_shapes,
            **kwargs
        )

    def _get_class_weights(self, graph: Graph) -> Dict[int, float]:
        """Returns dictionary with class weights."""
        raise NotImplementedError(
            "The method `get_class_weights` should be implemented "
            "in the child classes of `AbstractGCN`, but is missing "
            f"in the class {self.__class__.__name__}."
        )

    def _get_model_training_input(
        self,
        graph: Graph,
        support: Graph,
        node_features: Optional[List[np.ndarray]] = None,
        node_type_features: Optional[List[np.ndarray]] = None,
        edge_features: Optional[Union[Type[AbstractEdgeFeature], List[np.ndarray]]] = None,
    ) -> Tuple[Union[np.ndarray, Type[Sequence]]]:
        """Returns training input tuple."""
        raise NotImplementedError(
            "The method `get_model_training_input` should be implemented "
            "in the child classes of `AbstractGCN`, but is missing "
            f"in the class {self.__class__.__name__}."
        )

    def _get_model_training_output(
        self,
        graph: Graph,
    ) -> Optional[np.ndarray]:
        """Returns training output tuple."""
        raise NotImplementedError(
            "The method `get_model_training_output` should be implemented "
            "in the child classes of `AbstractGCN`, but is missing "
            f"in the class {self.__class__.__name__}."
        )

    def _get_model_training_sample_weights(
        self,
        graph: Graph,
    ) -> Optional[np.ndarray]:
        """Returns training output tuple."""
        raise NotImplementedError(
            "The method `_get_model_training_sample_weights` should be implemented "
            "in the child classes of `AbstractGCN`, but is missing "
            f"in the class {self.__class__.__name__}."
        )

    def _get_model_prediction_input(
        self,
        graph: Graph,
        support: Graph,
        node_features: Optional[List[np.ndarray]] = None,
        node_type_features: Optional[List[np.ndarray]] = None,
        edge_features: Optional[Union[Type[AbstractEdgeFeature], List[Union[np.ndarray, Type[AbstractEdgeFeature]]]]] = None,
    ) -> Tuple[Union[np.ndarray, Type[Sequence]]]:
        """Returns dictionary with class weights."""
        raise NotImplementedError(
            "The method `get_model_prediction_input` should be implemented "
            "in the child classes of `AbstractGCN`, but is missing "
            f"in the class {self.__class__.__name__}."
        )

    def _build_model(
        self,
        graph: Graph,
        graph_convolution_model: Model,
        edge_features: Optional[Union[Type[AbstractEdgeFeature], List[Union[np.ndarray, Type[AbstractEdgeFeature]]]]] = None,
    ) -> Type[Model]:
        """Returns GCN model."""
        raise NotImplementedError(
            "The method `_build_model` should be implemented "
            "in the child classes of `AbstractGCN`, but is missing "
            f"in the class {self.__class__.__name__}."
        )

    def _build_graph_convolution_model(
        self,
        graph: Graph,
        node_features: Optional[List[np.ndarray]] = None,
        node_type_features: Optional[List[np.ndarray]] = None,
    ) -> Model:
        """Create new GCN model."""
        # If we make the node embedding, we are making a closed world assumption,
        # while without we do not have them we can keep an open world assumption.
        # Basically, without node embedding we can have different vocabularies,
        # while with node embedding the vocabulary becomes fixed.
        nodes_number = graph.get_number_of_nodes() if self._use_node_embedding else None

        # We create the list we will use to collect the input features.
        input_features = []

        if self.has_convolutional_layers():
            # Input layer for the adjacency matrix. Do note that we can use in this
            # model multiple adjacency matrices because we are building it with an
            # open world assumption in mind. This means that we can train the model
            # and use it to run predictions on one
            # or more graphs that can have different nodes and edges.
            adjacency_matrix = Input(
                shape=(nodes_number,),
                batch_size=nodes_number,
                sparse=True,
                name=(
                    "Laplacian Matrix" if self._use_simmetric_normalized_laplacian else "Adjacency Matrix")
            )
        else:
            adjacency_matrix = None

        # We create the input layers for all of the node and node type features.

        for features, feature_names, feature_category in (
            (node_features, self._node_feature_names, "node feature"),
            (node_type_features, self._node_type_feature_names, "node type feature"),
        ):
            if features is not None:
                if feature_names is None:
                    feature_names = [
                        f"{number_to_ordinal(i+1)} {feature_category}"
                        for i in range(len(features))
                    ]
                if len(feature_names) != len(features):
                    raise ValueError(
                        f"You have provided {len(feature_names)} "
                        f"{feature_category} names but you have provided {len(features)} "
                        f"{feature_category}s to the model."
                    )
                input_features.extend([
                    Input(
                        shape=node_feature.shape[1:],
                        batch_size=nodes_number,
                        name=node_feature_name,
                    )
                    for node_feature, node_feature_name in zip(
                        features,
                        feature_names
                    )
                ])

        hidden = [*input_features]

        if self._use_node_embedding:
            node_ids = Input(
                shape=(1,),
                batch_size=nodes_number,
                name="Nodes",
                dtype=tf.int32
            )
            input_features.append(node_ids)

            node_embedding = FlatEmbedding(
                vocabulary_size=graph.get_number_of_nodes(),
                dimension=self._node_embedding_size,
                input_length=1,
                name="NodesEmbedding"
            )(node_ids)
            hidden.append(node_embedding)

        if self._use_node_type_embedding:
            node_type_ids = Input(
                shape=(graph.get_maximum_multilabel_count(),),
                batch_size=nodes_number,
                name="Node Types",
                dtype=tf.int32
            )
            input_features.append(node_type_ids)

            node_type_embedding = FlatEmbedding(
                vocabulary_size=graph.get_number_of_nodes(),
                dimension=self._node_embedding_size,
                input_length=graph.get_maximum_multilabel_count(),
                mask_zero=(
                    graph.has_multilabel_node_types() or
                    graph.has_unknown_node_types()
                ),
                name="NodeTypesEmbedding"
            )(node_type_ids)
            hidden.append(node_type_embedding)

        # Building the body of the model.
        for i, units in enumerate(self._number_of_units_per_graph_convolution_layers):
            hidden = GraphConvolution(
                units=units,
                combiner=self._combiner,
                dropout_rate=self._dropout_rate,
                apply_norm=self._apply_norm,
                name=f"{number_to_ordinal(i+1)}GraphConvolution"
            )((adjacency_matrix, *hidden))

        # Returning the convolutional portion of the model.
        return Model(
            inputs=[
                input_layer
                for input_layer in (
                    adjacency_matrix,
                    *input_features
                )
                if input_layer is not None
            ],
            outputs=(
                Concatenate(
                    name="ConcatenatedNodeFeatures",
                    axis=-1
                )(hidden)
                if len(hidden) > 1
                else hidden[0]
            )
        )

    def _fit(
        self,
        graph: Graph,
        support: Optional[Graph] = None,
        node_features: Optional[List[np.ndarray]] = None,
        node_type_features: Optional[List[np.ndarray]] = None,
        edge_features: Optional[Union[Type[AbstractEdgeFeature], List[Union[np.ndarray, Type[AbstractEdgeFeature]]]]] = None,
    ) -> pd.DataFrame:
        """Return pandas dataframe with training history.

        Parameters
        -----------------------
        graph: Graph,
            The graph whose edges are to be embedded and edge types extracted.
            It can either be an Graph or a list of lists of edges.
        support: Optional[Graph] = None
            The graph describiding the topological structure that
            includes also the above graph.
        node_features: Optional[List[np.ndarray]]
            The node features to be used in the training of the model.
        node_type_features: Optional[List[np.ndarray]]
            The node type features to be used in the training of the model.
        edge_features: Optional[Union[Type[AbstractEdgeFeature], List[Union[np.ndarray, Type[AbstractEdgeFeature]]]]] = None
            The edge features to be used in the training of the model.

        Returns
        -----------------------
        Dataframe with training history.
        """
        try:
            from tqdm.keras import TqdmCallback
            traditional_verbose = False
        except AttributeError:
            traditional_verbose = True

        if node_features is None and not self._use_node_embedding:
            raise ValueError(
                "Neither node features were provided nor the node "
                "embedding was enabled through the `use_node_embedding` "
                "parameter. If you do not provide node features or use an embedding layer "
                "it does not make sense to use a GCN model."
            )

        if support is None:
            support = graph

        class_weight = self._get_class_weights(
            graph) if self._use_class_weights else None

        if self._model is None:
            self._model: Type[Model] = self._build_model(
                support,
                graph_convolution_model=self._build_graph_convolution_model(
                    graph,
                    node_features=node_features,
                    node_type_features=node_type_features
                ),
                edge_features=edge_features,
            )

        # In a GCN model, the batch size is the number of nodes.
        batch_size = graph.get_number_of_nodes()

        # Within the expected input shapes, we do not have the batch size itself.
        # The batch size is left implicit as a None value, but we need to add it
        # to the expected input shapes to check that the input shapes are correct.

        expected_input_shapes = {
            input_layer.name: tuple([
                batch_size if dimension is None else dimension
                for dimension in tuple(input_layer.shape)
            ])
            for input_layer in self._model.inputs
        }

        model_input = self._get_model_training_input(
            graph,
            support=support,
            edge_features=edge_features,
            node_type_features=node_type_features,
            node_features=node_features
        )

        if not isinstance(model_input, tuple) and not issubclass(type(model_input), Sequence):
            raise RuntimeError(
                "The model input should be a subclass of `Sequence` or a tuple "
                f"but it is `{type(model_input)}`. "
                "This is an internal error, please open an issue at "
                "GRAPE's GitHub page."
            )

        if issubclass(type(model_input), Sequence):
            sequence_input_shapes = [
                tuple(feature.shape)
                for feature in model_input[0][0]
            ]
        elif isinstance(model_input, tuple):
            sequence_input_shapes = [
                tuple(feature.shape)
                for feature in model_input
            ]
        else:
            raise RuntimeError(
                "The model input should be a subclass of `Sequence` or a tuple "
                f"but it is `{type(model_input)}`. "
                "This is an internal error, please open an issue at "
                "GRAPE's GitHub page."
            )

        if len(expected_input_shapes) != len(sequence_input_shapes):
            raise RuntimeError(
                f"We expected {len(expected_input_shapes)} inputs "
                f"and we received {len(sequence_input_shapes)} inputs. "
                "Specifically, the input shapes we expected were "
                f"{expected_input_shapes}, but the training sequence "
                f"provided the input shapes {sequence_input_shapes}. "
                "This is an internal error, please open an issue at "
                "GRAPE's GitHub page."
            )

        for (layer_name, layer_input_shape), input_shape in zip(
            expected_input_shapes.items(),
            sequence_input_shapes
        ):
            if layer_input_shape != input_shape:
                raise RuntimeError(
                    f"We expected {len(expected_input_shapes)} inputs "
                    f"and we received {len(sequence_input_shapes)} inputs. "
                    f"The input shape of the layer `{layer_name}` "
                    f"should be `{layer_input_shape}` but it is `{input_shape}`. "
                    "Specifically, the input shapes we expected were "
                    f"{expected_input_shapes}, but the training sequence "
                    f"provided the input shapes {sequence_input_shapes}. "
                    "This is an internal error, please open an issue at "
                    "GRAPE's GitHub page."
                )

        self.history = self._model.fit(
            x=model_input,
            y=self._get_model_training_output(graph),
            sample_weight=self._get_model_training_sample_weights(graph),
            epochs=self._epochs,
            verbose=traditional_verbose and self._verbose > 0,
            batch_size=batch_size,
            shuffle=False,
            class_weight=class_weight,
            callbacks=[
                EarlyStopping(
                    monitor=self._early_stopping_monitor,
                    min_delta=self._early_stopping_min_delta,
                    patience=self._early_stopping_patience,
                    mode=self._early_stopping_mode,
                ),
                ReduceLROnPlateau(
                    monitor=self._reduce_lr_monitor,
                    min_delta=self._reduce_lr_min_delta,
                    patience=self._reduce_lr_patience,
                    factor=self._reduce_lr_factor,
                    mode=self._reduce_lr_mode,
                ),
                *((TqdmCallback(
                    verbose=1 if "edge" in self.task_name().lower() else 0,
                    leave=False
                ),)
                    if not traditional_verbose and self._verbose > 0 else ()),
            ],
        )

    def _predict_proba(
        self,
        graph: Graph,
        support: Optional[Graph] = None,
        node_features: Optional[List[np.ndarray]] = None,
        node_type_features: Optional[List[np.ndarray]] = None,
        edge_features: Optional[Union[Type[AbstractEdgeFeature], List[Union[np.ndarray, Type[AbstractEdgeFeature]]]]] = None,
    ) -> pd.DataFrame:
        """Run predictions on the provided graph."""
        if not graph.has_edges():
            return np.array([])

        if support is None:
            support = graph

        model_input = self._get_model_prediction_input(
            graph,
            support,
            node_features,
            node_type_features,
            edge_features,
        )

        return self._model.predict(
            model_input,
            batch_size=support.get_number_of_nodes(),
            verbose=False
        )

    def _predict(
        self,
        graph: Graph,
        support: Graph,
        node_features: Optional[List[np.ndarray]] = None,
        node_type_features: Optional[List[np.ndarray]] = None,
        edge_features: Optional[Union[Type[AbstractEdgeFeature], List[Union[np.ndarray, Type[AbstractEdgeFeature]]]]] = None,
    ) -> pd.DataFrame:
        """Run predictions on the provided graph."""
        predictions = self._predict_proba(
            graph,
            support,
            node_features=node_features,
            node_type_features=node_type_features,
            edge_features=edge_features
        )

        if (
            self.is_binary_prediction_task() or
            self.is_multilabel_prediction_task()
        ):
            return predictions > 0.5

        return predictions.argmax(axis=-1)

    def get_output_activation_name(self) -> str:
        """Return activation of the output."""
        # Adding the last layer of the model.
        if (
            self.is_binary_prediction_task() or
            self.is_multilabel_prediction_task()
        ):
            return "sigmoid"
        return "softmax"

    def get_loss_name(self) -> str:
        """Return model loss."""
        # Adding the last layer of the model.
        if (
            self.is_binary_prediction_task() or
            self.is_multilabel_prediction_task()
        ):
            return "binary_crossentropy"
        return "sparse_categorical_crossentropy"

    def get_output_classes(self, graph: Graph) -> int:
        """Returns number of output classes."""
        raise NotImplementedError(
            "The method `get_output_classes` should be implemented "
            "in the child classes of `AbstractGCN`, but is missing "
            f"in the class {self.__class__.__name__}."
        )

    def has_convolutional_layers(self) -> bool:
        """Returns whether the present model has convolutional layers."""
        return self._number_of_graph_convolution_layers

    def convert_graph_to_kernel(self, graph: Graph) -> Optional[tf.SparseTensor]:
        """Returns provided graph converted to a sparse Tensor.

        Implementation details
        ---------------------------
        Do note that when the model does not have convolutional layers
        the model will return None, as to avoid allocating like object for
        apparently no reason.
        """
        if not self.has_convolutional_layers():
            return None
        return graph_to_sparse_tensor(
            graph,
            use_weights=graph.has_edge_weights() and not self._use_simmetric_normalized_laplacian,
            use_simmetric_normalized_laplacian=self._use_simmetric_normalized_laplacian,
            handling_multi_graph=self._handling_multi_graph
        )

    @classmethod
    def requires_edge_weights(cls) -> bool:
        return False

    @classmethod
    def requires_positive_edge_weights(cls) -> bool:
        return False

    @classmethod
    def library_name(cls) -> str:
        """Return name of the model."""
        return "TensorFlow"

    @classmethod
    def can_use_edge_weights(cls) -> bool:
        """Returns whether the model can optionally use edge weights."""
        return True

    def is_using_edge_weights(self) -> bool:
        """Returns whether the model is parametrized to use edge weights."""
        return not self._use_simmetric_normalized_laplacian

    @classmethod
    def load(cls, path: str) -> "Self":
        """Load a saved version of the model from the provided path.

        Parameters
        -------------------
        path: str
            Path from where to load the model.
        """
        with tf.keras.utils.custom_object_scope({
            "GraphConvolution": GraphConvolution,
            "EmbeddingLookup": EmbeddingLookup,
            "FlatEmbedding": FlatEmbedding,
            "L2Norm": L2Norm
        }):
            return compress_pickle.load(path)

    def dump(self, path: str):
        """Dump the current model at the provided path.

        Parameters
        -------------------
        path: str
            Path from where to dump the model.
        """
        compress_pickle.dump(self, path)
