class ApiError(Exception):
    code = 500
    description = "internal_server_error"


class BadRequest(ApiError):
    code = 400
    description = "bad_request"


class Unauthorized(ApiError):
    code = 401
    description = "unauthorized"


class Forbidden(ApiError):
    code = 403
    description = "forbidden"


class ResourceNotFound(ApiError):
    code = 404
    description = "resource_not_found"


class PreconditionFailed(ApiError):
    code = 412
    description = "precondition_failed"
