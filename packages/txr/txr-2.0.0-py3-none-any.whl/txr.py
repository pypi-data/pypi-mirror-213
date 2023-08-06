__package_name__ = "txr"
__version__ = '2.0.0'
__author__ = "Idan Miara"
__author_email__ = "idan@miara.com"
__license__ = "GPL3"
__url__ = r"https://github.com/idanmiara/txr"
__description__ = "Stylish merge/split files (tar-like with txt output)"

import csv
import hashlib
import json
import logging
import os
import sys
import zlib
from argparse import ArgumentParser
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from datetime import datetime
from pathlib import Path
from typing import Union, List, TypedDict, Optional, Tuple, Sequence

try:
    crypo_support = True
    import secrets
    from cryptography.fernet import Fernet
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    if crypo_support:
        backend = default_backend()
except ImportError:
    crypo_support = False
crypto_key_iterations = 100_000

txr_version = __version__
txr_format = 2


# https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password

def generate_key() -> bytes:
    return Fernet.generate_key()


def encrypt(message: bytes, key: bytes, encode: bool = False) -> bytes:
    token = Fernet(key).encrypt(message)
    if not encode:
        token = b64d(token)
    return token


def decrypt(token: bytes, key: bytes, encoded: bool = False) -> bytes:
    if not encoded:
        token = b64e(token)
    return Fernet(key).decrypt(token)


def _derive_key(password: bytes, salt: bytes, iterations: int = crypto_key_iterations) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=backend)
    return b64e(kdf.derive(password))


def password_encrypt(message: bytes, password: str, iterations: int = crypto_key_iterations) -> bytes:
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, iterations)
    # return a concatenation of the salt, the iteration count and the encrypted message using the derived key
    # salt: 16 bytes
    # iterations: 4 bytes
    # message: all trailing bytes
    return b'%b%b%b' % (
        salt,
        iterations.to_bytes(4, 'big'),
        b64d(Fernet(key).encrypt(message)),
    )


def password_decrypt(value: bytes, password: str) -> bytes:
    # split the input into its 3 parts:
    salt, iter, token = value[:16], value[16:20], b64e(value[20:])
    iterations = int.from_bytes(iter, 'big')
    key = _derive_key(password.encode(), salt, iterations)
    return Fernet(key).decrypt(token)


class FileMeta(TypedDict):
    idx: int
    offset: int
    compression: str
    crypto: str
    encoding: str
    input_bytes: int
    compressed_bytes: int
    encrypted_bytes: int
    digested_bytes: int
    hash: str
    timestamp: str
    filename: str


class MetaHeader(TypedDict):
    txr_version: str
    txr_format: int
    sentinel: str
    datetime_format: str
    hash: str
    files: int
    total_bytes: int


logger = logging.root
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)

StrOrPathLike = Union[Path, str]


def error_log(msg: str):
    logger.error(msg)


def error_exception(msg: str):
    raise Exception(msg)


def txr_archive(
        root: Optional[StrOrPathLike] = None,
        pattern: Optional[Union[str, Sequence[str]]] = None,
        names: Optional[List[StrOrPathLike]] = None,
        txr_filename: Optional[StrOrPathLike] = None,
        txd_filename: Optional[StrOrPathLike] = None,
        test_txr: bool = False,
        test_txd: bool = False,
        hash: Optional[str] = 'sha256',
        encoding: str = '',
        password: str = '',
        compression: str = '',
        sentinel: str = '!@#$!@#$!@#$',
        txr_encoding='utf-8',
        keep_timestamp: bool = True,
        datetime_format: str = "%Y/%m/%d %H:%M:%S",
        force: bool = False,
        error_call=error_log,
        **kwargs
) -> Tuple[Path, Path]:
    filenames = []
    if root is None:
        root = names[0]
    root = Path(root)
    names = [Path(name) for name in names] if names else [root]

    if root.is_file():
        root = root.parent
    elif pattern is None:
        pattern = '**/*'
    if pattern:
        if isinstance(pattern, str):
            pattern = [pattern]
        for name in names:
            if name.is_file():
                filenames.append(name)
            elif name.is_dir():
                for pat in pattern:
                    filenames += list([f for f in Path(name).glob(pat) if f.is_file()])
    else:
        filenames += [f for f in names if f.is_file()]
    if not filenames:
        raise Exception(f'No files found for {root}/{pattern}')

    if txr_filename is None:
        txr_filename = str(root) + '.txr'
    txr_filename = Path(txr_filename)
    if txd_filename is None:
        txd_filename = txr_filename.with_suffix('.txd')
    txd_filename = Path(txd_filename)
    if txr_filename.is_file() or txd_filename.is_file():
        if not force:
            exist = [f for f in [txr_filename, txd_filename] if f.is_file()]
            raise Exception(f'{exist} exist. aborting. use `--force` to force overwrite.')

    total_input_bytes = 0
    total_compressed_bytes = 0
    total_encrypted_bytes = 0
    total_digested_bytes = 0
    total_output_bytes = 0

    meta = []
    b_sentinel = bytes(sentinel, 'ascii')

    f_txd = None
    if not test_txd:
        f_txd = open(txd_filename, mode='bw', **kwargs)
        logger.info(f'writing {txd_filename}')

    crypto = 'p' if password else ''
    if crypto and not crypo_support:
        raise Exception('file is encrypted, but cryptography was not installed.')
    hash_digest = ''
    logger.debug(f'Processing: {len(meta)} files, '
                 f'hash: {hash}, '
                 f'compression: {compression}, '
                 f'crypto: {crypto}, '
                 f'encoding: {encoding}')
    timestamp = ''
    for idx, filename in enumerate(filenames):
        filename = Path(filename)
        filename = filename.relative_to(root)
        file_path = root / filename
        if keep_timestamp:
            timestamp = file_path.stat().st_mtime  # float
            timestamp = datetime.fromtimestamp(timestamp)  # datetime
            timestamp = timestamp.strftime(datetime_format)  # string
        with open(file_path, mode='br', **kwargs) as f:
            file_data = f.read()
        if hash:
            hash_digest = hashlib.new(hash, file_data).hexdigest()

        input_bytes = len(file_data)
        total_input_bytes += input_bytes

        if compression:
            file_data = zlib.compress(file_data)
        compressed_bytes = len(file_data)

        if crypto:
            file_data = password_encrypt(file_data, password=password)
        encrypted_bytes = len(file_data)

        if encoding:
            file_data = b64e(file_data)
        digested_bytes = len(file_data)

        m = FileMeta(
            idx=idx,
            offset=total_output_bytes,
            input_bytes=input_bytes,
            compressed_bytes=compressed_bytes,
            encrypted_bytes=encrypted_bytes,
            digested_bytes=digested_bytes,
            filename=str(filename),
            timestamp=timestamp,
            crypto=crypto,
            hash=hash_digest,
            compression=compression,
            encoding=encoding,
        )
        logger.debug(m)
        meta.append(m)

        if not test_txd:
            f_txd.write(file_data)

        total_compressed_bytes += compressed_bytes
        total_encrypted_bytes += encrypted_bytes
        total_digested_bytes += digested_bytes
        total_output_bytes += digested_bytes

        if idx < len(filenames) - 1:
            if not test_txd:
                f_txd.write(b_sentinel)
            total_output_bytes += len(b_sentinel)

    if not test_txd:
        f_txd.close()

    meta_header = MetaHeader(
        txr_version=txr_version,
        txr_format=txr_format,
        sentinel=sentinel,
        datetime_format=datetime_format,
        hash=hash,
        files=len(filenames),
        total_bytes=total_output_bytes,
    )
    logger.info(meta_header)

    if not test_txr:
        logger.info(f'writing {txr_filename}')
        meta_fileds = list(FileMeta.__annotations__)
        # if not compression:
        #     meta_fileds.remove('compressed_bytes')
        # if not crypto:
        #     meta_fileds.remove('encrypted_bytes')
        with open(txr_filename, mode='w', newline='', encoding=txr_encoding) as f_txr:
            meta_header = json.dumps(meta_header)
            f_txr.write(f'{meta_header}\n')
            w = csv.DictWriter(f_txr, meta_fileds)
            w.writeheader()
            w.writerows(meta)

    logger.info(f'Processed: {len(meta)} files')
    logger.info(f'total input size {total_input_bytes}')
    if compression:
        logger.info(f'total compressed: {total_compressed_bytes}')
    if crypto:
        logger.info(f'total crypto: {total_encrypted_bytes}')
    logger.info(f'total digest size: {total_digested_bytes}')
    logger.info(f'total output size: {total_output_bytes}')
    logger.info(f'ratio: {total_output_bytes / total_input_bytes * 100:.2f}%')

    return txr_filename, txd_filename


def txr_extract(
        txr_filename: StrOrPathLike,
        txd_filename: Optional[StrOrPathLike] = None,
        root: Optional[StrOrPathLike] = None,
        enforce_hash: Optional[bool] = None,
        hash_file: bool = True,
        enforce_size_check: bool = True,
        password: Optional[str] = None,
        keep_timestamp: bool = True,
        txr_encoding='utf-8',
        test: bool = True,
        list_files: bool = False,
        force: bool = False,
        error_call=error_log,
        **kwargs
):
    txr_filename = Path(txr_filename)
    root = txr_filename.with_name(txr_filename.stem) if root is None else Path(root)
    txd_filename = txr_filename.with_suffix('.txd') if txd_filename is None else Path(txd_filename)

    ok_count = 0
    with open(txr_filename, mode='r', encoding=txr_encoding, newline='') as f_txr:
        meta_header = f_txr.readline().strip()
        meta_header = json.loads(meta_header)
        hash_alg = meta_header.get('hash')
        datetime_format = meta_header.get('datetime_format')
        if hash_alg:
            compare_hash = enforce_hash or enforce_hash is None
        else:
            compare_hash = False
        r = csv.DictReader(f_txr)
        meta = list(r)
        if list_files:
            for m in meta:
                filename = m['filename']
                logger.info(filename)

    root.mkdir(exist_ok=True, parents=True)
    hash_file = open(root / (txr_filename.stem + '.' + hash_alg), mode='w',
                     encoding=txr_encoding) if hash_file else None
    logger.info(f'reading {txr_filename}')
    with open(txd_filename, mode='br') as f_txd:
        for m in meta:
            offset = int(m['offset'])
            encoding = m.get('encoding')
            compression = m.get('compression')

            digested_bytes = int(m['digested_bytes'])
            encrypted_bytes = int(m['encrypted_bytes'])
            compressed_bytes = int(m['compressed_bytes'])
            input_bytes = int(m['input_bytes'])

            filename = m['filename']
            crypto = m['crypto']
            full_filename = root / filename
            if full_filename.is_file():
                if not force:
                    logger.warning(f'{full_filename} exist, skipping. use `--force` to force overwrite.')
                    continue

            full_filename.parent.mkdir(exist_ok=True, parents=True)
            f_txd.seek(offset)

            file_data = f_txd.read(digested_bytes)
            if encoding:
                file_data = b64d(file_data)
                if len(file_data) != encrypted_bytes:
                    error_call(f'Unexpected undigested size {len(file_data)}, expected {encrypted_bytes}.')
                    if enforce_size_check:
                        continue

            if crypto:
                if not crypo_support:
                    error_call('file is encrypted, but cryptography was not installed, skipped.')
                    continue
                if not password:
                    error_call('file is encrypted, but no password was provided, skipped')
                    continue
                file_data = password_decrypt(file_data, password=password)
                if len(file_data) != compressed_bytes:
                    error_call(f'Unexpected decrypted size {len(file_data)}, expected {compressed_bytes}.')
                    if enforce_size_check:
                        continue

            if compression:
                file_data = zlib.decompress(file_data)
                if len(file_data) != input_bytes:
                    error_call(f'Unexpected uncompressed size {len(file_data)}, expected {input_bytes}.')
                    if enforce_size_check:
                        continue

            if len(file_data) != input_bytes:
                error_call(f'Unexpected output file size {len(file_data)}, expected {input_bytes}.')
                if enforce_size_check:
                    continue

            logger.debug(m)
            hash_org = m.get('hash')
            if compare_hash:
                hash_new = hashlib.new(hash_alg, file_data).hexdigest()
                if hash_new != hash_org:
                    error_call(f'hash mismatch: {filename}: {hash_new} != {hash_org}')
                    if enforce_hash:
                        continue
            if hash_file:
                hash_file.write(f'{hash_org} *{filename}\n')

            if not test:
                with open(full_filename, mode='bw') as f:
                    f.write(file_data)
                if keep_timestamp:
                    timestamp = m.pop('timestamp')  # string
                    if timestamp:
                        timestamp = datetime.strptime(timestamp, datetime_format)  # datetime
                        timestamp = datetime.timestamp(timestamp)  # float
                        os.utime(full_filename, (timestamp, timestamp))
            ok_count += 1

    if hash_file:
        hash_file.close()
    logger.info(f'Extracted {ok_count}/{len(meta)} files')
    return meta


def main(argv=None):
    if argv is None:
        argv = sys.argv
    version_info = f'txr version: {txr_version}, txr format version: {txr_format}'
    parser = ArgumentParser(fromfile_prefix_chars='@', prog=f'txr: text-like-extractor\n{version_info}')

    parser.add_argument('-x', '--extract', dest="extract", action="store_true", help='extract archive')
    parser.add_argument('-F', '--force', dest="force", action="store_true", help="force overwrite of output file")
    parser.add_argument('-l', '--list', dest="list_files", action="store_true", help="list compressed file contents")
    parser.add_argument('-s', '--timestamp', dest="keep_timestamp", action="store_false",
                        help="do not store or restore the original timestamp")
    parser.add_argument('-i', '--hash', dest="enforce_hash", action="store_false",
                        help="do not creates or verifies hashes for integrity")
    parser.add_argument('-I', '--hash_file', dest="hash_file", action="store_true", help="create a hash file output")
    parser.add_argument('-V', '--version', dest="version", action="store_true", help="display version number")

    parser.add_argument('-q', '--quiet', dest="quiet", action="store_true", help="suppress all warnings")
    parser.add_argument('-v', '--verbose', dest="verbose", action="store_true", help="verbose mode")
    parser.add_argument('-t', '--test', dest="test", action="store_true", help="test compressed file integrity")

    # parser.add_argument('-C', '--key', dest="key", type=str,
    #                     help="encrypt/decrypt using a key. "
    #                          "the input parameter can either be a path to a file containing the key, "
    #                          "which must be a 32 url-safe base64-encoded bytes; "
    #                          "Or '?' (encryption only) to generate a random key, which is written to a sidecar file")
    parser.add_argument('-c', '--password', dest="password", type=str, help="encrypt/decrypt with a given password")

    parser.add_argument('-p', '--pattern', dest="pattern", type=str, default=None,
                        help="pattern for finding files, "
                             "default: if input is dir - include all files, recursively (**/*).")
    parser.add_argument('-f', '--file', dest='txr_filename', metavar="txr_filename", type=str,
                        help="input or output txr file")
    parser.add_argument('-d', '--dir', dest='root', metavar="dirname", type=str, help="input or output directory.")
    parser.add_argument('names', metavar="names", type=str, nargs='*',
                        help="archive mode: input filename(s) and/or dirname(s), extract: txr filename(s).")

    if len(argv) == 1:
        parser.print_help()
        return 1

    if len(argv) == 2 and argv[1] == '-V':
        print(version_info)
        return 1

    args = parser.parse_args(argv[1:])

    kwargs = vars(args)

    extract = kwargs.pop('extract')
    txr_filename = kwargs.pop('txr_filename')
    names = kwargs.pop('names')
    test = kwargs.pop('test')
    quiet = kwargs.pop('quiet')
    verbose = kwargs.pop('verbose')
    
    if quiet:
        logger.setLevel(logging.ERROR)
    elif verbose:
        logger.setLevel(logging.DEBUG)
    if extract:
        txr_filenames = [txr_filename] if txr_filename else []
        txr_filenames += names
        for txr_filename in txr_filenames:
            txr_extract(txr_filename=txr_filename, test=test, **kwargs)
    else:
        txr_archive(txr_filename=txr_filename, names=names,
                    test_txr=test, test_txd=test, **kwargs)
    return 0


if __name__ == '__main__':
    sys.exit(main())
