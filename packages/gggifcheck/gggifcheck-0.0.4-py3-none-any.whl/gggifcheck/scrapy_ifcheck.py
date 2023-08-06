import scrapy
from gggifcheck import fields
from gggifcheck.items import CheckItem


class ScrapyCheckItem(scrapy.Item, CheckItem):

    def __init__(self, *args, **kwargs):
        self._values = {}
        self._base_values = {}
        if args or kwargs:
            for k, v in dict(*args, **kwargs).items():
                self[k] = v

    def __getitem__(self, key):
        if key in self.fields and key not in self._values:
            value = None
            for field1, field2 in self.relate_process_default:
                value = self[field2]
                break
            self[key] = value
        return self._values[key]

    def __setitem__(self, key, value):
        if key in self.fields:
            self._base_values[key] = value
            field = self.fields[key]
            check_field = field.get('check_field')
            if isinstance(check_field, fields.CheckField):
                fe = check_field.from_instance()
                fe.input(key, value)
                self._values[key] = fe.value
            else:
                self._values[key] = value
        else:
            raise KeyError(
                f"{self.__class__.__name__} does not support field: {key}")

    def __setattr__(self, name, value):
        if name.startswith('_'):
            self.__dict__[name] = value
        else:
            raise AttributeError(
                f"Use item[{name!r}] = {value!r} to set field value")

    def check_all(self):
        """
        进行所有字段检查
        :return:
        """
        self._process_and_check()
        _ = [self[field] for field in self.fields]

    def keys(self):
        # 不能放在此处验证的原因是scrapy item进入pipeline前有日志打印等操作导致进行
        # 此处验证，导致如果在pipeline里进行透传时验证不生效，提前检查报错，此处验证放
        # 在check_all方法中，因此需要手动调用
        # self._process_and_check()
        # _ = [self[field] for field in self.fields]  # 进行所有字段检查
        return self._values.keys()


# 示例
class PostItem(ScrapyCheckItem):
    relate_process_default = [('channel', 'id')]
    id = scrapy.Field(
        check_field=fields.MD5CheckField(nullable=False))
    channel = scrapy.Field(
        check_field=fields.IntegerCheckField(
            nullable=False, min_value=1, max_value=6))


item = PostItem()
item['id'] = '81dc9bdb52d04dc20036dbd8313ed055'
item['channel'] = 1
item.check_all()
print(dict(item))
print(item.get_base_value('id'))
