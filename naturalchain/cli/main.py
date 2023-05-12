import argparse
from naturalchain.agents.default import naturalchain_agent


def main():
    parser = argparse.ArgumentParser(
        description="NaturalChain agent CLI",
        prog="naturalchain",
        usage="%(prog)s [options] [query]",
    )
    # add query argument (a natural language string between "")
    parser.add_argument("query", help="Your query or task for the NaturalChain agent")

    args = parser.parse_args()
    query: str = args.query
    response = naturalchain_agent.run(query)
    print(response)


if __name__ == "__main__":
    main()
