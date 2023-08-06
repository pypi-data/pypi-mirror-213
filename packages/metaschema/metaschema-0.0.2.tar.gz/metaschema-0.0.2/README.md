# Meta Schema

This library contains the Pydantic models for the metadata schema standard outlined in this [Schema Guide](https://mah0001.github.io/schema-guide/).

The pydantic models for each data type will allow for an easy conversion across JSON, dict, and Python-objects (Pydantic model). Additionally, the metadata is also automatically validated using the expected field types to guarantee that the metadata is consistent.


# Install

The package is available on PyPi:

```
pip install metaschema
```

# Notes

Generating the models from the JSON schema. This is done using the `datamodel-codegen`.

First, download the JSON schema from NADA API. For example, for documents (https://ihsn.github.io/nada-api-redoc/catalog-admin/#tag/Documents). Store the JSON schema in `data/examples/doc.json`.

Then, run the following command to generate the models. Note that the `--input-file-type` is `json` and not `jsonschema`

```
poetry run datamodel-codegen  --input data/examples/doc.json --input-file-type json --output src/metaschema/doc.py
```

We then change the `Model` to a more explicit name: `DocModel` .
