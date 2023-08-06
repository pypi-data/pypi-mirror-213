# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RocketQA文本向量

Authors: fubo
Date: 2023/1/29 10:46:00
"""
import copy
import logging
from enum import Enum
from typing import List
import numpy
from pydantic import BaseModel
from rocketqa import rocketqa


class ModelType(Enum):
    # 加载全部模型
    BOTH = 0

    # 仅加载embedding模型
    EMBEDDING_ONLY = 1

    # 仅加载相关性计算模型
    SIMILARITY_ONLY = 2


class RocketQAConfig(BaseModel):
    # rocket qa dual模型
    model_name_dual: str = "zh_dureader_de"

    # rocket qa cross模型
    model_name_cross: str = "zh_dureader_ce"

    # rocket qa dual模型使用的GPU index
    gpu_idx_dual: int = -1

    # rocket qa dual模型使用的batch size
    batch_size_dual: int = 4

    # rocket qa cross模型使用的GPU index
    gpu_idx_cross: int = -1

    # rocket qa cross模型使用的batch size
    batch_size_cross: int = 4

    # 只加载embedding模型
    model_type: str = "BOTH"


class RocketQASentSimEmbedding(object):
    def __init__(self, config: RocketQAConfig):
        self.config: RocketQAConfig = config
        self.model_type: ModelType = ModelType.__members__.get(self.config.model_type, ModelType.BOTH)
        self.vectorize_valid: bool = False
        self.similarity_valid: bool = False
        if self.model_type == ModelType.BOTH or self.model_type == ModelType.EMBEDDING_ONLY:
            self.vectorize_valid = True
            logging.info("Load RocketQA dual model by config")
            # 加载dual模型
            self.vectorize = rocketqa.load_model(
                model=self.config.model_name_dual,
                use_cuda=True if self.config.gpu_idx_dual >= 0 else False,
                device_id=self.config.gpu_idx_dual,
                batch_size=self.config.batch_size_dual
            )

        if self.model_type == ModelType.BOTH or self.model_type == ModelType.SIMILARITY_ONLY:
            self.similarity_valid = True
            logging.info("Load RocketQA cross model by config")
            # 加载cross模型
            self.similarity = rocketqa.load_model(
                model=self.config.model_name_cross,
                use_cuda=True if self.config.gpu_idx_cross >= 0 else False,
                device_id=self.config.gpu_idx_cross,
                batch_size=self.config.batch_size_cross
            )

    def doc_embedding(self, para: List[str], normalize: bool = True, title: List[str] = None) -> List[List[float]]:
        """
        doc embedding
        :param para 文档embedding
        :param title 标题embedding
        :param normalize 是否需要归一化
        """
        logging.info("Got docs for embedding count=%d" % len(para))
        if self.vectorize_valid is False:
            raise RuntimeError("Load embedding model first for doc embedding")

        if title is None:
            title = []

        if len(para) == 0:
            return []

        return [
            copy.deepcopy(
                (vec / numpy.linalg.norm(vec) if normalize else vec).tolist()
            ) for index, vec in enumerate(self.vectorize.encode_para(para=para, title=title))
        ]

    def query_embedding(self, queries: List[str], normalize: bool = True) -> List[List[float]]:
        """
        短文本embedding
        :param queries 短文本
        :param normalize 是否需要归一化
        """
        logging.info("Got queries for embedding count=%d" % len(queries))
        if self.vectorize_valid is False:
            raise RuntimeError("Load embedding model first for query embedding")

        if len(queries) == 0:
            return []

        return [
            copy.deepcopy(
                (vec / numpy.linalg.norm(vec) if normalize else vec).tolist()
            ) for index, vec in enumerate(self.vectorize.encode_query(query=queries))
        ]

    def similarity_calc(self, queries: List[str], para: List[str], title: List[str] = None) -> List[float]:
        """
        相关性计算
        :param queries 输入query
        :param para 文档内容
        :param title 文档标题
        """
        logging.info("Got similarity calculation count=%d" % len(queries))
        if self.similarity_valid is False:
            raise RuntimeError("Load similarity model first for similarity calculation")

        if title is None:
            title = []

        if len(queries) != len(para):
            return []

        if len(queries) == 0:
            return []

        return list(self.similarity.matching(query=queries, para=para, title=title))
