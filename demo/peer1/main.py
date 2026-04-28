from mpyc.runtime import mpc
import csv

async def main():

    await mpc.start()

    print(f"[{mpc.pid}] başladı")

    # her peer kendi local CSV'sini okur
    data = []
    with open("dataset.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                "age": int(row["age"]),
                "income": int(row["income"]),
                "score": int(row["score"]),
            })

    print(f"[{mpc.pid}] local data:", data)

    secint = mpc.SecInt() # 32 64

    # sadece age kolonunu al (örnek)
    local_ages = [secint(d["age"]) for d in data]

    # HER SATIR için input ver
    all_shared = []

    for age in local_ages:
        shared = mpc.input(age)
        all_shared.append(shared)

    # flatten (çok önemli)
    flat = []
    for s in all_shared:
        flat.extend(s)

    # toplam hesapla
    total = mpc.sum(flat)

    result = await mpc.output(total)

    if mpc.pid == 0:
        print("\n=== SONUÇ ===")
        print("Toplam age:", result)

    await mpc.shutdown()

mpc.run(main())