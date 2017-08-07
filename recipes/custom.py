# -*- Mode: Python -*- vi:si:et:sw=4:sts=4:ts=4:syntax=python
import os
import shutil
from collections import defaultdict

from cerbero.build import recipe
from cerbero.build.source import SourceType
from cerbero.build.cookbook import CookBook
from cerbero.config import Platform
from cerbero.enums import License
from cerbero.utils import shell, to_unixpath

class GStreamer(recipe.Recipe):
    licenses = [License.LGPLv2Plus]
    version = '1.13.0.1'
    commit = 'origin/master'

def list_gstreamer_1_0_plugins_by_category(config):
        cookbook = CookBook(config)
        # For plugins named differently
        replacements = {'decodebin': 'playback', 'playbin': 'playback',
                        'uridecodebin': 'playback', 'sdpelem': 'sdp',
                        'encodebin': 'encoding', 'souphttpsrc': 'soup',
                        'siren': 'gstsiren', 'scaletempoplugin' : 'scaletempo',
                        'rmdemux': 'realmedia', 'camerabin2': 'camerabin'}
        plugins = defaultdict(list)
        for r in ['gstreamer-1.0', 'gst-plugins-base-1.0', 'gst-plugins-good-1.0',
                  'gst-plugins-bad-1.0', 'gst-plugins-ugly-1.0',
                  'gst-libav-1.0', 'gst-editing-services-1.0', 'gst-rtsp-server-1.0']:
            r = cookbook.get_recipe(r)
            for attr_name in dir(r):
                if attr_name.startswith('files_plugins_'):
                    cat_name = attr_name[len('files_plugins_'):]
                    plugins_list = getattr(r, attr_name)
                elif attr_name.startswith('platform_files_plugins_'):
                    cat_name = attr_name[len('platform_files_plugins_'):]
                    plugins_dict = getattr(r, attr_name)
                    plugins_list = plugins_dict.get(config.target_platform, [])
                else:
                    continue
                for e in plugins_list:
                    if not e.startswith('lib/gstreamer-'):
                        continue
                    c = e.split('/')
                    if len(c) != 3:
                        continue
                    e = c[2]
                    if e.startswith('libgst'):
                        e = e[6:-8]
                    else:
                        e = e[3:-8]
                    plugins[cat_name].append(e)
        return plugins, replacements

def generate_gir_h_from_gir(gir_file, gir_h_file):
    """
    Generate a .gir.h file from the specified .gir file, and write to the
    specified gir.h file location

    @gir_file: The .gir file
    @gir_h_file: The location to write the generated .gir.h file to
    """
    outfname = gir_h_file
    # FIXME: xxd is provided by vim-common, and not installed by
    # bootstrap/build-tools
    hexdump = shell.check_call('xxd -i ' + gir_file, shell=True, split=False)
    outf = open(outfname, 'w')
    outf.write(hexdump)
    # Append checksum to .gir.h file
    shasum = shell.check_call('shasum -a 1 -b < ' + gir_file, shell=True,
                              split=False)[:40]
    sha1fname = gir_file + '.sha1'
    sha1f = open(sha1fname, 'w')
    sha1f.write(shasum)
    sha1f.close()
    hexdump = shell.check_call('xxd -i ' + sha1fname, shell=True,
                               split=False)
    outf.write(hexdump)
    outf.close()
    os.unlink(sha1fname)
