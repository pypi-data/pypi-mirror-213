# _*_coding:utf-8_*_
from rest_framework.views import APIView

from ..services.user_bank_service import UserBankCardsService
from ..utils.custom_tool import request_params_wrapper
from ..utils.model_handle import util_response
from ..utils.user_wrapper import user_authentication_force_wrapper


# 银行卡管理
class UserBankAPIView(APIView):
    # 卡片列表
    @request_params_wrapper
    def get(self, *args, request_params=None, detail_id=None, **kwargs):
        data, err = UserBankCardsService.list(params=request_params, detail_id=detail_id)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    # 添加卡片
    @user_authentication_force_wrapper
    @request_params_wrapper
    def post(self, *args, request_params=None, user_info, **kwargs):
        request_params.setdefault("user_id", user_info.get("user_id"))
        data, err = UserBankCardsService.add(params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response()

    # # 修改卡片
    @user_authentication_force_wrapper
    @request_params_wrapper
    def put(self, *args, request_params=None, **kwargs):
        pk = request_params.pop("id", None) or request_params.pop("pk", None)
        data, err = UserBankCardsService.edit(pk=pk, update_params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    # 删除卡片
    @user_authentication_force_wrapper
    @request_params_wrapper
    def delete(self, *args, request_params=None, **kwargs):
        pk = request_params.pop("id", None) or kwargs.pop("pk", None)
        data, err = UserBankCardsService.delete(pk=pk)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
