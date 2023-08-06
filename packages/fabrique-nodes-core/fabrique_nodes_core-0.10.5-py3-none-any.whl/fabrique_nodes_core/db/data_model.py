# flake8: noqa: E501

from typing import List, Literal, Optional
from pydantic import BaseModel, EmailStr


create_pub_keys_str = """
CREATE TABLE IF NOT EXISTS user_pub_keys (
    user_id TEXT PRIMARY KEY,
    key_pem TEXT
);
"""

create_priv_keys_str = """
CREATE TABLE IF NOT EXISTS user_priv_keys (
    user_id TEXT PRIMARY KEY,
    key_pem TEXT
);
"""


create_project_sql_str = """
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'project_status_enum') THEN
        CREATE TYPE project_status_enum AS ENUM ('idle', 'ready', 'runtime_error', 'emulation_error', 'unknown', 'online');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'project_desired_status_enum') THEN
        CREATE TYPE project_desired_status_enum AS ENUM ('idle', 'emulate', 'deploy', 'forced_deploy');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'project_type') THEN
        CREATE TYPE project_type AS ENUM ('pipeline', 'actor');
    END IF;
END
$$;

CREATE TABLE IF NOT EXISTS projects (
    rec_id VARCHAR PRIMARY KEY,
    prev_rec_id VARCHAR NOT NULL DEFAULT '',
    forked_from_rec_id VARCHAR NOT NULL DEFAULT '',
    project_id VARCHAR NOT NULL,
    version VARCHAR(255) NOT NULL DEFAULT '0.0.0-auto-' || EXTRACT(EPOCH FROM CURRENT_TIMESTAMP)::BIGINT,
    user_id VARCHAR NOT NULL,
    project_type project_type NOT NULL DEFAULT 'pipeline',
    created_ts BIGINT DEFAULT EXTRACT(EPOCH FROM NOW()) * 1000,
    updated_ts BIGINT DEFAULT EXTRACT(EPOCH FROM NOW()) * 1000,
    company_id VARCHAR NOT NULL DEFAULT '',
    creator_id VARCHAR NOT NULL DEFAULT '',
    is_public BOOLEAN NOT NULL DEFAULT FALSE,
    data JSON NOT NULL,
    samples JSON NOT NULL DEFAULT '{}',
    credential_pub_key VARCHAR DEFAULT '',
    status project_status_enum NOT NULL DEFAULT 'idle',
    desired_status project_desired_status_enum NOT NULL DEFAULT 'idle',
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE INDEX IF NOT EXISTS idx_projects_rec_id ON projects (rec_id);
CREATE INDEX IF NOT EXISTS idx_projects_project_id ON projects (project_id);
CREATE INDEX IF NOT EXISTS idx_projects_user_id ON projects (user_id);
CREATE INDEX IF NOT EXISTS idx_projects_project_type ON projects (project_type);
CREATE INDEX IF NOT EXISTS idx_projects_updated_ts ON projects (updated_ts);
CREATE INDEX IF NOT EXISTS idx_projects_is_public ON projects (is_public);
CREATE INDEX IF NOT EXISTS idx_projects_status ON projects (status);
CREATE INDEX IF NOT EXISTS idx_projects_desired_status ON projects (desired_status);
"""


class ProjectRecordModel(BaseModel):
    rec_id: Optional[str]
    project_id: str
    prev_rec_id: Optional[str] = ''
    version: Optional[str]
    user_id: str
    project_type: Optional[Literal['pipeline', 'actor']] = "pipeline"
    created_ts: Optional[float]
    updated_ts: Optional[float]
    company_id: Optional[str]
    creator_id: Optional[str]
    is_public: Optional[bool] = False
    data: dict
    samples: Optional[dict] = {}
    credential_pub_key: Optional[str] = ''
    desired_status: Optional[Literal["idle", "emulate", "deploy", "forced_deploy"]] = 'idle'
    status: Optional[Literal["idle", "ready", "runtime_error", "emulation_error", "unknown", "online"]] = 'idle'


class ProjectApiModel(ProjectRecordModel):
    project_id: Optional[str]


proj_field_names = [
    'rec_id', 'project_id', 'prev_rec_id', 'version', 'user_id',
    'project_type', 'created_ts', 'updated_ts',
    'company_id', 'creator_id', 'is_public', 'data',
    'samples', 'credential_pub_key', 'status', 'desired_status'
]

assert all((field in ProjectRecordModel.__fields__) for field in proj_field_names)
