from orbit_component_base.src.orbit_orm import BaseTable, BaseCollection, register_class, register_method
from orbit_database import SerialiserType
from loguru import logger as log
from gitlab import Gitlab

gitlab = Gitlab()


class APIsTable (BaseTable):

    norm_table_name = 'apis'
    norm_auditing = True
    norm_codec = SerialiserType.UJSON
    norm_ensure = [
        # {'index_name': 'by_path', 'func': '{provider}|{project}|{path}'},
        # {'index_name': 'by_parent', 'duplicates': True, 'func': 
        # """def func(doc): return (doc["path"][::-1].replace("/","|",1)[::-1] if "/" in doc["path"] else "|"+doc["path"]).encode()"""
        # },
        {'index_name': 'by_sorted', 'force': True, 'duplicates': True, 'func': '{isLeaf}|{path}'}
    ]

    @property
    def parent (self):
        prefix = "/" if "/" not in self["path"] else "/".join((self["path"]).split("/")[:-1])
        return (prefix + "|" + self["label"]).encode()
        # return ("/".join(self["path"].split("/")[:-1]) or "/")


@register_class
class APIsCollection (BaseCollection):

    table_class = APIsTable
    table_methods = []    

    async def put_api_tree (self, data, to_delete):
        log.success(f'Create> {data}')
        log.warning(f'Delete> {to_delete}')
        for item in data:
            key = item.get('_id')
            del item['_id']
            doc = APIsTable().from_key(key)
            if '|' in item.get('key'):
                item['key'] = item.get('key').split('|')[1]
            if doc.isValid:
                log.debug(f'Update: {key}')
                APIsTable(item, oid=key).save()
            else:
                log.debug(f'Append: {key}')
                APIsTable(item, oid=key).append()

        APIsTable().norm_tb.delete(to_delete)
        return {'ok': True}

    def get_api_remote (self, provider, api, branch, path):
        files = []
        folders = []
        if provider == 'gitlab':
            project = [p for p in gitlab.projects.list(search=api, ref=branch) if p.path == api]
            if not project:
                return {'ok': False, 'error': f'unable to find project: {api}'}
            for file in project[0].repository_tree(path=path, recursive=False, ref=branch):
                item = {
                    'key': f"{branch}|{file['id']}",
                    'label': file['name'],
                    'path': file['path'],
                    'type': file['type'],
                    'isLeaf': file['type'] == 'blob',
                    'provider': provider,
                    'project': api,
                    'branch': branch,
                }
                if file['type'] == 'blob':
                    files.append(item)
                else:
                    folders.append(item)
        else:
            return {'ok': False, 'error': f'unknown provider: {provider}'}
        return {'ok': True, 'data': [item for item in files + folders]}
