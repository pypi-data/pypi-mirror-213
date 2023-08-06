"""Call the pref.ai api"""
import os
import requests
import json
from typing import Optional, Dict

class PrefaiError(Exception):
    def __init__(
        self,
        code=None,
        detail=None,
        headers=None,
    ):
        self.code = code
        self.detail = detail
        self.headers = headers

    def __str__(self):
        return f"Pref.ai request failed [{self.code}]: {self.detail}"


class PrefaiTimeoutError(PrefaiError):
    pass

class PrefaiClient:
    _api_base_url = 'https://api.pref.ai'
    # _api_base_url = 'http://127.0.0.1:8000'

    def __init__(self, api_key: str = None):
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.getenv('PREFAI_API_KEY')

    def add_record(self,
        user_action: str,
        context: Optional[str] = None,
        user_email: Optional[str] = None,
        user_id: Optional[str] = None,
        interaction_title: Optional[str] = None,
        observation: Optional[str] = None,
        create_observation: Optional[bool] = True,
    ) -> Dict:
        """
        """

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                f"{self._api_base_url}/v1/records/add",
                json={
                    "user_email": user_email,
                    "user_id": user_id,
                    "user_action": user_action,
                    "context": context,
                    "interaction_title": interaction_title,
                    "observation": observation,
                    "create_observation": create_observation,
                },
                headers=headers,
                timeout=5
            )

            response.raise_for_status()
            json_response = response.json()

            return json_response
            # return {
            #     "index": json_response["index"],
            #     "expected_cost": json_response["expected_cost"],
            # }

        except requests.exceptions.Timeout:
            raise PrefaiTimeoutError("Request timed out")

        except requests.HTTPError as http_err:
            # Get details:
            detail = None
            json_body = None
            response_content = response.content.decode()
            if response_content:
                json_body = json.loads(response_content)
                detail = json_body.get('detail')
            # Construct PrefaiError
            raise PrefaiError(
                code=http_err.response.status_code,
                detail=detail,
                headers=http_err.response.headers or {},
            )


    def retrieve_records(self,
        user_action: str,
        context: Optional[str] = None,
        user_email: Optional[str] = None,
        user_id: Optional[str] = None,
        max_results: Optional[int] = 3,
        min_similarity: Optional[float] = None,
    ) -> Dict:

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                f"{self._api_base_url}/v1/records/retrieve",
                json={
                    "context": context,
                    "user_action": user_action,
                    "user_email": user_email,
                    "user_id": user_id,
                    "max_results": max_results,
                    "min_similarity": min_similarity,
                },
                headers=headers,
                timeout=5
            )

            response.raise_for_status()
            json_response = response.json()

            return json_response

        except requests.exceptions.Timeout:
            raise PrefaiTimeoutError("Request timed out")

        except requests.HTTPError as http_err:
            response_content = response.content.decode()
            if response_content:
                response_dict = json.loads(response_content)
                if 'detail' in response_dict:
                    raise PrefaiError(f"Request failed: {http_err}. Reason: {response_dict['detail']}")
            raise PrefaiError(f"Request failed: {http_err}")

    def pref_prompt(self,
        user_action: str,
        context: Optional[str] = None,
        user_email: Optional[str] = None,
        user_id: Optional[str] = None,
        max_tokens: Optional[int] = 300,
        min_similarity: Optional[float] = None,
    ) -> Dict:

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                f"{self._api_base_url}/v1/prompt/new",
                json={
                    "context": context,
                    "user_action": user_action,
                    "user_email": user_email,
                    "user_id": user_id,
                    "max_tokens": max_tokens,
                    "min_similarity": min_similarity,
                },
                headers=headers,
                timeout=5
            )

            response.raise_for_status()
            json_response = response.json()

            return json_response

        except requests.exceptions.Timeout:
            raise PrefaiTimeoutError("Request timed out")

        except requests.HTTPError as http_err:
            response_content = response.content.decode()
            if response_content:
                response_dict = json.loads(response_content)
                if 'detail' in response_dict:
                    raise PrefaiError(f"Request failed: {http_err}. Reason: {response_dict['detail']}")
            raise PrefaiError(f"Request failed: {http_err}")

# Initialize client
prefai_client = PrefaiClient()
