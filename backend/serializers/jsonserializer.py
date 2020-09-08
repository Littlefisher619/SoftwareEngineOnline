import json

from rest_framework import serializers


class JsonSerializer(serializers.JSONField):
    default_error_messages = {
        'invalid_json': '无法将提供的数据进行JSON序列化'
    }

    def to_representation(self, value):
        if value == None or value == "":
            return None
        # print(value)
        try:
            return json.loads(value)

        except (TypeError, ValueError):
            # self.fail('invalid_json')
            return {'error': '存储在数据库中的JSON格式有误'}

    def to_internal_value(self, data):
        try:
            res = json.dumps(data)
            print('to_internal: ', res)
        except (TypeError, ValueError):
            self.fail('invalid_json')
        return res