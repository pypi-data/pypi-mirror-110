# Introduction
This is a HTTP client to [Purview](https://azure.microsoft.com/sv-se/services/purview/) as the complemntary of Python [wrapper](https://github.com/wjohnson/pyapacheatlas) for Appache Atlas.

# Installation

Install the package
```
pip install -i https://test.pypi.org/simple/ pvclient
```

# Authentication

Create a file named as `auth.json` in the same directory
```
{
    "tenant_id": "Tentant id where Purview accounts are provisioned under", 
    "client_id": "Client id of a service principal which is used to run the program", 
    "client_secret": "Client secret of a service principal which is used to run the program",
    "subscription_id":"Subscription id where Purview accounts are provisioned under",
    "Groups id": "Id of group(s) who interactively work with Purview"
}
```
# Configurations:

The content of `configs.json` looks like
```
{
    "Resource-group": "Resource group name",
    "location" : "location",
    "Purview-account-name": "Name of Purview account"
}
```
# Usage:
```
purview [-h] [--create-purview] [--assign-roles] [--delete-purview] [--create-glossary CREATE_GLOSSARY] [--list-terms] [--upload-entities]
                  [--import-terms IMPORT_TERMS] [--delete-term DELETE_TERM] [--delete-all-terms] [--list-term-templates]
                  [--import-term-templates IMPORT_TERM_TEMPLATES] [--delete-term-templates DELETE_TERM_TEMPLATES]

Interaction with Purview

optional arguments:
  -h, --help            show this help message and exit
  --create-purview
  --assign-roles
  --delete-purview
  --create-glossary CREATE_GLOSSARY
                        Create a glossary with name
  --list-terms
  --upload-entities
  --import-terms IMPORT_TERMS
  --delete-term DELETE_TERM
                        Delete a term from the default Glossary
  --delete-all-terms    Delete all terms from the default Glossary
  --list-term-templates
                        List all term templates from the default Glossary
  --import-term-templates IMPORT_TERM_TEMPLATES
                        Import term templates from a file to the default Glossary
  --delete-term-templates DELETE_TERM_TEMPLATES
                        Delete all templates from a file from the default Glossary
```
