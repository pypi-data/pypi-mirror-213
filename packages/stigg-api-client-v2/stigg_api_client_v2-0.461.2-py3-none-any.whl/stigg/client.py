from stigg.generated import Client


class StiggClient(Client):
    pass


class Stigg:
    @staticmethod
    def create_async_client(
            api_key: str, api_url: str = "https://api.stigg.io/graphql"
    ) -> StiggClient:
        headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
        return StiggClient(url=api_url, headers=headers)
