async def parsed_sql_pydantic(schema, data):
    """
    Convert SQLAlchemy model to Pydantic model.
    """
    if not schema:
        raise ValueError("Schema is required")
    if not data:
        raise ValueError("Data is required")

    # Convert SQLAlchemy model to dictionary
    data_dict = data.__dict__

    # Remove the SQLAlchemy specific attributes
    for key in list(data_dict.keys()):
        if key.startswith("_"):
            del data_dict[key]

    # Convert to Pydantic model
    pydantic_model = schema(**data_dict)

    return pydantic_model
