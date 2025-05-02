from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "lpu" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "active" BOOL NOT NULL DEFAULT True,
    "deleted" BOOL NOT NULL DEFAULT False,
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(200) NOT NULL UNIQUE,
    "lpu_name" VARCHAR(500) NOT NULL,
    "lpu_email" VARCHAR(200),
    "lpu_phone" VARCHAR(200),
    "org_www" VARCHAR(200),
    "lputype_name" VARCHAR(200),
    "lpu_worktime" VARCHAR(500),
    "address_nick" VARCHAR(500)
);
COMMENT ON COLUMN "lpu"."created_at" IS 'Дата и время создания записи';
COMMENT ON COLUMN "lpu"."updated_at" IS 'Дата и время последнего обновления записи';
COMMENT ON TABLE "lpu" IS 'Медицинские организации';
CREATE TABLE IF NOT EXISTS "profile" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "active" BOOL NOT NULL DEFAULT True,
    "deleted" BOOL NOT NULL DEFAULT False,
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(200) NOT NULL UNIQUE
);
COMMENT ON COLUMN "profile"."created_at" IS 'Дата и время создания записи';
COMMENT ON COLUMN "profile"."updated_at" IS 'Дата и время последнего обновления записи';
COMMENT ON TABLE "profile" IS 'Профиль оказания медицинской помощи';
CREATE TABLE IF NOT EXISTS "reason" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "active" BOOL NOT NULL DEFAULT True,
    "deleted" BOOL NOT NULL DEFAULT False,
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(200) NOT NULL UNIQUE
);
COMMENT ON COLUMN "reason"."created_at" IS 'Дата и время создания записи';
COMMENT ON COLUMN "reason"."updated_at" IS 'Дата и время последнего обновления записи';
COMMENT ON TABLE "reason" IS 'Причина обращения';
CREATE TABLE IF NOT EXISTS "problem" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "active" BOOL NOT NULL DEFAULT True,
    "deleted" BOOL NOT NULL DEFAULT False,
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(200) NOT NULL,
    "profile_id" BIGINT REFERENCES "profile" ("id") ON DELETE SET NULL,
    "reason_id" BIGINT REFERENCES "reason" ("id") ON DELETE SET NULL
);
COMMENT ON COLUMN "problem"."created_at" IS 'Дата и время создания записи';
COMMENT ON COLUMN "problem"."updated_at" IS 'Дата и время последнего обновления записи';
COMMENT ON TABLE "problem" IS 'Проблема';
CREATE TABLE IF NOT EXISTS "role" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "active" BOOL NOT NULL DEFAULT True,
    "deleted" BOOL NOT NULL DEFAULT False,
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(13) NOT NULL UNIQUE DEFAULT 'user',
    "description" VARCHAR(200)
);
COMMENT ON COLUMN "role"."created_at" IS 'Дата и время создания записи';
COMMENT ON COLUMN "role"."updated_at" IS 'Дата и время последнего обновления записи';
COMMENT ON COLUMN "role"."name" IS 'Роль пользователя';
COMMENT ON TABLE "role" IS 'Роли';
CREATE TABLE IF NOT EXISTS "user" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "active" BOOL NOT NULL DEFAULT True,
    "deleted" BOOL NOT NULL DEFAULT False,
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "nickname" VARCHAR(128),
    "phone" VARCHAR(20),
    "email" VARCHAR(128),
    "polis" VARCHAR(16),
    "person_id" BIGINT UNIQUE,
    "lpu_id" BIGINT REFERENCES "lpu" ("id") ON DELETE SET NULL
);
COMMENT ON COLUMN "user"."created_at" IS 'Дата и время создания записи';
COMMENT ON COLUMN "user"."updated_at" IS 'Дата и время последнего обновления записи';
COMMENT ON COLUMN "user"."polis" IS 'Единый номер полиса ОМС';
COMMENT ON TABLE "user" IS 'Пользователи телеграмм бота';
CREATE TABLE IF NOT EXISTS "petition" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "active" BOOL NOT NULL DEFAULT True,
    "deleted" BOOL NOT NULL DEFAULT False,
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "appeal_text" TEXT NOT NULL,
    "response_text" TEXT,
    "communication_by" VARCHAR(8) NOT NULL DEFAULT 'no',
    "current_status" VARCHAR(20),
    "contacted" BOOL NOT NULL DEFAULT False,
    "unresolved_reason" TEXT,
    "closed" BOOL NOT NULL DEFAULT False,
    "quality_solution" VARCHAR(20),
    "rating" SMALLINT NOT NULL DEFAULT 0,
    "mo_confirmed" BOOL NOT NULL DEFAULT False,
    "user_confirmed" BOOL NOT NULL DEFAULT False,
    "improve_offer" TEXT,
    "lpu_id" BIGINT NOT NULL REFERENCES "lpu" ("id") ON DELETE CASCADE,
    "mo_user_id" BIGINT REFERENCES "user" ("id") ON DELETE CASCADE,
    "problem_id" BIGINT REFERENCES "problem" ("id") ON DELETE SET NULL,
    "simple_user_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "petition"."created_at" IS 'Дата и время создания записи';
COMMENT ON COLUMN "petition"."updated_at" IS 'Дата и время последнего обновления записи';
COMMENT ON COLUMN "petition"."appeal_text" IS 'Текст обращения от заявителя';
COMMENT ON COLUMN "petition"."response_text" IS 'Текст ответа от ответчика';
COMMENT ON COLUMN "petition"."communication_by" IS 'Способ связи с заявителем';
COMMENT ON COLUMN "petition"."current_status" IS 'Текущий статус обращения';
COMMENT ON COLUMN "petition"."contacted" IS 'МО связались с заявителем';
COMMENT ON COLUMN "petition"."unresolved_reason" IS 'Причина почему проблема не решена';
COMMENT ON COLUMN "petition"."closed" IS 'Обращение закрыто';
COMMENT ON COLUMN "petition"."quality_solution" IS 'Качество решения проблемы';
COMMENT ON COLUMN "petition"."rating" IS 'Рейтинг качества решения, установленный пользователем';
COMMENT ON COLUMN "petition"."mo_confirmed" IS 'Получение обращения подтверждено МО';
COMMENT ON COLUMN "petition"."user_confirmed" IS 'Решение проблемы подтверждено пользователем';
COMMENT ON COLUMN "petition"."improve_offer" IS 'Предложение по улучшению качества решения аналогичных проблем';
COMMENT ON COLUMN "petition"."lpu_id" IS 'МО которую выбрал заявитель и к которой привязан ответчик';
COMMENT ON COLUMN "petition"."mo_user_id" IS 'Ответчик';
COMMENT ON COLUMN "petition"."simple_user_id" IS 'Заявитель';
COMMENT ON TABLE "petition" IS 'Обращения заявителей';
CREATE TABLE IF NOT EXISTS "status" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "active" BOOL NOT NULL DEFAULT True,
    "deleted" BOOL NOT NULL DEFAULT False,
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(10) NOT NULL DEFAULT 'new',
    "petition_id" BIGINT NOT NULL REFERENCES "petition" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "status"."created_at" IS 'Дата и время создания записи';
COMMENT ON COLUMN "status"."updated_at" IS 'Дата и время последнего обновления записи';
COMMENT ON COLUMN "status"."name" IS 'Статусы обращения';
COMMENT ON TABLE "status" IS 'Статус обращения';
CREATE TABLE IF NOT EXISTS "user_role" (
    "user_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "role_id" BIGINT NOT NULL REFERENCES "role" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_user_role_user_id_d0bad3" ON "user_role" ("user_id", "role_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
