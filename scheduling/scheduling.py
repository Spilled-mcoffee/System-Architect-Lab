from collections import deque

# ------------------ PROCESS CLASS ------------------
class Process:
    def __init__(self, pid, arrival, burst):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.remaining = burst
        self.completion = 0


# ------------------ ROUND ROBIN ------------------
def round_robin(processes, quantum):
    time = 0
    queue = deque()
    gantt = []
    completed = []

    processes.sort(key=lambda p: p.arrival)
    i = 0

    while queue or i < len(processes):

        while i < len(processes) and processes[i].arrival <= time:
            queue.append(processes[i])
            i += 1

        if not queue:
            time += 1
            continue

        current = queue.popleft()
        start_time = time
        execution_time = min(quantum, current.remaining)

        time += execution_time
        current.remaining -= execution_time

        gantt.append((current.pid, start_time, time))

        while i < len(processes) and processes[i].arrival <= time:
            queue.append(processes[i])
            i += 1

        if current.remaining > 0:
            queue.append(current)
        else:
            current.completion = time
            completed.append(current)

    return gantt, completed


# ------------------ SRTF ------------------
def srtf(processes):
    time = 0
    gantt = []
    completed = []
    n = len(processes)
    finished = 0

    while finished < n:
        available = [p for p in processes if p.arrival <= time and p.remaining > 0]

        if not available:
            time += 1
            continue

        current = min(available, key=lambda p: p.remaining)

        start_time = time
        time += 1
        current.remaining -= 1

        gantt.append((current.pid, start_time, time))

        if current.remaining == 0:
            current.completion = time
            completed.append(current)
            finished += 1

    return gantt, completed


# ------------------ GANTT UTILITIES ------------------
def compress_gantt(gantt):
    compressed = []

    for p in gantt:
        if not compressed or compressed[-1][0] != p[0]:
            compressed.append([p[0], p[1], p[2]])
        else:
            compressed[-1][2] = p[2]

    return compressed


def print_gantt(gantt):
    print("\nGantt Chart:\n")

    # Process blocks
    for p in gantt:
        print(f"| {p[0]} ", end="")
    print("|")

    # Time line
    print(gantt[0][1], end="")
    for p in gantt:
        print(f"   {p[2]}", end="")
    print("\n")


# ------------------ METRICS ------------------
def calculate_metrics(processes):
    total_waiting = 0

    print("\nProcess Metrics:")
    for p in processes:
        turnaround = p.completion - p.arrival
        waiting = turnaround - p.burst
        total_waiting += waiting

        print(f"{p.pid}: Waiting = {waiting}, Turnaround = {turnaround}")

    avg_waiting = total_waiting / len(processes)
    print(f"\nAverage Waiting Time = {avg_waiting:.2f}")

    return avg_waiting


# ------------------ ANALYSIS ------------------
def compare_algorithms(avg_rr, avg_srtf):
    print("\n=== ANALYTICAL COMPARISON ===\n")

    print(f"Round Robin Average Waiting Time: {avg_rr:.2f}")
    print(f"SRTF Average Waiting Time: {avg_srtf:.2f}\n")

    if avg_srtf < avg_rr:
        print("→ SRTF is more efficient in minimizing waiting time.")
    else:
        print("→ Round Robin performed better in this case.")

    print("\nInterpretation:")
    print("- SRTF dynamically selects the shortest remaining job, reducing idle wait.")
    print("- However, it may cause starvation for longer processes.")
    print("- Round Robin ensures fairness but increases waiting time due to context switching.")
    print("- The choice depends on system goals: efficiency vs fairness.\n")


# ------------------ MAIN ------------------
def main():

    # Separate copies (VERY IMPORTANT)
    processes_rr = [
        Process("P1", 0, 7),
        Process("P2", 2, 4),
        Process("P3", 4, 1),
        Process("P4", 5, 4),
    ]

    processes_srtf = [
        Process("P1", 0, 7),
        Process("P2", 2, 4),
        Process("P3", 4, 1),
        Process("P4", 5, 4),
    ]

    print("comparing Round Robin and SRTF scheduling algorithms with the same set of processes:\n")
    print("""
process       |AT 	| Burst
---------------------------
P1 	      |0    	| 7
P2 	      |2    	| 4
P3 	      |4    	| 1
P4 	      |5    	| 4\n""")
    # ------------------ ROUND ROBIN ------------------
    print("=== ROUND ROBIN (q = 2) ===")
    gantt_rr, completed_rr = round_robin(processes_rr, quantum=2)

    gantt_rr = compress_gantt(gantt_rr)
    print_gantt(gantt_rr)

    avg_rr = calculate_metrics(completed_rr)

    # ------------------ SRTF ------------------
    print("\n=== SRTF ===")
    gantt_srtf, completed_srtf = srtf(processes_srtf)

    gantt_srtf = compress_gantt(gantt_srtf)
    print_gantt(gantt_srtf)

    avg_srtf = calculate_metrics(completed_srtf)

    # ------------------ COMPARISON ------------------
    compare_algorithms(avg_rr, avg_srtf)


if __name__ == "__main__":
    main()