#!/usr/bin/python3
# PYTHON_ARGCOMPLETE_OK
'''Stateless OpenPGP Scaffolding

Author: Daniel Kahn Gillmor
Date: April 2022
License: MIT (see below)

This module implements a pythonic framework for `sop`, the Stateless
OpenPGP command-line interface.  It makes it easier to build out a
python-based backend.

  https://datatracker.ietf.org/doc/draft-dkg-openpgp-stateless-cli/

In particular, sop.StatelessOpenPGP presents a generic baseclass for
building an implementation of `sop`.

To use it sensibly, subclass sop.StatelessOpenPGP and override the
following methods:

 - generate_key()
 - extract_cert()
 - sign()
 - verify()
 - encrypt()
 - decrypt()
 - armor()
 - dearmor()
 - inline_detach()
 - inline_sign()
 - inline_verify()

See the docstrings for each of these functions for more detail on
their expected behavior.

To augment the interface by adding new subcommands, or to add
arguments to existing subcommands, override extend_parsers().

To add an additional indirect forms of input like @FOO:bar, create a
method indirect_input_FOO(self, name:str)->bytes.  For example, if a default
keyring is available, indexable by primary key fingerprint:

    def indirect_input_KEYRING(self, name:str) -> bytes:
         return self._keyring.get_certificate_by_fingerprint(name)

The program invocable from the command line should instantiate the
subclass, and then call dispatch() on it.

A simple example follows:

----------
#!/usr/bin/python3
# PYTHON_ARGCOMPLETE_OK
import sop
import foo

class FooSop(sop.StatelessOpenPGP):
    def __init__(self):
        super().__init__(prog='FooPGP', version='0.17')
    # overrides go here...
    def extract_cert(self, key:bytes, armor:bool=True, **kwargs:Namespace) -> bytes:
        self.raise_on_unknown_options(**kwargs)
        return foo.bytes_to_openpgp_key(key).get_certificate(armor=armor)

if __name__ = "__main__":
    foo = FooSop()
    foo.dispatch()
----------

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation files
(the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import os
import io
import sys
import enum
import string
import logging

from binascii import unhexlify, hexlify
from datetime import datetime, timezone
from argparse import ArgumentParser, _SubParsersAction, Namespace, SUPPRESS
from typing import List, Optional, Dict, Sequence, MutableMapping, Tuple, BinaryIO, TYPE_CHECKING

from .__version__ import __version__

try:
    import argcomplete #type: ignore
except ImportError:
    argcomplete = None


class SOPSigType(enum.Enum):
    binary = enum.auto()
    text = enum.auto()

class SOPInlineSigType(enum.Enum):
    binary = enum.auto()
    text = enum.auto()
    clearsigned = enum.auto()
    
class SOPLiteralDataType(enum.Enum):
    binary = enum.auto()
    text = enum.auto()

class SOPArmorLabel(enum.Enum):
    auto = enum.auto()
    sig = enum.auto()
    cert = enum.auto()
    key = enum.auto()
    message = enum.auto()

class SOPException(Exception):
    exit_code:int = 2
    mnemonic:Optional[str] = None
class SOPNoSignature(SOPException):
    exit_code = 3
    mnemonic = 'NO_SIGNATURE'
class SOPAsymmetricAlgorithmUnsupported(SOPException):
    exit_code = 13
    mnemonic = 'UNSUPPORTED_ASYMMETRIC_ALGO'
class SOPCertificateNotEncryptionCapable(SOPException):
    exit_code = 17
    mnemonic = 'CERT_CANNOT_ENCRYPT'
class SOPMissingRequiredArgument(SOPException):
    exit_code = 19
    mnemonic = 'MISSING_ARG'
class SOPIncompleteVerificationInstructions(SOPException):
    exit_code = 23
    mnemonic = 'INCOMPLETE_VERIFICATION'
class SOPCouldNotDecrypt(SOPException):
    exit_code = 29
    mnemonic = 'CANNOT_DECRYPT'
class SOPPasswordNotHumanReadable(SOPException):
    exit_code = 31
    mnemonic = 'PASSWORD_NOT_HUMAN_READABLE'
class SOPUnsupportedOption(SOPException):
    exit_code = 37
    mnemonic = 'UNSUPPORTED_OPTION'
class SOPInvalidDataType(SOPException):
    exit_code = 41
    mnemonic = 'BAD_DATA'
class SOPNotUTF8Text(SOPException):
    exit_code = 53
    mnemonic = 'EXPECTED_TEXT'
class SOPOutputExists(SOPException):
    exit_code = 59
    mnemonic = 'OUTPUT_EXISTS'
class SOPMissingInput(SOPException):
    exit_code = 61
    mnemonic = 'MISSING_INPUT'
class SOPKeyIsProtected(SOPException):
    exit_code = 67
    mnemonic = 'KEY_IS_PROTECTED'
class SOPUnsupportedSubcommand(SOPException):
    exit_code = 69
    mnemonic = 'UNSUPPORTED_SUBCOMMAND'
class SOPUnsupportedSpecialPrefix(SOPException):
    exit_code = 71
    mnemonic = 'UNSUPPORTED_SPECIAL_PREFIX'
class SOPAmbiguousInput(SOPException):
    exit_code = 73
    mnemonic = 'AMBIGUOUS_INPUT'
class SOPKeyCannotSign(SOPException):
    exit_code = 79
    mnemonic = 'KEY_CANNOT_SIGN'
class SOPIncompatibleOptions(SOPException):
    exit_code = 83
    mnemonic = 'INCOMPATIBLE_OPTIONS'
class SOPUnsupportedProfile(SOPException):
    exit_code = 89
    mnemonic = 'UNSUPPORTED_PROFILE'


class SOPSessionKey(object):
    '''Stateless OpenPGP session key

    Simple class to represent an OpenPGP session key.

    Destroy this object as soon as possible, as leaking it will allow
    decryption of whatever is encrypted with it.

    `algo`: integer value referring to the number of the symmetric key algorithm

    `key`: bytes of the actual session key

    '''
    def __init__(self, algo:int, key:bytes):
        self.algo:int = algo
        self.key:bytes = key

    def __str__(self) -> str:
        key:str = hexlify(self.key).decode('ascii')
        return f'{self.algo}:{key}'


class SOPProfile(object):
    '''A Profile for SOP

    Simple baseclass to represent a profile, for example for key
    generation or encryption.

    Initialize it with a name (a UTF-8 string with no whitespace) and
    a description (a UTF-8 string with no newlines).
    '''
    def __init__(self, name:str, description:str):
        if len(list(filter(str.isspace, name))):
            raise ValueError(f'Bad profile name "{name}": must not contain whitespace')
        if description.count('\n'):
            raise ValueError(f'Bad profile description "{description}": must not contain any newline')
        self.name = name
        self.description = description
    def __str__(self) -> str:
        return f'{self.name}: {self.description}'
    
class SOPSigResult(object):
    '''Stateless OpenPGP Signature Result

    This class describes a valid OpenPGP signature.
    '''
    def __init__(self, when:datetime, signing_fpr:str, primary_fpr:str, sig_type:Optional[SOPSigType] = None, moreinfo:str = ''):
        self._when:datetime = when
        self._signing_fpr:str = signing_fpr
        self._primary_fpr:str = primary_fpr
        self._sig_type:Optional[SOPSigType] = sig_type
        self._moreinfo:str = moreinfo

    def __str__(self) -> str:
        # ensure tz=UTC:
        whendt:datetime = datetime.fromtimestamp(self._when.timestamp(), tz=timezone.utc)
        when:str = whendt.strftime('%Y-%m-%dT%H:%M:%SZ')
        # strip all whitespace from fprs:
        signing_fpr:str = self._signing_fpr.translate(str.maketrans('', '', string.whitespace))
        primary_fpr:str = self._primary_fpr.translate(str.maketrans('', '', string.whitespace))
        sig_type:str = ''
        if self._sig_type is not None:
            sig_type = f'mode:{self._sig_type.name} '
        # strip all newlines from moreinfo
        moreinfo:str = self._moreinfo.translate(str.maketrans('\n\r', '  '))
        return f'{when} {signing_fpr} {primary_fpr} {sig_type}{moreinfo}'
    
class StatelessOpenPGP(object):
    '''Stateless OpenPGP baseclass

    Subclass this object, overriding the methods with code that
    implements their declared behavior.  The methods to override are:
    generate_key, extract_cert, sign, verify, encrypt, decrypt, armor,
    and dearmor.

    Then, instantiate your subclass and call dispatch() on it.

    '''
    def __init__(self, version:str, name:Optional[str]=None,
                 description:Optional[str]='A Stateless OpenPGP implementation',
                 backend:Optional[str]=None,
                 extended:Optional[str]=None,
                 sop_spec:Optional[str]=None):
        '''Set up Stateless OpenPGP command line interface parser

        `version` should be a version string like "0.17.3"

        `name` should be a human-readable name for the project with no
        whitespace in it.

        `description` should be human-readable text that describes the
        implementation.

        `backend` should be a single line string of the most significant
        backend, for example "CryptoLib 1.14".

        `extended` is any amount of version-related text that
        describes the tool.  This module will add its own information
        to the output of `sop version --extended` in addition to any
        text supplied here.

        `sop_spec` is the string of the version of sop.  Only provide
        this if the version is fully implemented.

        '''
        self._version = version
        self._backend = backend
        self._extended = extended
        self._sop_spec = sop_spec

        self._parser = ArgumentParser(prog=name, description=description)
        self._parser.add_argument('--debug', action='store_true',
                                  help='show debugging data')
        _cmds:_SubParsersAction[ArgumentParser] = self._parser.add_subparsers(required=True,
                                            metavar='SUBCOMMAND',
                                            dest='subcmd')
        _subs = {}
        _version = _cmds.add_parser('version', help='emit version')
        version_type = _version.add_mutually_exclusive_group(required=False)
        version_type.add_argument('--backend', action='store_true')
        version_type.add_argument('--extended', action='store_true')
        version_type.add_argument('--sop-spec', action='store_true')
        _subs['version'] = _version

        def _add_armor_flag(parser:ArgumentParser) -> None:
            parser.add_argument('--no-armor', dest='armor', action='store_false',
                                help='generate binary output')
            parser.set_defaults(armor=True)
        
        _generate_key = _cmds.add_parser('generate-key',
                                         help='generate a secret key to stdout')
        _add_armor_flag(_generate_key)
        _generate_key.add_argument('--with-key-password',
                                    dest='keypassword',
                                    metavar='PASSWORD',
                                    help='filename containing a password to encrypt the secret key')
        _generate_key.add_argument('--profile',
                                   metavar='PROFILE',
                                   choices=[x.name for x in self.generate_key_profiles],
                                   help=f'Available key generation profiles: [{" ".join(x.name for x in self.generate_key_profiles)}]')
        _generate_key.add_argument('uids', metavar='USERID', nargs='*',
                                   help='a User ID (a UTF-8 string)')
        _subs['generate-key'] = _generate_key

        _extract_cert_h = 'convert a secret key from stdin to a certificate on stdout'
        _extract_cert = _cmds.add_parser('extract-cert',
                                          help=_extract_cert_h)
        _add_armor_flag(_extract_cert)
        _subs['extract-cert'] = _extract_cert
        
        _sign = _cmds.add_parser('sign',
                                 help='create a detached signature')
        _add_armor_flag(_sign)
        _sign.add_argument('--as', dest='sigtype',
                           choices=SOPSigType.__members__,
                           default='binary',
                           help='sign as binary document or canonical text document')
        _sign.add_argument('--micalg-out', dest='micalgout', metavar='MICALG',
                           help='filename to output digest algorithm to on successful signature')
        _sign.add_argument('--with-key-password', dest='keypasswords', metavar='PASSWORD',
                           action='append',
                           help='filename containing a password for unlocking the signing KEYS')

        _sign.add_argument('signers', metavar='KEYS', nargs='+',
                           help='filename containing one or more secret keys')
        _subs['sign'] = _sign

        _verify = _cmds.add_parser('verify', help='verify detached signatures')
        _verify.add_argument('--not-before', dest='start', metavar='DATE',
                             default='-',
                             help='ignore signatures before (ISO-8601 timestamp)')
        _verify.add_argument('--not-after', dest='end', metavar='DATE',
                             default='now',
                             help='ignore signatures after (ISO-8601 timestamp)')
        _verify.add_argument('sig', metavar='SIGNATURE',
                             help='filename containing signature(s)')
        _verify.add_argument('signers', metavar='CERTS', nargs='+',
                             help='filename containing certificate of acceptable signer')
        _subs['verify'] = _verify
        
        _encrypt = _cmds.add_parser('encrypt', help='encrypt message')
        _add_armor_flag(_encrypt)
        _encrypt.add_argument('--as', dest='literaltype',
                              choices=SOPLiteralDataType.__members__,
                              default='binary',
                              help='encrypt cleartext as binary or UTF-8')
        _encrypt.add_argument('--with-password', dest='passwords', metavar='PASSWORD',
                              action='append',
                              help='filename containing a password for symmetric encryption')
        _encrypt.add_argument('--sign-with', dest='signers', metavar='KEYS', action='append',
                              help='filename containing one or more secret keys to sign with')
        _encrypt.add_argument('--with-key-password', dest='keypasswords', metavar='PASSWORD',
                              action='append',
                              help='filename containing a password for unlocking the signing KEYS')
        _encrypt.add_argument('--profile',
                              metavar='PROFILE',
                              choices=[x.name for x in self.encrypt_profiles],
                              help=f'Available encryption profiles: [{" ".join(x.name for x in self.encrypt_profiles)}]')
        _encrypt.add_argument('recipients', metavar='CERTS', nargs='*',
                              help='filename containing certificate')
        _subs['encrypt'] = _encrypt


        _decrypt = _cmds.add_parser('decrypt', help='decrypt message')
        _decrypt.add_argument('--session-key-out', dest='sessionkeyout', metavar='SESSIONKEY',
                              help='filename to output session key to on successful decryption')
        _decrypt.add_argument('--with-session-key', dest='sessionkeys', metavar='SESSIONKEY',
                              action='append',
                              help='filename containing session key to use for decryption')
        _decrypt.add_argument('--with-password', dest='passwords',
                              metavar='PASSWORD', action='append',
                              help='filename containing a password for symmetric encryption')
        _decrypt.add_argument('--verifications-out', dest='verifications', metavar='VERIFICATIONS',
                             help='filename to output verification status')
        # deprecated old variant of --verifications-out:
        _decrypt.add_argument('--verify-out', dest='verifyout', metavar='VERIFICATIONS',
                              help=SUPPRESS)
        _decrypt.add_argument('--verify-with', dest='signers', metavar='CERTS',
                              action='append',
                             help='filename containing certificate of acceptable signer')
        _decrypt.add_argument('--verify-not-before', dest='start', metavar='DATE',
                              default='-',
                              help='ignore signatures before (ISO-8601 timestamp)')
        _decrypt.add_argument('--verify-not-after', dest='end', metavar='DATE',
                              default='now',
                              help='ignore signatures after (ISO-8601 timestamp)')
        _decrypt.add_argument('--with-key-password', dest='keypasswords', metavar='PASSWORD',
                              action='append',
                              help='filename containing a password for unlocking the decrypting KEYS')
        _decrypt.add_argument('secretkeys', metavar='KEYS', nargs='*',
                              help='filename containing secret keys')
        _subs['decrypt'] = _decrypt

        _armor = _cmds.add_parser('armor', help='add ASCII armor')
        _armor.add_argument('--label', choices=SOPArmorLabel.__members__,
                            default='auto',
                            help='specify the type of ASCII armoring')

        _subs['armor'] = _armor

        _dearmor = _cmds.add_parser('dearmor', help='remove ASCII armor')
        _subs['dearmor'] = _dearmor

        _inline_detach = _cmds.add_parser('inline-detach', help='detach inline signatures from a clearsigned message')
        _add_armor_flag(_inline_detach)
        _inline_detach.add_argument('--signatures-out', dest='sigsout',
                                    metavar='SIGNATURES', 
                                    help='Where to write signature data',
                                    required=True)
        _subs['inline-detach'] = _inline_detach

        _inline_sign = _cmds.add_parser('inline-sign',
                                        help='create an inline-signed message')
        _add_armor_flag(_inline_sign)
        _inline_sign.add_argument('--as', dest='sigtype',
                                  choices=SOPInlineSigType.__members__,
                                  default='binary',
                                  help='create inline-signed message as binary, canonical text, or clearsigned document')
        _inline_sign.add_argument('--with-key-password', dest='keypasswords', metavar='PASSWORD',
                                  action='append',
                                  help='filename containing a password for unlocking the signing KEYS')

        _inline_sign.add_argument('signers', metavar='KEYS', nargs='+',
                                  help='filename containing one or more secret keys')
        _subs['inline-sign'] = _inline_sign

        _inline_verify = _cmds.add_parser('inline-verify', help='verify an inline-signed message')
        _inline_verify.add_argument('--not-before', dest='start', metavar='DATE',
                                    default='-',
                                    help='ignore signatures before (ISO-8601 timestamp)')
        _inline_verify.add_argument('--not-after', dest='end', metavar='DATE',
                                    default='now',
                                    help='ignore signatures after (ISO-8601 timestamp)')
        _inline_verify.add_argument('--verifications-out', dest='verifications', metavar='VERIFICATIONS',
                                    help='filename to output verification status')
        _inline_verify.add_argument('signers', metavar='CERTS', nargs='+',
                                    help='filename containing certificate of acceptable signer')
        _subs['inline-verify'] = _inline_verify

        
        self.extend_parsers(_cmds, _subs)

        _list_profiles = _cmds.add_parser('list-profiles', help='Describe available profiles for subcommand')
        _list_profiles.add_argument('subcommand', metavar='SUBCOMMAND',
                                    choices= list(_subs.keys()) + ['list-profiles'],
                                    help='The subcommand to list profiles for')
        _subs['list-profiles'] = _list_profiles

        if argcomplete:
            argcomplete.autocomplete(self._parser)
        elif '_ARGCOMPLETE' in os.environ:
            logging.error('Argument completion requested but the "argcomplete" module is not installed.'
                          'It can be obtained at https://pypi.python.org/pypi/argcomplete')
            sys.exit(1)

    def _get_indirect_input(self, name:str) -> bytes:
        if name.startswith('@'):
            method, target = name[1:].split(':', maxsplit=1)
            finder = getattr(self, f'indirect_input_{method}')
            return bytes(finder(target))
        else:
            with open(name, 'rb') as f:
                return f.read()

    def indirect_input_FD(self, name:str) -> bytes:
        '''Retrieve indirect data from an open file descriptor

        When providing indirect data to `sop`, rather than providing a
        filename, the user can indicate an already open file
        descriptor nnn (where nnn is a decimal integer) as `@FD:nnn`.

        '''
        with open(int(name), 'rb') as filed:
            return filed.read()
        
    def indirect_input_ENV(self, name:str) -> bytes:
        '''Retrieve indirect data from the environment

        When providing indirect data to `sop`, rather than providing a
        filename, the user can indicate an environment variable foo as
        `@ENV:foo`.
        '''
        return os.environ[name].encode()


    def _get_session_key_from_handle(self, handle:str) -> SOPSessionKey:
        try:
            data:bytes = self._get_indirect_input(handle).strip()
            algob:bytes
            keyb:bytes
            algob, keyb = data.split(b':', maxsplit=2)
            return SOPSessionKey(int(algob),unhexlify(keyb))
        except Exception as e:
            raise SOPInvalidDataType(f'Malformed session key {handle} ({e})')
    
    def _write_indirect_output(self, name:str, data:bytes) -> None:
        indirectout:BinaryIO
        if name.startswith('@FD:'):
            indirectout = open(int(name.split(':',maxsplit=1)[1]), 'wb')
        else:
            indirectout = open(name, 'wb')
        if data:
            indirectout.write(data)
        indirectout.close()

    if TYPE_CHECKING:
        subparsertype = _SubParsersAction[ArgumentParser]
    else:
        subparsertype = _SubParsersAction
    def extend_parsers(self, subcommands:subparsertype,
                       subparsers:Dict[str,ArgumentParser]) -> None:
        '''override this function to add options or subcommands

        To add a new option to an existing subcommand, look up the
        subcommand in `subparsers` and call `add_argument` on it.

        The new option will show up in the **kwargs of the
        corresponding function.

        To add a new subcommand entirely, invoke `add_parser` on
        `subcommands`, and populate it appropriately.  Then implement
        method `_handle_xxx` (where `xxx` is the name of the new
        subcommand).

        '''
        pass

    def raise_on_unknown_options(self, **kwargs:Namespace) -> None:
        '''if any options are left in the `args` namespace, raise an exception'''
        # an empty or default value for --profile can be ignored:
        if 'profile' in kwargs and (kwargs['profile'] is None or kwargs['profile'] == 'default'):
            del kwargs['profile']
        if kwargs:
            missingargs:str = ','.join([f'--{arg}' for arg in kwargs.keys()])
            s:str = ''
            if len(kwargs) > 1:
                s = 's'
            raise SOPUnsupportedOption(f'Unsupported argument{s} {missingargs}')


    def parse_timestamp(self, when:Optional[str]) -> Optional[datetime]:
        '''Parse a user-supplied string that represents a timestamp

        Handle strict ISO-8601 date formats.  Override this function
        if you want to accept fancier formats.
        '''
        if when is None or when == '-':
            return None
        if when == 'now':
            return datetime.now(timezone.utc)
        return datetime.strptime(when, '%Y-%m-%dT%H:%M:%S%z')


    def dispatch(self, argstrs:Optional[Sequence[str]]=None) -> None:

        '''handle the arguments passed by the user, and invoke the correct subcommand'''
        args:Namespace = self._parser.parse_args(argstrs)
        subcmd = args.subcmd
        method = getattr(self, f'_handle_{args.subcmd.replace("-","_",-1)}')
        debug = args.debug
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        subargs = vars(args)
        del subargs['subcmd']
        del subargs['debug']
        try:
            out = method(sys.stdin.buffer, **subargs)
            sys.stdout.buffer.write(out)
        except SOPException as e:
            logging.error(f'[{e.mnemonic}] {e}')
            exit(e.exit_code)


    def _handle_version(self, inp:io.BufferedReader,
                        backend:bool = False,
                        extended:bool = False,
                        sop_spec:bool = False) -> bytes:
        if sop_spec:
            if self._sop_spec is not None:
                return f'{self._sop_spec}\n'.encode('utf-8')
            else:
                return '~draft-dkg-openpgp-stateless-cli-06\n'.encode('utf-8')
        if backend:
            if self._backend:
                return f'{self._backend}\n'.encode('utf-8')
            else:
                raise SOPUnsupportedOption('--backend')
        verstring = f'{self._parser.prog} {self._version}\n'
        if extended:
            verstring += f'python-sop {__version__}\n'
            if self._extended:
                verstring += f'{self._extended}\n'
            if self._backend:
                verstring += f'{self._backend}\n'
        return verstring.encode('utf-8')


    @property
    def generate_key_profiles(self) -> List[SOPProfile]:
        '''Override this to offer multiple key generation profiles'''
        return [SOPProfile('default', 'The default key generation profile')]

    @property
    def encrypt_profiles(self) -> List[SOPProfile]:
        '''Override this to offer multiple encryption profiles'''
        return [SOPProfile('default', 'The default encryption profile')]


    def _handle_list_profiles(self,
                              inp:io.BufferedReader,
                              subcommand:str,
                              **kwargs:Namespace) -> bytes:
        if subcommand == 'generate-key':
            return ('\n'.join(map(lambda x: str(x), self.generate_key_profiles)) + '\n').encode()
        if subcommand == 'encrypt':
            return ('\n'.join(map(lambda x: str(x), self.encrypt_profiles)) + '\n').encode()
        else:
            raise SOPUnsupportedProfile(f'no profiles for subcommand "{subcommand}"')


    def _handle_generate_key(self,
                             inp:io.BufferedReader,
                             armor:bool=True,
                             keypassword:Optional[str]=None,
                             uids:List[str]=[],
                             profile:Optional[str]=None,
                             **kwargs:Namespace) -> bytes:
        prof:Optional[SOPProfile] = None
        if profile is not None:
            if profile == 'default':
                prof = self.generate_key_profiles[0]
            else:
                for p in self.generate_key_profiles:
                    if p.name == profile:
                        prof = p
                        break
            if prof is None:
                raise SOPUnsupportedProfile(f'profile "{profile}" not supported for generate_key subcommand')
        return self.generate_key(armor=armor, uids=uids,
                                 keypassword=self._get_indirect_input(keypassword) if keypassword else None,
                                 profile=prof,
                                 **kwargs)
    def generate_key(self, armor:bool=True, uids:List[str]=[],
                     keypassword:Optional[bytes]=None,
                     profile:Optional[SOPProfile]=None,
                     **kwargs:Namespace) -> bytes:
        '''Produce an OpenPGP transferable secret key

`armor`: whether to produce an ASCII-armored form or a binary-encoded form.

`key_password`: if present, ensure that all secret key material is locked with this password.
        '''
        raise SOPUnsupportedSubcommand('generate-key')

    def _handle_extract_cert(self,
                             inp:io.BufferedReader,
                             armor:bool=True,
                             **kwargs:Namespace) -> bytes:
        return self.extract_cert(key=inp.read(), armor=armor, **kwargs)
    def extract_cert(self, key:bytes, armor:bool=True, **kwargs:Namespace) -> bytes:
        '''Convert an OpenPGP transferable secret key to an OpenPGP certificate

        `key`: the OpenPGP secret key (may be in armored or unarmored
        form).

        `armor`: whether to produce an ASCII-armored form or a
        binary-encoded form.

        '''
        raise SOPUnsupportedSubcommand('extract-cert')

    def _handle_sign(self,
                     inp:io.BufferedReader,
                     armor:bool=True,
                     sigtype:str='binary',
                     signers:List[str]=[],
                     micalgout:Optional[str]=None,
                     keypasswords:List[str]=[]
                     ) -> bytes:
        ret:bytes
        micalg:Optional[str] = None
        ret,micalg = self.sign(inp.read(),
                               armor,
                               SOPSigType.__members__[sigtype],
                               dict((signer, self._get_indirect_input(signer)) for signer in signers),
                               wantmicalg=micalgout is not None,
                               keypasswords=dict((pwfile, self._get_indirect_input(pwfile))
                                                 for pwfile in keypasswords) if keypasswords else dict())
        if micalgout and micalg:
            self._write_indirect_output(micalgout, micalg.encode() if micalg else b'')

        return ret
    def sign(self,
             data:bytes,
             armor:bool=True,
             sigtype:SOPSigType=SOPSigType.binary,
             signers:MutableMapping[str,bytes]={},
             wantmicalg:bool=False,
             keypasswords:MutableMapping[str,bytes]={}
             ) -> Tuple[bytes, Optional[str]]:
        '''Create a detached OpenPGP signature

        `data`: the data to sign.

        `armor`: whether to produce an ASCII-armored form or a
        binary-encoded form.

        `sigtype`: whether to make the signature as a binary signature
        or as a signature in canonical text form.

        `signers`: a map of OpenPGP transferable secret keys with
        signing capability.  The keys of this map are handles that can
        be used to identify a particular secret key in error messages.

        `wantmicalg`: whether the requestor is interested in the
        signing digest algorithm.

        `keypasswords`: a map of passwords available to try to unlock
        the secret keys in `signers`.  The keys in the map can be used
        as identifiers.

        Returns a tuple of the signature itself as a bytes object, and
        (if requested) a string representation of the digest algorithm
        used that can be used with the micalg parameter in a
        multipart/signed MIME message).

        '''
        raise SOPUnsupportedSubcommand('sign')

    def _handle_verify(self,
                       inp:io.BufferedReader,
                       start:Optional[str]=None,
                       end:Optional[str]=None,
                       sig:str='',
                       signers:List[str]=[],
                       **kwargs:Namespace) -> bytes:
        ret:List[SOPSigResult] = []
        ret =  self.verify(inp.read(),
                           start=self.parse_timestamp(start),
                           end=self.parse_timestamp(end),
                           sig=self._get_indirect_input(sig),
                           signers=dict((signer, self._get_indirect_input(signer)) for signer in signers))
        return ''.join([f'{status}\n' for status in ret]).encode()
    def verify(self, data:bytes,
               start:Optional[datetime]=None,
               end:Optional[datetime]=None,
               sig:bytes=b'',
               signers:MutableMapping[str,bytes]={},
               **kwargs:Namespace) -> List[SOPSigResult]:
        '''Verify a detached OpenPGP signature

        If an acceptable signature was found, return a list of
        SOPSigResult objects.

        If no acceptable signature is found, raise SOPNoSignature.

        `data`: what was ostensibly signed.

        `start`: the earliest acceptable time for a signature (`None`
        means no required time).
        
        `end`: the latest acceptable time for a signature (`None`
        means "right now" -- signatures in the future should not be
        accepted).

        `signers`: the OpenPGP certificates of any acceptable signers.
        The keys to this map are handles that can be used to identify
        a particular certificate in error messages.

        '''
        raise SOPUnsupportedSubcommand('verify')

    def _handle_encrypt(self,
                        inp:io.BufferedReader,
                        literaltype:str,
                        armor:bool,
                        passwords:List[str],
                        signers:List[str],
                        keypasswords:List[str],
                        recipients:List[str],
                        profile:Optional[str] = None,
                        **kwargs:Namespace) -> bytes:
        prof:Optional[SOPProfile] = None
        if profile is not None:
            if profile == 'default':
                prof = self.encrypt_profiles[0]
            else:
                for p in self.encrypt_profiles:
                    if p.name == profile:
                        prof = p
                        break
            if prof is None:
                raise SOPUnsupportedProfile(f'profile "{profile}" not supported for encrypt subcommand')
        return self.encrypt(inp.read(),
                            literaltype=SOPLiteralDataType.__members__[literaltype],
                            armor=armor,
                            passwords=dict((password, self._get_indirect_input(password))
                                           for password in passwords) if passwords else dict(),
                            signers=dict((signer, self._get_indirect_input(signer))
                                         for signer in signers) if signers else dict(),
                            keypasswords=dict((password, self._get_indirect_input(password))
                                           for password in keypasswords) if keypasswords else dict(),
                            recipients=dict((recipient, self._get_indirect_input(recipient))
                                            for recipient in recipients) if recipients else dict(),
                            profile=prof,
                            **kwargs)
    def encrypt(self, data:bytes,
                literaltype:SOPLiteralDataType=SOPLiteralDataType.binary,
                armor:bool=True,
                passwords:MutableMapping[str,bytes]={},
                signers:MutableMapping[str,bytes]={},
                keypasswords:MutableMapping[str,bytes]={},
                recipients:MutableMapping[str,bytes]={},
                profile:Optional[SOPProfile]=None,
                **kwargs:Namespace) -> bytes:
        '''Encrypt a message

        Encrypt a message so that only the intended recipients (or
        someone with access to a provided password) can read it.

        `data`: the message to be encrypted

        `armor`: whether to produce an ASCII-armored message or a
        binary-encoded message.

        `passwords`: a map of passwords for symmetric encryption.  The
        keys to the map are identifiers.

        `signers`: a map of OpenPGP secret keys to sign with.  The
        keys to this map are handles that can be used to refer to
        specific secret keys in error messages.

        `keypasswords`: a map of passwords available to try to unlock
        the secret keys in `signers`.  The keys in the map can be used
        as identifiers.

        `recipients`: a map of OpenPGP certificates that should be
        able to decrypt the resulting message.  The keys to this map
        are handles that can be used to refer to specific certificates
        in error messages.

        '''
        raise SOPUnsupportedSubcommand('encrypt')


    def _handle_decrypt(self,
                        inp:io.BufferedReader,
                        sessionkeyout:Optional[str]=None,
                        sessionkeys:List[str]=[],
                        passwords:List[str]=[],
                        verifications:Optional[str]=None,
                        verifyout:Optional[str]=None,
                        signers:List[str]=[],
                        start:Optional[str]=None,
                        end:Optional[str]=None,
                        keypasswords:List[str]=[],
                        secretkeys:List[str]=[],
                        **kwargs:Namespace) -> bytes:
        if verifyout is not None:
            if verifications is not None and verifyout != verifications:
                logging.warn("Both --verifications-out= and the legacy --verify-out= were supplied and they disagreed with each other.  Ignoring --verify-out= and relying on --verifications-out=")
            else:
                logging.warn("Using legacy option --verify-out=, please use --verifications-out= in the future")
                verifications = verifyout

        if verifications and not signers:
            raise SOPIncompleteVerificationInstructions('When --verify-out is present, at least one '
                                                        '--verify-with argument must also be present')
        if signers and not verifications:
            raise SOPIncompleteVerificationInstructions('When --verify-with is present, '
                                                        '--verify-out must also be present')
        msg:bytes
        verifs:List[SOPSigResult]
        sess:Optional[SOPSessionKey]
        msg,verifs,sess = self.decrypt(inp.read(),
                                       wantsessionkey=sessionkeyout is not None,
                                       sessionkeys=dict((sessionkey, self._get_session_key_from_handle(sessionkey))
                                                        for sessionkey in sessionkeys) if sessionkeys else dict(),
                                       passwords=dict((password, self._get_indirect_input(password))
                                                      for password in passwords) if passwords else dict(),
                                       signers=dict((signer, self._get_indirect_input(signer))
                                                    for signer in signers) if signers else dict(),
                                       start=self.parse_timestamp(start),
                                       end=self.parse_timestamp(end),
                                       keypasswords=dict((pwfile, self._get_indirect_input(pwfile))
                                                         for pwfile in keypasswords) if keypasswords else dict(),
                                       secretkeys=dict((secretkey, self._get_indirect_input(secretkey))
                                                       for secretkey in secretkeys) if secretkeys else dict(),
                                       **kwargs)
        if verifications:
            self._write_indirect_output(verifications,
                                        ''.join([f'{status}\n' for status in verifs]).encode())
        if sessionkeyout:
            self._write_indirect_output(sessionkeyout, str(sess).encode() if sess else b'')

        return msg
                                
    def decrypt(self,
                data:bytes,
                wantsessionkey:bool=False,
                sessionkeys:MutableMapping[str,SOPSessionKey]={},
                passwords:MutableMapping[str,bytes]={},
                signers:MutableMapping[str,bytes]={},
                start:Optional[datetime]=None,
                end:Optional[datetime]=None,
                keypasswords:MutableMapping[str,bytes]={},
                secretkeys:MutableMapping[str,bytes]={},
                **kwargs:Namespace) -> Tuple[bytes, List[SOPSigResult], Optional[SOPSessionKey]]:
        raise SOPUnsupportedSubcommand('decrypt')

    def _handle_armor(self,
                      inp:io.BufferedReader,
                      label:str,
                      **kwargs:Namespace) -> bytes:
        return self.armor(inp.read(), label=SOPArmorLabel.__members__[label],
                          **kwargs)
    def armor(self, data:bytes, label:SOPArmorLabel,
              **kwargs:Namespace) -> bytes:
        '''Add OpenPGP ASCII Armor

        Return the ASCII-armored form of `data`.

        `label`: which type of ASCII armor to provide (default: best guess)
        '''
        raise SOPUnsupportedSubcommand('armor')

    def _handle_dearmor(self,
                        inp:io.BufferedReader,
                        **kwargs:Namespace) -> bytes:
        return self.dearmor(inp.read(), **kwargs)
    def dearmor(self, data:bytes, **kwargs:Namespace) -> bytes:
        '''Remove OpenPGP ASCII Armor

        Return the binary-encoded form of `data`, removing any OpenPGP ASCII armor.
        '''
        raise SOPUnsupportedSubcommand('dearmor')


    def _handle_inline_detach(self,
                              inp:io.BufferedReader,
                              armor:bool,
                              sigsout:str,
                              **kwargs:Namespace) -> bytes:
        (message, sigs) = self.inline_detach(inp.read(), armor=armor, **kwargs)
        self._write_indirect_output(sigsout, sigs)
        return message
    def inline_detach(self,
                      clearsigned:bytes,
                      armor:bool=True,
                      **kwargs:Namespace) -> Tuple[bytes,bytes]:
        '''Detach signatures from clearsigned message

        Return a tuple containing two elements: the body of the
        message and (if requested with `wantsigs`), the detached
        signature(s) found in the cleartext message.

        `armor`: whether the signatures should be in binary or
        ASCII-Armored form

        `wantsigs`: if set to False, the signatures member of the
        output tuple will be None.
        '''
        raise SOPUnsupportedSubcommand('inline-detach')

    def _handle_inline_sign(self,
                     inp:io.BufferedReader,
                     armor:bool=True,
                     sigtype:str='binary',
                     signers:List[str]=[],
                     keypasswords:List[str]=[]
                     ) -> bytes:
        insigtype = SOPInlineSigType.__members__[sigtype]
        if insigtype == SOPInlineSigType.clearsigned and not armor:
            raise SOPIncompatibleOptions("cannot specify both --as=clearsigned and --no-armor")
        return self.inline_sign(inp.read(),
                                armor,
                                insigtype,
                                dict((signer, self._get_indirect_input(signer)) for signer in signers),
                                keypasswords=dict((pwfile, self._get_indirect_input(pwfile))
                                                  for pwfile in keypasswords) if keypasswords else dict())
    def inline_sign(self,
                    data:bytes,
                    armor:bool=True,
                    sigtype:SOPInlineSigType=SOPInlineSigType.binary,
                    signers:MutableMapping[str,bytes]={},
                    keypasswords:MutableMapping[str,bytes]={},
                    **kwargs:Namespace,                    
                    ) -> bytes:
        '''Create an inline-signed OpenPGP message

        `data`: the data to sign.

        `armor`: whether to produce an ASCII-armored form or a
        binary-encoded form.

        `sigtype`: whether to treat the inline-signed document as
        binary, text, or to use the OpenPGP cleartext signging
        framework.

        `signers`: a map of OpenPGP transferable secret keys with
        signing capability.  The keys of this map are handles that can
        be used to identify a particular secret key in error messages.

        `keypasswords`: a map of passwords available to try to unlock
        the secret keys in `signers`.  The keys in the map can be used
        as identifiers.

        Returns the inline-signed document itself as a bytes object.

        '''
        raise SOPUnsupportedSubcommand('inline-sign')
    
    def _handle_inline_verify(self,
                              inp:io.BufferedReader,
                              start:Optional[str]=None,
                              end:Optional[str]=None,
                              verifications:Optional[str]=None,
                              signers:List[str]=[],
                              **kwargs:Namespace) -> bytes:
        verifs:List[SOPSigResult]
        msg:bytes
        (msg, verifs) = self.inline_verify(inp.read(),
                                 start=self.parse_timestamp(start),
                                 end=self.parse_timestamp(end),
                                 signers=dict((signer, self._get_indirect_input(signer)) for signer in signers))
        if verifications is not None:
            verifstring = ''.join([f'{status}\n' for status in verifs]).encode()
            self._write_indirect_output(verifications, verifstring)
        return msg
    def inline_verify(self, data:bytes,
                      start:Optional[datetime]=None,
                      end:Optional[datetime]=None,
                      signers:MutableMapping[str,bytes]={},
                      **kwargs:Namespace) -> Tuple[bytes, List[SOPSigResult]]:
        '''Verify an inline-signed OpenPGP message

        If no acceptable signature is found, raise SOPNoSignature.

        Otherwise, returns a tuple of the message and any signature
        details as SOPSigResult objects.

        `data`: the inline-signed message itself.

        `start`: the earliest acceptable time for a signature (`None`
        means no required time).
        
        `end`: the latest acceptable time for a signature (`None`
        means "right now" -- signatures in the future should not be
        accepted).

        `signers`: the OpenPGP certificates of any acceptable signers.
        The keys to this map are handles that can be used to identify
        a particular certificate in error messages.

        '''
        raise SOPUnsupportedSubcommand('inline-verify')

