import pathlib
import os

data_suffix = ['.indd', 'ppt', 'iso', '.gif', '.cr2', 'pptx', 'docx', 'avi', '.pdf', '.pptx', 'mp4', '.avi', 'json',
               '.tiff', '.heif', '.xlsx', 'pdf', 'exe', '.mp4', 'doc', '.bmp', '.ppt', '.jpeg', '.mp3', '.dmg', 'dmg',
               '.jpg', '.xls', '.png', '.doc', '.tif', '.eps', '.csv', '.orf', 'lance', 'text', '.nef', '.rar', '.docx',
               'arrow', '.psd', '.mov', '.zip', 'parquet', 'zip', '.webp', 'xls', 'rar', '.iso', '.wav', '.ai', '.exe',
               '.sr2', '.svg', '.raw', 'mp3', 'txt', 'mov', 'xlsx', 'wav']
code_suffix = ['pyc', '.py', '.c', '.cpp', '.java', '.html', '.js', '.css', '.php', '.rb', '.pl', '.swift', '.go',
               '.sql', '.xml', '.vb']
GITLLM_DB = os.getenv("GITLLM_DB", str(pathlib.Path.home().joinpath('.gitllm.db')))
