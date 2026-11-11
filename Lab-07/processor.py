"""Library fines application with defensive input validation."""


def _parse_nonnegative_integer(value):
    """Convert a nonnegative decimal field, or return None if it is invalid."""
    value = value.strip()
    if not value or not value.isdecimal():
        return None
    try:
        return int(value)
    except ValueError:
        # Python can reject decimal strings exceeding its integer digit limit.
        return None


def parse_member_id(member_id):
    """Return (uppercase letter prefix, nonnegative number), or None."""
    if not isinstance(member_id, str):
        return None
    parts = member_id.split('-')
    if len(parts) != 2:
        return None
    member_type = parts[0].strip()
    if not member_type.isalpha():
        return None
    number = _parse_nonnegative_integer(parts[1])
    if number is None:
        return None
    return member_type.upper(), number


def total_fine(days_csv):
    """Sum fines for a valid day list; return None if any field is invalid."""
    if not isinstance(days_csv, str):
        return None
    fine = 0
    for field in days_csv.split(','):
        days = _parse_nonnegative_integer(field)
        if days is None:
            return None
        fine += max(days - 14, 0) * 2
    return fine


def shelf_code(title):
    """Return initials for up to two words, or an empty code if unavailable."""
    if not isinstance(title, str):
        return ""
    words = title.split()
    return "".join(word[0] for word in words[:2]).upper()


def main():
    print("==== Running parse_member_id ====")
    user_input = input("Enter a member ID (e.g. STU-1023): ")
    result = parse_member_id(user_input)
    if result is None:
        print("Invalid member ID. Use a letter prefix and number, e.g. STU-1023.")
    else:
        print("Member Type and Number:", result)

    print("\n==== Running total_fine ====")
    user_input = input("Enter days kept for each book as CSV (e.g. 10,20,30): ")
    result = total_fine(user_input)
    if result is None:
        print("Invalid days list. Enter nonnegative whole numbers separated by commas.")
    else:
        print("Total Fine:", result)

    print("\n==== Running shelf_code ====")
    user_input = input("Enter a book title: ")
    result = shelf_code(user_input)
    if result:
        print("Shelf Code:", result)
    else:
        print("No shelf code: enter a nonblank book title.")


if __name__ == "__main__":
    main()
