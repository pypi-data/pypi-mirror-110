from datetime import datetime
from functools import cached_property, lru_cache
from typing import Any, Dict, Optional, Tuple, Type

from pydantic import validate_model
from tortoise import fields
from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise.contrib.pydantic import PydanticModel, pydantic_model_creator
from tortoise.contrib.pydantic.creator import PydanticMeta
from tortoise.exceptions import NoValuesFetched
from tortoise.models import Model
from tortoise.queryset import AwaitableQuery


def patch_pydantic_model(model: Type[PydanticModel]) -> Type[PydanticModel]:
    # 解决数据动态加载的问题
    for field in model.__fields__.values():
        if not field.required:
            continue
        field.required = not issubclass(field.type_, PydanticModel)
        field.allow_none = True
        config = getattr(field.type_, "__config__", None)
        if config:
            orig_model: Optional[BaseModel] = getattr(
                config, "orig_model", None
            )
            if orig_model:
                field.type_ = orig_model.detail()

    def from_orm(obj: Any) -> PydanticModel:
        obj = model._decompose_class(obj)  # type: ignore
        new_obj: Dict[str, Any] = {}
        for k, v in obj.items():
            if k not in model.__fields__:
                continue

            if isinstance(v, AwaitableQuery):
                v = None
            if isinstance(v, fields.ReverseRelation) or isinstance(
                v, fields.ManyToManyRelation
            ):
                try:
                    v.__len__()
                except NoValuesFetched:
                    v = None
            new_obj[k] = v

        m = model.__new__(model)
        values, fields_set, validation_error = validate_model(model, new_obj)
        if validation_error:
            raise validation_error
        object.__setattr__(m, "__dict__", values)
        object.__setattr__(m, "__fields_set__", fields_set)
        m._init_private_attributes()
        return m

    def dict(self: model, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        if kwargs and kwargs.get("exclude_none") is not None:
            kwargs["exclude_none"] = True
        return super(model, self).dict(*args, **kwargs)

    model.from_orm = from_orm
    model.dict = dict

    return model


class BaseModel(Model):
    id: int = fields.IntField(pk=True)
    created_at: datetime = fields.DatetimeField(null=False, auto_now_add=True)
    updated_at: datetime = fields.DatetimeField(null=False, auto_now=True)

    class Meta:
        abstract = True

    # class PydanticMeta:
    #     list_exclude: Tuple[str, ...] = ()  # 列表排除
    #     detail_include: Tuple[str, ...] = ()  # 详情叠加

    @cached_property
    def computed_cache(self) -> Dict[str, Any]:
        return {}

    @classmethod
    @lru_cache
    def list(cls) -> Type[PydanticModel]:
        meta: PydanticMeta = getattr(cls, "PydanticMeta")
        list_exclude: Tuple[str, ...] = getattr(meta, "list_exclude", ())
        return patch_pydantic_model(
            pydantic_model_creator(
                cls, name=cls.pydantic_name() + ".list", exclude=list_exclude
            )
        )

    @classmethod
    @lru_cache
    def detail(cls) -> Type[PydanticModel]:
        meta: PydanticMeta = getattr(cls, "PydanticMeta")
        detail_include: Tuple[str, ...] = getattr(meta, "detail_include", ())
        return patch_pydantic_model(
            pydantic_model_creator(
                cls,
                name=cls.pydantic_name() + ".detail",
                include=detail_include,
            )
        )

    @classmethod
    def pydantic_name(cls) -> str:
        return f"{cls.__module__}.{cls.__qualname__}"

    def update(self, input: Any):
        dic: Dict[str, Any] = (
            input
            if isinstance(input, dict)
            else input.dict(exclude_unset=True)
        )
        self.update_from_dict(dic)  # type: ignore

    def get_computed(self, field: str, default: Any = None) -> Any:
        return self.computed_cache.get(field, default)

    async def fetch_related(
        self, *args: Any, using_db: Optional[BaseDBAsyncClient] = None
    ) -> None:
        meta: Optional[PydanticMeta] = getattr(
            self.__class__, "PydanticMeta", None
        )
        if meta and hasattr(meta, "computed"):
            for field in args:
                if field in meta.computed:
                    f = getattr(self, f"compute_{field}", None)
                    if not f:
                        continue
                    self.computed_cache[field] = await f()
        normlized_args = [
            field.replace(".", "__") if isinstance(field, str) else field
            for field in args
        ]
        return await super().fetch_related(*normlized_args, using_db=using_db)
