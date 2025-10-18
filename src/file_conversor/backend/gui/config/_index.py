# src/file_conversor/backend/gui/config/index.py

from flask import render_template, url_for

# user-provided modules
from file_conversor.backend import FFmpegBackend, Img2PDFBackend, PillowBackend, GhostscriptBackend

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation, AVAILABLE_LANGUAGES

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def config_index():
    return render_template(
        'config/index.jinja2',
        breadcrumb_items=[
            {
                'label': _("Home"),
                'url': url_for('index'),
            },
            {
                'label': _("Configuration"),
                'url': url_for('config_index'),
            },
        ],
        config_index={
            'category': {
                'current': 'general',
                'available': [
                    ('general', _('General')),
                    ('network', _('Network')),
                    ('audio_video', _('Audio & Video')),
                    ('image', _('Image')),
                    ('pdf', _('PDF')),
                ],
            },
            'language': {
                'current': CONFIG['language'],
                'available': AVAILABLE_LANGUAGES,
                'label': _('Application Language'),
                'placeholder': _('Select application language'),
                'help': _('Select the language for the application interface.'),
            },
            'host': {
                'current': CONFIG['host'],
                'label': _('GUI Host IP Address'),
                'placeholder': _('IP address'),
                'help': _('Type 127.0.0.1 for localhost, 0.0.0.0 for all interfaces.'),
            },
            'port': {
                'current': CONFIG['port'],
                'label': _('Port'),
                'placeholder': _('Port number (1-65535)'),
                'help': _('Ports 1-1024 require priviledge elevation.'),
            },
            'install_deps': {
                'current': CONFIG['install-deps'],
                'label': _('Automatic install of missing dependencies, on demand.'),
            },
            'audio': {
                'bitrate': {
                    'current': CONFIG['audio-bitrate'],
                    'label': _('Audio Bitrate (kbps)'),
                    'placeholder': _('Bitrate in kbps'),
                    'help': _('Audio bitrate for the output files (0 to keep original bitrate).'),
                },
            },
            'video': {
                'bitrate': {
                    'current': CONFIG['video-bitrate'],
                    'label': _('Video Bitrate (kbps)'),
                    'placeholder': _('Bitrate in kbps'),
                    'help': _('Video bitrate for the output files (0 to keep original bitrate).'),
                },
                'format': {
                    'current': CONFIG['video-format'],
                    'available': filter(lambda x: x != 'null', FFmpegBackend.SUPPORTED_OUT_VIDEO_FORMATS),
                    'label': _('Video Format'),
                    'placeholder': _('Video format (e.g., mp4, mkv, avi)'),
                    'help': _('Default format for converted video files.'),
                },
                'encoding_speed': {
                    'current': CONFIG['video-encoding-speed'],
                    'available': FFmpegBackend.ENCODING_SPEEDS,
                    'label': _('Video Encoding Speed'),
                    'help': _('Set the default video encoding speed. Faster speeds result in lower quality and larger file sizes.'),
                },
                'quality': {
                    'current': CONFIG['video-quality'],
                    'available': FFmpegBackend.QUALITY_PRESETS,
                    'label': _('Video Quality'),
                    'help': _('Set the default video quality. Higher quality results in larger file sizes.'),
                },
            },
            'image': {
                'quality': {
                    'current': CONFIG['image-quality'],
                    'label': _('Image Quality'),
                    'placeholder': _('Quality (1-100)'),
                    'help': _('Set the default image quality. Higher quality results in larger file sizes.'),
                },
                'dpi': {
                    'current': CONFIG['image-dpi'],
                    'label': _('Image to PDF DPI'),
                    'placeholder': _('DPI (40-3600)'),
                    'help': _('Dots per inch (DPI) for images converted to PDF. Higher DPI results in better quality but larger file size.'),
                },
                'fit': {
                    'current': CONFIG['image-fit'],
                    'available': ['into', 'fill'],
                    'label': _('Image to PDF Fit Mode'),
                    'help': _('Fit mode for images converted to PDF. "into" fits the image within the page, "fill" fills the entire page.'),
                },
                'page_size': {
                    'current': str(CONFIG['image-page-size']),
                    'available': list(Img2PDFBackend.PAGE_LAYOUT) + ['None'],
                    'label': _('Image to PDF Page Size'),
                    'help': _('Page size for images converted to PDF. Choose from standard sizes or "None" for original size.'),
                },
                'resampling': {
                    'current': CONFIG['image-resampling'],
                    'available': PillowBackend.RESAMPLING_OPTIONS,
                    'label': _('Image Resampling Algorithm'),
                    'help': _('Resampling algorithm used when resizing images.'),
                },
            },
            'pdf': {
                'compression': {
                    'current': CONFIG['pdf-compression'],
                    'available': GhostscriptBackend.Compression.get_dict(),
                    'label': _('PDF Compression Level'),
                    'help': _('Set the default PDF compression level. Higher compression results in lower quality.'),
                },
            },
            'config_saved': {
                'title': _('Configuration Save'),
                'success': _('The configuration has been saved successfully. Some changes may require a server restart to take effect.'),
                'error': _('An error occurred while saving the configuration:'),
            },
            'save_changes': _('Save Changes'),
        },
    )
