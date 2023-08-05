from orbit_component_base.src.orbit_shared import world
from orbit_component_vcheck.schema.Users import UsersCollection, UsersTable
from orbit_component_vcheck.src.cli_base import CliBase
from rich.console import Console
from rich.table import Table


class Users (CliBase):

    COLLECTIONS = [UsersCollection]

    def list (self):
        table = Table(
            title='Registered Users',
            title_style='bold green',
            caption=f'authentication="{world.conf.authentication}"',
            caption_style='bold magenta'
        )
        rstyle = 'cyan'
        hstyle = 'deep_sky_blue4'
        table.add_column('Host Id',     style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('User Id',     style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Active',      style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Code',        style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Tries',       style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Version',     style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Permission',  style=rstyle, header_style=hstyle, no_wrap=True)
        for result in UsersCollection():
            doc = UsersTable(result.doc.doc, oid=result.doc.key)
            table.add_row(
                doc.key,
                doc._user_id,
                str(doc._active),
                doc.code,
                str(doc._tries),
                doc._version,
                doc._perm)
        Console().print(table)
        print()

    def auth (self, perm, host):
        doc = UsersTable().from_key(host)
        if not doc.isValid:
            print(f'No such hostid: {host}')
        else:
            if perm in ('user', 'admin'):
                doc.update({'perm': perm}).save()
                print('Updated!')
            else:
                print(f'Invalid permission: {perm}, try "admin" or "user"')
