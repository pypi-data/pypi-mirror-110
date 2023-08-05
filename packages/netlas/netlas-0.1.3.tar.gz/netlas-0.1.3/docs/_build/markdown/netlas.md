# netlas package

## Netlas


### class netlas.client.Netlas(api_key: str = '', apibase: str = 'https://app.netlas.io', debug: bool = False)
Bases: `object`


#### count(query: str, datatype: str = 'response', indices: str = '')
Calculate total count of query string results


* **Parameters**

    
    * **query** (*str*) – Search query string


    * **datatype** (*str**, **optional*) – Data type (choises: response, cert, domain), defaults to “response”


    * **indices** (*str**, **optional*) – Comma-separated IDs of selected data indices (can be retrieved by indices method), defaults to “”



* **Returns**

    JSON object with total count of query string results



* **Return type**

    dict



#### download(query: str, fields: list = [], source_type: str = 'include', datatype: str = 'response', size: int = 10, indices: str = '')
Download data from Netlas


* **Parameters**

    
    * **query** (*str*) – Search query string


    * **fields** (*list*) – Comma-separated list of fields to include/exclude, defaults to []


    * **source_type** (*str*) – Include or exclude fields (choices: include, exclude), defaults to “include”


    * **datatype** (*str**, **optional*) – Data type (choices: response, cert, domain), defaults to “response”


    * **size** (*int**, **optional*) – Download documents count, defaults to 10


    * **indices** (*list**, **optional*) – Comma-separated IDs of selected data indices (can be retrieved by indices method), defaults to “”



* **Returns**

    Iterator of raw data



* **Return type**

    Iterator[bytes]



#### host(host: str, hosttype: str = 'ip', index: str = '')
Get full information about host (ip or domain)


* **Parameters**

    
    * **host** (*str*) – IP or domain string


    * **hosttype** (*str**, **optional*) – “ip” or “domain”, defaults to “ip”


    * **index** (*str**, **optional*) – ID of selected data indices (can be retrieved by indices method), defaults to “”



* **Returns**

    JSON object with full information about host



* **Return type**

    dict



#### indices()
Get available data indices


* **Returns**

    List of available indices



* **Return type**

    list



#### profile()
Get user profile data


* **Returns**

    JSON object with user profile data



* **Return type**

    dict



#### query(query: str, datatype: str = 'response', page: int = 0, indices: str = '')
Send search query to Netlas API


* **Parameters**

    
    * **query** (*str*) – Search query string


    * **datatype** (*str**, **optional*) – Data type (choises: response, cert, domain), defaults to “response”


    * **page** (*int**, **optional*) – Page number of data, defaults to 0


    * **indices** (*str**, **optional*) – Comma-separated IDs of selected data indices (can be retrieved by indices method), defaults to “”



* **Returns**

    search query result



* **Return type**

    dict



#### stat(query: str, indices: str = '')
Get statistics of responses query string results


* **Parameters**

    
    * **query** (*str*) – Search query string


    * **indices** (*str**, **optional*) – Comma-separated IDs of selected data indices (can be retrieved by indices method), defaults to “”



* **Returns**

    JSON object with statistics of responses query string results



* **Return type**

    dict


## Exception


### exception netlas.exception.APIError(value)
Bases: `Exception`

Basic Netlas.io Exception class
