from http import HTTPStatus
from google.cloud import secretmanager
from fastapi import HTTPException
from loguru import logger

# Create the Secret Manager client.


client = secretmanager.SecretManagerServiceClient()


def get_secret(
        project_number: str,
        secret_name: str,
        version: str = "latest") -> str:
    """Get the secret value from gcp secret manager
        secret = get_secret(
                name_of_the_secret: str,
                gcp_project_number: str,
                version_id: str)
        Args:
            project_number: A unique gcp project id, where the secret exists
            secret_name: Name of the secret to access
            version: version of secret, default latest

        Returns:
            Secret value in string format

        Raises:
            HTTPException if secret id is not provided
            Exception
    """

    if not secret_name:
        logger.error("No secret id provided")
        raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Its not you its us, please try again in sometime")

    name = (f'projects/{project_number}/secrets/{secret_name}/versions/'
            '{version_id}')

    # Access the secret version.
    response = client.access_secret_version(name=name)

    # Return the decoded payload.
    return str(response.payload.data.decode('UTF-8'))
