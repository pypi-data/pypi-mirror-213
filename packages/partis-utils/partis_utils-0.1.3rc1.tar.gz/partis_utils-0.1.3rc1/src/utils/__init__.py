# NOTE: this variable is used for conditional import of type-hint related modules
# during either type-checking or during documentation generation.
# TYPE_CHECKING is *not* used directly so that TYPING can be set to True
# *without* globally setting TYPE_CHECKING = True (which can break things).
from typing import TYPE_CHECKING
TYPING = TYPE_CHECKING

from . import special
from .special import (
  NotSet)
from . import module

from .inspect import (
  caller_module,
  caller_vars,
  caller_class_var,
  make_dynamic_class_name,
  filter_traceback,
  defer_imports,
  apply_deferred_imports,
  pedantic_isinstance,
  direct_isinstance,
  permissive_issubclass)

from .property import (
  cached_property )

from .valid import (
  isinstance_any,
  issubclass_any,
  valid_list,
  ensure_iterable,
  ensure_callable )

from .fmt import (
  as_rich,
  join_attr_path,
  split_attr_path,
  do_pprint,
  f,
  fmt_src_line,
  split_lines,
  indent_lines,
  line_segment,
  fmt_limit,
  fmt_base_or_type,
  fmt_iterable,
  fmt_iterable_or,
  fmt_iterable_and,
  StringFunction,
  fmt_obj )

from .fmt_doc import (
  _fmt_class_name,
  fmt_class_name,
  fmt_attr_doc )

from .hint import (
  HINT_LEVELS,
  HINT_LEVELS_DESC,
  hint_level_name,
  hint_level_num,
  ModelHint,
  ModelError,
  Loc )

from .log import (
  log_levels,
  logging_parser_add,
  logging_parser_get,
  logging_parser_init,
  init_logging,
  getLogger,
  record_to_hint,
  LogListHandler,
  branched_log )

from .data import (
  protected_attr,
  attrs_modify,
  mapping_attrs,
  adict_frozen,
  adict_struct,
  adict,
  odict,
  owdict,
  rdict,
  rlist,
  update_recursive )

from .file import (
  head,
  tail,
  checksum,
  copytree,
  BackupFile )

from .mutex_file import (
  MutexFileError,
  MutexFileTimeout,
  MutexBase,
  MutexFile )

from .similarity import (
  max_similarity )

from .time import (
  TimerMono,
  TimeEncode )

from .venv import (
  ProcessEnv,
  VirtualEnv )
