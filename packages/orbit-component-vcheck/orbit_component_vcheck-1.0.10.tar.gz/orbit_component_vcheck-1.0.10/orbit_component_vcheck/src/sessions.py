from orbit_component_base.src.orbit_shared import world
from orbit_component_vcheck.schema.Sessions import SessionsCollection
from orbit_component_vcheck.src.cli_base import CliBase
from rich.console import Console
from rich.table import Table


class Sessions (CliBase):

    COLLECTIONS = [SessionsCollection]

    def list (self):
        table = Table(
            title='Current Sessions',
            title_style='bold green',
            caption=f'authentication="{world.conf.authentication}"',
            caption_style='bold magenta'
        )
        rstyle = 'cyan'
        hstyle = 'deep_sky_blue4'
        table.add_column('Session Id', style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Namespace',  style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Host Id',    style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Start Time', style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Vendor',     style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Platform',   style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Language',   style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Client',     style=rstyle, header_style=hstyle, no_wrap=True)
        for result in SessionsCollection():
            doc = result.doc
            table.add_row(
                doc._sid,
                doc._ns,
                doc._host_id,
                doc.when,
                doc._vendor,
                doc._platform,
                doc._language,
                doc._product)
        Console().print(table)
        print()
