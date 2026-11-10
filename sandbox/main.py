from order import calculate_total


def main():
    total = calculate_total(price=40, quantity=3)
    print(f"bill of order: {total:.2f}")


if __name__ == "__main__":
    main()