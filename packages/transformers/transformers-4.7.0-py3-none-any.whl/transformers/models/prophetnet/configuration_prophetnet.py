# coding=utf-8
# Copyright 2020 The Microsoft Authors and The HuggingFace Inc. team.
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
""" ProphetNet model configuration """


from ...configuration_utils import PretrainedConfig
from ...utils import logging


logger = logging.get_logger(__name__)

PROPHETNET_PRETRAINED_CONFIG_ARCHIVE_MAP = {
    "microsoft/prophetnet-large-uncased": "https://huggingface.co/microsoft/prophetnet-large-uncased/resolve/main/config.json",
}


class ProphetNetConfig(PretrainedConfig):
    r"""
    This is the configuration class to store the configuration of a :class:`~transformers.ProphetNetModel`. It is used
    to instantiate a ProphetNet model according to the specified arguments, defining the model architecture.

    Configuration objects inherit from :class:`~transformers.PretrainedConfig` and can be used to control the model
    outputs. Read the documentation from :class:`~transformers.PretrainedConfig` for more information.

    Args:
        activation_dropout (:obj:`float`, `optional`, defaults to 0.1):
            The dropout ratio for activations inside the fully connected layer.
        activation_function (:obj:`str` or :obj:`function`, `optional`, defaults to :obj:`"gelu"`):
            The non-linear activation function (function or string) in the encoder and pooler. If string,
            :obj:`"gelu"`, :obj:`"relu"`, :obj:`"silu"` and :obj:`"gelu_new"` are supported.
        vocab_size (:obj:`int`, `optional`, defaults to 30522):
            Vocabulary size of the ProphetNET model. Defines the number of different tokens that can be represented by
            the :obj:`inputs_ids` passed when calling :class:`~transformers.ProphetNetModel`.
        hidden_size (:obj:`int`, `optional`, defaults to 1024):
            Dimensionality of the layers and the pooler layer.
        encoder_ffn_dim (:obj:`int`, `optional`, defaults to 4096):
            Dimensionality of the "intermediate" (often named feed-forward) layer in decoder.
        num_encoder_layers (:obj:`int`, `optional`, defaults to 12):
            Number of encoder layers.
        num_encoder_attention_heads (:obj:`int`, `optional`, defaults to 16):
            Number of attention heads for each attention layer in the Transformer encoder.
        decoder_ffn_dim (:obj:`int`, `optional`, defaults to 4096):
            Dimensionality of the ``intermediate`` (often named feed-forward) layer in decoder.
        num_decoder_layers (:obj:`int`, `optional`, defaults to 12):
            Number of decoder layers.
        num_decoder_attention_heads (:obj:`int`, `optional`, defaults to 16):
            Number of attention heads for each attention layer in the Transformer decoder.
        attention_dropout (:obj:`float`, `optional`, defaults to 0.1):
            The dropout ratio for the attention probabilities.
        dropout (:obj:`float`, `optional`, defaults to 0.1):
            The dropout probability for all fully connected layers in the embeddings, encoder, and pooler.
        max_position_embeddings (:obj:`int`, `optional`, defaults to 512):
            The maximum sequence length that this model might ever be used with. Typically set this to something large
            just in case (e.g., 512 or 1024 or 2048).
        init_std (:obj:`float`, `optional`, defaults to 0.02):
            The standard deviation of the truncated_normal_initializer for initializing all weight matrices.
        add_cross_attention (:obj:`bool`, `optional`, defaults to :obj:`True`):
            Whether cross-attention layers should be added to the model.
        is_encoder_decoder (:obj:`bool`, `optional`, defaults to :obj:`True`):
            Whether this is an encoder/decoder model.
        pad_token_id (:obj:`int`, `optional`, defaults to 1)
            Padding token id.
        bos_token_id (:obj:`int`, `optional`, defaults to 0)
            Beginning of stream token id.
        eos_token_id (:obj:`int`, `optional`, defaults to 2)
            End of stream token id.
        ngram (:obj:`int`, `optional`, defaults to 2)
            Number of future tokens to predict. Set to 1 to be same as traditional Language model to predict next first
            token.
        num_buckets (:obj:`int`, `optional`, defaults to 32)
            The number of buckets to use for each attention layer. This is for relative position calculation. See the
            `T5 paper <see https://arxiv.org/abs/1910.10683>`__ for more details.
        relative_max_distance (:obj:`int`, `optional`, defaults to 128)
            Relative distances greater than this number will be put into the last same bucket. This is for relative
            position calculation. See the `T5 paper <see https://arxiv.org/abs/1910.10683>`__ for more details.
        disable_ngram_loss (:obj:`bool`, `optional`, defaults to :obj:`False`):
            Whether be trained predicting only the next first token.
        eps (:obj:`float`, `optional`, defaults to 0.0):
            Controls the ``epsilon`` parameter value for label smoothing in the loss calculation. If set to 0, no label
            smoothing is performed.
        use_cache (:obj:`bool`, `optional`, defaults to :obj:`True`):
            Whether or not the model should return the last key/values attentions (not used by all models).
        gradient_checkpointing (:obj:`bool`, `optional`, defaults to :obj:`False`):
            If True, use gradient checkpointing to save memory at the expense of slower backward pass.
    """
    model_type = "prophetnet"
    keys_to_ignore_at_inference = ["past_key_values"]

    def __init__(
        self,
        activation_dropout=0.1,
        activation_function="gelu",
        vocab_size=30522,
        hidden_size=1024,
        encoder_ffn_dim=4096,
        num_encoder_layers=12,
        num_encoder_attention_heads=16,
        decoder_ffn_dim=4096,
        num_decoder_layers=12,
        num_decoder_attention_heads=16,
        attention_dropout=0.1,
        dropout=0.1,
        max_position_embeddings=512,
        init_std=0.02,
        is_encoder_decoder=True,
        add_cross_attention=True,
        decoder_start_token_id=0,
        ngram=2,
        num_buckets=32,
        relative_max_distance=128,
        disable_ngram_loss=False,
        gradient_checkpointing=False,
        eps=0.0,
        use_cache=True,
        pad_token_id=0,
        bos_token_id=1,
        eos_token_id=2,
        **kwargs
    ):
        super().__init__(
            pad_token_id=pad_token_id,
            bos_token_id=bos_token_id,
            eos_token_id=eos_token_id,
            is_encoder_decoder=is_encoder_decoder,
            add_cross_attention=add_cross_attention,
            decoder_start_token_id=decoder_start_token_id,
            **kwargs,
        )
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.encoder_ffn_dim = encoder_ffn_dim
        self.num_encoder_layers = num_encoder_layers
        self.num_encoder_attention_heads = num_encoder_attention_heads
        self.decoder_ffn_dim = decoder_ffn_dim
        self.num_decoder_layers = num_decoder_layers
        self.num_decoder_attention_heads = num_decoder_attention_heads
        self.max_position_embeddings = max_position_embeddings
        self.init_std = init_std  # Normal(0, this parameter)
        self.activation_function = activation_function

        # parameters for prophetnet
        self.ngram = ngram
        self.num_buckets = num_buckets
        self.relative_max_distance = relative_max_distance
        self.disable_ngram_loss = disable_ngram_loss
        self.eps = eps

        # 3 Types of Dropout
        self.attention_dropout = attention_dropout
        self.activation_dropout = activation_dropout
        self.dropout = dropout

        self.use_cache = use_cache

        # 4 Training Args (should be removed soon)
        self.gradient_checkpointing = gradient_checkpointing

    @property
    def num_attention_heads(self) -> int:
        return self.num_encoder_attention_heads

    @property
    def num_hidden_layers(self) -> int:
        return self.num_encoder_layers + self.num_decoder_layers
