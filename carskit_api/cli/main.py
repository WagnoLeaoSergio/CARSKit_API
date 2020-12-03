import sys
import os
import pathlib as pl
from cliff.app import App
from cliff.commandmanager import CommandManager
from ..editors import Settings_Editor


class CAPI_App(App):
    def __init__(self):
        super(CAPI_App, self).__init__(
            description="An API for the CARSKit engine",
            version="0.0.1",
            command_manager=CommandManager("capi"),
            deferred_help=True,
        )

    def initialize_app(self, argv):
        self.LOG.debug("initialize_app")
        app_path = pl.Path(os.path.dirname(os.path.abspath(__file__))).parent

        settings_editor = Settings_Editor(
            os.path.join(app_path, "carskit", "setting.conf")
        )

        settings_editor.save_settings()


def main(argv=sys.argv[1:]):
    app = CAPI_App()
    return app.run(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
