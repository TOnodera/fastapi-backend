-- ���[�U�[�e�[�u��
create table if not exists users (
  id integer not null
  , name varchar(100) not null
  , email varchar(256) not null
  , password varchar(32) not null
  , updated_at timestamp not null
  , create_at timestamp not null
  , constraint users_PKC primary key (id)
) ;

comment on table users is '���[�U�[�e�[�u��:���[�U�[�e�[�u��';
comment on column users.id is 'id:�V�[�P���X';
comment on column users.name is '���O';
comment on column users.email is '���[���A�h���X';
comment on column users.password is '�p�X���[�h';
comment on column users.updated_at is '�X�V��';
comment on column users.create_at is '�쐬��';

create sequence user_id_seq
    start with 1
    increment by 1
    no minvalue
    no maxvalue
    no cycle
    owned by users.id
    
