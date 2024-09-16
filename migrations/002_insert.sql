-- +goose Up
-- +goose StatementBegin

INSERT INTO member (tg, name, group_name) 
VALUES ('@Andre1ch', 'Андрей Поляков', 'ИУ7-52Б');



-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin

truncate table member CASCADE;

-- +goose StatementEnd
