from collections import defaultdict
import os
from snipper.block_parsing import block_iterate
from snipper.snipper_main import full_strip
from snipper.block_parsing import indent


def get_s(lines):
    """ Return snips from 'lines' """
    blocks = defaultdict(list)
    for c in block_iterate(lines, "#!s"):
        # c['start_tag_args']
        if not c['start_tag_args'].get('keeptags', False):
            c['block'] = full_strip(c['block'])
        else:
            # In this case the #! tags are kept in.
            pass
        if 'dse' in c['start_tag_args']:
            print("asdfasdfs")
        # print(c['start_tag_args'])
        if 'nodoc' in c['start_tag_args'] and c['start_tag_args']['nodoc']:
            c['block'] = rm_docstring(c['block'])
            print("No documentation!")
        blocks[c['name']].append(c)

    output = {}
    for name, co in blocks.items():
        slines = [l for c in co for l in c['block']]
        # full_strip("")
        # c['block']['args']
        # slines = slines[ 23]
        # co.



        # if slines[f.lineno].strip().startswith('"' * 3):
        #     print("got a docstrnig")
        #     for k in range(f.lineno, f.end_lineno + 1):
        #         l = slines[k] if k != f.lineno else slines[k].strip()[3:]
        #         if l.find('"' * 3) >= 0:
        #             break
        # else:
        #     k = -1
        # if k > 0:
        #     print("Docstring detected")
        #     for i in range(f.lineno, k + 1):
        #         ll2[i] = None
        output[name] = slines
    return output

def rm_docstring(lines):
    slines = lines
    slines = dedent(lines)
    source = "\n".join(slines)
    import ast
    node = ast.parse(source)
    classes = [n for n in node.body if isinstance(n, ast.ClassDef)]
    functions = [n for n in node.body if isinstance(n, ast.FunctionDef)]
    ll2 = slines.copy()

    def rm_ds(f, ll2):
        if slines[f.lineno].strip().startswith('"' * 3):
            # print("got a docstrnig")
            for k in range(f.lineno-1, f.end_lineno + 1):
                l = slines[k] if k != f.lineno else slines[k].strip()[3:]
                if l.find('"' * 3) >= 0:
                    break
        else:
            k = -1
        if k > 0:
            # print("Docstring detected")
            for i in range(f.lineno, k + 1):
                ll2[i] = None

    for f in functions:
        rm_ds(f, ll2)
    for c in classes:
        for f in c.body:
            rm_ds(f, ll2)
        rm_ds(c, ll2)
    nodoc = [l for l in ll2 if l is not None]
    # print("\n".join(nodoc))
    return nodoc


def dedent(lines):
    ll = lines
    id = [indent(l) for l in ll if len(l.strip()) > 0]
    id_len = [len(i) for i in id]
    mindex = id_len[id_len.index(min(id_len))]
    return [l[mindex:] for l in ll]


# def _s_block_process():
#
#     pass

def save_s(lines, output_dir, file_path): # save file snips to disk
    content = get_s(lines)
    # Only make output dir if needed.
    if len(content) > 0 and not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    for name, ll in content.items():
        if file_path is not None:
            file_path = file_path.replace("\\", "/")
            ll = [f"{indent(ll[0])}# {file_path}"] + ll

        out = "\n".join(ll)

        fname = output_dir + "/" + os.path.basename(file_path)[:-3] + ("_" + name if len(name) > 0 else name) + ".py"
        with open(fname, 'w') as f:
            f.write(out)

        # Dedent it for better plotting.
        fname_stripped = fname[:-3] + "_stripped.py"
        id = [indent(l) for l in ll if len(l.strip()) > 0]
        id_len = [len(i) for i in id]
        mindex = id_len[id_len.index(min(id_len))]
        out2 = "\n".join([l[mindex:] for l in ll])

        with open(fname_stripped, 'w') as f:
            f.write(out2)

s1 = """
L1
L2 #!s=a
L3 #!s=b
L4
L5 
L6 
L7 #!s=a
L8 
L9 #!s=b
went
"""
if __name__ == "__main__":
    # for c in block_iterate(s1.splitlines(), tag="#!s"):
    #     print(c['block'])
    output = get_s(s1.splitlines())
    for k, v in output.items():
        print("name:", k)
        print("\n".join(v))
        print("="*10)

