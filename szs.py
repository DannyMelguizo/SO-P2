
open("archive.BYTES", "w").close()

with open("archive.BYTES", "ab") as f:
    for i in range(0, 100):
        num = i.to_bytes(1, 'big')
        print(f"{i} - {num}")
        f.write(num+b'\n')



with open("archive.BYTES", "rb") as f:

    file = f.readlines()

    for i in file:
        print(i)
