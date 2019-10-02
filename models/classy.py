import uuid

from schemas import classes as schema
from models.single_table.schoolio import Schoolio


SCHOOLIO = 'schoolio'


class Class:
    def __init__(self, class_id=f'class_{str(uuid.uuid4())}', name=None):
        self.class_id = class_id
        self.name = name

    def save(self):
        if self.name is None:
            raise Exception('name cannot be None for class entity')
        self._make_schoolio_object(self.class_id, self.name).save()
        return schema.Class(self.class_id, self.name).__dict__

    @staticmethod
    def get_class_by_id(class_id):
        schoolio_class_record = Schoolio.get(f'{SCHOOLIO}_{class_id}', class_id)
        return schema.Class(schoolio_class_record.sk, schoolio_class_record.name).__dict__

    @staticmethod
    def _make_schoolio_object(class_id, name):
        class_schema_dict = Class._make_class_schema_dict(class_id, name)
        schoolio_class_record = Schoolio(class_schema_dict.pop('pk'), class_schema_dict.pop('sk'),
                                         **class_schema_dict)
        return schoolio_class_record

    @staticmethod
    def _make_class_schema_dict(class_id, name):
        class_obj = schema.Class(class_id, name)
        class_schema = schema.ClassSchema(only=('name', 'pk', 'sk'))
        class_schema.context = {
            'pk': f'{SCHOOLIO}_{class_id}',
            'sk': class_id
        }
        return class_schema.dump(class_obj)

