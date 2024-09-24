-- +goose Up
-- +goose StatementBegin

ALTER TABLE member ADD COLUMN mc_time text default 'не принимает участие';

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin

ALTER TABLE member drop COLUMN mc_time;

-- +goose StatementEnd