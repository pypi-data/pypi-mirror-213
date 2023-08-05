The Stateless OpenPGP Command-Line Interface
============================================

The [Stateless OpenPGP Command-Line
Interface](https://datatracker.ietf.org/doc/draft-dkg-openpgp-stateless-cli/)
(or `sop`) is a specification that encourages OpenPGP implementors
to provide a common, relatively simple command-line API for purposes
of object security.

This Python module helps implementers build such a CLI from any
implementation accessible to the Python interpreter.

It does *not* provide such an implementation itself -- this is just
the scaffolding for the command line, which should make it relatively
easy to supply a handful of python functions as methods to a class.

Note that if the user has `argcomplete` installed, they should also
get tab completion in standard shells like `bash` basically for free.

Example
-------

Here is an example of a minimal command-line tool that just implements
the `extract_cert()` interface, using (imaginary) module `foo` that has the
appropriate

```
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
```

Module Goals
------------

### Extensibility

An implementer who wants to extend `sop` in a simple way (e.g. adding
an option to an existing subcommand, or adding a special option)
should be able to do so without breaking this interface.

### Minimal dependencies

The aim is to only depend on modules from stdlib.  We make an
exception for optional modules like `argcomplete`, which can be
skipped.

### Type-checking

All the code in here should be well-annotated

### Self-documenting

Implementers should learn what they need to know from the docstrings,
like so:

    import sop
    help(sop)
    help(sop.StatelessOpenPGP)

### Semantic Versioning

The major version number will only change when backward-incompatible
changes are made.

As long as the major version number is 0, the same holds true for the
minor version number.

