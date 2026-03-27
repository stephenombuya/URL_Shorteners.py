import pyshorteners
import os

HISTORY_FILE = "history.txt"


def shorten_url(long_url, service="tinyurl"):
    try:
        s = pyshorteners.Shortener()

        if service == "tinyurl":
            return s.tinyurl.short(long_url)

        elif service == "bitly":
            # NOTE: Requires Bitly API key configuration
            return s.bitly.short(long_url)

        else:
            return "❌ Unsupported service."

    except Exception as e:
        return f"Error: {str(e)}"


def expand_url(short_url):
    try:
        s = pyshorteners.Shortener()
        return s.tinyurl.expand(short_url)
    except Exception as e:
        return f"Error: {str(e)}"


def save_history(long_url, short_url):
    try:
        with open(HISTORY_FILE, "a") as file:
            file.write(f"{long_url} -> {short_url}\n")
    except Exception as e:
        print(f"⚠️ Could not save history: {e}")


def view_history():
    if not os.path.exists(HISTORY_FILE):
        print("📂 No history found.")
        return

    print("\n📜 URL History:")
    print("-" * 40)

    with open(HISTORY_FILE, "r") as file:
        print(file.read())


def is_valid_url(url):
    return url.startswith("http://") or url.startswith("https://")


def menu():
    while True:
        print("\n🔗 URL Shortener Menu")
        print("-" * 40)
        print("1. Shorten URL")
        print("2. Expand URL")
        print("3. View History")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            long_url = input("Enter a long URL: ").strip()

            if not is_valid_url(long_url):
                print("❌ Invalid URL. Must start with http:// or https://")
                continue

            print("\nChoose service:")
            print("1. TinyURL (default)")
            print("2. Bitly")

            service_choice = input("Select (1-2): ").strip()
            service = "tinyurl" if service_choice != "2" else "bitly"

            short_url = shorten_url(long_url, service)

            if "Error" in short_url:
                print(short_url)
            else:
                print(f"✅ Shortened URL: {short_url}")
                save_history(long_url, short_url)

        elif choice == "2":
            short_url = input("Enter a short URL: ").strip()
            result = expand_url(short_url)

            if "Error" in result:
                print(result)
            else:
                print(f"🔍 Original URL: {result}")

        elif choice == "3":
            view_history()

        elif choice == "4":
            print("👋 Exiting... Stay productive!")
            break

        else:
            print("❌ Invalid choice. Please select 1-4.")


def main():
    print("🚀 Welcome to the PRO URL Shortener")
    menu()


if __name__ == "__main__":
    main()
