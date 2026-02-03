from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, AnyUrl

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    retrieval_url: AnyUrl = Field(validation_alias="RETRIEVAL_URL")
    ab_retrieval_url: AnyUrl = Field(validation_alias="AB_RETRIEVAL_URL")
    corpus_retrieval_url : AnyUrl = Field(validation_alias="CORUS_RETRIEVAL_URL")
    model_url: AnyUrl = Field(validation_alias="MODEL_URL")
    model_answer: str = Field(validation_alias="MODEL_ANSWER")
    timeout: int = Field(validation_alias="REQUEST_TIMEOUT_S")
    default_rewrites: int = Field(validation_alias="DEFAULT_REWRITES")
    default_chunks: int = Field(validation_alias="DEFAULT_CHUNKS")
    chroma_dir: str = Field(validation_alias="CHROMA_DIR")

settings = Settings()