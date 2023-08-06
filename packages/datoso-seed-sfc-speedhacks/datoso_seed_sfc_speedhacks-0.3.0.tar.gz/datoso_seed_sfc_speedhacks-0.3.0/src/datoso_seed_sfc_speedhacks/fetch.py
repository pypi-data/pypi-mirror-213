from datoso_plugin_internetarchive.fetch import fetch_helper
from datoso_plugin_internetarchive.ia import Archive
from datoso.configuration.folder_helper import Folders
from datoso_seed_sfc_speedhacks import __preffix__

def fetch():
    folder_helper = Folders(seed=__preffix__)
    folder_helper.clean_dats()
    folder_helper.create_all()
    archive = Archive(dat_folder='DAT', item='sfc-speedhacks')
    fetch_helper(archive, folder_helper, __preffix__)
