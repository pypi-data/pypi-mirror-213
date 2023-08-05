from orbit_component_base.src.orbit_plugin import PluginBase
from orbit_component_base.src.orbit_decorators import navGuard, apiSentry
from orbit_component_zerodocs.schema.Cache import CacheCollection
from orbit_component_zerodocs.schema.APIs import APIsCollection
from orbit_component_zerodocs.schema.Project import ProjectCollection
from loguru import logger as log


class Plugin (PluginBase):

    NAMESPACE = 'zerodocs'
    COLLECTIONS = [
        CacheCollection,
        APIsCollection,
        ProjectCollection
    ]

    @navGuard
    async def on_cache_fetch (self, sid, params, force=False):
        return await CacheCollection(sid).fetch(params, force)

    @navGuard
    async def on_get_project_id (self, sid, params):
        return await CacheCollection(sid).get_project_id(params)

    @navGuard
    async def on_get_api_remote (self, sid, provider, api, branch, path):
        return APIsCollection(sid).get_api_remote(provider, api, branch, path)

    @apiSentry(['admin'])
    async def on_cache_put (self, sid, old_data, new_data):
        return await CacheCollection(sid).put(old_data, new_data)

    @apiSentry(['admin'])
    async def on_project_put (self, sid, params):
        return await ProjectCollection(sid).put(params)

    @apiSentry(['admin'])
    async def on_project_remove (self, sid, params):
        try:
            await ProjectCollection(sid).remove(params)
            await CacheCollection(sid).remove(params)
            return {'ok': True}
        except Exception as e:
            log.exception(e)
            return {'ok': False, 'error': str(e)}
