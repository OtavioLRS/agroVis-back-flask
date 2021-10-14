from sqlalchemy.inspection import inspect

# Classe responsavel por converter o resultado da query em JSON


class Serializer(object):
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_rowlist(list):
        return [row._asdict() for row in list]

    @staticmethod
    def serialize_rowlist(list, cast_to_int):
        result = []
        for row in list:
            item = row._asdict()
            for fix in cast_to_int:
                item[fix] = int(item[fix])
            result.append(item)
        return result

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]
