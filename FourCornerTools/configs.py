from pathlib import Path

PROJ_ROOT = Path(__file__).resolve().parent.parent

PATHS = {
    'ref': PROJ_ROOT / 'json',
    'raw': PROJ_ROOT / 'rawtxt',
    'out': PROJ_ROOT / 'marked'
}