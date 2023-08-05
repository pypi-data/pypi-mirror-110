from json import dump, load
from pathlib import Path

from requests import HTTPError

from .convert_json import convert
from .route import Site
from .unix import create_requests


def get_url(net_address, default_host):
    if net_address.startswith('unix/'):
        return net_address.replace('unix/', 'unix://')
    elif net_address.startswith('udp/'):
        raise TypeError('Upd sockets are not supported.')
    else:
        net_address = net_address.removeprefix('tcp/')
        if net_address.startswith(':'):
            net_address = default_host + net_address
        return f'http://{net_address}'


class Caddy:
    def __init__(
            self,
            *,
            caddyfile: Path = None,
            socket_path: Path = None,
            update_caddyfile=False,
            caddy_host='localhost',
    ):
        if not socket_path:
            with caddyfile.open() as file_obj:
                config = load(file_obj)

            try:
                listen = config['admin']['listen']
            except KeyError:
                raise TypeError(
                    'Caddyfile must have an admin unix socket configured',
                )

            if listen.startswith('unix/'):
                socket_path = listen.removeprefix('unix/')
                self.base = 'unix://caddy'
            else:
                self.base = get_url(listen, caddy_host)

        elif isinstance(socket_path, Path):
            socket_path = str(socket_path)

        self.requests = create_requests(socket_path)
        self.update_caddyfile = update_caddyfile
        self.caddyfile = caddyfile

    def url(self, path):
        return self.base + path

    def get(self, path, *args, **kwargs):
        return self.requests.get(self.url(path), *args, **kwargs)

    def add_site(self, site: Site):
        site_id = f'site_{site.name}'
        json = convert(site)
        json['@id'] = site_id

        try:
            resp = self.requests.patch(self.url(f'/id/{site_id}'), json=json)
            resp.raise_for_status()
        except HTTPError:
            url = self.url('/id/server/routes')
            resp = self.requests.post(url, json=json)
            resp.raise_for_status()

        if self.update_caddyfile:
            updated_resp = self.get('/config')
            updated_resp.raise_for_status()

            updated_config = updated_resp.json()

            with self.caddyfile.open('w') as file:
                dump(
                    updated_config,
                    file,
                    sort_keys=True,
                    indent=4,
                    ensure_ascii=False,
                )
