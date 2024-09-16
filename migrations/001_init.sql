-- +goose Up
-- +goose StatementBegin

CREATE TABLE IF NOT EXISTS member (
    id serial PRIMARY KEY,
    tg text,
    name text,
    group_name text
);


-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin

drop TABLE IF EXISTS member CASCADE;

-- +goose StatementEnd
