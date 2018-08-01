# Simple File Uploader


This is a simple python script written with [cherrypy](https://cherrypy.org/) to upload files based on api keys requests, it was used with [Segments](https://github.com/AandersonL/Segments-Android) project to upload and retrieve images from a remote server.

### Setup

You will need cherrypy in order to use the server propeply, just hit:

```
pip3 install cherrypy --user
```

After that, you need gen your api key to use in the upload requests

```
python3 key.py
```
This will genarate a random key that you need to pass as first argument, after that you just need

```
python3 api.py <api_key>
```

You also can save in some file then use the same api key everytime.

```
python3 key.py > key && python3 api.py $(cat key)
```



### Request

This is the request structure expected:
```javascript
header: {
  Api-Key: <api>,
  data: file_data
}
```
[Axios](https://github.com/axios/axios) example:
```javascript
axios({
  method: 'POST',
  data: file_data,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'multipart/form-data',
    'api_key': API_KEY
  },
  url: URL
});
```
The only response send back is the file url for future uses (download, image source or stream), there is only one route here, use GET to retrieve files and POST method to upload files.
# Warning

This is a simple file uploader only, its not recommend to use widely in a huge application, just plug-in in your server and use to upload your songs, videos and simple files, no sensitive data. enjoy :D 
