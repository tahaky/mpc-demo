from mpyc.runtime import mpc
import csv

async def main():
    await mpc.start()

    print(f"[{mpc.pid}] başladı", flush=True)

    data = []
    with open("dataset.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                "age": int(row["age"]),
                "income": int(row["income"]),
                "score": int(row["score"]),
            })

    print(f"[{mpc.pid}] local data:", data, flush=True)

    secint = mpc.SecInt()

    local_age_sum = sum(d["age"] for d in data)

    print(f"[{mpc.pid}] local age sum:", local_age_sum, flush=True)

    secret_local_sum = secint(local_age_sum)


    shared_sums = []

    for sender in range(len(mpc.parties)):
        print(f"[{mpc.pid}] input sender={sender} öncesi", flush=True)

        if mpc.pid == sender:
            x = secret_local_sum
        else:
            x = None

    shared = mpc.input(x, senders=sender)
    shared_sums.append(shared)

    print(f"[{mpc.pid}] input sender={sender} sonrası", flush=True)

    total = mpc.sum(shared_sums)

    print(f"[{mpc.pid}] output öncesi", flush=True)

    result = await mpc.output(total)

    print(f"[{mpc.pid}] output sonrası result={result}", flush=True)

    if mpc.pid == 0:
        print("\n=== SONUÇ ===", flush=True)
        print("Toplam age:", result, flush=True)

    await mpc.shutdown()

mpc.run(main())