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

    # Her peer kendi local toplamını hesaplar
    local_age_sum = sum(d["age"] for d in data)

    print(f"[{mpc.pid}] local age sum:", local_age_sum, flush=True)

    # Her party kendi local toplamını secret input olarak verir
    secret_local_sum = secint(local_age_sum)

    shared_sums = mpc.input(
        secret_local_sum,
        senders=list(range(len(mpc.parties)))
    )

    total = mpc.sum(shared_sums)

    result = await mpc.output(total)

    if mpc.pid == 0:
        print("\n=== SONUÇ ===", flush=True)
        print("Toplam age:", result, flush=True)

    await mpc.shutdown()

mpc.run(main())