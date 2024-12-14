from marshmallow import Schema, fields, validates, ValidationError, post_load
from database.queries import check_user_by_telegram_id, User


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
