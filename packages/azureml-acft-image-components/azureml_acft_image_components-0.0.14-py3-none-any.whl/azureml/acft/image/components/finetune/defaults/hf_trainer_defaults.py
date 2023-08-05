# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Finetuning component HuggingFace Trainer defaults."""

from dataclasses import dataclass


@dataclass
class HFTrainerDefaults:
    """
    This class contain Hugging Face trainer defaults

    Note: This class is not meant to be used directly.
    Provide the defaults name consistently with the Hugging Face Trainer class.
    """

    _num_train_epochs: int = 3
    _per_device_train_batch_size: int = 8
    _per_device_eval_batch_size: int = 8
    _learning_rate: float = 5e-5
    _optim: str = "adamw_hf"
    _gradient_accumulation_steps: int = 1
    _max_steps: int = -1
    _auto_find_batch_size: bool = False
    _evaluation_strategy: str = "steps"
    _eval_steps: int = 500
    _save_strategy: str = "steps"
    _save_steps: int = 500
    _logging_strategy: str = "steps"
    _logging_steps: int = 500
    _warmup_steps: int = 0
    _weight_decay: float = 0.0
    _adam_beta1: float = 0.9
    _adam_beta2: float = 0.999
    _adam_epsilon: float = 1e-8
    _lr_scheduler_type: str = "linear"
    _dataloader_num_workers: int = 0
    _seed: int = 42
    _save_total_limit: int = 1
    _metric_for_best_model: str = "loss"
    _label_smoothing_factor: float = 0.0
    _max_grad_norm: float = 1.0
