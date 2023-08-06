from typing import Any

import sqlalchemy
from perun.connector import AdaptersManager
from perun.connector import Logger
from pymongo import MongoClient
from pymongo.collection import Collection
from sqlalchemy import delete
from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import Session

from perun.utils.ConfigStore import ConfigStore


class UserManager:
    def __init__(self, cfg):
        GLOBAL_CONFIG = ConfigStore.get_global_cfg(cfg.get("global_cfg_filepath"))
        ADAPTERS_MANAGER_CFG = GLOBAL_CONFIG["adapters_manager"]
        ATTRS_MAP = ConfigStore.get_attributes_map(GLOBAL_CONFIG["attrs_cfg_path"])

        self._ADAPTERS_MANAGER = AdaptersManager(ADAPTERS_MANAGER_CFG, ATTRS_MAP)
        self._SUBJECT_ATTRIBUTE = cfg.get("perun_person_principal_names_attribute")

        self.logger = Logger.get_logger(__name__)
        self._cfg = cfg

    def get_mongo_db_collection(self, cfg_db_name: str) -> Collection:
        client = MongoClient(self._cfg[cfg_db_name]["connection_string"])
        database_name = self._cfg[cfg_db_name]["database_name"]
        collection_name = self._cfg[cfg_db_name]["collection_name"]

        return client[database_name][collection_name]

    def _revoke_ssp_sessions(
        self, subject: str, ssp_sessions_collection: Collection
    ) -> int:
        result = ssp_sessions_collection.delete_many({"user": subject})
        return result.deleted_count

    def _revoke_satosa_grants(
        self, subject: str, satosa_sessions_collection: Collection
    ) -> int:
        result = satosa_sessions_collection.delete_many({"sub": subject})
        return result.deleted_count

    def _get_postgres_engine(self) -> Engine:
        connection_string = self._cfg["mitre_database"]["connection_string"]
        engine = sqlalchemy.create_engine(connection_string)

        return engine

    def _get_mitre_delete_statements(self, user_id: str, engine: Engine) -> list[Any]:
        meta_data = sqlalchemy.MetaData(bind=engine)
        sqlalchemy.MetaData.reflect(meta_data)

        AUTH_HOLDER_TBL = meta_data.tables["authentication_holder"]
        SAVED_USER_AUTH_TBL = meta_data.tables["saved_user_auth"]

        ACCESS_TOKEN_TBL = meta_data.tables["access_token"]
        delete_access_tokens_stmt = delete(ACCESS_TOKEN_TBL).where(
            ACCESS_TOKEN_TBL.auth_holder_id.in_(
                Session.query(AUTH_HOLDER_TBL.id).filter(
                    AUTH_HOLDER_TBL.user_auth_id.in_(
                        Session.query(SAVED_USER_AUTH_TBL.id).filter(
                            SAVED_USER_AUTH_TBL.name == user_id
                        )
                    )
                )
            )
        )

        AUTH_CODE_TBL = meta_data.tables["authorization_code"]
        delete_authorization_codes_stmt = delete(AUTH_CODE_TBL).where(
            AUTH_CODE_TBL.auth_holder_id.in_(
                Session.query(AUTH_HOLDER_TBL.id).filter(
                    AUTH_HOLDER_TBL.user_auth_id.in_(
                        Session.query(SAVED_USER_AUTH_TBL.id).filter(
                            SAVED_USER_AUTH_TBL.name == user_id
                        )
                    )
                )
            )
        )

        DEVICE_CODE = meta_data.tables["device_code"]
        delete_device_codes_stmt = delete(DEVICE_CODE).where(
            DEVICE_CODE.auth_holder_id.in_(
                Session.query(AUTH_HOLDER_TBL.id).filter(
                    AUTH_HOLDER_TBL.user_auth_id.in_(
                        Session.query(SAVED_USER_AUTH_TBL.id).filter(
                            SAVED_USER_AUTH_TBL.name == user_id
                        )
                    )
                )
            )
        )

        return [
            delete_access_tokens_stmt,
            delete_authorization_codes_stmt,
            delete_device_codes_stmt,
        ]

    def _delete_mitre_tokens(self, user_id: str) -> int:
        deleted_mitre_tokens_count = 0

        engine = self._get_postgres_engine()
        statements = self._get_mitre_delete_statements(user_id, engine)

        for stmt in statements:
            result = engine.execute(stmt)
            deleted_mitre_tokens_count += result.rowcount

        return deleted_mitre_tokens_count

    def _get_satosa_sessions_collection(self) -> Collection:
        return self.get_mongo_db_collection("satosa_database")

    def _get_ssp_sessions_collection(self) -> Collection:
        return self.get_mongo_db_collection("ssp_database")

    def logout(self, user_id: str) -> None:
        user_attrs = self._ADAPTERS_MANAGER.get_user_attributes(
            int(user_id), [self._SUBJECT_ATTRIBUTE]
        )
        subject_candidates = user_attrs.get(self._SUBJECT_ATTRIBUTE, [])
        subject = subject_candidates[0] if subject_candidates else None

        ssp_sessions_collection = self._get_ssp_sessions_collection()
        revoked_sessions_count = self._revoke_ssp_sessions(
            subject, ssp_sessions_collection
        )

        satosa_sessions_collection = self._get_satosa_sessions_collection()
        revoked_grants_count = self._revoke_satosa_grants(
            subject, satosa_sessions_collection
        )

        deleted_tokens_count = self._delete_mitre_tokens(user_id)

        self.logger.info(
            f"Logged out user {subject} from {revoked_sessions_count} SSP "
            f"sessions, deleted {revoked_grants_count} SATOSA sessions and "
            f"deleted {deleted_tokens_count} mitre tokens."
        )
