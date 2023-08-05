import multiprocessing as mp
import math


def bypass(file, processes=mp.cpu_count(), executor=exec, gilb_global='gilb:global', gilb_chunk='gilb:chunk', gilb_header='gilb:header', gilb_footer='gilb:footer'):
    with open(file, 'r') as f:
        lines = f.readlines()

    lines = [line for line in lines if (not line.strip().startswith('#') or
                                        line.strip().lower().endswith(gilb_chunk) or
                                        line.strip().lower().endswith(gilb_global) or
                                        line.strip().lower().endswith(gilb_header) or
                                        line.strip().lower().endswith(gilb_footer)) and line.strip() != '']

    global_chunks = []
    global_chunk = []

    header_chunks = []
    header_chunk = []

    footer_chunks = []
    footer_chunk = []

    chunks = []
    chunk = []

    global_mid = False
    header_mid = False
    footer_mid = False

    for line in lines:
        if line.strip().startswith('#') and line.strip().lower().endswith(gilb_chunk):
            chunks.append(chunk)
            chunk = []

        elif line.strip().startswith('#') and line.strip().lower().endswith(gilb_global):
            global_mid = not global_mid
            if not global_mid:
                global_chunks.append(global_chunk)
                global_chunk = []

        elif line.strip().startswith('#') and line.strip().lower().endswith(gilb_header):
            header_mid = not header_mid
            if not header_mid:
                header_chunks.append(header_chunk)
                header_chunk = []

        elif line.strip().startswith('#') and line.strip().lower().endswith(gilb_footer):
            footer_mid = not footer_mid
            if not footer_mid:
                footer_chunks.append(footer_chunk)
                footer_chunk = []

        else:
            if global_mid:
                global_chunk.append(line)
            elif header_mid:
                header_chunk.append(line)
            elif footer_mid:
                footer_chunk.append(line)
            else:
                chunk.append(line)

    del global_chunk
    del global_mid

    del header_chunk
    del header_mid

    del footer_chunk
    del footer_mid

    chunks.append(chunk)
    del chunk

    if len(chunks) < processes:
        processes = len(chunks)

    chunks_per_process = math.ceil(len(chunks) / processes)

    g = ""
    for global_chunk in global_chunks:
        g += "".join(global_chunk)

    h = ""
    for header_chunk in header_chunks:
        h += "".join(header_chunk)

    f = ""
    for footer_chunk in footer_chunks:
        f += "".join(footer_chunk)

    raw = "def f{}():\n" \
          "    {}\n    {}\n\n"

    p = []
    for i in range(processes):
        sliced_chunks = chunks[:chunks_per_process]
        chunks = chunks[chunks_per_process:]
        text = h
        for j, chunk in enumerate(sliced_chunks):
            text += raw.format(j, g, "    ".join(chunk))

        for j in range(len(sliced_chunks)):
            text += f"f{j}()\n"

        text += f

        p.append(mp.Process(target=executor, args=(text,)))
        p[-1].start()

    for process in p:
        process.join()
