from client import RZNClient

def main():
    # Initialize the client
    client = RZNClient(host="localhost", port=9928)

    # Ask a query
    query = "How to position a product"
    results = client.search(query, search_type="composite", rerank=True)

    # Print results
    for result in results:
        print(f"Title: {result.title}")
        print(f"Text: {result.text}")
        print(f"Path: {result.path}")
        print(f"Score: {result.score}")
        print("------------------------")

if __name__ == "__main__":
    main()

