from orbit_component_base.src.orbit_plugin import PluginBase, ArgsBase
from orbit_component_base.schema.OrbitVersions import VersionsCollection
from orbit_component_vcheck.schema.Sessions import SessionsCollection
from orbit_component_vcheck.schema.Users import UsersCollection
from orbit_component_vcheck.src.users import Users
from orbit_component_vcheck.src.versions import Versions
from orbit_component_vcheck.src.sessions import Sessions


class Plugin (PluginBase):

    NAMESPACE = 'vcheck'
    COLLECTIONS = [
        VersionsCollection,
        UsersCollection,
        SessionsCollection
    ]


class Args (ArgsBase):
        
    def setup (self):
        self._parser.add_argument("--vc-users", action='store_true', help="List version check users")
        self._parser.add_argument("--vc-versions", action='store_true', help="List version check versions")
        self._parser.add_argument("--vc-sessions", action='store_true', help="List version check sessions")
        self._parser.add_argument("--vc-add", type=str, help='Set the version for a given product string', metavar="<product>")
        self._parser.add_argument("--vc-del", type=str, help='Delete the specified product record', metavar="<product>")
        self._parser.add_argument("--vc-ver", type=str, help='The version for set-version', metavar="<version>")
        self._parser.add_argument("--vc-perm", type=str, metavar="<perm>", help='Set permission [user|admin] for a given host id')
        self._parser.add_argument("--vc-host", type=str, metavar="<host>", help='The host id for a "perm" operation')
        return self
    
    def process (self):
        if self._args.vc_users:
            return Users(self._odb).setup().list()
        if self._args.vc_versions:
            return Versions(self._odb).setup().list()
        if self._args.vc_sessions:
            return Sessions(self._odb).setup().list()
        if self._args.vc_add:
            if not self._args.vc_ver:
                self._parser.error('You need to specify a version (vc-ver) argument to add a new product')
                exit()
            return Versions(self._odb).setup().add(self._args.vc_add, self._args.vc_ver)
        if self._args.vc_del:
            return Versions(self._odb).setup().delete(self._args.vc_del)
        if self._args.vc_perm:
            if not self._args.vc_host:
                self._parser.error('You need to specify a host (vc-host) argument to authorize a user')
                exit()
            return Users(self._odb).setup().auth(self._args.vc_perm, self._args.vc_host)
