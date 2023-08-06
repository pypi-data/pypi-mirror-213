from __future__ import annotations

__all__ = [
        'ModelMap',
        'context_model',
        'BaseDescriptor',
        'BaseValidator',
        'ContextBase',
        'Descriptor',
        'Validator',
        'DescriptorModel',
        'compare_descriptors',
        'descriptorsmap',
        'descriptors_items',
        'compare_dict',
        'compare_tuple',
        'hash_tuple',
        'hash_dict',
        'hash_descriptors',
        'check_hash',
        'check_compare',
        'instance_hash',
        'lesser_than',
        'orderby',
        'ordered',
        'reversed_dict',
        'db_descriptors',
        'query_from_string',
        'exist_query',
        'descriptors',
        'display_items',
        'display_repr',
        'eq_function',
        'get_attr_or_item',
        'filter_dict',
        'make_dict',
        'dict_items',
        'normalize_lower_if_string',
        'exclude_keys_from_dict'
]


from deta.base import FetchResponse
from dtfield._imports import *
from dtbase import *
from .parse import *
from .functions import *


context = copy_context()


def exclude_keys_from_dict(data: Mapping, exclude: list[str]):
    return {k: v for k, v in data.items() if not k in exclude}


def get_attr_or_item(obj: Any, name: str = 'key'):
    if isinstance(obj, Mapping):
        return obj.get(name)
    elif hasattr(obj, name):
        return getattr(obj, 'key')
    raise AttributeError(f'O objeto "{obj}" não possuir uma chave ou attributo "{name}".')


def make_dict(
        iterable: Iterable[T],
        key_func: Callable[[T], str] = get_attr_or_item,
        value_func: Callable[[T], Any] = lambda x: x,
        condition: Callable[[T], bool] = lambda x: True
    ) -> dict[str, T]:
    return {key_func(item): value_func(item) for item in iterable if condition(item) is True}


def filter_dict(data: Mapping[str, T], condition: Callable[[T], bool]) -> dict[str, T]:
    return make_dict(data.items(), key_func=lambda x: x[0], value_func=lambda x: x[1], condition=condition)

def dict_items(data: Mapping) -> list[tuple[Any, Any]]:
    return list(data.items())

normalize_lower_if_string = partial(lambda x: x if not isinstance(x, str) else normalize_lower(x))
descriptorsmap = partial(lambda cls: cls.descriptorsmap())
descriptors = partial(lambda cls: cls.descriptorsmap().values())
descriptors_items = partial(lambda cls: dict_items(descriptorsmap(cls)))
compare_descriptors = partial(lambda x: filter_dict(descriptorsmap(x), condition=lambda x: x[1].compare is True))
compare_dict = partial(lambda x: {k: normalize_lower_if_string(v.__get__(x)) for k, v in compare_descriptors(x).items()})
compare_tuple = partial(lambda x: tuple(compare_dict(x).values()))
check_compare = partial(lambda self, other: compare_tuple(self) == compare_tuple(other))
hash_descriptors = partial(lambda x: filter_dict(descriptorsmap(x), condition=lambda x: x[1].hash is True))
hash_dict = partial(lambda x: {k: v.__get__(x) for k, v in hash_descriptors(x).items()})
hash_tuple = partial(lambda x: tuple(hash_dict(x).values()))
check_hash = partial(lambda self, other: hash(hash_tuple(self)) == hash(hash_tuple(other)))
instance_hash = partial(lambda self: hash(hash_tuple(self)))
reversed_dict = partial(lambda x: {k: x[k] for k in reversed(x.keys())})
lesser_than = partial(lambda self, other: compare_tuple(self) < compare_tuple(other))
greater_than = partial(lambda self, other: compare_tuple(self) > compare_tuple(other))
orderby = partial(lambda iterable, public_name: sorted(iterable, key=lambda item: normalize_lower_if_string(getattr(item, public_name))))
db_descriptors = partial(lambda x: filter_dict(descriptorsmap(x), condition=lambda x: x[1].db is True))
query_from_string = partial(lambda self, query_string: filter_dict(asdict(self), condition=lambda x: all([x[0] in query_string.split(), is_null(x[1]) is False])))


def exist_query(self: ContextBase):
    if not self.exist_params():
        raise ValueError(f'{self.clsname()} não definiu EXIST_PARAMS')
    qr = None
    if isinstance(self.exist_params(), str):
        qr = json_parse(query_from_string(self, self.exist_params()))
    elif isinstance(self.exist_params(), list):
        qr = json_parse(list(filter(lambda x: is_null(x) is False, [query_from_string(self, i) for i in self.exist_params()])))
    if isinstance(qr, list):
        if len(qr) == 1:
            return qr[0]
    return qr
    

def repr_func(self: ContextBase):
    items = (f'{k}={getattr(self, v.public_name)!r}' for k, v in self.descriptorsmap().items() if v.public == True)
    return '{}({})'.format(self.clsname(), ', '.join(items))

def display_items(self: ContextBase) -> list[tuple[str, Any]]:
    if self.display_properties():
        return [(i.split('.')[-1], getter(self, i)) for i in self.display_properties()]
    return []

def display_repr(self: ContextBase):
    items = display_items(self)
    if items:
        return ', '.join([f'{i[0]}={i[1]}' for i in items ])
    return None

def eq_function(self: T, other: T) -> bool:
    return check_hash(self, other)


def ordered(iterable: list[DescriptorModel]):
    result = iterable
    if iterable:
        item = iterable[0]
        keys = compare_descriptors(item).keys()
        for key in reversed(keys):
            result = orderby(result, key)
    return result


@dataclass
class DescriptorModel(ABC):
    
    def __post_init__(self):
        for d in self.post_init_descriptors().values():
            if is_null(getattr(self, d.public_name)):
                setattr(self, d.public_name, d.post_init_factory())
    
    @classmethod
    def initfields(cls) -> tuple[Field, ...]:
        return tuple([f for f in fields(cls) if f.init == True])
    
    @classmethod
    @cache
    def initfields_keys(cls) -> list[str]:
        return [i.name for i in cls.initfields()]
    
    @classmethod
    def post_init_descriptors(cls) -> dict[str, BaseDescriptor]:
        return filter_dict(cls.descriptorsmap(), lambda x: x[1].post_init_factory is not MISSING)
    
    @classmethod
    def fields(cls) -> tuple[Field, ...]:
        return fields(cls)
    
    @classmethod
    def fieldsmap(cls) -> dict[str, Field]:
        return make_dict(cls.fields(),  key_func=lambda x: get_attr_or_item(x, 'public_name'))

    
    @classmethod
    def safe_create(cls, *args, **kwargs) -> Self:
        return cls(*args, **{k: v for k, v in kwargs.items() if k in cls.initfields_keys()})
    
    @classmethod
    def dataclass_bases(cls) -> tuple:
        return tuple([b for b in cls.mro() if is_dataclass(b)])
    
    @classmethod
    def clsname(cls) -> str:
        return cls.__name__
    
    @classmethod
    def fullvars(cls) -> dict[str, Any]:
        return {**ChainMap(*[vars(b) for b in cls.mro()])}
    
    @classmethod
    def descriptorsmap(cls) -> dict[str, BaseDescriptor]:
        return filter_dict(cls.fullvars(), condition=lambda x: isinstance(x[1], BaseDescriptor))
    
    @classmethod
    def descriptors(cls):
        return tuple(descriptors(cls))
    
    @classmethod
    def descriptorskeys(cls):
        return tuple([i.public_name for i in cls.descriptors()])
    
    def asjson(self, exclude: list[str] = None):
        return json_parse(exclude_keys_from_dict(asdict(self), exclude or list()))
    
    def asjson_to_db(self):
        return json_parse(filter_dict(asdict(self), condition=lambda x: x[0] in db_descriptors(self).keys()))


        
@dataclass
class ContextBase(DescriptorModel):
    CTXVAR: ClassVar[ContextVar] = None
    DETA_QUERY: ClassVar[Optional[DetaQuery]] = None
    TABLE: ClassVar[Optional[str]] = None
    ITEM_NAME: ClassVar[Optional[str]] = None
    DISPLAY_PROPERTIES: ClassVar[Optional[list[str]]] = None
    SINGULAR: ClassVar[Optional[str]] = None
    PLURAL: ClassVar[Optional[str]] = None
    EXIST_PARAMS: ClassVar[DetaQuery] = None
    DELETABLE: ClassVar[bool] = True
    
    async def delete(self):
        if self.DELETABLE:
            return await DetaBase(self.table()).delete(getattr(self, 'key'))
        print(f'{self.clsname()}.FROZEN is True and cannot be deleted')
        return
    
    @classmethod
    def exist_params(cls):
        return cls.EXIST_PARAMS
    
    async def exist_response(self):
        return await DetaBase(self.table()).fetch(exist_query(self))
    
    async def save(self):
        new = await DetaBase(self.table()).insert(self.asjson_to_db())
        if new:
            await self.update_context()
            return self.safe_create(**new)
        return None
    
    async def save_new(self):
        exist = await self.exist_response()
        if exist.count == 0:
            return await self.save()
        elif exist.count == 1:
            return self.safe_create(**exist.items[0])
        else:
            return None
        
    async def update_instance(self, **kwargs):
        current = self.asjson()
        current.update(exclude_keys_from_dict(kwargs, exclude=['key']))
        key = current.pop('key')
        updated = await DetaBase(self.table()).put(data=current, key=key)
        await self.update_context()
        return self.from_context(key)
        
    
    @classmethod
    def singular(cls):
        return cls.SINGULAR or cls.clsname()
    
    @classmethod
    def plural(cls):
        return cls.PLURAL or f'{cls.singular()}s'
    
    @classmethod
    def display_properties(cls):
        return cls.DISPLAY_PROPERTIES or list()
    
    @classmethod
    def item_name(cls):
        return cls.ITEM_NAME or slug(cls.table())
    
    @classmethod
    def table(cls):
        return cls.TABLE or cls.clsname()
    
    @classmethod
    def dependant_descriptors(cls):
        return {d.public_name: d for d in cls.descriptorsmap().values() if d.has_dependants is True}
    
    @classmethod
    def model_dependants(cls, collection: list = None):
        return model_dependants(cls, collection or list())

    @classmethod
    def from_context(cls, key: str = None) -> Self:
        if key is None:
            return None
        data = cls.get_context().get(key, None)
        if data:
            return cls.safe_create(**data)
        return None
    
    @classmethod
    async def set_context(cls):
        context.run(cls.CTXVAR.set, make_dict(await cls.fetch_all()))
        
    @classmethod
    def get_context(cls):
        return context.get(cls.CTXVAR)

    @classmethod
    async def fetch_all(cls, query: DetaQuery = None) -> list[dict[str, Jsonable]]:
        return await DetaBase(cls.table()).fetch_all(query or cls.DETA_QUERY)
    
    @classmethod
    async def fetch(cls, query: DetaQuery = None, last: Optional[str] = None, limit: int = 1000) -> FetchResponse:
        return await DetaBase(cls.table()).fetch(query or cls.DETA_QUERY, last, limit)
    
    @classmethod
    async def update_context(cls):
        async with create_task_group() as tks:
            for item in cls.model_dependants():
                tks.start_soon(item.set_context)
                
    def __lt__(self, other):
        return normalize_lower(str(self)) < normalize_lower(str(other))
    
    @classmethod
    def instances_list(cls) -> list[Self]:
        return [cls.from_context(i) for i in cls.get_context().keys()]
    
    @classmethod
    def sorted_instances_list(cls) -> list[Self]:
        return sorted(cls.instances_list())
    
    @classmethod
    def ordered_instances_list(cls) -> list[Self]:
        return ordered(cls.instances_list())
    

def model_dependants(obj: type[ContextBase], collection: list = None):
    collection = collection or list()
    for item in obj.dependant_descriptors().values():
        models = item.dependants
        for model in models:
            if not model in collection:
                collection = model_dependants(model, collection)
    if not obj in collection:
        collection.append(obj)
    return collection



ModelMap: ChainMap[str, type[ContextBase]] = ChainMap()


def context_model(cls: type[ContextBase]):
    @wraps(cls)
    def wrapper():
        cls.CTXVAR = ContextVar(f'{cls.__name__}Var')
        cls.__repr__ = partialmethod(repr_func)
        cls.__eq__ = partialmethod(eq_function)

        ModelMap[cls.__name__] = cls
        return cls
    
    return wrapper()


class BaseDescriptor:
    BASE_NUMBER_TYPES: ClassVar[TupleOfTypes] = (int, float, Decimal)
    BASE_DATETIME_TYPES: ClassVar[TupleOfTypes] = (datetime.datetime, datetime.date)
    STRING_TYPES: ClassVar[TupleOfTypes]
    BASE_TYPES: ClassVar[TupleOfTypes] = tuple([str, *BASE_NUMBER_TYPES, *BASE_DATETIME_TYPES])
    
    def __init__(
            self,
            default: Any = MISSING,
            # callabes
            default_factory: Optional[Callable[[], Any]] = MISSING,
            post_init_factory: Optional[Callable[[], Any]] = MISSING,
            auto: Optional[Callable[[DescriptorModel], Any]] = MISSING,
            update_auto: Optional[Callable[[DescriptorModel], Any]] = MISSING,
            cls_auto: Optional[Callable[[Type[DescriptorModel]], Any]] = MISSING,
            post_parse: Optional[Callable[[Any], Any]] = MISSING,
            pre_parse: Optional[Callable[[Any], Any]] = MISSING,
            # bools
            private: bool = False,
            repr: bool = True,
            compare: bool = True,
            hash: Optional[bool] = None,
            frozen: Optional[bool] = None,
            db: bool = True,
            tablekey: bool = False,
            multiple: bool = False,
            # maps
            metadata: Optional[Mapping] = None,
            # strings
            label: Optional[str] = None,
            table: Optional[str] = None,
            item_name: Optional[str] = None,
            # lists
            tables: Optional[list[str]] = None
    ):
        self._default = default
        self.private = private
        self.auto = auto
        self.update_auto = update_auto
        self.default_factory = default_factory
        self.post_init_factory = post_init_factory
        self.cls_auto = cls_auto
        self._label = label
        self._repr = repr
        self.compare = compare
        self.hash = hash
        self.metadata = metadata
        self.table = table
        self.tables = tables
        self.multiple = multiple
        self._item_name = item_name
        self.db = db
        self._tablekey = tablekey
        self.frozen = frozen
        self.post_parse = post_parse
        self.pre_parse = pre_parse
        if self.hash is True:
            assert any([self.granted is True, self.required is True]), f'If "hash" is True, the attribute is "granted" or "required" need be True'
        
    def __repr__(self):
        return '{}({})'.format(
                type(self).__name__,
                ', '.join([f'{k}={getattr(self, k)!r}' for k in [
                        'field_type', 'public_name', 'required', 'owner', 'dependants', 'db'
                ]])
        )
    
    @property
    def public(self):
        return True if all([self.private == False, self.repr == True]) else False
    
    @property
    def has_dependants(self):
        return True if any([self.tables is not None, self.table is not None]) else False
    
    @property
    def tablekey(self):
        return all([self.has_dependants is True, any([self._tablekey is True, self.tables is not None])])
    
    @property
    def item_name(self):
        if self._item_name:
            return self._item_name
        elif self.table:
            return ModelMap.get(self.table).item_name()
        return re.sub(r'_key', '', self.public_name)
            
    @property
    def repr(self):
        if self.private:
            return False
        return self._repr
        
    @property
    def dependants(self) -> tuple[Optional[Type[ContextBase]]]:
        if self.tables:
            return tuple([ModelMap.get(item) for item in self.tables])
        elif self.table:
            return tuple([ModelMap.get(self.table)])
        return tuple()
    
    @property
    def auto_or_factory(self):
        return True if any([
                self.default_factory is not MISSING,
                self.auto is not MISSING,
                self.cls_auto is not MISSING,
                self.update_auto is not MISSING,
                self.post_init_factory is not MISSING,
        ]) else False
    
    @property
    def required(self):
        return all([self._default is MISSING, self.auto_or_factory is False])
        # return True if all([
        #         self._default is MISSING,
        #         self.default_factory is MISSING,
        #         self.auto is MISSING,
        #         self.cls_auto is MISSING,
        #         self.update_auto is MISSING,
        #         self.post_init_factory is MISSING,
        # ]) else False
    
    @property
    def granted(self):
        return any([is_null(self._default) is False, self.auto_or_factory is True])
    
    @property
    def default(self):
        if self._default is MISSING:
            if self.auto_or_factory is True:
                return None
        return self._default
    
    @property
    def label(self):
        return self._label or self.public_name
    
    @property
    def field_type(self):
        return get_type_hints(self.owner)[self.public_name]
    
    def __set_name__(self, owner, name):
        self.private_name = f'_{name}'
        self.public_name = name
        self.owner: Type[DescriptorModel] = owner
    
    def __get__(self, instance, owner=None):
        if instance is None:
            return self.default
        return getattr(instance, self.private_name)
    
    def __set__(self, instance, value):
        if self.frozen:
            if not is_null(value):
                value = getattr(instance, self.private_name, value)
        else:
            value = self.parse(instance, self.set_lookup(instance, value))
        self.validate(instance, value)
        setattr(instance, self.private_name, value)
        if not is_null(value):
            if self.has_dependants:
                if self.tablekey:
                    model = ModelMap.get(value.split('.')[0])
                    setattr(instance, self.item_name, model.from_context(value.split('.')[-1]))
                else:
                    model = ModelMap.get(self.table)
                    setattr(instance, self.item_name, model.from_context(value))

    
    def set_lookup(self, instance, value):
        if self.update_auto is not MISSING:
            value = self.update_auto(instance)
        else:
            if value is None:
                if self.auto is not MISSING:
                    value = self.auto(instance)
                elif self.cls_auto is not MISSING:
                    value = self.cls_auto(self.owner)
                if self.default_factory is not MISSING:
                    value = self.default_factory()
        return value
    
    def parse(self, instance, value):
        if all([is_null(value) is False, is_null(self.pre_parse) is False]):
            value = self.pre_parse(value)
        value = Parser.get(value, self.field_type)
        if all([is_null(value) is False, is_null(self.post_parse) is False]):
            value = self.post_parse(value)
        return value
    
    def validate(self, instance, value):
        pass
    
    @property
    def name(self):
        return '{}.{}'.format(self.owner.__name__, self.public_name)
    
    @property
    def type_hint(self):
        return TypeHint(self.field_type)
    
    @property
    def expected_type(self):
        return self.type_hint.expected_type


class BaseValidator(BaseDescriptor):
    def __init__(
            self,
            step: Optional[int, float] = None,
            min: Optional[int, float] = None,
            max: Optional[int, float] = None,
            min_lenght: Optional[int] = None,
            max_lenght: Optional[int] = None,
            predicate: Optional[Callable[[DescriptorModel], bool]] = None,
            **kwargs):
        self.min = min
        self.max = max
        self.step = step
        self.min_lenght = min_lenght
        self.max_lenght = max_lenght
        self.predicate = predicate
        super().__init__(**kwargs)
    
    def validate_null(self, instance, value):
        if is_null(value):
            if self.required:
                raise ValueError(f'{self.name} não pode ser nulo.')
    
    def validate_type(self, instance, value):
        if not self.type_hint.check_type(value):
            raise ValueError(
                f'{self.name} exige como tipo(s) "{self.expected_type}". O encontrado para "{value}" foi "{type(value)}".')
    
    def validate_other(self, instance, value):
        if self.field_type in self.BASE_NUMBER_TYPES:
            self.validate_min(instance, value)
            self.validate_max(instance, value)
        elif hasattr(self.field_type, '__len__'):
            self.validate_min_length(instance, value)
            self.validate_max_length(instance, value)
        self.validate_predicate(instance, value)
    
    def validate_min_length(self, instance, value):
        if self.min_lenght:
            if len(value) < self.min_lenght:
                raise ValueError(
                    f'{self.name} não pode ter tamanho menor que "{self.min_lenght}". O encontrado para "{value}" é "{len(value)}".')
    
    def validate_max_length(self, instance, value):
        if self.max_lenght:
            if len(value) > self.max_lenght:
                raise ValueError(
                    f'{self.name} não pode ter tamanho maior que "{self.max_lenght}". O encontrado para "{value}" é "{len(value)}".')
    
    def validate_min(self, instance, value):
        if self.min:
            if self.min > value:
                raise ValueError(f'{self.name} não pode ser menor que "{self.min}". O encontrado é "{value}".')
    
    def validate_max(self, instance, value):
        if self.max:
            if self.max < value:
                raise ValueError(f'{self.name} não pode ser maior que "{self.max}". O encontrado é "{value}".')
    
    def validate_predicate(self, instance, value):
        if self.predicate:
            if self.predicate(value) is False:
                raise ValueError(f'{self.name} não passou no teste de predicativo com o valor "{value}".')
    
    def validate(self, instance, value):
        self.validate_null(instance, value)
        if not is_null(value):
            self.validate_type(instance, value)
            self.validate_other(instance, value)


class Descriptor(BaseDescriptor):
    pass


class Validator(BaseValidator):
    pass


