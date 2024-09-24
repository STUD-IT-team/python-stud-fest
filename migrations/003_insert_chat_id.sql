-- +goose Up
-- +goose StatementBegin

ALTER TABLE member ADD COLUMN chat_id BIGINT;
ALTER TABLE member ALTER COLUMN chat_id SET DEFAULT NULL;

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin

-- +goose StatementEnd
