import re


def is_line_correct(line):
    return bool(re.match('^(\[.*\])+[^\[\]]+(\[.*\])+$', line))


def input_graph(content):
    graph = {}
    rules = []
    get_params = re.compile('\[([^\[\]]*)\]')
    for line in content:
        if not is_line_correct(line):
            graph = None
            rules = None
            break
        params, func, results = re.split('(?<=\])([^\[\]]+)', line, maxsplit=1)
        params = get_params.findall(params)
        results = get_params.findall(results)
        rules.append((params, func, results))
        for param in params:
            for result in results:
                graph.setdefault(param, {})[result] = func
    return (graph, rules)


def top_sort(graph):
    def dfs(v):
        if color.get(v, 2) == 0 or cycled[0]:
            return
        if color.get(v, 2) == 1:
            cycled[0] = True
            return
        color[v] = 1
        for nx in graph.get(v, {}):
            dfs(nx)
        sorted_ver.append(v)
        color[v] = 0
    color = {}
    cycled = [False]
    sorted_ver = []
    for v in graph:
        dfs(v)
    return None if cycled[0] else list(reversed(sorted_ver))


def param_to_key(param, indexes):
    return list(reversed(sorted(map(lambda x: indexes[x], param))))


def refactor_answer(ans):
    def refactor_params(params):
        return ''.join(map(lambda p: '[' + str(p) + ']', params))
    refactored_ans = []
    for rule in ans:
        refactored_ans.append(refactor_params(rule[0]) +
                              rule[1] +
                              refactor_params(rule[2]))
    return refactored_ans

def main(input):
    with open(input) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    graph, rules = input_graph(content)
    if not graph:
        return('Incorect input')
    sorted_ver = top_sort(graph)
    if not sorted_ver:
        return("Cycle was found")
    indexes = {}
    for index, i in enumerate(sorted_ver):
        indexes[i] = index
    ans = sorted(rules, key=lambda rule: (param_to_key(rule[0], indexes),
                                          param_to_key(rule[2], indexes),
                                          rule[1]))
    return ('\n'.join(refactor_answer(ans)))

#print(main("input"))
