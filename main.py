from collections import deque
import time

def kahn_topological_sort(graph):
    indegree={v:0 for v in graph}
    for u in graph:
        for v in graph[u]: indegree[v]+=1
    queue=deque(v for v in graph if indegree[v]==0); order=[]
    while queue:
        u=queue.popleft(); order.append(u)
        for v in graph[u]:
            indegree[v]-=1
            if indegree[v]==0: queue.append(v)
    return order if len(order)==len(graph) else None

def dfs_topological_sort(graph):
    visited=set(); active=set(); order=[]
    def visit(v):
        if v in active: return False
        if v in visited: return True
        active.add(v)
        for n in graph[v]:
            if not visit(n): return False
        active.remove(v); visited.add(v); order.append(v); return True
    for v in graph:
        if not visit(v): return None
    return list(reversed(order))

def demo_graph():
    prereq={'Testing':['Coding'],'Coding':['Design'],'Design':['Planning'],'Planning':[],'Documentation':['Planning']}
    graph={t:[] for t in prereq}
    for task,deps in prereq.items():
        for dep in deps: graph[dep].append(task)
    return prereq,graph

def custom_graph():
    tasks=[t.strip() for t in input('Enter task names separated by commas: ').split(',') if t.strip()]
    prereq={t:[] for t in tasks}
    for task in tasks:
        deps=[d.strip() for d in input(f'Prerequisites for {task} (comma-separated, blank if none): ').split(',') if d.strip()]
        for d in deps:
            if d not in prereq: print(f'Unknown task {d!r}; skipped.')
            elif d==task: print('Self dependency skipped.')
            else: prereq[task].append(d)
    graph={t:[] for t in tasks}
    for task,deps in prereq.items():
        for dep in deps: graph[dep].append(task)
    return prereq,graph

def main():
    print('\n=== SMART DEPENDENCY & PROJECT EXECUTION MANAGER ===\n1. Sample project  2. Enter your own project  3. Exit')
    choice=input('Choose: ').strip()
    if choice=='3': return
    if choice=='1': prereq,graph=demo_graph()
    elif choice=='2': prereq,graph=custom_graph()
    else: print('Invalid option.'); return
    print('\nTasks and prerequisites:')
    for t,deps in prereq.items(): print(f'{t}: {", ".join(deps) if deps else "None"}')
    s=time.perf_counter(); bfs=kahn_topological_sort(graph); tb=time.perf_counter()-s
    s=time.perf_counter(); dfs=dfs_topological_sort(graph); td=time.perf_counter()-s
    print('\n--- RESULTS ---')
    print('Kahn BFS:', 'Cycle detected; no valid order.' if bfs is None else ' -> '.join(bfs), f'(time: {tb:.8f}s)')
    print('DFS:', 'Cycle detected; no valid order.' if dfs is None else ' -> '.join(dfs), f'(time: {td:.8f}s)')
if __name__=='__main__': main()
