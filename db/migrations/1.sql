-- ユーザーテーブル
create table if not exists users (
  id serial not null
  , name varchar(100) not null
  , email varchar(256) not null
  , password varchar(32) not null
  , updated_at timestamp default now() not null
  , created_at timestamp default now() not null
  , constraint users_PKC primary key (id)
) ;

comment on table users is 'ユーザーテーブル:ユーザーテーブル';
comment on column users.id is 'id:シーケンス';
comment on column users.name is '名前';
comment on column users.email is 'メールアドレス';
comment on column users.password is 'パスワード';
comment on column users.updated_at is '更新日';
comment on column users.created_at is '作成日';


create sequence user_id_seq
    start with 1
    increment by 1
    no minvalue
    no maxvalue
    no cycle
    owned by users.id
    
