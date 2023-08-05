from temper_core import TemperObject as TemperObject0, cast_by_type as cast_by_type8, Label as Label10, NoResultException as NoResultException11, isinstance_int as isinstance_int12, cast_by_test as cast_by_test13, list_join as list_join_1213, generic_eq as generic_eq_1222, list_builder_add as list_builder_add_1215, string_code_points as string_code_points_1225, bool_not as bool_not_1214, list_get as list_get_1231, int_to_string as int_to_string_1241, str_cat as str_cat_1212
from typing import Union as Union4, NoReturn as NoReturn5, Callable as Callable2, Any as Any6, Tuple as Tuple7, List as List1
from builtins import Exception as Exception9, len as len_1230, list as list_1210
from temper_core.regex import compiled_regex_compile_formatted as compiled_regex_compile_formatted_1216, compiled_regex_compiled_found as compiled_regex_compiled_found_1217, compiled_regex_compiled_find as compiled_regex_compiled_find_1218, compiled_regex_compiled_replace as compiled_regex_compiled_replace_1219, regex_formatter_push_capture_name as regex_formatter_push_capture_name_1223, regex_formatter_push_code_to as regex_formatter_push_code_to_1224
class Regex(TemperObject0):
  __slots__ = ()
  def compiled(this__8) -> 'CompiledRegex':
    return__46: 'CompiledRegex'
    t_1201: 'CompiledRegex' = CompiledRegex(this__8)
    return__46 = t_1201
    return return__46
  def found(this__9, text__120: 'str') -> 'bool':
    return__47: 'bool'
    t_1198: 'CompiledRegex' = this__9.compiled()
    t_1199: 'bool' = t_1198.found(text__120)
    return__47 = t_1199
    return return__47
  def find(this__10, text__123: 'str') -> 'Union4[(Map__16[str, Group]), NoReturn5]':
    return__48: 'Map__16[str, Group]'
    t_836: 'Map__16[str, Group]'
    t_1196: 'CompiledRegex' = this__10.compiled()
    t_836 = t_1196.find(text__123)
    return__48 = t_836
    return return__48
  def replace(this__11, text__126: 'str', format__127: 'Callable2[[Map__16[str, Group]], str]') -> 'str':
    return__49: 'str'
    t_1193: 'CompiledRegex' = this__11.compiled()
    t_1194: 'str' = t_1193.replace(text__126, format__127)
    return__49 = t_1194
    return return__49
class Capture(Regex):
  name__129: 'str'
  item__130: 'Regex'
  __slots__ = ('name__129', 'item__130')
  def constructor__131(this__50, name__132: 'str', item__133: 'Regex') -> Any6:
    return__51: 'None'
    return__51 = None
    this__50.name__129 = name__132
    this__50.item__130 = item__133
    return return__51
  def __init__(this__50, name__132: 'str', item__133: 'Regex') -> None:
    this__50.constructor__131(name__132, item__133)
  @property
  def name(this__298) -> 'str':
    return__299: 'str'
    return__299 = this__298.name__129
    return return__299
  @property
  def item(this__302) -> 'Regex':
    return__303: 'Regex'
    return__303 = this__302.item__130
    return return__303
class CodePart(Regex):
  __slots__ = ()
class CodePoints(CodePart):
  value__134: 'str'
  __slots__ = ('value__134',)
  def constructor__135(this__52, value__136: 'str') -> Any6:
    return__53: 'None'
    return__53 = None
    this__52.value__134 = value__136
    return return__53
  def __init__(this__52, value__136: 'str') -> None:
    this__52.constructor__135(value__136)
  @property
  def value(this__306) -> 'str':
    return__307: 'str'
    return__307 = this__306.value__134
    return return__307
class Special(Regex):
  __slots__ = ()
class SpecialSet(CodePart, Special):
  __slots__ = ()
class CodeRange(CodePart):
  min__144: 'int'
  max__145: 'int'
  __slots__ = ('min__144', 'max__145')
  def constructor__146(this__68, min__147: 'int', max__148: 'int') -> Any6:
    return__69: 'None'
    return__69 = None
    this__68.min__144 = min__147
    this__68.max__145 = max__148
    return return__69
  def __init__(this__68, min__147: 'int', max__148: 'int') -> None:
    this__68.constructor__146(min__147, max__148)
  @property
  def min(this__310) -> 'int':
    return__311: 'int'
    return__311 = this__310.min__144
    return return__311
  @property
  def max(this__314) -> 'int':
    return__315: 'int'
    return__315 = this__314.max__145
    return return__315
class CodeSet(Regex):
  items__149: 'Tuple7[CodePart, ...]'
  negated__150: 'bool'
  __slots__ = ('items__149', 'negated__150')
  def constructor__151(this__70, items__152: 'Tuple7[CodePart, ...]', negated: 'bool' = ...) -> Any6:
    negated__153: 'bool' = negated
    return__72: 'None'
    return__72 = None
    if negated__153 is ...:
      negated__153 = False
    this__70.items__149 = items__152
    this__70.negated__150 = negated__153
    return return__72
  def __init__(this__70, items__152: 'Tuple7[CodePart, ...]', negated: 'bool' = ...) -> None:
    negated__153: 'bool' = negated
    this__70.constructor__151(items__152, negated__153)
  @property
  def items(this__318) -> 'Tuple7[CodePart, ...]':
    return__319: 'Tuple7[CodePart, ...]'
    return__319 = this__318.items__149
    return return__319
  @property
  def negated(this__322) -> 'bool':
    return__323: 'bool'
    return__323 = this__322.negated__150
    return return__323
class Or(Regex):
  items__154: 'Tuple7[Regex, ...]'
  __slots__ = ('items__154',)
  def constructor__155(this__73, items__156: 'Tuple7[Regex, ...]') -> Any6:
    return__75: 'None'
    return__75 = None
    this__73.items__154 = items__156
    return return__75
  def __init__(this__73, items__156: 'Tuple7[Regex, ...]') -> None:
    this__73.constructor__155(items__156)
  @property
  def items(this__326) -> 'Tuple7[Regex, ...]':
    return__327: 'Tuple7[Regex, ...]'
    return__327 = this__326.items__154
    return return__327
class Repeat(Regex):
  item__157: 'Regex'
  min__158: 'int'
  max__159: 'Union4[int, None]'
  reluctant__160: 'bool'
  __slots__ = ('item__157', 'min__158', 'max__159', 'reluctant__160')
  def constructor__161(this__76, item__162: 'Regex', min__163: 'int', max__164: 'Union4[int, None]', reluctant: 'bool' = ...) -> Any6:
    reluctant__165: 'bool' = reluctant
    return__78: 'None'
    return__78 = None
    if reluctant__165 is ...:
      reluctant__165 = False
    this__76.item__157 = item__162
    this__76.min__158 = min__163
    this__76.max__159 = max__164
    this__76.reluctant__160 = reluctant__165
    return return__78
  def __init__(this__76, item__162: 'Regex', min__163: 'int', max__164: 'Union4[int, None]', reluctant: 'bool' = ...) -> None:
    reluctant__165: 'bool' = reluctant
    this__76.constructor__161(item__162, min__163, max__164, reluctant__165)
  @property
  def item(this__330) -> 'Regex':
    return__331: 'Regex'
    return__331 = this__330.item__157
    return return__331
  @property
  def min(this__334) -> 'int':
    return__335: 'int'
    return__335 = this__334.min__158
    return return__335
  @property
  def max(this__338) -> 'Union4[int, None]':
    return__339: 'Union4[int, None]'
    return__339 = this__338.max__159
    return return__339
  @property
  def reluctant(this__342) -> 'bool':
    return__343: 'bool'
    return__343 = this__342.reluctant__160
    return return__343
class Sequence(Regex):
  items__174: 'Tuple7[Regex, ...]'
  __slots__ = ('items__174',)
  def constructor__175(this__82, items__176: 'Tuple7[Regex, ...]') -> Any6:
    return__84: 'None'
    return__84 = None
    this__82.items__174 = items__176
    return return__84
  def __init__(this__82, items__176: 'Tuple7[Regex, ...]') -> None:
    this__82.constructor__175(items__176)
  @property
  def items(this__346) -> 'Tuple7[Regex, ...]':
    return__347: 'Tuple7[Regex, ...]'
    return__347 = this__346.items__174
    return return__347
class Group(TemperObject0):
  name__177: 'str'
  value__178: 'str'
  codePointsBegin__179: 'int'
  __slots__ = ('name__177', 'value__178', 'codePointsBegin__179')
  def constructor__180(this__85, name__181: 'str', value__182: 'str', codePointsBegin__183: 'int') -> Any6:
    return__86: 'None'
    return__86 = None
    this__85.name__177 = name__181
    this__85.value__178 = value__182
    this__85.codePointsBegin__179 = codePointsBegin__183
    return return__86
  def __init__(this__85, name__181: 'str', value__182: 'str', codePointsBegin__183: 'int') -> None:
    this__85.constructor__180(name__181, value__182, codePointsBegin__183)
  @property
  def name(this__350) -> 'str':
    return__351: 'str'
    return__351 = this__350.name__177
    return return__351
  @property
  def value(this__354) -> 'str':
    return__355: 'str'
    return__355 = this__354.value__178
    return return__355
  @property
  def code_points_begin(this__358) -> 'int':
    return__359: 'int'
    return__359 = this__358.codePointsBegin__179
    return return__359
class RegexRefs__19(TemperObject0):
  codePoints__184: 'CodePoints'
  group__185: 'Group'
  orObject__186: 'Or'
  __slots__ = ('codePoints__184', 'group__185', 'orObject__186')
  def constructor__187(this__87, code_points: 'CodePoints' = ..., group: 'Group' = ..., or_object: 'Or' = ...) -> Any6:
    codePoints__188: 'CodePoints' = code_points
    group__189: 'Group' = group
    orObject__190: 'Or' = or_object
    return__88: 'None'
    t_1145: 'CodePoints'
    t_1147: 'Group'
    t_1149: 'Or'
    return__88 = None
    if codePoints__188 is ...:
      t_1145 = CodePoints('')
      codePoints__188 = t_1145
    if group__189 is ...:
      t_1147 = Group('', '', 0)
      group__189 = t_1147
    if orObject__190 is ...:
      t_1149 = Or(())
      orObject__190 = t_1149
    this__87.codePoints__184 = codePoints__188
    this__87.group__185 = group__189
    this__87.orObject__186 = orObject__190
    return return__88
  def __init__(this__87, code_points: 'CodePoints' = ..., group: 'Group' = ..., or_object: 'Or' = ...) -> None:
    codePoints__188: 'CodePoints' = code_points
    group__189: 'Group' = group
    orObject__190: 'Or' = or_object
    this__87.constructor__187(codePoints__188, group__189, orObject__190)
  @property
  def code_points(this__362) -> 'CodePoints':
    return__363: 'CodePoints'
    return__363 = this__362.codePoints__184
    return return__363
  @property
  def group(this__366) -> 'Group':
    return__367: 'Group'
    return__367 = this__366.group__185
    return return__367
  @property
  def or_object(this__370) -> 'Or':
    return__371: 'Or'
    return__371 = this__370.orObject__186
    return return__371
class CompiledRegex(TemperObject0):
  data__192: 'Regex'
  compiled__206: 'Any6'
  __slots__ = ('data__192', 'compiled__206')
  def constructor__193(this__20, data__194: 'Regex') -> Any6:
    return__89: 'None'
    return__89 = None
    this__20.data__192 = data__194
    t_1139: 'str' = this__20.format__225()
    t_1140: 'Any6' = compiled_regex_compile_formatted_1216(this__20, t_1139)
    this__20.compiled__206 = t_1140
    return return__89
  def __init__(this__20, data__194: 'Regex') -> None:
    this__20.constructor__193(data__194)
  def found(this__21, text__197: 'str') -> 'bool':
    return__90: 'bool'
    t_1138: 'bool' = compiled_regex_compiled_found_1217(this__21, this__21.compiled__206, text__197)
    return__90 = t_1138
    return return__90
  def find(this__22, text__200: 'str') -> 'Union4[(Map__16[str, Group]), NoReturn5]':
    return__91: 'Map__16[str, Group]'
    t_795: 'Map__16[str, Group]'
    t_795 = compiled_regex_compiled_find_1218(this__22, this__22.compiled__206, text__200, regexRefs__191)
    return__91 = t_795
    return return__91
  def replace(this__23, text__203: 'str', format__204: 'Callable2[[Map__16[str, Group]], str]') -> 'str':
    return__92: 'str'
    t_1135: 'str' = compiled_regex_compiled_replace_1219(this__23, this__23.compiled__206, text__203, format__204, regexRefs__191)
    return__92 = t_1135
    return return__92
  def format__225(this__28) -> 'str':
    return__97: 'str'
    t_1128: 'RegexFormatter__29' = RegexFormatter__29()
    t_1129: 'str' = t_1128.format(this__28.data__192)
    return__97 = t_1129
    return return__97
  @property
  def data(this__374) -> 'Regex':
    return__375: 'Regex'
    return__375 = this__374.data__192
    return return__375
class RegexFormatter__29(TemperObject0):
  out__227: 'List1[str]'
  __slots__ = ('out__227',)
  def format(this__30, regex__229: 'Regex') -> 'str':
    return__101: 'str'
    this__30.pushRegex__232(regex__229)
    t_1124: 'List1[str]' = this__30.out__227
    def fn__1120(x__231: 'str') -> 'str':
      return__866: 'str'
      return__866 = x__231
      return return__866
    t_1123: 'Callable2[[str], str]' = fn__1120
    t_1125: 'str' = list_join_1213(t_1124, '', t_1123)
    return__101 = t_1125
    return return__101
  def pushRegex__232(this__31, regex__233: 'Regex') -> 'None':
    return__102: 'None'
    return__102 = None
    t_755: 'bool'
    t_756: 'Capture'
    t_759: 'bool'
    t_760: 'CodePoints'
    t_763: 'bool'
    t_764: 'CodeRange'
    t_767: 'bool'
    t_768: 'CodeSet'
    t_771: 'bool'
    t_772: 'Or'
    t_775: 'bool'
    t_776: 'Repeat'
    t_779: 'bool'
    t_780: 'Sequence'
    try:
      cast_by_type8(regex__233, Capture)
      t_755 = True
    except Exception9:
      t_755 = False
    with Label10() as s__1220_1221:
      if t_755:
        try:
          t_756 = cast_by_type8(regex__233, Capture)
        except Exception9:
          s__1220_1221.break_()
        this__31.pushCapture__235(t_756)
      else:
        try:
          cast_by_type8(regex__233, CodePoints)
          t_759 = True
        except Exception9:
          t_759 = False
        if t_759:
          try:
            t_760 = cast_by_type8(regex__233, CodePoints)
          except Exception9:
            s__1220_1221.break_()
          this__31.pushCodePoints__251(t_760, False)
        else:
          try:
            cast_by_type8(regex__233, CodeRange)
            t_763 = True
          except Exception9:
            t_763 = False
          if t_763:
            try:
              t_764 = cast_by_type8(regex__233, CodeRange)
            except Exception9:
              s__1220_1221.break_()
            this__31.pushCodeRange__256(t_764)
          else:
            try:
              cast_by_type8(regex__233, CodeSet)
              t_767 = True
            except Exception9:
              t_767 = False
            if t_767:
              try:
                t_768 = cast_by_type8(regex__233, CodeSet)
              except Exception9:
                s__1220_1221.break_()
              this__31.pushCodeSet__262(t_768)
            else:
              try:
                cast_by_type8(regex__233, Or)
                t_771 = True
              except Exception9:
                t_771 = False
              if t_771:
                try:
                  t_772 = cast_by_type8(regex__233, Or)
                except Exception9:
                  s__1220_1221.break_()
                this__31.pushOr__274(t_772)
              else:
                try:
                  cast_by_type8(regex__233, Repeat)
                  t_775 = True
                except Exception9:
                  t_775 = False
                if t_775:
                  try:
                    t_776 = cast_by_type8(regex__233, Repeat)
                  except Exception9:
                    s__1220_1221.break_()
                  this__31.pushRepeat__278(t_776)
                else:
                  try:
                    cast_by_type8(regex__233, Sequence)
                    t_779 = True
                  except Exception9:
                    t_779 = False
                  if t_779:
                    try:
                      t_780 = cast_by_type8(regex__233, Sequence)
                    except Exception9:
                      s__1220_1221.break_()
                    this__31.pushSequence__283(t_780)
                  elif generic_eq_1222(regex__233, begin):
                    try:
                      list_builder_add_1215(this__31.out__227, '^')
                    except Exception9:
                      s__1220_1221.break_()
                  elif generic_eq_1222(regex__233, dot):
                    try:
                      list_builder_add_1215(this__31.out__227, '.')
                    except Exception9:
                      s__1220_1221.break_()
                  elif generic_eq_1222(regex__233, end):
                    try:
                      list_builder_add_1215(this__31.out__227, '$')
                    except Exception9:
                      s__1220_1221.break_()
                  elif generic_eq_1222(regex__233, word_boundary):
                    try:
                      list_builder_add_1215(this__31.out__227, '\\b')
                    except Exception9:
                      s__1220_1221.break_()
                  elif generic_eq_1222(regex__233, digit):
                    try:
                      list_builder_add_1215(this__31.out__227, '\\d')
                    except Exception9:
                      s__1220_1221.break_()
                  elif generic_eq_1222(regex__233, space):
                    try:
                      list_builder_add_1215(this__31.out__227, '\\s')
                    except Exception9:
                      s__1220_1221.break_()
                  elif generic_eq_1222(regex__233, word):
                    try:
                      list_builder_add_1215(this__31.out__227, '\\w')
                    except Exception9:
                      s__1220_1221.break_()
      return return__102
    raise NoResultException11()
  def pushCapture__235(this__32, capture__236: 'Capture') -> 'None':
    return__103: 'None'
    t_1106: 'str'
    t_1108: 'Regex'
    return__103 = None
    t_750: 'List1[str]'
    list_builder_add_1215(this__32.out__227, '(')
    t_750 = this__32.out__227
    t_1106 = capture__236.name
    regex_formatter_push_capture_name_1223(this__32, t_750, t_1106)
    t_1108 = capture__236.item
    this__32.pushRegex__232(t_1108)
    list_builder_add_1215(this__32.out__227, ')')
    return return__103
  def pushCode__242(this__34, code__243: 'int', insideCodeSet__244: 'bool') -> 'None':
    return__105: 'None'
    return__105 = None
    regex_formatter_push_code_to_1224(this__34, this__34.out__227, code__243, insideCodeSet__244)
    return return__105
  def pushCodePoints__251(this__36, codePoints__252: 'CodePoints', insideCodeSet__253: 'bool') -> 'None':
    return__107: 'None'
    t_1096: 'bool'
    t_1097: 'int'
    t_1098: 'Any6'
    return__107 = None
    t_1095: 'str' = codePoints__252.value
    t_1100: 'Any6' = string_code_points_1225(t_1095)
    slice__255: 'Any6' = t_1100
    while True:
      t_1096 = slice__255.is_empty
      if bool_not_1214(t_1096):
        t_1097 = slice__255.read()
        this__36.pushCode__242(t_1097, insideCodeSet__253)
        t_1098 = slice__255.advance(1)
        slice__255 = t_1098
      else:
        break
    return return__107
  def pushCodeRange__256(this__37, codeRange__257: 'CodeRange') -> 'None':
    return__108: 'None'
    return__108 = None
    list_builder_add_1215(this__37.out__227, '[')
    this__37.pushCodeRangeUnwrapped__259(codeRange__257)
    list_builder_add_1215(this__37.out__227, ']')
    return return__108
  def pushCodeRangeUnwrapped__259(this__38, codeRange__260: 'CodeRange') -> 'None':
    return__109: 'None'
    t_1090: 'int'
    return__109 = None
    t_1088: 'int' = codeRange__260.min
    this__38.pushCode__242(t_1088, True)
    list_builder_add_1215(this__38.out__227, '-')
    t_1090 = codeRange__260.max
    this__38.pushCode__242(t_1090, True)
    return return__109
  def pushCodeSet__262(this__39, codeSet__263: 'CodeSet') -> 'None':
    return__110: 'None'
    t_1082: 'Tuple7[CodePart, ...]'
    t_1083: 'Tuple7[CodePart, ...]'
    t_1085: 'int'
    t_1086: 'bool'
    return__110 = None
    t_720: 'bool'
    t_721: 'CodeSet'
    t_727: 'CodePart'
    t_1080: 'Regex' = this__39.adjustCodeSet__267(codeSet__263, regexRefs__191)
    adjusted__265: 'Regex' = t_1080
    try:
      cast_by_type8(adjusted__265, CodeSet)
      t_720 = True
    except Exception9:
      t_720 = False
    with Label10() as s__1226_1228:
      if t_720:
        with Label10() as s__1227_1229:
          try:
            t_721 = cast_by_type8(adjusted__265, CodeSet)
            list_builder_add_1215(this__39.out__227, '[')
          except Exception9:
            s__1227_1229.break_()
          t_1086 = t_721.negated
          if t_1086:
            try:
              list_builder_add_1215(this__39.out__227, '^')
            except Exception9:
              s__1227_1229.break_()
          i__266: 'int' = 0
          while True:
            t_1082 = t_721.items
            t_1085 = len_1230(t_1082)
            if i__266 < t_1085:
              t_1083 = t_721.items
              try:
                t_727 = list_get_1231(t_1083, i__266)
              except Exception9:
                s__1227_1229.break_()
              this__39.pushCodeSetItem__271(t_727)
              i__266 = i__266 + 1
            else:
              break
          try:
            list_builder_add_1215(this__39.out__227, ']')
            s__1226_1228.break_()
          except Exception9:
            pass
        raise NoResultException11()
      this__39.pushRegex__232(adjusted__265)
    return return__110
  def adjustCodeSet__267(this__40, codeSet__268: 'CodeSet', regexRefs__269: 'RegexRefs__19') -> 'Regex':
    return__111: 'Regex'
    return__111 = codeSet__268
    return return__111
  def pushCodeSetItem__271(this__41, codePart__272: 'CodePart') -> 'None':
    return__112: 'None'
    return__112 = None
    t_707: 'bool'
    t_708: 'CodePoints'
    t_711: 'bool'
    t_712: 'CodeRange'
    t_715: 'bool'
    t_716: 'SpecialSet'
    try:
      cast_by_type8(codePart__272, CodePoints)
      t_707 = True
    except Exception9:
      t_707 = False
    with Label10() as s__1232_1233:
      if t_707:
        try:
          t_708 = cast_by_type8(codePart__272, CodePoints)
        except Exception9:
          s__1232_1233.break_()
        this__41.pushCodePoints__251(t_708, True)
      else:
        try:
          cast_by_type8(codePart__272, CodeRange)
          t_711 = True
        except Exception9:
          t_711 = False
        if t_711:
          try:
            t_712 = cast_by_type8(codePart__272, CodeRange)
          except Exception9:
            s__1232_1233.break_()
          this__41.pushCodeRangeUnwrapped__259(t_712)
        else:
          try:
            cast_by_type8(codePart__272, SpecialSet)
            t_715 = True
          except Exception9:
            t_715 = False
          if t_715:
            try:
              t_716 = cast_by_type8(codePart__272, SpecialSet)
            except Exception9:
              s__1232_1233.break_()
            this__41.pushRegex__232(t_716)
      return return__112
    raise NoResultException11()
  def pushOr__274(this__42, or__275: 'Or') -> 'None':
    return__113: 'None'
    t_1067: 'Tuple7[Regex, ...]'
    t_1068: 'Tuple7[Regex, ...]'
    t_1070: 'int'
    t_1071: 'Tuple7[Regex, ...]'
    return__113 = None
    t_697: 'Regex'
    t_702: 'Regex'
    t_1066: 'Tuple7[Regex, ...]' = or__275.items
    t_1073: 'bool' = not t_1066
    with Label10() as s__1234_1237:
      if bool_not_1214(t_1073):
        with Label10() as s__1235_1238:
          try:
            list_builder_add_1215(this__42.out__227, '(?:')
            t_1071 = or__275.items
            t_697 = list_get_1231(t_1071, 0)
          except Exception9:
            s__1235_1238.break_()
          this__42.pushRegex__232(t_697)
          i__277: 'int' = 1
          while True:
            t_1067 = or__275.items
            t_1070 = len_1230(t_1067)
            if i__277 < t_1070:
              try:
                list_builder_add_1215(this__42.out__227, '|')
                t_1068 = or__275.items
                t_702 = list_get_1231(t_1068, i__277)
              except Exception9:
                break
              this__42.pushRegex__232(t_702)
              i__277 = i__277 + 1
            else:
              try:
                list_builder_add_1215(this__42.out__227, ')')
              except Exception9:
                s__1235_1238.break_()
              s__1234_1237.break_()
        raise NoResultException11()
    return return__113
  def pushRepeat__278(this__43, repeat__279: 'Repeat') -> 'None':
    return__114: 'None'
    t_1059: 'Regex'
    t_1061: 'int'
    t_1062: 'str'
    t_1063: 'str'
    t_1064: 'bool'
    return__114 = None
    t_676: 'Union4[int, None]'
    t_677: 'bool'
    t_679: 'bool'
    t_681: 'bool'
    t_684: 'List1[str]'
    t_685: 'int'
    t_687: 'List1[str]'
    with Label10() as s__1239_1240:
      min__281: 'int'
      try:
        list_builder_add_1215(this__43.out__227, '(?:')
        t_1059 = repeat__279.item
        this__43.pushRegex__232(t_1059)
        list_builder_add_1215(this__43.out__227, ')')
        t_1061 = repeat__279.min
        min__281 = t_1061
        t_676 = repeat__279.max
      except Exception9:
        s__1239_1240.break_()
      max__282: 'Union4[int, None]' = t_676
      if min__281 == 0:
        t_677 = max__282 == 1
      else:
        t_677 = False
      if t_677:
        try:
          list_builder_add_1215(this__43.out__227, '?')
        except Exception9:
          s__1239_1240.break_()
      else:
        if min__281 == 0:
          t_679 = max__282 == None
        else:
          t_679 = False
        if t_679:
          try:
            list_builder_add_1215(this__43.out__227, '*')
          except Exception9:
            s__1239_1240.break_()
        else:
          if min__281 == 1:
            t_681 = max__282 == None
          else:
            t_681 = False
          if t_681:
            try:
              list_builder_add_1215(this__43.out__227, '+')
            except Exception9:
              s__1239_1240.break_()
          else:
            t_684 = this__43.out__227
            t_1062 = int_to_string_1241(min__281)
            try:
              list_builder_add_1215(t_684, str_cat_1212('{', t_1062))
            except Exception9:
              s__1239_1240.break_()
            if min__281 != max__282:
              try:
                list_builder_add_1215(this__43.out__227, ',')
              except Exception9:
                s__1239_1240.break_()
              if max__282 != None:
                t_687 = this__43.out__227
                try:
                  t_685 = cast_by_test13(max__282, isinstance_int12)
                  t_1063 = int_to_string_1241(t_685)
                  list_builder_add_1215(t_687, t_1063)
                except Exception9:
                  s__1239_1240.break_()
            try:
              list_builder_add_1215(this__43.out__227, '}')
            except Exception9:
              s__1239_1240.break_()
      t_1064 = repeat__279.reluctant
      if t_1064:
        try:
          list_builder_add_1215(this__43.out__227, '?')
        except Exception9:
          s__1239_1240.break_()
      return return__114
    raise NoResultException11()
  def pushSequence__283(this__44, sequence__284: 'Sequence') -> 'None':
    return__115: 'None'
    t_1054: 'Tuple7[Regex, ...]'
    t_1055: 'Tuple7[Regex, ...]'
    t_1057: 'int'
    return__115 = None
    t_670: 'Regex'
    i__286: 'int' = 0
    with Label10() as s__1242_1243:
      while True:
        t_1054 = sequence__284.items
        t_1057 = len_1230(t_1054)
        if i__286 < t_1057:
          t_1055 = sequence__284.items
          try:
            t_670 = list_get_1231(t_1055, i__286)
          except Exception9:
            break
          this__44.pushRegex__232(t_670)
          i__286 = i__286 + 1
        else:
          s__1242_1243.break_()
      raise NoResultException11()
    return return__115
  def max_code(this__45, codePart__288: 'CodePart') -> 'Union4[int, None]':
    return__116: 'Union4[int, None]'
    t_1041: 'Any6'
    t_1042: 'Any6'
    t_1043: 'Any6'
    t_1044: 'str'
    t_1045: 'bool'
    t_1046: 'Any6'
    t_1047: 'bool'
    t_1048: 'int'
    t_1049: 'Any6'
    t_1050: 'Union4[int, None]'
    t_1051: 'Union4[int, None]'
    t_1052: 'Union4[int, None]'
    t_1053: 'Union4[int, None]'
    t_643: 'bool'
    t_644: 'CodePoints'
    t_651: 'Union4[int, None]'
    t_652: 'Union4[int, None]'
    t_656: 'bool'
    t_657: 'CodeRange'
    t_666: 'Union4[int, None]'
    try:
      cast_by_type8(codePart__288, CodePoints)
      t_643 = True
    except Exception9:
      t_643 = False
    with Label10() as s__1244_1245:
      if t_643:
        try:
          t_644 = cast_by_type8(codePart__288, CodePoints)
        except Exception9:
          s__1244_1245.break_()
        t_1044 = t_644.value
        value__290: 'str' = t_1044
        t_1045 = not value__290
        if t_1045:
          t_652 = None
        else:
          max__291: 'int' = 0
          t_1046 = string_code_points_1225(value__290)
          slice__292: 'Any6' = t_1046
          while True:
            t_1047 = slice__292.is_empty
            if bool_not_1214(t_1047):
              t_1048 = slice__292.read()
              next__293: 'int' = t_1048
              if next__293 > max__291:
                max__291 = next__293
              t_1049 = slice__292.advance(1)
              slice__292 = t_1049
            else:
              break
          t_651 = max__291
          t_652 = t_651
        t_666 = t_652
      else:
        try:
          cast_by_type8(codePart__288, CodeRange)
          t_656 = True
        except Exception9:
          t_656 = False
        if t_656:
          try:
            t_657 = cast_by_type8(codePart__288, CodeRange)
          except Exception9:
            s__1244_1245.break_()
          t_1050 = t_657.max
          t_666 = t_1050
        elif generic_eq_1222(codePart__288, digit):
          t_1041 = string_code_points_1225('9')
          t_1051 = t_1041.read()
          t_666 = t_1051
        elif generic_eq_1222(codePart__288, space):
          t_1042 = string_code_points_1225(' ')
          t_1052 = t_1042.read()
          t_666 = t_1052
        elif generic_eq_1222(codePart__288, word):
          t_1043 = string_code_points_1225('z')
          t_1053 = t_1043.read()
          t_666 = t_1053
        else:
          t_666 = None
      try:
        return__116 = t_666
        return return__116
      except Exception9:
        pass
    raise NoResultException11()
  def constructor__294(this__98, out: 'List1[str]' = ...) -> Any6:
    out__295: 'List1[str]' = out
    return__100: 'None'
    t_1037: 'List1[str]'
    return__100 = None
    if out__295 is ...:
      t_1037 = list_1210()
      out__295 = t_1037
    this__98.out__227 = out__295
    return return__100
  def __init__(this__98, out: 'List1[str]' = ...) -> None:
    out__295: 'List1[str]' = out
    this__98.constructor__294(out__295)
class Begin__12(Special):
  __slots__ = ()
  def constructor__137(this__54) -> Any6:
    return__55: 'None'
    return__55 = None
    return return__55
  def __init__(this__54) -> None:
    this__54.constructor__137()
t_1202: 'Begin__12' = Begin__12()
begin: 'Begin__12' = t_1202
class Dot__13(Special):
  __slots__ = ()
  def constructor__138(this__56) -> Any6:
    return__57: 'None'
    return__57 = None
    return return__57
  def __init__(this__56) -> None:
    this__56.constructor__138()
t_1203: 'Dot__13' = Dot__13()
dot: 'Dot__13' = t_1203
class End__14(Special):
  __slots__ = ()
  def constructor__139(this__58) -> Any6:
    return__59: 'None'
    return__59 = None
    return return__59
  def __init__(this__58) -> None:
    this__58.constructor__139()
t_1204: 'End__14' = End__14()
end: 'End__14' = t_1204
class WordBoundary__15(Special):
  __slots__ = ()
  def constructor__140(this__60) -> Any6:
    return__61: 'None'
    return__61 = None
    return return__61
  def __init__(this__60) -> None:
    this__60.constructor__140()
t_1205: 'WordBoundary__15' = WordBoundary__15()
word_boundary: 'WordBoundary__15' = t_1205
class Digit__16(SpecialSet):
  __slots__ = ()
  def constructor__141(this__62) -> Any6:
    return__63: 'None'
    return__63 = None
    return return__63
  def __init__(this__62) -> None:
    this__62.constructor__141()
t_1206: 'Digit__16' = Digit__16()
digit: 'Digit__16' = t_1206
class Space__17(SpecialSet):
  __slots__ = ()
  def constructor__142(this__64) -> Any6:
    return__65: 'None'
    return__65 = None
    return return__65
  def __init__(this__64) -> None:
    this__64.constructor__142()
t_1207: 'Space__17' = Space__17()
space: 'Space__17' = t_1207
class Word__18(SpecialSet):
  __slots__ = ()
  def constructor__143(this__66) -> Any6:
    return__67: 'None'
    return__67 = None
    return return__67
  def __init__(this__66) -> None:
    this__66.constructor__143()
t_1208: 'Word__18' = Word__18()
word: 'Word__18' = t_1208
def entire(item__166: 'Regex') -> 'Regex':
  global begin, end
  return__79: 'Regex'
  t_1165: 'Regex' = Sequence((begin, item__166, end))
  return__79 = t_1165
  return return__79
def one_or_more(item__168: 'Regex', reluctant: 'bool' = ...) -> 'Repeat':
  reluctant__169: 'bool' = reluctant
  return__80: 'Repeat'
  if reluctant__169 is ...:
    reluctant__169 = False
  t_1163: 'Repeat' = Repeat(item__168, 1, None, reluctant__169)
  return__80 = t_1163
  return return__80
def optional(item__171: 'Regex', reluctant: 'bool' = ...) -> 'Repeat':
  reluctant__172: 'bool' = reluctant
  return__81: 'Repeat'
  if reluctant__172 is ...:
    reluctant__172 = False
  t_1160: 'Repeat' = Repeat(item__171, 0, 1, reluctant__172)
  return__81 = t_1160
  return return__81
t_1209: 'RegexRefs__19' = RegexRefs__19()
regexRefs__191: 'RegexRefs__19' = t_1209
return__865: 'Any6' = ('<<lang.temper.value.TypeTag<out kotlin.Any>: Type, lang.temper.value.Value<*>: RegexFormatter__29: Type>>', NotImplemented)[1]
export = return__865
