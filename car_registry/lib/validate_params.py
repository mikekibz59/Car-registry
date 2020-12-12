"""Helper file to handle validations """

from rest_framework.exceptions import ParseError, ValidationError


def validate_post_car_params(post_dict: dict) -> None:
    """helper method to validating car dict """

    required_fields = ('make_id', 'model_id', 'submodel_id',
                       'year', 'price', 'mileage')

    _validate_presence_of_fields_in_dict(required_fields, post_dict)

    _validate_the_required_fields_are_not_null(required_fields, post_dict)


def validate_query_params(query_params: dict) -> None:
    """ Helper method to validate car query dict"""

    if not query_params:
        return

    for k, v in query_params.items():

        if v and v.isdigit() and float(v) < 0:
            raise ParseError(f'{k} cannot be less than Zero')


def _validate_presence_of_fields_in_dict(fields: tuple,
                                         dict_: dict) -> None:
    """Check of field presence in dict_ """
    for field in fields:
        if field not in dict_:
            raise ParseError(f'{field} should be in the request param')


def _validate_the_required_fields_are_not_null(fields: tuple,
                                               dict_: dict) -> None:
    """ Check if fields are null """
    for field in fields:
        if not dict_[field]:
            raise ValidationError(f'{field} cannot be blank')
