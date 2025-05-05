from factories.base import PayGateFactory


def process_payment(factory: PayGateFactory, raw_data: dict) -> dict:
    """
    Processes a payment by parsing request data and building a response
    using the provided gateway factory.

    :param factory: A concrete factory implementing PayGateFactory.
    :param raw_data: Raw request data to be parsed and processed.
    :return: Formatted response dictionary.
    """
    parser = factory.create_request_parser()
    builder = factory.create_response_builder()

    parsed_data = parser.parse(raw_data)

    # Simulate business logic here (e.g., send to processor)
    result = {"status": "approved", "parsed": parsed_data}

    return builder.build(result)
