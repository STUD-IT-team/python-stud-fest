-- +goose Up
-- +goose StatementBegin

ALTER TABLE member
ALTER COLUMN name SET DEFAULT 'Cock Balls Penisович',
ALTER COLUMN group_name SET DEFAULT 'Орехи';

ALTER TABLE member
ADD CONSTRAINT unique_tg UNIQUE (tg);

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin



-- +goose StatementEnd
