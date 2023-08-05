# basylic-python-client
Class to access Basylic API

# Summary

Developed by ETAONIS, Basylic is a SaaS solution performing document fraud detection with "state-of-the-art" performances. The solution is also used as a powerful tool to extract information from documents. This module provides a Python interface for accessing Basylic.
    
# Installation

This module is available on PyPI. You can install it with `pip` command:

```pip install basylic```

Alternatively, you can access the module source code on GitHub:

* https://github.com/basylic-team/basylic-python-client

# Basic usage

To access the API, a token must be provided. We recommend you to store this token as an environment variable called `BASYLIC_ACCESS_TOKEN` and then import the module. 

```
from basylic import Basylic
basylic = Basylic()
```

Alternatively, if your token is stored in a non-standard location, you can specify it with argument `token` during class instantiation:

```
from basylic import Basylic
basylic = Basylic(token=...)
```

2. Two arguments are mandatory: `file_path` and `document_type`:
```
basylic.send_document(file_path = "corinne-berthier-recto-verso.pdf", document_type="french_ids")
```
* The `file_path` argument is a string with the document path (e.g.: "~/FILE.pdf") 
* `document_type` is a string specifying which Basylic API to call (e.g.: "french_ids")

Possible values for `document_type` are: `'french_ids'`, `'rib'`, `'ri'`, `'avis-imposition'`...

With those arguments specified, `send_document` returns a comprehensive JSON document.

3. Data about applicants can also be joined to the API call:
```
applicants_information = {"applicant_0": {"identity": "BERTHIER CORINNE"}}
basylic_result = basylic.send_document(
    file_path="corinne-berthier-recto-verso.pdf", 
    document_type="french_ids", applicants_information=applicants_information)
print(basylic_result)
```

4. And various arguments could be passed as kwargs. For example:
* a. `save_report=True` will save the result of your request in your user space on Basylic Portal;
* b. `with_image=True` will return a base64 image for each recognised document;
* c. `reference='abc...'` will add a key-value pair to the API output. If this key is specified, the report will appear under this reference in Basylic Portal.

For example, this code: 

```
applicants_information = {"applicant_0": {"identity": "BERTHIER CORINNE"}}
basylic_result = basylic.send_document(
    file_path="corinne-berthier-recto-verso.pdf", 
    document_type="french_ids", applicants_information=applicants_information,
    with_image=True, reference="XX45678-BERTH-PARIS", save_report=True)
print(basylic_result)
```

will act in the following way:

1. Upload of document whose path is `file_path` to Basylic service `french_ids`;
2. Produce of a JSON document `basylic_result` with all relevant information;
3. Compare `identity` provided and identity extracted by Basylic OCR;
5. A base64 encoded image will be returned in the approriate key of `7basylic_result`;
6. The reference `XX45678-BERTH-PARIS` will be included in `basylic_result` and used as reference in Basylic's Portal.

