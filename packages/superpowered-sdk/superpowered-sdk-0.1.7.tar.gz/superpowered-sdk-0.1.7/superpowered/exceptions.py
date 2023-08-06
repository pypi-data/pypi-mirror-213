import json
import os

def read_errors():
    module_path = os.path.abspath(__file__)
    module_dir = os.path.dirname(module_path)
    errors_path = os.path.join(module_dir, 'errors.json')
    
    with open(errors_path) as file:
        errors_data = json.load(file)
    
    return errors_data

ERRORS = {e['code']: e for e in read_errors()}


class DuplicateKnowledgeBaseError(Exception):
    pass


class DuplicateDocumentContentError(Exception):
    pass


class DocumentLengthError(Exception):
    pass


class AuthenticationFailedError(Exception):
    pass


class InternalServerError(Exception):
    pass


class InvalidRequestError(Exception):
    pass


class TimeoutError(Exception):
    pass


class NotFoundError(Exception):
    pass


exception_classes = {
    "AuthenticationFailedError": AuthenticationFailedError,
    "DuplicateDocumentContentError": DuplicateDocumentContentError,
    "DocumentLengthError": DocumentLengthError,
    "InternalServerError": InternalServerError,
    "InvalidRequestError": InvalidRequestError,
    "NotFoundError": NotFoundError,
    "TimeoutError": TimeoutError,
    "DuplicateKnowledgeBaseError": DuplicateKnowledgeBaseError
}


for code, error in ERRORS.items():
    error['python_sdk_exception'] = exception_classes[error['python_sdk_exception']]
