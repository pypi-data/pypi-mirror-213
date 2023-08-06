
### Blueprints auto-registration example

Run the command and follow the link http://127.0.0.1:5000/api/:

```shell
docker run --rm -ti \
    --name flask_1 \
    -p 5000:5000 \
    -v $(pwd)/examples:/app \
    -v $(pwd)/src:/python_packages \
    -e FLASK_APP="blueprints:create_app()" \
    kyzimaspb/flask
```
