import functools
import textwrap
from snipper.legacy import block_process
from snipper.block_parsing import full_strip
import os
if os.name == 'nt':
    import wexpect as we
else:
    import pexpect as we


def rsession(analyzer, lines, extra):
    l2 = []
    dbug = False
    # analyzer = we.spawn("python", encoding="utf-8", timeout=20)
    # analyzer.expect([">>>"])
    if "You can group" in "\n".join(lines): # in "\n".join(lines):
        print("\n".join(lines))
        print("-"*50)
        for k in extra['session_results']:
            print(k['input'])
            print(k['output'])

        import time
        an = we.spawn("python", encoding="utf-8", timeout=20)
        an.setwinsize(400, 400) # set window size to avoid truncated output or input.
        an.expect([">>>"])
        l3 = """
2 + 4 # Add two integers
50 - 5 * 6
(2 + 2) * (3 - 1) # You can group operations using parenthesis
width = 20 # Assign the variable 'width' to a value of 20
height = 5*9 # And also height is assigned the value of 5 * 9 = 45
area = 2*3 # Compute the area of a rectangle and assign it to area now the text will be longer is that an issue
area # This line shows us the value of 'area' #!i=b
"""
        lines2 = l3.strip().splitlines()
        from collections import defaultdict
        dd = defaultdict(list)

        for l in lines2:
            dd['code'].append(l)
            an.sendline(l.rstrip())
            an.expect_exact([">>>", "..."])
            dd["output"].append(an.before.strip())
            # print(">>>", an.before.strip())
            if len(an.after.strip()) > 4:
                print(">>>>>>>>>>>>> That was a long after?")
            # analyzer.be

        print('*' * 50)
        # analyzer = an
        dbug = True
        import tabulate
        print(tabulate.tabulate(dd, headers='keys'))

    lines = "\n".join(lines).replace("\r", "").splitlines()

    for i, l in enumerate(lines):
        l2.append(l)
        if l.startswith(" ") and i < len(lines)-1 and not lines[i+1].startswith(" "):
            if not lines[i+1].strip().startswith("else:") and not lines[i+1].strip().startswith("elif") :
                l2.append("") # Empty line instead?

    lines = l2
    alines = []
    in_dot_mode = False
    if len(lines[-1]) > 0 and (lines[-1].startswith(" ") or lines[-1].startswith("\t")):
        lines += [""]


    for i, word in enumerate(lines):
        if dbug:
            print("> Sending...", word)
        analyzer.sendline(word.rstrip())
        import time
        before = ""
        while True:
            time.sleep(0.05)
            analyzer.expect_exact([">>>", "..."])
            # if dbug and "total_cost" in word:
            #     aaa = 23234
            before += analyzer.before
            # if dbug:
            # print(">  analyzer.before...", analyzer.before.strip(), "...AFTER...", analyzer.after.strip())
            # AFTER =
            if analyzer.before.endswith("\n"):
                # print("> BREAKING LOOP")
                break
            else:
                before += analyzer.after
            break


        # print("Before is", before)
        abefore = analyzer.before.rstrip()
        # Sanitize by removing garbage binary stuff the terminal puts in
        abefore = "\n".join([l for l in abefore.splitlines() if not l.startswith('\x1b')] )


        dotmode = analyzer.after == "..."
        if 'dir(s)' in word:
            pass
        if 'help(s.find)' in word:
            pass
        if dotmode:
            alines.append(">>>" +abefore.rstrip() if not in_dot_mode else "..." + abefore.rstrip())
            in_dot_mode = True
        else:
            alines.append( ("..." if in_dot_mode else ">>>") + abefore.rstrip())
            in_dot_mode = False
    if dbug:
        print("-"*50)
        print("\n".join(alines))
    extra['session_results'].append({'input': '\n'.join(lines), 'output': '\n'.join(alines)})
    return alines


def run_i(lines, file, output):
    if 'python0A' in str(file):
        print(234)
    extra = dict(python=None, output=output, evaluated_lines=0, session_results=[])
    def block_fun(lines, start_extra, end_extra, art, head="", tail="", output=None, extra=None):
        outf = output + ("_" + art if art is not None and len(art) > 0 else "") + ".shell"
        lines = full_strip(lines)
        s = "\n".join(lines)
        s.replace("...", "..") # passive-aggressively truncate ... because of #issues.
        lines = textwrap.dedent(s).strip().splitlines()
        # an.setecho(True) # TH January 2023: Seems to fix an issue on linux with truncated lines. May cause problems on windows?

        if extra['python'] is None:
            an = we.spawn("python", encoding="utf-8", timeout=20)
            an.setwinsize(400, 400)  # set window size to avoid truncated output or input.
            an.expect([">>>"])
            extra['python'] = an

        # analyzer = extra['python']
        # What does this do?
        # for l in (head[extra['evaluated_lines']:] + ["\n"]):
        #     analyzer.sendline(l)
        #     analyzer.expect_exact([">>>", "..."])
        alines = rsession(extra['python'], lines, extra) # give it the analyzer
        extra['evaluated_lines'] += len(head) + len(lines)
        lines = alines
        return lines, [outf, lines]
    try:
        a,b,c,_ = block_process(lines, tag="#!i", block_fun=functools.partial(block_fun, output=output, extra=extra))
        if extra['python'] is not None:
            extra['python'].close()

        if len(c)>0:
            kvs= { v[0] for v in c}
            for outf in kvs:
                out = "\n".join( ["\n".join(v[1]) for v in c if v[0] == outf] )
                out = out.replace("\r", "")
                # if outf.endswith("python0B_e4.shell"):
                #     print(outf)

                with open(outf, 'w') as f:
                    f.write(out)

    except Exception as e:
        print("lines are")
        print("\n".join(lines))
        print("Bad thing in #!i command in file", file)
        raise e
    return lines