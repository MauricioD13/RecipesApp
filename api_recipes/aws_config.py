import boto3


def get_parameters(parameter_names: list, region: str) -> dict:
    """_summary_

    Args:
        parameter_names (list): key string to retrieve the parameter
        region (str): ssm aws region

    Returns:
        dict: all the parameters in format key - value
    """
    ssm = boto3.client("ssm", region_name=region)
    response = ssm.get_parameters(Names=parameter_names, WithDecryption=True)
    parameters = {param["Name"]: param["Value"] for param in response["Parameters"]}
    return parameters


# Usage
if __name__ == "__main__":
    param_names = [
        "/myapp/prod/db_username",
        "/myapp/prod/db_password",
        "/myapp/prod/db_endpoint",
    ]
    params = get_parameters(param_names, "eu-west-1")
    db_username = params["/myapp/prod/db_username"]
    db_password = params["/myapp/prod/db_password"]
    db_endpoint = params["/myapp/prod/db_endpoint"]
