import json
import requests
import urllib.parse

import quart
import quart_cors
from quart import request

# Note: Setting CORS to allow chat.openapi.com is only required when running a localhost plugin
app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")
HOST_URL = "http://localhost:3000"
headers = {
            "content-type": "application/x-www-form-urlencoded",
            "X-RapidAPI-Key": ".........................", # put your RapidAPI-Key Here
            "X-RapidAPI-Host": "textanalysis-text-summarization.p.rapidapi.com"
        }


@app.get("/url")
async def get_url():
    query = request.args.get("query")
    res = requests.get(
        f"{HOST_URL}/url?search={query}")
    body = res.json()
    return quart.Response(response=json.dumps(body), headers=headers, status=200)


@app.get("/text")
async def get_text():
    query = request.args.get("query")
    res = requests.get(
        f"{HOST_URL}/text?search={query}")
    body = res.json()
    return quart.Response(response=json.dumps(body), status=200)


@app.get("/logo.png")
async def plugin_logo():
    filename = 'summary.png'
    return await quart.send_file(filename, mimetype='image/png')


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open(".well-known/ai-plugin.json") as f:
        text = f.read()
        # This is a trick we do to populate the PLUGIN_HOSTNAME constant in the manifest
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        return quart.Response(text, mimetype="text/json")


@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        # This is a trick we do to populate the PLUGIN_HOSTNAME constant in the OpenAPI spec
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        return quart.Response(text, mimetype="text/yaml")


def main():
    app.run(debug=True, host="0.0.0.0", port=5001)


if __name__ == "__main__":
    main()
