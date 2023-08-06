from . import _libprotein

try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        if _newclass:
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError("'%s' object has no attribute '%s'" % (class_type.__name__, name))


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except __builtin__.Exception:
    class _object:
        pass
    _newclass = 0

class SwigPyIterator(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SwigPyIterator, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SwigPyIterator, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _libprotein.delete_SwigPyIterator
    __del__ = lambda self: None

    def value(self):
        return _libprotein.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _libprotein.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _libprotein.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _libprotein.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _libprotein.SwigPyIterator_equal(self, x)

    def copy(self):
        return _libprotein.SwigPyIterator_copy(self)

    def next(self):
        return _libprotein.SwigPyIterator_next(self)

    def __next__(self):
        return _libprotein.SwigPyIterator___next__(self)

    def previous(self):
        return _libprotein.SwigPyIterator_previous(self)

    def advance(self, n):
        return _libprotein.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _libprotein.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _libprotein.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _libprotein.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _libprotein.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _libprotein.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _libprotein.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self
SwigPyIterator_swigregister = _libprotein.SwigPyIterator_swigregister
SwigPyIterator_swigregister(SwigPyIterator)

class IntVector(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, IntVector, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, IntVector, name)
    __repr__ = _swig_repr

    def iterator(self):
        return _libprotein.IntVector_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _libprotein.IntVector___nonzero__(self)

    def __bool__(self):
        return _libprotein.IntVector___bool__(self)

    def __len__(self):
        return _libprotein.IntVector___len__(self)

    def __getslice__(self, i, j):
        return _libprotein.IntVector___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _libprotein.IntVector___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _libprotein.IntVector___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _libprotein.IntVector___delitem__(self, *args)

    def __getitem__(self, *args):
        return _libprotein.IntVector___getitem__(self, *args)

    def __setitem__(self, *args):
        return _libprotein.IntVector___setitem__(self, *args)

    def pop(self):
        return _libprotein.IntVector_pop(self)

    def append(self, x):
        return _libprotein.IntVector_append(self, x)

    def empty(self):
        return _libprotein.IntVector_empty(self)

    def size(self):
        return _libprotein.IntVector_size(self)

    def swap(self, v):
        return _libprotein.IntVector_swap(self, v)

    def begin(self):
        return _libprotein.IntVector_begin(self)

    def end(self):
        return _libprotein.IntVector_end(self)

    def rbegin(self):
        return _libprotein.IntVector_rbegin(self)

    def rend(self):
        return _libprotein.IntVector_rend(self)

    def clear(self):
        return _libprotein.IntVector_clear(self)

    def get_allocator(self):
        return _libprotein.IntVector_get_allocator(self)

    def pop_back(self):
        return _libprotein.IntVector_pop_back(self)

    def erase(self, *args):
        return _libprotein.IntVector_erase(self, *args)

    def __init__(self, *args):
        this = _libprotein.new_IntVector(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def push_back(self, x):
        return _libprotein.IntVector_push_back(self, x)

    def front(self):
        return _libprotein.IntVector_front(self)

    def back(self):
        return _libprotein.IntVector_back(self)

    def assign(self, n, x):
        return _libprotein.IntVector_assign(self, n, x)

    def resize(self, *args):
        return _libprotein.IntVector_resize(self, *args)

    def insert(self, *args):
        return _libprotein.IntVector_insert(self, *args)

    def reserve(self, n):
        return _libprotein.IntVector_reserve(self, n)

    def capacity(self):
        return _libprotein.IntVector_capacity(self)
    __swig_destroy__ = _libprotein.delete_IntVector
    __del__ = lambda self: None
IntVector_swigregister = _libprotein.IntVector_swigregister
IntVector_swigregister(IntVector)

class StringVector(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, StringVector, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, StringVector, name)
    __repr__ = _swig_repr

    def iterator(self):
        return _libprotein.StringVector_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _libprotein.StringVector___nonzero__(self)

    def __bool__(self):
        return _libprotein.StringVector___bool__(self)

    def __len__(self):
        return _libprotein.StringVector___len__(self)

    def __getslice__(self, i, j):
        return _libprotein.StringVector___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _libprotein.StringVector___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _libprotein.StringVector___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _libprotein.StringVector___delitem__(self, *args)

    def __getitem__(self, *args):
        return _libprotein.StringVector___getitem__(self, *args)

    def __setitem__(self, *args):
        return _libprotein.StringVector___setitem__(self, *args)

    def pop(self):
        return _libprotein.StringVector_pop(self)

    def append(self, x):
        return _libprotein.StringVector_append(self, x)

    def empty(self):
        return _libprotein.StringVector_empty(self)

    def size(self):
        return _libprotein.StringVector_size(self)

    def swap(self, v):
        return _libprotein.StringVector_swap(self, v)

    def begin(self):
        return _libprotein.StringVector_begin(self)

    def end(self):
        return _libprotein.StringVector_end(self)

    def rbegin(self):
        return _libprotein.StringVector_rbegin(self)

    def rend(self):
        return _libprotein.StringVector_rend(self)

    def clear(self):
        return _libprotein.StringVector_clear(self)

    def get_allocator(self):
        return _libprotein.StringVector_get_allocator(self)

    def pop_back(self):
        return _libprotein.StringVector_pop_back(self)

    def erase(self, *args):
        return _libprotein.StringVector_erase(self, *args)

    def __init__(self, *args):
        this = _libprotein.new_StringVector(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def push_back(self, x):
        return _libprotein.StringVector_push_back(self, x)

    def front(self):
        return _libprotein.StringVector_front(self)

    def back(self):
        return _libprotein.StringVector_back(self)

    def assign(self, n, x):
        return _libprotein.StringVector_assign(self, n, x)

    def resize(self, *args):
        return _libprotein.StringVector_resize(self, *args)

    def insert(self, *args):
        return _libprotein.StringVector_insert(self, *args)

    def reserve(self, n):
        return _libprotein.StringVector_reserve(self, n)

    def capacity(self):
        return _libprotein.StringVector_capacity(self)
    __swig_destroy__ = _libprotein.delete_StringVector
    __del__ = lambda self: None
StringVector_swigregister = _libprotein.StringVector_swigregister
StringVector_swigregister(StringVector)

class Uniprot(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Uniprot, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Uniprot, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _libprotein.new_Uniprot()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def set_uniprot_id(self, idd):
        return _libprotein.Uniprot_set_uniprot_id(self, idd)

    def set_uniprot_seq(self, seqq):
        return _libprotein.Uniprot_set_uniprot_seq(self, seqq)

    def set_uniprot_location(self, loc):
        return _libprotein.Uniprot_set_uniprot_location(self, loc)

    def add_to_interactwith(self, inter):
        return _libprotein.Uniprot_add_to_interactwith(self, inter)

    def add_to_pdb_struct(self, pdb):
        return _libprotein.Uniprot_add_to_pdb_struct(self, pdb)

    def get_uniprot_id(self):
        return _libprotein.Uniprot_get_uniprot_id(self)

    def get_uniprot_seq(self):
        return _libprotein.Uniprot_get_uniprot_seq(self)

    def get_uniprot_location(self):
        return _libprotein.Uniprot_get_uniprot_location(self)

    def affich_interactwith(self):
        return _libprotein.Uniprot_affich_interactwith(self)

    def affich_pdb_struct(self):
        return _libprotein.Uniprot_affich_pdb_struct(self)

    def get_list_pdb(self):
        return _libprotein.Uniprot_get_list_pdb(self)
    __swig_destroy__ = _libprotein.delete_Uniprot
    __del__ = lambda self: None
Uniprot_swigregister = _libprotein.Uniprot_swigregister
Uniprot_swigregister(Uniprot)

class Ptm(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Ptm, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Ptm, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _libprotein.new_Ptm()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def set_ptm_pos(self, pos):
        return _libprotein.Ptm_set_ptm_pos(self, pos)

    def set_ptm_name(self, name):
        return _libprotein.Ptm_set_ptm_name(self, name)

    def get_ptm_pos(self):
        return _libprotein.Ptm_get_ptm_pos(self)

    def get_ptm_name(self):
        return _libprotein.Ptm_get_ptm_name(self)
    __swig_destroy__ = _libprotein.delete_Ptm
    __del__ = lambda self: None
Ptm_swigregister = _libprotein.Ptm_swigregister
Ptm_swigregister(Ptm)

class Scop(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Scop, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Scop, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _libprotein.new_Scop()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def set_scop_familyID(self, id):
        return _libprotein.Scop_set_scop_familyID(self, id)

    def set_scop_desc(self, desc):
        return _libprotein.Scop_set_scop_desc(self, desc)

    def get_scop_familyID(self):
        return _libprotein.Scop_get_scop_familyID(self)

    def get_scop_desc(self):
        return _libprotein.Scop_get_scop_desc(self)
    __swig_destroy__ = _libprotein.delete_Scop
    __del__ = lambda self: None
Scop_swigregister = _libprotein.Scop_swigregister
Scop_swigregister(Scop)

class Cath(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Cath, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Cath, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _libprotein.new_Cath()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def set_superfamily_id(self, id):
        return _libprotein.Cath_set_superfamily_id(self, id)

    def set_cath_desc(self, desc):
        return _libprotein.Cath_set_cath_desc(self, desc)

    def get_superfamily_id(self):
        return _libprotein.Cath_get_superfamily_id(self)

    def get_cath_desc(self):
        return _libprotein.Cath_get_cath_desc(self)
    __swig_destroy__ = _libprotein.delete_Cath
    __del__ = lambda self: None
Cath_swigregister = _libprotein.Cath_swigregister
Cath_swigregister(Cath)

class Pfam(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Pfam, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Pfam, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _libprotein.new_Pfam()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def set_pfam_id(self, id):
        return _libprotein.Pfam_set_pfam_id(self, id)

    def set_pfam_name(self, name):
        return _libprotein.Pfam_set_pfam_name(self, name)

    def set_start(self, st):
        return _libprotein.Pfam_set_start(self, st)

    def set_end(self, ed):
        return _libprotein.Pfam_set_end(self, ed)

    def get_pfam_id(self):
        return _libprotein.Pfam_get_pfam_id(self)

    def get_pfam_name(self):
        return _libprotein.Pfam_get_pfam_name(self)

    def get_start(self):
        return _libprotein.Pfam_get_start(self)

    def get_end(self):
        return _libprotein.Pfam_get_end(self)
    __swig_destroy__ = _libprotein.delete_Pfam
    __del__ = lambda self: None
Pfam_swigregister = _libprotein.Pfam_swigregister
Pfam_swigregister(Pfam)

class Libprotein(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Libprotein, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Libprotein, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _libprotein.new_Libprotein(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def set_uniprot_info(self, u):
        return _libprotein.Libprotein_set_uniprot_info(self, u)

    def add_to_PtmList(self, p):
        return _libprotein.Libprotein_add_to_PtmList(self, p)

    def add_to_ScopList(self, s):
        return _libprotein.Libprotein_add_to_ScopList(self, s)

    def add_to_CathList(self, c):
        return _libprotein.Libprotein_add_to_CathList(self, c)

    def add_to_PfamList(self, pf):
        return _libprotein.Libprotein_add_to_PfamList(self, pf)

    def printUniprotInfo(self):
        return _libprotein.Libprotein_printUniprotInfo(self)

    def printListPtm(self):
        return _libprotein.Libprotein_printListPtm(self)

    def printListScop(self):
        return _libprotein.Libprotein_printListScop(self)

    def printListCath(self):
        return _libprotein.Libprotein_printListCath(self)

    def printListPfam(self):
        return _libprotein.Libprotein_printListPfam(self)

    def downloadXML(self, id):
        return _libprotein.Libprotein_downloadXML(self, id)

    def downloadScopCLA(self):
        return _libprotein.Libprotein_downloadScopCLA(self)

    def downloadScopDES(self):
        return _libprotein.Libprotein_downloadScopDES(self)

    def downloadPfam(self, id):
        return _libprotein.Libprotein_downloadPfam(self, id)

    def get_code_ptm(self, p):
        return _libprotein.Libprotein_get_code_ptm(self, p)

    def annotateMyprot(self, id):
        return _libprotein.Libprotein_annotateMyprot(self, id)

    def get_dom_pos(self):
        return _libprotein.Libprotein_get_dom_pos(self)

    def get_list_ptm(self):
        return _libprotein.Libprotein_get_list_ptm(self)

    def get_list_pdb(self):
        return _libprotein.Libprotein_get_list_pdb(self)
    __swig_destroy__ = _libprotein.delete_Libprotein
    __del__ = lambda self: None
Libprotein_swigregister = _libprotein.Libprotein_swigregister
Libprotein_swigregister(Libprotein)

# This file is compatible with both classic and new-style classes.


