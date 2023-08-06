import base64
import hashlib
import os
import requests
import warnings

from .exceptions import ERRORS


_base_url = 'https://api.superpowered.ai/v1'


def get_base_url():
    return _base_url


def set_base_url(url: str):
    global _base_url
    _base_url = url


API_KEY_PAIR = (None, None)
def set_api_key(key_id: str, key_secret: str):
    global API_KEY_PAIR
    API_KEY_PAIR = (key_id, key_secret)


def auth():
    # default to use the API_KEY_PAIR if set
    if API_KEY_PAIR[0] and API_KEY_PAIR[1]:
        return API_KEY_PAIR

    # otherwise, use the environment variables
    if not os.getenv('SUPERPOWERED_API_KEY_ID') or not os.getenv('SUPERPOWERED_API_KEY_SECRET'):
        raise Exception('SUPERPOWERED_API_KEY_ID and SUPERPOWERED_API_KEY_SECRET must be set as environment variables')
    return (os.getenv('SUPERPOWERED_API_KEY_ID'), os.getenv('SUPERPOWERED_API_KEY_SECRET'))


def make_api_call(args: dict) -> dict:
    """
    Make an API call to the Superpowered API
    """
    resp = requests.request(**args)
    headers = resp.headers
    if args['method'] == 'DELETE':
        return resp.ok
    resp_json = resp.json()
    if headers.get('error_code'):
        error_code = int(headers['error_code'])
        if error_code in ERRORS:
            try:
                raise ERRORS[error_code]['python_sdk_exception'](resp_json, resp.status_code)
            except KeyError:
                raise Exception(resp_json, resp.status_code)
        else:
            raise Exception(resp_json, resp.status_code)
    elif not resp.ok:
        print(args)
        raise Exception(resp_json, resp.status_code)
    else:
        return resp_json


def get_total_storage():
    """
    GET /usage/total_storage
    """
    args = {
        'method': 'GET',
        'url': f'{get_base_url()}/usage/total_storage',
        'auth': auth(),
    }
    return make_api_call(args)


def create_knowledge_base(title: str, description: str = None, supp_id: str = None) -> dict:
    """
    POST /knowledge_bases
    """
    data = {
        'title': title,
    }
    if description:
        data['description'] = description
    if supp_id:
        data['supp_id'] = supp_id
    args = {
        'method': 'POST',
        'url': f'{get_base_url()}/knowledge_bases',
        'json': data,
        'auth': auth(),
    }
    return make_api_call(args)


def list_knowledge_bases(title: str = None, supp_id: str = None) -> dict:
    """
    GET /knowledge_bases
    """
    params = {}
    if title:
        params['title_begins_with'] = title
    if supp_id:
        params['supp_id'] = supp_id

    args = {
        'method': 'GET',
        'url': f'{get_base_url()}/knowledge_bases',
        'params': params,
        'auth': auth(),
    }
    resp = make_api_call(args)
    knowledge_bases = resp.get('knowledge_bases', [])

    while resp.get('next_page_token'):
        args['params']['next_page_token'] = resp['next_page_token']
        resp = make_api_call(args)
        knowledge_bases.extend(resp.get('knowledge_bases', []))

    return knowledge_bases


def get_knowledge_base(knowledge_base_id: str) -> dict:
    """
    GET /knowledge_bases/{knowledge_base_id}
    """
    args = {
        'method': 'GET',
        'url': f'{get_base_url()}/knowledge_bases/{knowledge_base_id}',
        'auth': auth(),
    }
    return make_api_call(args)


def delete_knowledge_base(knowledge_base_id: str) -> bool:
    """
    DELETE /knowledge_bases/{knowledge_base_id}
    """
    args = {
        'method': 'DELETE',
        'url': f'{get_base_url()}/knowledge_bases/{knowledge_base_id}',
        'auth': auth(),
    }
    return make_api_call(args)


def create_document_via_text(knowledge_base_id: str, content: str, title: str = None, link_to_source: str = None, description: str = None, supp_id: str = None) -> dict:
    """
    POST /knowledge_bases/{knowledge_base_id}/documents/raw_text
    """
    data = {
        'content': content,
    }
    if title:
        data['title'] = title
    if description:
        data['description'] = description
    if supp_id:
        data['supp_id'] = supp_id
    if link_to_source:
        data['link_to_source'] = link_to_source
    args = {
        'method': 'POST',
        'url': f'{get_base_url()}/knowledge_bases/{knowledge_base_id}/documents/raw_text',
        'json': data,
        'auth': auth(),
    }
    return make_api_call(args)


def create_document_via_url(knowledge_base_id: str, url: str, title: str = None, description: str = None, supp_id: str = None) -> dict:
    """
    POST /knowledge_bases/{knowledge_base_id}/documents/url
    """
    data = {
        'url': url,
    }
    if title:
        data['title'] = title
    if description:
        data['description'] = description
    if supp_id:
        data['supp_id'] = supp_id
    args = {
        'method': 'POST',
        'url': f'{get_base_url()}/knowledge_bases/{knowledge_base_id}/documents/url',
        'json': data,
        'auth': auth(),
    }
    return make_api_call(args)


def create_document_via_file(knowledge_base_id: str, file_path: str, description: str = None, supp_id: str = None) -> dict:
    """
    POST /knowledge_bases/{knowledge_base_id}/documents/request_signed_file_url
    +
    PUT response['temporary_url']
    """
    # read the file and get the encoded md5 for the presigned url request
    with open(file_path, 'rb') as f:
        file_content = f.read()
        file_md5 = hashlib.md5(file_content).hexdigest()
        encoded_md5 = base64.b64encode(bytes.fromhex(file_md5)).decode('utf-8')

    # make the request for the presigned url
    data = {
        'filename': os.path.basename(file_path),
        'method': 'PUT',
        'encoded_md5': encoded_md5,
    }
    if description:
        data['description'] = description
    if supp_id:
        data['supp_id'] = supp_id

    args = {
        'method': 'POST',
        'url': f'{get_base_url()}/knowledge_bases/{knowledge_base_id}/documents/request_signed_file_url',
        'json': data,
        'auth': auth(),
    }
    resp = make_api_call(args)

    # upload the file to the presigned url
    headers = {
        'Content-MD5': encoded_md5,
    }
    args = {
        'url': resp['temporary_url'],
        'data': file_content,
        'headers': headers,
    }
    with requests.put(**args) as r:
        pass

    return resp['document']


def download_file(knowledge_base_id: str, file_name: str, destination_path: str = None) -> bytes:
    """
    POST /knowledge_bases/{knowledge_base_id}/documents/request_signed_file_url
    +
    GET response['temporary_url']
    """
    # make the request for the presigned url
    data = {
        'filename': file_name,
        'method': 'GET',
    }
    args = {
        'method': 'POST',
        'url': f'{get_base_url()}/knowledge_bases/{knowledge_base_id}/documents/request_signed_file_url',
        'json': data,
        'auth': auth(),
    }
    resp = make_api_call(args)
    download_url = resp['temporary_url']

    # download the file from the presigned url
    file = requests.get(download_url).content

    # save the file to the destination path if provided
    # make the file path if it doesn't exist
    if destination_path:
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        with open(destination_path, 'wb') as f:
            f.write(file)

    return file


def list_documents(knowledge_base_id: str, title_begins_with: str = None, link_to_source: str = None, supp_id: str = None, vectorization_status: str = None) -> list:
    """
    GET /knowledge_bases/{knowledge_base_id}/documents
    """
    params = {}
    if title_begins_with:
        params['title_begins_with'] = title_begins_with
    if supp_id:
        params['supp_id'] = supp_id
    if vectorization_status:
        params['status'] = vectorization_status
    if link_to_source:
        params['link_to_source'] = link_to_source

    args = {
        'method': 'GET',
        'url': f'{get_base_url()}/knowledge_bases/{knowledge_base_id}/documents',
        'params': params,
        'auth': auth(),
    }
    resp = make_api_call(args)
    documents = resp.get('documents', [])
    while resp.get('next_page_token'):
        args['params']['next_page_token'] = resp['next_page_token']
        resp = make_api_call(args)
        documents.extend(resp.get('documents', []))

    return documents


def get_document(knowledge_base_id: str, document_id: str) -> dict:
    """
    GET /knowledge_bases/{knowledge_base_id}/documents/{document_id}
    """
    args = {
        'method': 'GET',
        'url': f'{get_base_url()}/knowledge_bases/{knowledge_base_id}/documents/{document_id}',
        'auth': auth(),
    }
    return make_api_call(args)


def update_document(knowledge_base_id: str, document_id: str, title: str = None, description: str = None, supp_id: str = None) -> dict:
    """
    PATCH /knowledge_bases/{knowledge_base_id}/documents/{document_id}
    """
    data = {}
    if title:
        data['title'] = title
    if description:
        data['description'] = description
    if supp_id:
        data['supp_id'] = supp_id
    args = {
        'method': 'PATCH',
        'url': f'{get_base_url()}/knowledge_bases/{knowledge_base_id}/documents/{document_id}',
        'json': data,
        'auth': auth(),
    }
    return make_api_call(args)


def delete_document(knowledge_base_id: str, document_id: str) -> dict:
    """
    DELETE /knowledge_bases/{knowledge_base_id}/documents/{document_id}
    """
    args = {
        'method': 'DELETE',
        'url': f'{get_base_url()}/knowledge_bases/{knowledge_base_id}/documents/{document_id}',
        'auth': auth(),
    }
    return make_api_call(args)


def query(knowledge_base_ids: list, query: str, top_k: int = 5, summarize_results: bool = False):
    """
    BACKWARD COMPATIBILITY
    POST /knowledge_bases/query
    """
    class RenameWarning(Warning):
        pass
    
    warnings.warn(
        message="The 'query' function has been renamed to 'query_knowledge_bases' for clarity.",
        category=RenameWarning,
        stacklevel=2
    )
    return query_knowledge_bases(knowledge_base_ids, query, top_k, summarize_results)


def query_knowledge_bases(knowledge_base_ids: list, query: str, top_k: int = 5, summarize_results: bool = False, summary_system_message: str = None) -> dict:
    """
    POST /knowledge_bases/query
    """
    data = {
        'query': query,
        'knowledge_base_ids': knowledge_base_ids,
    }
    if top_k:
        data['top_k'] = top_k
    if summarize_results:
        data['summarize_results'] = summarize_results
    if summary_system_message:
        data['summary_system_message'] = summary_system_message
    args = {
        'method': 'POST',
        'url': f'{get_base_url()}/knowledge_bases/query',
        'json': data,
        'auth': auth(),
    }
    return make_api_call(args)


def query_passages(query: str, passages: list, top_k: int = 5, max_chunk_length: int = 500, summarize_results: bool = False, summary_system_message: str = None) -> dict:
    """
    POST /query_passages
    """
    data = {
        'query': query,
        'passages': passages,
    }
    if top_k:
        data['top_k'] = top_k
    if max_chunk_length:
        data['max_chunk_length'] = max_chunk_length
    if summarize_results:
        data['summarize_results'] = summarize_results
    if summary_system_message:
        data['summary_system_message'] = summary_system_message
    args = {
        'method': 'POST',
        'url': f'{get_base_url()}/query_passages',
        'json': data,
        'auth': auth(),
    }
    return make_api_call(args)
