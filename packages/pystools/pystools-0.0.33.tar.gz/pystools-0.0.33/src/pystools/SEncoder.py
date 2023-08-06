import hashlib
import uuid
import shortuuid


class SEncoder:
    @staticmethod
    def md5_from_uuid(to_upper=False):
        # 生成唯一的uuid
        v = str(uuid.uuid1())
        m = hashlib.md5()
        # 将args中的所有值拼接起来
        m.update(f"{v}".encode("utf-8"))
        if to_upper:
            return m.hexdigest().upper()
        return m.hexdigest()

    @staticmethod
    def short_uuid(to_upper=False):
        unique_id = shortuuid.uuid()
        if to_upper:
            return unique_id.upper()
        return unique_id