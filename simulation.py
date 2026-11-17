def heading(title):
    print("\n" + "=" * 68)
    print(title)
    print("=" * 68)


def pause():
    input("\nPress ENTER to continue...")


def get_free_blocks(bitmap):
    return [i for i, used in enumerate(bitmap) if not used]


def show_disk(bitmap):
    print("\nDISK MAP")
    for start in range(0, len(bitmap), 4):
        cells = []
        for i in range(start, min(start + 4, len(bitmap))):
            status = "USED" if bitmap[i] else "FREE"
            cells.append(f"[{i:02}: {status}]")
        print("  ".join(cells))

    print(f"\nFree blocks: {bitmap.count(False)}")
    print(f"Allocated blocks: {bitmap.count(True)}")


def show_bitmap(bitmap):
    print("\nBITMAP")
    print("Block:", " ".join(f"{i:02}" for i in range(len(bitmap))))
    print("Bit:  ", " ".join(str(int(value)) for value in bitmap))
    print("0 = Free | 1 = Allocated")


def find_free_run(bitmap, needed):
    for start in range(len(bitmap) - needed + 1):
        candidate = bitmap[start:start + needed]
        if len(candidate) == needed and all(not used for used in candidate):
            return list(range(start, start + needed))
    return None


def ask_number(prompt, minimum, maximum):
    while True:
        answer = input(prompt).strip()
        if answer.isdigit() and minimum <= int(answer) <= maximum:
            return int(answer)
        print(f"Please enter a whole number from {minimum} to {maximum}.")


def bitmap_demo(bitmap):
    heading("1. BITMAP: ALLOCATION AND RELEASE")

    print("Each disk block has one corresponding bit.")
    print("For this demonstration: 0 = FREE, 1 = ALLOCATED.")
    show_bitmap(bitmap)

    needed = ask_number(
        "\nCLASS CHALLENGE: How many consecutive blocks does the new file need? (1-4): ",
        1, 4
    )

    print(f"\nSearching for {needed} consecutive free blocks...")
    selected = find_free_run(bitmap, needed)

    if selected is None:
        print("No suitable consecutive free run was found.")
        print("The requested allocation cannot be made in this example.")
    else:
        print(f"Found consecutive free blocks: {selected}")
        for block in selected:
            bitmap[block] = True

        print("Allocation successful. Their bitmap bits change from 0 to 1.")
        show_bitmap(bitmap)
        show_disk(bitmap)

        print("\nNOW DEMONSTRATING RELEASE")
        print(f"The file is deleted, releasing blocks {selected}.")
        for released_block in selected:
            bitmap[released_block] = False
            print(
                f"Block {released_block} changes from "
                "1 (allocated) to 0 (free)."
            )
        show_bitmap(bitmap)
        show_disk(bitmap)

    print("\nTRADE-OFF")
    print("Bitmap: compact representation and easy status checking.")
    print("However, finding a long consecutive run may require scanning bits.")
    pause()


def linked_list_demo(bitmap):
    heading("2. LINKED FREE LIST: POINTER TRAVERSAL")

    free_blocks = get_free_blocks(bitmap)

    print("The head points to the first free block.")
    print("Each free block points to the next free block.\n")

    if not free_blocks:
        print("There are no free blocks.")
        pause()
        return

    print("HEAD")
    for index, block in enumerate(free_blocks):
        next_block = free_blocks[index + 1] if index + 1 < len(free_blocks) else "NULL"
        print(f"  |")
        print(f"  v")
        print(f"[Block {block}] ----> {next_block}")

    print("\nTRAVERSAL")
    for step, block in enumerate(free_blocks, start=1):
        print(f"Step {step}: follow the pointer and visit free block {block}")

    print(f"\nBlocks visited: {len(free_blocks)}")
    print("TRADE-OFF")
    print("A linked list can locate free blocks by following pointers.")
    print("But traversal can be slow, and finding consecutive blocks is difficult.")
    pause()


def grouping_demo(bitmap):
    heading("3. GROUPING: ADDRESSES STORED IN GROUPS")

    free_blocks = get_free_blocks(bitmap)
    group_size = 3

    groups = [
        free_blocks[i:i + group_size]
        for i in range(0, len(free_blocks), group_size)
    ]

    print("A group stores several free-block addresses.")
    print("Its final entry links to the next group.\n")

    for index, group in enumerate(groups):
        next_group = f"GROUP {index + 2}" if index + 1 < len(groups) else "NULL"

        print(f"+---------------- GROUP {index + 1} ----------------+")
        for address in group:
            print(f"| Free block address: {address:<19}|")
        print(f"| Next group pointer: {next_group:<19}|")
        print("+------------------------------------------+")
        if next_group != "NULL":
            print("                    |")
            print("                    v")

    print("\nTRADE-OFF")
    print("Grouping stores several free-block addresses together.")
    print("It can reduce the need to follow a separate pointer for every block.")
    print("However, the group entries and links must be maintained correctly.")
    pause()


def get_free_runs(bitmap):
    runs = []
    start = None
    count = 0

    for index, used in enumerate(bitmap + [True]):
        if not used:
            if start is None:
                start = index
            count += 1
        elif start is not None:
            runs.append((start, count))
            start = None
            count = 0

    return runs


def counting_demo(bitmap):
    heading("4. COUNTING: CONSECUTIVE FREE-BLOCK RECORDS")

    runs = get_free_runs(bitmap)

    print("Counting records a starting block and the number of")
    print("consecutive free blocks that follow it.\n")

    print("START BLOCK | COUNT | BLOCKS REPRESENTED")
    print("------------|-------|-------------------")

    for start, count in runs:
        represented = ", ".join(str(b) for b in range(start, start + count))
        print(f"{start:^11} | {count:^5} | {represented}")

    print("\nCLASS QUESTION")
    print("What does the record (20, 5) represent?")
    answer = input("Your answer: ").strip().lower()

    if "20" in answer and "24" in answer:
        print("Correct: blocks 20, 21, 22, 23 and 24.")
    else:
        print("Answer: blocks 20, 21, 22, 23 and 24.")

    print("\nTRADE-OFF")
    print("Counting is compact when free blocks occur in long consecutive runs.")
    print("It is less compact when free space is highly fragmented.")
    pause()


def free_space_comparison():
    heading("5. COMPARING FREE-SPACE MANAGEMENT METHODS")

    rows = [
        ("Bitmap", "One bit per block", "Compact; easy to inspect",
         "May scan many bits for a long run"),
        ("Linked list", "Pointers between free blocks", "Simple structure",
         "Traversal can be slow"),
        ("Grouping", "Several addresses stored per group", "Batch access",
         "Groups and links need maintenance"),
        ("Counting", "Start block plus run length", "Compact for long runs",
         "Less effective with fragmentation"),
    ]

    print(f"{'METHOD':<13} {'HOW IT STORES SPACE':<29} {'ADVANTAGE':<27} LIMITATION")
    print("-" * 110)
    for method, storage, advantage, limitation in rows:
        print(f"{method:<13} {storage:<29} {advantage:<27} {limitation}")

    print("\nCLASS QUESTION")
    print("Which method would be compact when free space occurs in long runs?")
    print("Expected answer: Counting.")
    pause()


def crash_challenge(bitmap):
    heading("6. SERVER CRASH: FIND THE INCONSISTENCY")

    # Deliberately create a teaching example:
    # file metadata references block 15, but the bitmap marks it free.
    bitmap[15] = False
    file_references = {15}

    print("SCENARIO")
    print("The university server loses power during a filesystem update.")
    print("A student's assignment metadata references block 15.")
    print("However, the free-space bitmap marks block 15 as FREE.")

    print("\nFILE METADATA:")
    print("  Student assignment -> Block 15 (in use)")

    print("\nBITMAP:")
    print("  Block 15 -> FREE (0)")

    print("\nCLASS CHALLENGE")
    print("What is the inconsistency?")
    print("A. A file references a block marked free.")
    print("B. A file references a block marked allocated.")
    print("C. The bitmap and file metadata agree.")

    answer = input("\nChoose A, B or C: ").strip().upper()

    if answer == "A":
        print("Correct. The file references a block marked as free.")
    else:
        print("The correct answer is A.")

    print("\nThis mismatch can cause the same block to be allocated again")
    print("while an existing file still references it.")
    pause()

    return file_references


def consistency_check(bitmap, file_references):
    heading("7. RECOVERY METHOD ONE: CONSISTENCY CHECKING")

    print("The checker compares file references with the free-space map.")
    print("\nChecking referenced blocks...")

    for block in sorted(file_references):
        if not bitmap[block]:
            print(f"INCONSISTENCY: Block {block} is referenced but marked FREE.")
            print(f"REPAIR: Marking block {block} as ALLOCATED.")
            bitmap[block] = True
        else:
            print(f"Block {block}: metadata and bitmap agree.")

    print("\nConsistency check finished.")
    show_bitmap(bitmap)

    print("\nTRADE-OFF")
    print("It can detect and repair structural inconsistencies.")
    print("A full check can take time, especially on large filesystems.")
    pause()


def journaling_demo(bitmap):
    heading("8. RECOVERY METHOD TWO: JOURNALING")

    free_blocks = get_free_blocks(bitmap)

    if len(free_blocks) < 2:
        print("Not enough free blocks for both journal examples.")
        pause()
        return

    committed_block = free_blocks[0]
    incomplete_block = free_blocks[1]

    print("Journaling records filesystem updates in a journal.")
    print("\nEXAMPLE 1: COMMITTED TRANSACTION")
    print(f"1. Record an update to allocate block {committed_block}.")
    print("2. Record that the transaction is COMMITTED.")
    print("3. A crash happens before the main bitmap is updated.")
    print("4. During recovery, the committed update is replayed.")

    print("\nSimulating recovery...")
    bitmap[committed_block] = True
    print(f"Block {committed_block} is now marked ALLOCATED.")

    print("\nEXAMPLE 2: INCOMPLETE TRANSACTION")
    print(f"1. A second update begins for block {incomplete_block}.")
    print("2. The update is recorded, but no commit is recorded.")
    print("3. A crash happens before the transaction commits.")
    print("4. Recovery does not replay this incomplete transaction.")

    print("\nSimulating recovery...")
    print(f"Block {incomplete_block} remains FREE.")
    print("The incomplete transaction is not treated as committed.")

    print("\nUPDATED BITMAP")
    show_bitmap(bitmap)

    print("\nIMPORTANT")
    print("This is a simplified teaching model of journal recovery.")
    print("Actual journal ordering and recovery rules depend on the filesystem.")
    pause()


def recovery_comparison():
    heading("9. CONSISTENCY CHECKING VS JOURNALING")

    print("CONSISTENCY CHECKING")
    print("- Examines filesystem structures.")
    print("- Compares references and allocation information.")
    print("- Detects and may repair inconsistencies.")
    print("- A full scan can take considerable time.")

    print("\nJOURNALING")
    print("- Records filesystem updates in a journal.")
    print("- Uses transaction commit information.")
    print("- Replays committed updates during recovery.")
    print("- Helps reduce the need for a full filesystem scan after a crash.")

    print("\nKEY DIFFERENCE")
    print("Consistency checking finds problems by examining filesystem state.")
    print("Journaling uses recorded updates to help recover committed changes.")
    print("They are different approaches and may be used together.")
    pause()


def main():
    # True = allocated; False = free.
    bitmap = [
        True, False, True, False,
        False, True, False, True,
        False, False, True, False,
        True, False, False, True
    ]

    heading("GROUP 10: FILESYSTEM SIMULATION")
    print("Scenario: University server storing student assignments.")
    print("Disk size: 16 blocks.")
    print("This is an educational model; it does not modify real disk data.")
    show_disk(bitmap)
    pause()

    bitmap_demo(bitmap)
    linked_list_demo(bitmap)
    grouping_demo(bitmap)
    counting_demo(bitmap)
    free_space_comparison()

    file_references = crash_challenge(bitmap)
    consistency_check(bitmap, file_references)
    journaling_demo(bitmap)
    recovery_comparison()

    heading("SIMULATION COMPLETE")
    print("Demonstrated:")
    print("1. Bitmap allocation and release")
    print("2. Linked free-list traversal")
    print("3. Grouping")
    print("4. Counting")
    print("5. Free-space method trade-offs")
    print("6. Crash and filesystem inconsistency")
    print("7. Consistency checking and repair")
    print("8. Committed and incomplete journal transactions")
    print("9. Recovery method comparison")
    print("\nNo real files or filesystem structures were modified.")


if __name__ == "__main__":
    main()
