CREATE TABLE "users"(
    "id" bigint GENERATED ALWAYS AS IDENTITY,
    "login" VARCHAR(255) NOT NULL,
    "password" VARCHAR(255) NOT NULL,
    "balance" BIGINT NOT NULL DEFAULT 0,
    "can_create_events" BOOLEAN NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "is_confirmed" BOOLEAN NOT NULL
);
ALTER TABLE
    "users" ADD PRIMARY KEY("id");
ALTER TABLE
    "users" ADD CONSTRAINT "users_email_unique" UNIQUE("email");
CREATE TABLE "events"(
    "id" bigint GENERATED ALWAYS AS IDENTITY,
    "name" VARCHAR(255) NOT NULL,
    "description" TEXT NOT NULL,
    "author_id" BIGINT NOT NULL,
    "final_outcome_id" BIGINT NULL,
    "ended_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "events" ADD PRIMARY KEY("id");
CREATE TABLE "bets"(
    "id" bigint GENERATED ALWAYS AS IDENTITY,
    "user_id" BIGINT NOT NULL,
    "event_id" BIGINT NOT NULL,
    "size" BIGINT NOT NULL,
    "outcome_id" BIGINT NOT NULL,
    "coefficient" DECIMAL(8, 2) NOT NULL
);
ALTER TABLE
    "bets" ADD PRIMARY KEY("id");
CREATE TABLE "outcomes"(
    "id" bigint GENERATED ALWAYS AS IDENTITY,
    "name" VARCHAR(255) NOT NULL,
    "event_id" BIGINT NOT NULL,
    "coefficient" DECIMAL(8, 2) NOT NULL
);
ALTER TABLE
    "outcomes" ADD PRIMARY KEY("id");
CREATE TABLE "email_codes"(
    "email" VARCHAR(255) NOT NULL,
    "code" INTEGER NOT NULL,
    "expires_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "email_codes" ADD CONSTRAINT "email_codes_email_unique" UNIQUE("email");
ALTER TABLE
    "email_codes" ADD PRIMARY KEY("email");
CREATE TABLE "sessions"(
    "id" bigint GENERATED ALWAYS AS IDENTITY,
    "user_id" BIGINT NOT NULL,
    "expires_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "sessions" ADD PRIMARY KEY("id");
ALTER TABLE
    "bets" ADD CONSTRAINT "bets_event_id_foreign" FOREIGN KEY("event_id") REFERENCES "events"("id");
ALTER TABLE
    "bets" ADD CONSTRAINT "bets_outcome_id_foreign" FOREIGN KEY("outcome_id") REFERENCES "outcomes"("id");
ALTER TABLE
    "sessions" ADD CONSTRAINT "sessions_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");
ALTER TABLE
    "outcomes" ADD CONSTRAINT "outcomes_event_id_foreign" FOREIGN KEY("event_id") REFERENCES "events"("id");
ALTER TABLE
    "events" ADD CONSTRAINT "events_final_outcome_id_foreign" FOREIGN KEY("final_outcome_id") REFERENCES "outcomes"("id");
ALTER TABLE
    "bets" ADD CONSTRAINT "bets_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");