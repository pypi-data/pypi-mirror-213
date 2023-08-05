#####################################################################################
#
#  Copyright (c) 2023 - Mad Penguin Consulting Ltd
#
#####################################################################################
#
#   WORK IN PROGRESS
#
#   Experimentation re; generating API documentation automatically from code
#   Designed specifically to cope with P3 typing
#   This was pulled from the original - needs a rewrite really, mostly works for now
#
import ast
from ujson import dumps
from loguru import logger as log

class MethodVisitor(ast.NodeVisitor):

    def __init__(self, root):
        self._root = root
        super().__init__()

    def visit_FunctionDef(self, node):
        args = []
        anns = []
        defs = []
        for default in node.args.defaults:
            if isinstance(default, ast.NameConstant):
                v = str(default.value)
            elif isinstance(default, ast.Num):
                v = str(default.n)
            elif isinstance(default, ast.Attribute):
                v = f'{default.value.id}.{default.attr}'
            elif isinstance(default, ast.Name):
                v = str(default.id)
            elif isinstance(default, ast.UnaryOp):
                v = str(-1 * default.operand.n)
            elif isinstance(default, ast.Constant):
                v = str(default.value)
            else:
                print("Unknown type: ", type(default))

            defs.append(v)

        defs = [None for i in range(len(node.args.args) - len(node.args.defaults))] + defs

        for x in node.args.args:
            args.append(x.arg)
            if isinstance(x.annotation, ast.Name):
                anns.append(x.annotation.id)
            elif isinstance(x.annotation, ast.Subscript):
                if isinstance(x.annotation.slice, ast.Name):
                    anns.append(x.annotation.slice.id)
                elif hasattr(x.annotation.slice, 'value'):
                    if isinstance(x.annotation.slice.value, ast.Name):
                        anns.append(x.annotation.slice.value.id)
                    elif isinstance(x.annotation.slice.value, ast.Subscript):
                        anns.append(x.annotation.slice.value)
                    else:
                        lst = []
                        for elt in x.annotation.slice.value.elts:
                            if isinstance(elt, ast.Name):
                                lst.append(elt.id)
                            else:
                                if not isinstance(elt, ast.List):
                                    lst.append(elt.value.id)
                                else:
                                    print(">>>", lst)
                        anns.append((x.annotation.value.id, lst))
                else:
                    print("Not sure what to do with: (", type(x.annotation.slice), ') ||', type(x.annotation), x.arg)
                    anns.append(None)
            else:
                anns.append(None)

        if isinstance(node.returns, ast.Name):
            rets = node.returns.id
        elif isinstance(node.returns, ast.NameConstant):
            rets = node.returns.value
        else:
            rets = None

        self._root['args'] = args
        self._root['anns'] = anns
        self._root['defs'] = defs
        self._root['rets'] = rets
        self._root['line'] = node.lineno
        self._root['docs'] = ast.get_docstring(node, clean=True) or ''
        for item in node.decorator_list:
            if item.id == 'property':
                self._root['prop'] = True

    def generic_visit(self, node):
        print(f"B> Unhandled node: {node}")


class ClassVisitor(ast.NodeVisitor):

    def __init__(self, root):
        self._root = root
        super().__init__()

    def visit_Module(self, node):
        super().generic_visit(node)

    def parse_value(self, val):
        if isinstance(val, ast.Str):
            return val.s
        elif isinstance(val, ast.NameConstant):
            return val.value
        elif isinstance(val, ast.Num):
            return val.n
        elif isinstance(val, ast.Bytes):
            return val.s

        print("Unknown type: ", type(val))
        return None

    def visit_ClassDef(self, node):
        log.error(f"BASES: {node.bases} node: {node.name} line: {node.lineno}")
        self._root[node.name] = {
            'base': [base.id for base in node.bases],
            'name': node.name,
            'defs': {},
            'docs': ast.get_docstring(node, clean=True) or '',
            'cdef': {},
            'line': node.lineno
        }
        root = self._root[node.name]
        for method_node in ast.iter_child_nodes(node):
            if isinstance(method_node, ast.FunctionDef):
                root['defs'][method_node.name] = {}
                MethodVisitor(root['defs'][method_node.name]).visit(method_node)
            elif isinstance(method_node, ast.Name):
                pass
            elif isinstance(method_node, ast.Pass):
                pass
            elif isinstance(method_node, ast.Assign):
                if isinstance(method_node.value, ast.Dict):
                    cdef = {}
                    while len(method_node.value.keys):
                        key = method_node.value.keys.pop(0)
                        val = method_node.value.values.pop(0)
                        if isinstance(val, ast.NameConstant):
                            cdef[key.s] = val.value
                        elif isinstance(val, ast.Num):
                            cdef[key.s] = val.n
                        else:
                            print(dir(val))
                            cdef[key.s] = val
                    root['cdef'][method_node.targets[0].id] = cdef
                elif isinstance(method_node.value, ast.List):
                    root['cdef'][method_node.targets[0].id] = "[...]"
                elif type(method_node.value) in [ast.Str, ast.NameConstant, ast.Num, ast.Bytes]:
                    root['cdef'][method_node.targets[0].id] = self.parse_value(method_node.value)
                elif type(method_node.value) in [ast.Constant]:
                    root['cdef'][method_node.targets[0].id] = method_node.value.value
                else:
                    print(f'1.Not handled: {method_node.value} => {type(method_node.value)}')
                    print(f"{node.name} !!!!!>", method_node, type(method_node.value))
            else:
                if isinstance(method_node, ast.AsyncFunctionDef):
                    print(method_node)
                elif isinstance(method_node.value, ast.Str):
                    pass
                else:
                    print(f'2.Not handled: {type(method_node)} {method_node.value} {method_node.lineno}')
                    print(node.name, dir(method_node))
                    if isinstance(method_node.value, ast.Str):
                        print(dir(method_node.value))
                        print('<<<', method_node.value.s, '>>>')

    def visit_ImportFrom(self, node):
        pass


class Documentation:

    BASE_URL = 'https://gitlab.com/oddjobz/pynndb2/-/blob/master/pynndb'
    EXAMPLE_URL = 'https://gitlab.com/oddjobz/pynndb2-examples/-/blob/master'

    def present(self):
        css_module = '<div class="moduledef">'
        css_module_doc = '<div class="moduledoc">'
        css_module_doc_end = '</div>'
        css_module_end = '</div>'
        css_class_end = '</div>'
        css_klass = '<span class="klass">'
        css_klass_end = '</span>'
        keyword = '<span class="keyword">'
        keyword_end = '</span>'
        docstring = '<div class="docstring">'
        docstring_end = '</div>'
        methodslabel = '<div class="methodslabeldiv"><span class="methodslabel">'
        methodslabel_end = '</span></div>'
        method = '<span class="method">'
        method_end = '</span>'
        css_function_end = '</div>'
        paramslabel = '<div class="paramslabeldiv"><span class="paramslabel">'
        paramslabel_end = '</span></div>'
        params = '<ul class="params">'
        params_end = '</ul>'
        param = '<span class="param">'
        param_end = '</span>'
        typ = '<span class="type">'
        typ_end = '</span>'
        css_arg = '<span class="var">'
        css_arg_end = '</span>'
        css_return = '<span class="return">'
        css_return_end = '</span>'
        css_default = '<span class="defaultvalue">'
        css_default_end = '</span>'
        css_literal = '<span class="literal">'
        css_literal_end = '</span>'

        def function_href(k, f):
            f = f.replace("_", "")
            return f'<div class="function" id="item-{k}-{f}">'

        def class_href(k):
            return f'<div class="classdef" id="section-{k}">'

        def format_docstringmod(text):
            lines = text.split('\n')
            section1 = ''
            section2 = ''

            while len(lines):
                line = lines.pop(0)
                if not len(line):
                    break
                section1 += line + '\n'
            while len(lines):
                line = lines.pop(0)
                section2 += line

            return f'{css_module_doc}{section1}\n<div>{section2}</div>{css_module_doc_end}'

        def format_docstring(text):
            result = ''
            lines = text.split('\n')
            out = ''
            while len(lines):
                line = lines.pop(0)
                if not len(line):
                    result += out + '\n'
                    out = ''
                elif line == '---':
                    result += out + '\n'
                    out = ''
                    while len(lines):
                        line = lines.pop(0)
                        if line == '---':
                            out += '\n'
                            break
                        else:
                            out += f'{line}\n'
                elif line == '```':
                    result += out
                    out = ''
                    while len(lines):
                        line = lines.pop(0)
                        if line == '```':
                            break
                        out += f'{line}\n'
                    out = f'<div class="docs-code-block"><pre class="shadow-lg rounded"><code class="python hljs">{out}</code></pre></div>'
                elif line[:2] in ['  ', 'o ', '- ', '* ']:
                    result += '\n' + line.replace('* ', '📌 ')
                    out = ''
                else:
                    out += line + ' '
            result += '\n' + out
            return f'{docstring}{result.strip()}{docstring_end}'

        def parse_tuple(text):
            items = ''
            for item in text:
                if len(items):
                    items += ' | '
                items += (item.id if isinstance(item, ast.Name) else item)
            return items

        def parse_ann(text):
            if text is None or isinstance(text, str):
                return text
            elif isinstance(text, ast.Subscript):
                if text.value.id == 'Union':
                    slice = text.slice.value
                    if isinstance(slice, ast.Tuple):
                        return parse_tuple(slice.elts)
                    else:
                        print(f'Unknown slice: {slice}')
                elif text.value.id == 'Callable':
                    if isinstance(text.slice.value, ast.Tuple):
                        t = []
                        for i in text.slice.value.elts:
                            if isinstance(i, ast.List):
                                qq = []
                                for lst in i.elts:
                                    qq.append(lst.id)
                                t.append(qq)
                            elif isinstance(i, ast.Name):
                                t.append(i.id)
                        return 'Callable' + str(t).replace("'", '')
                    else:
                        print("Not Handled: ", text.slice.value, dir(text.slice.value))
                else:
                    print(f'Unknown subscript: {text.value.id}')
            elif isinstance(text, tuple):
                if text[0] == 'Optional':
                    return parse_tuple(text[1])
                elif text[0] == 'Union':
                    return parse_tuple(text[1])
                else:
                    print("Don't know how to handle: ", text, type(text))
            else:
                print(type(text))
                return '???'

        def function_definition(module, klass, name):
            fn = klass['defs'][name]
            # base = self.BASE_URL if self._name == 'pynndb' else f'{self.EXAMPLE_URL}/{self._name}'
            # url = f'{base}/{module_name}.py#L{fn.get("line")}'
            url = 'need a module url'
            s = f'<a href="{url}" target="_blank">{method}{name}{method_end} </a>'

            docs = fn.get('docs')
            anns = fn.get('anns')
            args = fn.get('args')
            defs = fn.get('defs')
            line = fn.get('line')

            text = ''
            look = {}
            newa = []
            for arg in args:
                look[arg] = {'ann': anns.pop(0), 'def': defs.pop(0)}
                a = look[arg]['def']
                if isinstance(a, str):
                    arg = f'[{css_arg}{arg}{css_arg_end}]'
                else:
                    arg = f'{css_arg}{arg}{css_arg_end}'
                newa.append(arg)

            s += f'({", ".join(newa)}) -> {css_return}{fn.get("rets")}{css_return_end}'
            p = ''
            pcount = 0
            p += f'{params}'
            for line in docs.split("\n"):
                parts = line.split(" ")
                if len(parts) > 1 and parts[1] == '-':
                    pcount += 1
                    ann = parse_ann(look.get(parts[0], {}).get("ann"))
                    val = look.get(parts[0], {}).get("def")
                    p += f'<li>'
                    p += f'{param}{parts[0]}{param_end} '
                    if isinstance(val, str):
                        p += f'[{typ}{ann}{typ_end} / default={css_default}{val}{css_default_end}] - '
                    else:
                        p += f'[{typ}{ann}{typ_end}] - '

                    p += ' '.join(parts[2:])
                    p += '</li>\n'
                else:
                    if len(line):
                        text += line + '\n'
            p += f'{params_end}'
            s += format_docstring(text)
            if pcount:
                s += f'{paramslabel}PARAMETERS{paramslabel_end}{p}'
            else:
                s += f'{params}{params_end}'
            return s

        def module_definition(module):
            # module = self._modules.get(module_name)
            docs = module.get('__doc__') if '__doc__' in module else None
            # if not module:
            #     print(f'Module not found: {module_name}')
            #     return ''
            s = f'{format_docstringmod(docs)}' if docs else ''
            for klass_name in module.keys():
                if klass_name in ['__doc__']:
                    continue
                klass = module[klass_name]
                # base = self.BASE_URL if self._name == 'pynndb' else f'{self.EXAMPLE_URL}/{self._name}'
                # url = f'{base}/{module_name}.py#L{klass.get("line")}'
                url = 'need url'

                # sidebar.write(f'<li class="nav-item section-title mt-3">\n')
                # sidebar.write(f' <a class="nav-link scrollto" href="#section-{klass_name}">\n')
                # sidebar.write(f'{CLASS_ICON}{klass_name}')
                # sidebar.write(f' </a></li>\n')

                s += f'{class_href(klass_name)}\n'
                s += f'{keyword}class{keyword_end} <a href="{url}" target="_blank">{css_klass}{klass_name}{css_klass_end}</a>\n'
                if klass.get('base'):
                    params = ", ".join([f"{css_arg}{base}{css_arg_end}\n" for base in klass["base"]])
                    s += f'({params})'
                    s += ':'
                s += format_docstring(klass.get("docs"))

                # sidebar.write(f'<ul class="section-items list-unstyled nav flex-column pb3">')
                if 'cdef' in klass:
                    cdef = klass.get('cdef')
                    if len(cdef):
                        s += f'{methodslabel}CLASS PROPERTIES{methodslabel_end}\n'
                        for item in sorted(cdef):
                            href = f'#item-{klass_name}-{item}'
                            # sidebar.write(f'<li class="nav-item"><a class="nav-link scrollto" href="{href}">{item}</a></li>')
                            s += f'<div class="cdef" id="item-{klass_name}-{item}">{method}{item}{method_end} =\n'
                            if isinstance(cdef[item], dict):
                                s += f'<pre>{dumps(cdef[item], indent=4)}'
                            else:
                                s += f'"{css_literal}{cdef[item]}{css_literal_end}"'
                            s += f'</div>'

                if klass.get('defs'):
                    p = f'{methodslabel}PROPERTIES{methodslabel_end}\n'
                    found = False
                    for fn in sorted(klass['defs']):
                        if klass['defs'][fn].get('prop'):
                            found = True
                            href = f'item-{klass_name}-{fn.replace("_", "")}'

                            line = klass['defs'][fn].get('line')

                            self.addIndex('property', href, fn, line)
                            # sidebar.write(f'<li class="nav-item"><a class="nav-link scrollto" href="{href}">{fn}</a></li>')
                            p += f'{function_href(klass_name, fn)}{function_definition(self._module, klass, fn)}{css_function_end}\n'
                    if found:
                        s += p

                if klass.get('defs'):
                    m = f'{methodslabel}METHODS{methodslabel_end}\n'
                    found = False
                    for fn in sorted(klass['defs']):
                        if not klass['defs'][fn].get('prop'):
                            found = True
                            href = f'item-{klass_name}-{fn.replace("_", "")}'

                            line = klass['defs'][fn].get('line')

                            self.addIndex('method', href, fn, line)
                            # sidebar.write(f'<li class="nav-item"><a class="nav-link scrollto" href="{href}">{fn}</a></li>')
                            m += f'{function_href(klass_name, fn)}{function_definition(self._module, klass, fn)}{css_function_end}\n'
                    s += m

                s += f'{css_class_end}\n'
                # sidebar.write(f'</ul>')
            return s

        return f'{css_module}{module_definition(self._module)}{css_module_end}'

    def addIndex (self, typ, href, fn, ln):
        node = {
            'parent': self._key,
            'type': typ,
            'label': fn,
            'isLeaf': True,
            'line': ln,
            '_id': href,
        }
        self._index.append(node)

    def __init__(self):
        self._module = {}
        self._index = []
        self._key = None

    def run(self, key, text):
        self._key = key
        tree = ast.parse(text)
        self._module['__doc__'] = ast.get_docstring(tree)
        ClassVisitor(self._module).visit(tree)
        return self._index, self.present()


if __name__ == '__main__':
    with open('test1.py') as io:
        text = io.read()
    print(Documentation().run(text))

