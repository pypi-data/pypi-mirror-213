import base64, logging, os, sys
from io import BytesIO, StringIO
import boto3
from hashlib import sha1
from typing import NamedTuple, List, Tuple, cast, TextIO, Dict, Any

import requests
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from tqdm import tqdm
from zstd import compress, decompress  # type: ignore

from modelbit.cli.local_config import AppDirs, getCacheDir
from modelbit.utils import inNotebook

logger = logging.getLogger(__name__)

defaultRequestTimeout = 10


class S3UploadInfo:

  def __init__(self, data: Dict[str, Any]):
    self.bucket: str = data["bucket"]
    self.s3Key: str = data["s3Key"]
    self.awsCreds: Dict[str, str] = data["awsCreds"]
    self.metadata: Dict[str, str] = data["metadata"]
    self.fileKey64: str = data["fileKey64"]
    self.fileIv64: str = data["fileIv64"]
    self.objectExists: bool = data["objectExists"]


class EncryptedObjectInfo(NamedTuple):
  contentHash: str
  signedDataUrl: str
  key64: str
  iv64: str
  objectExists: bool


def calcHash(content: bytes) -> str:
  return f"sha1:{sha1(content).hexdigest()}"


def objectCacheFilePath(workspaceId: str, contentHash: str) -> str:
  contentHash = contentHash.replace(":", "_")
  return os.path.join(getCacheDir(workspaceId, "largeFiles"), f"{contentHash}.zstd.enc")


def putSecureData(uploadInfo: S3UploadInfo, obj: bytes, desc: str) -> None:
  if uploadInfo.objectExists:
    return
  cipher = AES.new(  # type: ignore
      mode=AES.MODE_CBC,
      key=base64.b64decode(uploadInfo.fileKey64),
      iv=base64.b64decode(uploadInfo.fileIv64))
  body = cipher.encrypt(pad(compress(obj, 10), AES.block_size))

  s3Client = boto3.client('s3', **uploadInfo.awsCreds)  # type: ignore
  outputStream: TextIO = sys.stdout
  if not inNotebook():  # printing to stdout breaks git's add file flow
    outputStream = sys.stderr
  if os.getenv('MB_TXT_MODE'):
    outputStream = StringIO()
  with BytesIO(body) as b, tqdm(total=len(body),
                                unit='B',
                                unit_scale=True,
                                miniters=1,
                                desc=f"Uploading '{desc}'",
                                file=outputStream) as t:
    s3Client.upload_fileobj(  # type: ignore
        b,
        uploadInfo.bucket,
        uploadInfo.s3Key,
        ExtraArgs={"Metadata": uploadInfo.metadata},
        Callback=lambda bytes_transferred: t.update(bytes_transferred))  # type: ignore


def getSecureData(workspaceId: str, dri: EncryptedObjectInfo, desc: str) -> bytes:
  if not dri:
    raise Exception("Download info missing from API response.")
  filepath = objectCacheFilePath(workspaceId, dri.contentHash)

  if os.path.exists(filepath):  # Try cache
    try:
      return readAndDecryptFile(filepath, dri)
    except Exception as e:
      logger.info("Failed to read from cache", exc_info=e)

  downloadFile(dri, filepath, desc)
  return readAndDecryptFile(filepath, dri)


def downloadFile(dri: EncryptedObjectInfo, filepath: str, desc: str) -> None:
  logger.info(f"Downloading to {filepath}")
  resp = requests.get(dri.signedDataUrl, stream=True, timeout=defaultRequestTimeout)
  total = int(resp.headers.get('content-length', 0))
  with open(filepath, "wb") as f, tqdm(total=total,
                                       unit='B',
                                       unit_scale=True,
                                       miniters=1,
                                       desc=f"Downloading '{desc}'",
                                       file=sys.stderr) as t:
    for data in resp.iter_content(chunk_size=32 * 1024):
      size = f.write(data)
      t.update(size)


def readAndDecryptFile(filepath: str, dri: EncryptedObjectInfo) -> bytes:
  with open(filepath, "rb") as f:
    data = f.read()
  return decryptAndValidate(dri, data)


def decryptAndValidate(dri: EncryptedObjectInfo, data: bytes) -> bytes:
  cipher = AES.new(base64.b64decode(dri.key64), AES.MODE_CBC, iv=base64.b64decode(dri.iv64))  # type: ignore
  data = unpad(cipher.decrypt(data), AES.block_size)
  data = decompress(data)
  actualHash = calcHash(data)
  if actualHash != dri.contentHash:
    raise ValueError(f"Hash mismatch. Tried to fetch {dri.contentHash}, calculated {actualHash}")
  return data


def _userCacheDir() -> str:
  return cast(str, AppDirs.user_cache_dir)  # type: ignore


def clearCache() -> None:
  import shutil
  shutil.rmtree(_userCacheDir())


_cacheNameMap = {'largeFiles': 'Encrypted Data', 'largeFileStubs': 'Description'}


def getCacheList() -> List[Tuple[str, str, str, int]]:
  import glob
  import stat
  if not os.path.exists(_userCacheDir()):
    return []
  filedata: List[Tuple[str, str, str, int]] = []
  for filepath in glob.iglob(os.path.join(_userCacheDir(), "**"), recursive=True):
    statinfo = os.stat(filepath)
    if not stat.S_ISDIR(statinfo.st_mode):
      relpath = os.path.relpath(filepath, _userCacheDir())
      [workspace, kind, name] = relpath.split("/")
      filedata.append((workspace, _cacheNameMap.get(kind, 'Unknown'), name, statinfo[stat.ST_SIZE]))
  return filedata
