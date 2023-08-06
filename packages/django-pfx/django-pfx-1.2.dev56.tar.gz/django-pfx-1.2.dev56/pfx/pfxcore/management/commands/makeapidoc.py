import inspect
import json
import re
from pathlib import Path

from django.core.management.base import BaseCommand

from apispec import APISpec
from apispec.utils import deepupdate
from apispec.yaml_utils import load_operations_from_docstring

from pfx.pfxcore import __PFX_VIEWS__
from pfx.pfxcore.apidoc import __PARAMETERS__, ParameterGroup
from pfx.pfxcore.settings import PFXSettings
from pfx.pfxcore.views import FilterGroup, ModelMixin

settings = PFXSettings()
DEFAULT_TEMPLATE = dict(
    title="PFX API",
    version="1.0.0",
    openapi_version="3.0.2")
RE_PATH_PARAMS = re.compile(r'<(?:(\w+):)?(\w+)>')
DJANGO_OPENAPI_TYPES = {
    'str': 'string',
    'int': 'integer',
    'slug': 'string',
    'uuid': 'string',
    'path': 'string',
}


def from_django_path(path):
    return RE_PATH_PARAMS.sub(r'{\g<2>}', path)


def path_parameters(spec, path):
    def as_dict(data):
        return data if isinstance(data, dict) else dict(description=data)

    existings = {
        p.get('name', '#N/A') for p in spec.get('parameters', [])
        if isinstance(p, dict)}
    extras = spec.pop('parameters extras', {}).copy()
    for ptype, name in RE_PATH_PARAMS.findall(path):
        if name in existings:
            # Ignore path parameters that are manually described.
            continue
        yield deepupdate({
            'in': 'path',
            'name': name,
            'schema': {'type': DJANGO_OPENAPI_TYPES.get(ptype, 'string')},
            'required': True}, as_dict(extras.get(name, {})))


def global_parameters(spec, method):
    def extend_groups(params):
        for p in params:
            if issubclass(p, ParameterGroup):
                yield from p.parameters
            else:
                yield p

    existings = {
        p.get('name', '#N/A') for p in spec.get('parameters', [])
        if isinstance(p, dict)}
    for qp in extend_groups(method.rest_api_params):
        if qp.name in existings:
            # Ignore path parameters that are manually described.
            continue
        yield qp.id()


def filters_parameters(view):
    def get_filters(src):
        if not hasattr(src, 'filters'):
            return
        for e in src.filters:
            if isinstance(e, FilterGroup):
                yield from get_filters(e)
            else:
                yield e

    for f in get_filters(view):
        yield {
            'in': 'query',
            'name': str(f.name),
            'description': f"Filter by {f.label.lower()}"}


def get_operations(view, url):
    order = dict(get=1, post=2, put=3, delete=4)
    for op, method_name in sorted(
            url['methods'].items(), key=lambda e: order.get(e[0], 99)):
        method = getattr(view, method_name)
        doc = inspect.getdoc(method)
        vars = {}
        if issubclass(view, ModelMixin) and view.model:
            vars.update(
                model=view.model._meta.verbose_name.lower(),
                models=view.model._meta.verbose_name_plural.lower())
        if doc:
            doc = doc.format(**vars)
        spec = deepupdate(
            load_operations_from_docstring(doc).get(op, {}),
            view.rest_doc.get((url['path'], op), {}).copy())
        spec.setdefault('summary', from_django_path(url['fixed_path']))
        parameters = spec.setdefault('parameters', [])
        parameters.extend(global_parameters(spec, method))
        parameters.extend(path_parameters(spec, url['path']))
        if method.rest_api_filters:
            parameters.extend(filters_parameters(view))
        for p in parameters:
            if 'name' in p and p['name'] == 'id':
                p['name'] = 'pk'
        yield op, spec


def get_spec():
    re_pk = re.compile(r'<(\w+:)?id>')
    spec = APISpec(**{**DEFAULT_TEMPLATE, **settings.PFX_OPENAPI_TEMPLATE})
    for parameter in __PARAMETERS__:
        spec.components.parameter(
            parameter.id(), parameter.location, parameter.as_parameter())
    for view in __PFX_VIEWS__:
        for url in view.get_urls():
            url['fixed_path'] = re_pk.sub(r'<\g<1>pk>', url['path'])
            spec.path(
                path=from_django_path(url['fixed_path']),
                operations=dict(get_operations(view, url)))
    return spec


class Command(BaseCommand):
    help = 'Generate OpenAPI documentation'

    def handle(self, *args, **options):
        spec = get_spec()

        path = Path(settings.PFX_OPENAPI_PATH)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as outfile:
            json.dump(spec.to_dict(), outfile, indent=2)

        self.stdout.write(self.style.SUCCESS(
            f"OpenAPI documentation generated: {path}"))
