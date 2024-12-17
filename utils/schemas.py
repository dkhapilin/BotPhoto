from marshmallow import Schema, fields, validates, ValidationError, post_load
from database.queries import check_user_by_telegram_id, User, Client, get_client_by_name, get_client_by_id


class UserSchema(Schema):
    users_id = fields.Int(dump_only=True)
    users_name = fields.Str(required=True)
    access = fields.Int(required=True)
    telegram_id = fields.Int(required=True)

    @validates('telegram_id')
    def validate_telegram_id(self, telegram_id):
        if check_user_by_telegram_id(telegram_id) is None:
            raise ValidationError('Invalid telegram id')

    @post_load
    def create_user(self, data, **kwargs) -> User:
        return User(**data)


class ClientSchema(Schema):
    name = fields.Str(required=True)
    id = fields.Int()

    @validates('name')
    def validate_name(self, name):
        if get_client_by_name(name):
            raise ValidationError(f'Клиент "{name}" существует.', messages='')

    @validates('id')
    def validate_id(self, id):
        if get_client_by_id(id):
            raise ValidationError(f'Клиент с id {id} существует.')

    @post_load
    def create_client(self, data, **kwargs) -> Client:
        return Client(**data)
