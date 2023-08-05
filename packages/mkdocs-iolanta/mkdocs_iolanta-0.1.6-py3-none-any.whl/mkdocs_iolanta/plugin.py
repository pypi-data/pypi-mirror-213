import functools
from pathlib import Path
from typing import Optional

from iolanta.iolanta import Iolanta
from iolanta.namespaces import IOLANTA
from iolanta_jinja2.macros import template_render
from mkdocs.config import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation


class IolantaPlugin(BasePlugin):   # type: ignore
    """Integrate MkDocs + iolanta."""

    iolanta: Iolanta

    def on_files(
        self,
        files: Files,
        *,
        config: MkDocsConfig,
    ) -> Optional[Files]:
        """Construct the local iolanta instance and load files."""
        self.iolanta.add(source=Path(config.docs_dir))
        return files

    def on_config(self, config: MkDocsConfig) -> Optional[Config]:
        """Expose configuration & template variables."""
        self.iolanta = Iolanta()

        config.extra['iolanta'] = self.iolanta
        config.extra['render'] = functools.partial(
            template_render,
            iolanta=self.iolanta,
            environments=[IOLANTA.html],
        )
        return config

    def on_nav(
        self, nav: Navigation, *, config: MkDocsConfig, files: Files,
    ) -> Optional[Navigation]:
        """Assign schema:url to pages."""
        self.iolanta.add({
            '$included': [
                {
                    '$id': f'file://{page.file.abs_src_path}',
                    'mkdocs:url': f'/{page.url}',
                }
                for page in nav.pages
            ],
        })
        return nav
