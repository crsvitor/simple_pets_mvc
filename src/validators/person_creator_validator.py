from pydantic import BaseModel, constr, ValidationError
from src.views.http_types.http_request import HttpRequest
from src.errors.error_types.http_unprocessable_entity import HttpUnprocessableEntityError

def person_creator_validator(http_request: HttpRequest) -> None:

    class BodyData(BaseModel):
        first_name: constr(min_length=1) # type: ignore
        last_name: constr(min_length=1) # type: ignore
        age: int # type: ignore
        pet_id: int # type: ignore

    try:
        BodyData(**http_request.body)
    except ValidationError as validation_error:
        raise HttpUnprocessableEntityError(validation_error.errors()) from validation_error
