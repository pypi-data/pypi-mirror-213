from typing import Any, List, Optional, Callable, Type, Tuple

from fastapi import Depends, HTTPException
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.contrib.pydantic.base import PydanticModel

from fastapi_module_register.base_method import BaseMethod
from fastapi_module_register.schema import BaseApiOut


class TortoiseMethod(BaseMethod):

    def __init__(self, module: Model, depend_func: Optional[Callable] = None)-> None:
        """_summary_

        Args:
            module (Model): The tortoise model
            depend_func (Optional[Callable], optional): _description_. Defaults to None.
        """
        self._module = module
        self._depend_func = depend_func
        self._base_request = pydantic_model_creator(
            module, 
            name=f"{module.__name__}_req",
            exclude=[module._meta.pk_attr]
        )
        self._get_response = pydantic_model_creator(module, name=f"{module.__name__}_get")
        self._base_response = pydantic_model_creator(module, name=f"{module.__name__}_res")

    def get(self, filter_by_pk: bool = False, *args, **kwargs) -> Tuple[Callable, Any]:
        """The http get method
        Args:
            filter_by_pk (bool): Get item by pk
        Returns:
            Callable: _description_
        """
        if filter_by_pk:
            async def wapper(pk: int):
                result = self._module.get(pk=pk)
                result = await self._get_response.from_queryset_single(result)
                return result
            return wapper, self._base_response
        async def wapper():
            results = self._module.all()
            results = await self._get_response.from_queryset(results)
            return results
        return wapper, List[self._get_response]

    def post(
        self,
        depend_func: Optional[Callable] = None,
        request_model: Optional[Type[PydanticModel]] = None
    ) -> Tuple[Callable, Any]:
        """The http post method

        Args:
            depend_func (Optional[Callable], optional): _description_. Defaults to None.
            request_model (Optional[Type[PydanticModel]], optional): _description_. Defaults to None.

        Returns:
            Callable: _description_
        """
        if not request_model:
            request_model = self._base_request

        depend_func = depend_func if depend_func else self._depend_func
        if depend_func:
            async def wapper(req: request_model, _ = Depends(depend_func)):
                save_item = await self._module.create(**req.dict(exclude_unset=True))
                return await self._base_response.from_tortoise_orm(save_item)
            return wapper, self._base_response
        
        async def wapper(req: request_model):
            save_item = await self._module.create(**req.dict(exclude_unset=True))
            return await self._base_response.from_tortoise_orm(save_item)
        return wapper, self._base_response

    def put(
        self,
        depend_func: Optional[Callable] = None,
        request_model: Optional[Type[PydanticModel]] = None
    ) -> Tuple[Callable, Any]:
        """_summary_

        Args:
            depend_func (Optional[Callable], optional): _description_. Defaults to None.
            request_model (Optional[Type[PydanticModel]], optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        if not request_model:
            request_model = self._base_request
        
        depend_func = depend_func if depend_func else self._depend_func
        if depend_func:
            async def wapper(pk: int, req: request_model, _ = Depends(depend_func)):
                await self._module.filter(pk=pk).update(**req.dict(exclude_unset=True))
                return await self._base_response.from_queryset_single(
                    self._module.get(pk=pk)
                )
            return wapper, self._base_response

        async def wapper(pk: int, req: request_model):
            await self._module.filter(pk=pk).update(**req.dict(exclude_unset=True))
            return await self._base_response.from_queryset_single(
                self._module.get(pk=pk)
            )
        return wapper, self._base_response

    def delete(self) -> Tuple[Callable, BaseApiOut]:
        """Delete the item by primary key

        Returns:
            Callable: _description_
        """
        async def wapper(pk: int):
            item = await self._module.get(pk=pk)
            if not item:
                raise HTTPException(status_code=404, detail=f"{self._module.__name__} {pk} not found")
            await item.delete()
            return BaseApiOut()
        return wapper, BaseApiOut
