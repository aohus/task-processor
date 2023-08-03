from rest_framework.response import Response
import json


def SuccessResponse(status=200):
    return Response(
        status=status,
        data=dict(result_code=0, result_msg="success"),
    )


def SuccessResponseWithData(data, status=200):
    return Response(
        status=status,
        data=dict(result_code=0, result_msg="success", data=data),
    )


def ErrorResponse(msg, status=400):
    return Response(
        status=status,
        data=dict(result_code=999, result_msg=msg),
    )
