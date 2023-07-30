import asyncio

import httpx
from flask import Flask, request, jsonify, render_template, abort


async def fetch_ip_info(ip_address):
    url = f"https://ipinfo.io/{ip_address}"
    headers = {"Authorization": "Bearer your_api"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            res = response.json()
            return res
    except httpx.HTTPError as exc:
        return {'error': str(exc)}


app = Flask(__name__)
ALLOW_ROUTE = ['/', '/all']


@app.before_request
def before_request():
    if request.path not in ALLOW_ROUTE:
        abort(404)


@app.route('/', methods=['GET', 'POST'])
def ip_info():
    if request.method == 'POST':
        ip_address = request.remote_addr
        ip_json = asyncio.run(fetch_ip_info(ip_address))
        return jsonify({'ip_info': ip_json})
    return render_template('ip_info.html')


if __name__ == '__main__':
    app.run()
