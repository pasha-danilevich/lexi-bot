from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_reason_name_b6a320";
        DROP INDEX IF EXISTS "uid_profile_name_e27058";
        ALTER TABLE "problem" DROP CONSTRAINT IF EXISTS "fk_problem_profile_d17143f2";
        CREATE TABLE IF NOT EXISTS "drug" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "active" BOOL NOT NULL DEFAULT True,
    "deleted" BOOL NOT NULL DEFAULT False,
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(200) NOT NULL,
    "reason_id" BIGINT NOT NULL REFERENCES "reason" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "drug"."created_at" IS 'Дата и время создания записи';
COMMENT ON COLUMN "drug"."updated_at" IS 'Дата и время последнего обновления записи';
COMMENT ON TABLE "drug" IS 'Медикаменты ОНКО';
        ALTER TABLE "petition" ADD "title" VARCHAR(50);
        ALTER TABLE "petition" ADD "drug_id" BIGINT;
        ALTER TABLE "petition" ADD "reasondetail_id" BIGINT;
        ALTER TABLE "petition" ADD "reason_id" BIGINT;
        ALTER TABLE "petition" ADD "profile_id" BIGINT;
        ALTER TABLE "problem" ADD "short" VARCHAR(20);
        ALTER TABLE "problem" DROP COLUMN "profile_id";
        ALTER TABLE "profile" ADD "short" VARCHAR(20);
        ALTER TABLE "reason" ADD "short" VARCHAR(20);
        CREATE TABLE IF NOT EXISTS "reasondetail" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "active" BOOL NOT NULL DEFAULT True,
    "deleted" BOOL NOT NULL DEFAULT False,
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(200) NOT NULL,
    "short" VARCHAR(20),
    "reason_id" BIGINT NOT NULL REFERENCES "reason" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "petition"."title" IS 'Заголовок обращения';
COMMENT ON COLUMN "reasondetail"."created_at" IS 'Дата и время создания записи';
COMMENT ON COLUMN "reasondetail"."updated_at" IS 'Дата и время последнего обновления записи';
COMMENT ON TABLE "reasondetail" IS 'Детализация вопросов к поводу';
        ALTER TABLE "petition" ADD CONSTRAINT "fk_petition_drug_44041ce4" FOREIGN KEY ("drug_id") REFERENCES "drug" ("id") ON DELETE SET NULL;
        ALTER TABLE "petition" ADD CONSTRAINT "fk_petition_reason_af42810d" FOREIGN KEY ("reason_id") REFERENCES "reason" ("id") ON DELETE SET NULL;
        ALTER TABLE "petition" ADD CONSTRAINT "fk_petition_reasonde_6f13066f" FOREIGN KEY ("reasondetail_id") REFERENCES "reasondetail" ("id") ON DELETE SET NULL;
        ALTER TABLE "petition" ADD CONSTRAINT "fk_petition_profile_aa63fea9" FOREIGN KEY ("profile_id") REFERENCES "profile" ("id") ON DELETE SET NULL;
        CREATE TABLE "problem_to_profile" (
    "problem_id" BIGINT NOT NULL REFERENCES "problem" ("id") ON DELETE CASCADE,
    "profile_id" BIGINT NOT NULL REFERENCES "profile" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "petition" DROP CONSTRAINT IF EXISTS "fk_petition_profile_aa63fea9";
        ALTER TABLE "petition" DROP CONSTRAINT IF EXISTS "fk_petition_reasonde_6f13066f";
        ALTER TABLE "petition" DROP CONSTRAINT IF EXISTS "fk_petition_reason_af42810d";
        ALTER TABLE "petition" DROP CONSTRAINT IF EXISTS "fk_petition_drug_44041ce4";
        DROP TABLE IF EXISTS "problem_to_profile";
        ALTER TABLE "reason" DROP COLUMN "short";
        ALTER TABLE "problem" ADD "profile_id" BIGINT;
        ALTER TABLE "problem" DROP COLUMN "short";
        ALTER TABLE "profile" DROP COLUMN "short";
        ALTER TABLE "petition" DROP COLUMN "title";
        ALTER TABLE "petition" DROP COLUMN "drug_id";
        ALTER TABLE "petition" DROP COLUMN "reasondetail_id";
        ALTER TABLE "petition" DROP COLUMN "reason_id";
        ALTER TABLE "petition" DROP COLUMN "profile_id";
        DROP TABLE IF EXISTS "drug";
        DROP TABLE IF EXISTS "reasondetail";
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_reason_name_b6a320" ON "reason" ("name");
        ALTER TABLE "problem" ADD CONSTRAINT "fk_problem_profile_d17143f2" FOREIGN KEY ("profile_id") REFERENCES "profile" ("id") ON DELETE SET NULL;
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_profile_name_e27058" ON "profile" ("name");"""
