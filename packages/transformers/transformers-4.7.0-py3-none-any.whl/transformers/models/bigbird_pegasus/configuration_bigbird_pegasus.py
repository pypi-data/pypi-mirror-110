# coding=utf-8
# Copyright Google Research and The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" BigBirdPegasus model configuration """

from ...configuration_utils import PretrainedConfig
from ...utils import logging


logger = logging.get_logger(__name__)

BIGBIRD_PEGASUS_PRETRAINED_CONFIG_ARCHIVE_MAP = {
    "google/bigbird-pegasus-large-arxiv": "https://huggingface.co/google/bigbird-pegasus-large-arxiv/resolve/main/config.json",
    "google/bigbird-pegasus-large-pubmed": "https://huggingface.co/google/bigbird-pegasus-large-pubmed/resolve/main/config.json",
    "google/bigbird-pegasus-large-bigpatent": "https://huggingface.co/google/bigbird-pegasus-large-bigpatent/resolve/main/config.json",
    # See all BigBirdPegasus models at https://huggingface.co/models?filter=bigbird_pegasus
}


class BigBirdPegasusConfig(PretrainedConfig):
    r"""
    This is the configuration class to store the configuration of a :class:`~transformers.BigBirdPegasusModel`. It is
    used to instantiate an BigBirdPegasus model according to the specified arguments, defining the model architecture.
    Instantiating a configuration with the defaults will yield a similar configuration to that of the BigBirdPegasus
    `google/bigbird-pegasus-large-arxiv <https://huggingface.co/google/bigbird-pegasus-large-arxiv>`__ architecture.

    Configuration objects inherit from :class:`~transformers.PretrainedConfig` and can be used to control the model
    outputs. Read the documentation from :class:`~transformers.PretrainedConfig` for more information.


    Args:
        vocab_size (:obj:`int`, `optional`, defaults to 96103):
            Vocabulary size of the BigBirdPegasus model. Defines the number of different tokens that can be represented
            by the :obj:`inputs_ids` passed when calling :class:`~transformers.BigBirdPegasusModel`.
        d_model (:obj:`int`, `optional`, defaults to 1024):
            Dimension of the layers and the pooler layer.
        encoder_layers (:obj:`int`, `optional`, defaults to 16):
            Number of encoder layers.
        decoder_layers (:obj:`int`, `optional`, defaults to 16):
            Number of decoder layers.
        encoder_attention_heads (:obj:`int`, `optional`, defaults to 16):
            Number of attention heads for each attention layer in the Transformer encoder.
        decoder_attention_heads (:obj:`int`, `optional`, defaults to 16):
            Number of attention heads for each attention layer in the Transformer decoder.
        decoder_ffn_dim (:obj:`int`, `optional`, defaults to 4096):
            Dimension of the "intermediate" (often named feed-forward) layer in decoder.
        encoder_ffn_dim (:obj:`int`, `optional`, defaults to 4096):
            Dimension of the "intermediate" (often named feed-forward) layer in decoder.
        activation_function (:obj:`str` or :obj:`function`, `optional`, defaults to :obj:`"gelu_new"`):
            The non-linear activation function (function or string) in the encoder and pooler. If string,
            :obj:`"gelu"`, :obj:`"relu"`, :obj:`"silu"` and :obj:`"gelu_new"` are supported.
        dropout (:obj:`float`, `optional`, defaults to 0.1):
            The dropout probability for all fully connected layers in the embeddings, encoder, and pooler.
        attention_dropout (:obj:`float`, `optional`, defaults to 0.0):
            The dropout ratio for the attention probabilities.
        activation_dropout (:obj:`float`, `optional`, defaults to 0.0):
            The dropout ratio for activations inside the fully connected layer.
        classifier_dropout (:obj:`float`, `optional`, defaults to 0.0):
            The dropout ratio for classifier.
        max_position_embeddings (:obj:`int`, `optional`, defaults to 4096):
            The maximum sequence length that this model might ever be used with. Typically set this to something large
            just in case (e.g., 1024 or 2048 or 4096).
        init_std (:obj:`float`, `optional`, defaults to 0.02):
            The standard deviation of the truncated_normal_initializer for initializing all weight matrices.
        encoder_layerdrop: (:obj:`float`, `optional`, defaults to 0.0):
            The LayerDrop probability for the encoder. See the `LayerDrop paper <see
            https://arxiv.org/abs/1909.11556>`__ for more details.
        decoder_layerdrop: (:obj:`float`, `optional`, defaults to 0.0):
            The LayerDrop probability for the decoder. See the `LayerDrop paper <see
            https://arxiv.org/abs/1909.11556>`__ for more details.
        use_cache (:obj:`bool`, `optional`, defaults to :obj:`True`):
            Whether or not the model should return the last key/values attentions (not used by all models).
        attention_type (:obj:`str`, `optional`, defaults to :obj:`"block_sparse"`)
            Whether to use block sparse attention (with n complexity) as introduced in paper or original attention
            layer (with n^2 complexity) in encoder. Possible values are :obj:`"original_full"` and
            :obj:`"block_sparse"`.
        use_bias (:obj:`bool`, `optional`, defaults to :obj:`False`)
            Whether to use bias in query, key, value.
        block_size (:obj:`int`, `optional`, defaults to 64)
            Size of each block. Useful only when :obj:`attention_type == "block_sparse"`.
        num_random_blocks (:obj:`int`, `optional`, defaults to 3)
            Each query is going to attend these many number of random blocks. Useful only when :obj:`attention_type ==
            "block_sparse"`.
        scale_embeddings (:obj:`bool`, `optional`, defaults to :obj:`True`)
            Whether to rescale embeddings with (hidden_size ** 0.5).
        gradient_checkpointing (:obj:`bool`, `optional`, defaults to :obj:`False`):
            If True, use gradient checkpointing to save memory at the expense of slower backward pass.

        Example::

        >>> from transformers import BigBirdPegasusModel, BigBirdPegasusConfig

        >>> # Initializing a BigBirdPegasus bigbird-pegasus-base style configuration
        >>> configuration = BigBirdPegasusConfig()

        >>> # Initializing a model from the bigbird-pegasus-base style configuration
        >>> model = BigBirdPegasusModel(configuration)

        >>> # Accessing the model configuration
        >>> configuration = model.config
    """
    model_type = "bigbird_pegasus"
    keys_to_ignore_at_inference = ["past_key_values"]

    def __init__(
        self,
        vocab_size=96103,
        max_position_embeddings=4096,
        encoder_layers=16,
        encoder_ffn_dim=4096,
        encoder_attention_heads=16,
        decoder_layers=16,
        decoder_ffn_dim=4096,
        decoder_attention_heads=16,
        encoder_layerdrop=0.0,
        decoder_layerdrop=0.0,
        use_cache=True,
        is_encoder_decoder=True,
        activation_function="gelu_new",
        d_model=1024,
        dropout=0.1,
        attention_dropout=0.0,
        activation_dropout=0.0,
        init_std=0.02,
        decoder_start_token_id=2,
        classifier_dropout=0.0,
        scale_embedding=True,
        gradient_checkpointing=False,
        pad_token_id=0,
        bos_token_id=2,
        eos_token_id=1,
        attention_type="block_sparse",  # only for encoder
        block_size=64,
        num_random_blocks=3,
        use_bias=False,
        **kwargs
    ):
        super().__init__(
            pad_token_id=pad_token_id,
            bos_token_id=bos_token_id,
            eos_token_id=eos_token_id,
            is_encoder_decoder=is_encoder_decoder,
            decoder_start_token_id=decoder_start_token_id,
            **kwargs,
        )

        self.vocab_size = vocab_size
        self.max_position_embeddings = max_position_embeddings
        self.d_model = d_model
        self.encoder_ffn_dim = encoder_ffn_dim
        self.encoder_layers = encoder_layers
        self.encoder_attention_heads = encoder_attention_heads
        self.decoder_ffn_dim = decoder_ffn_dim
        self.decoder_layers = decoder_layers
        self.decoder_attention_heads = decoder_attention_heads
        self.dropout = dropout
        self.attention_dropout = attention_dropout
        self.activation_dropout = activation_dropout
        self.activation_function = activation_function
        self.init_std = init_std
        self.encoder_layerdrop = encoder_layerdrop
        self.decoder_layerdrop = decoder_layerdrop
        self.classifier_dropout = classifier_dropout
        self.use_cache = use_cache
        self.num_hidden_layers = encoder_layers
        self.gradient_checkpointing = gradient_checkpointing
        self.scale_embedding = scale_embedding  # scale factor will be sqrt(d_model) if True

        # extra config
        self.attention_type = attention_type
        self.block_size = block_size
        self.num_random_blocks = num_random_blocks
        self.use_bias = use_bias

    @property
    def num_attention_heads(self) -> int:
        return self.encoder_attention_heads

    @property
    def hidden_size(self) -> int:
        return self.d_model

    @property
    def attention_probs_dropout_prob(self) -> float:
        return self.attention_dropout
