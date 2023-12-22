from __future__ import annotations

import pandas as pd
from pymilvus import (
    connections,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)
from sentence_transformers import SentenceTransformer

import logging
from os import path

from core.settings import settings
from schemas.models import ModelResponseSchema

logger = logging.getLogger("API")

_HOST = '127.0.0.1'
_PORT = '19530'
_USER = "username"
_USER_PASSWORD = "password"
db_name="default"


class ModelService:
    def __init__(self):
        self.model_loaded = False
        self.model: SentenceTransformer | None = None
        self._load_model()

    def _load_model(self):
        try:
            self._load_database()
            self.model = SentenceTransformer(settings.MODEL_NAME)
            self.model_loaded = True
        except Exception as e:
            logger.error("model loading error", exc_info=e)
    
    def _load_database(self):
        data_dir = path(settings.DATA_PATH)
        embeddings_dir = path.join(data_dir, 'embeddings')
        vacancies_emb_path = path.join(embeddings_dir, 'vacancies.csv')
        cvs_emb_path = path.join(embeddings_dir, 'cvs.csv')
        raw_dir = path.join(data_dir, 'raw')
        vacancies_path = path.join(raw_dir, 'hhparser_vacancy.csv')
        cvs_path = path.join(raw_dir, 'dst-3.0_16_1_hh_database.csv')

        connections.connect(
            host=_HOST,
            port=_PORT,
            user=_USER,
            password=_USER_PASSWORD,
            db_name=db_name,
        )
        print(f"Connected to milvus\n")

        vacancies = pd.read_csv(vacancies_emb_path)
        vacancies_fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=768),
        ]
        self.vacancies_collection = Collection(name="vacancies", schema=CollectionSchema(fields=vacancies_fields))
        self.vacancies_collection.insert(vacancies.T.tolist())
        self.vacancies_collection.flush()
        print('Vacancies embeddings loaded')

        cvs = pd.read_csv(cvs_emb_path)
        cvs_fields = [
            FieldSchema(name="ind", dtype=DataType.INT64, is_primary=True),
            FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=768),
        ]
        self.cvs_collection = Collection(name="cvs", schema=CollectionSchema(fields=cvs_fields))
        self.cvs_collection.insert(cvs.T.tolist())
        self.cvs_collection.flush()
        print('CVs embeddings loaded')

        self.vacancies = pd.read(vacancies_path, index_col='id')
        self.cvs = pd.read(cvs_path, index_col='ind')


    def get_cvs_by_vacancy(self, text: str) -> ModelResponseSchema:
        encoded = self.model.encode(text)
        results = self.cvs_collection.search(
            data=[encoded],
            anns_field = "embeddings",
            output_fields=["ind"],
            limit=10,
        )
        ind = []
        for hits in results:
            for hit in hits:
                ind.append(hit.entity.get("ind"))
        res = self.cvs.iloc[ind]
        return ModelResponseSchema(texts=(
            'Пол, возраст' + res['Пол, возраст'] +
            '\nЗанятость' + res['Занятость'] +
            '\nОпыт работы' + res['Опыт работы'] +
            '\nПоследнее/нынешнее место работы' + res['Последнее/нынешнее место работы']
            ).tolist()
        )


    def get_vacancies_by_cv(self, text: str) -> ModelResponseSchema:
        encoded = self.model.encode(text)
        results = self.cvs_collection.search(
            data=[encoded],
            anns_field = "embeddings",
            output_fields=["id"],
            limit=10,
        )
        ind = []
        for hits in results:
            for hit in hits:
                ind.append(hit.entity.get("id"))
        return ModelResponseSchema(
            texts=self.cvs.iloc[ind]['description'].tolist()
        )
