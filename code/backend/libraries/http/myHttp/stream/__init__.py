from typing import Any, List, Dict
from exceptions import InvalidFormatError


def parse_server_side_events(data: bytes) -> List[Dict[str, Any]]:
    """
    Parses Server-Sent Events (SSE) from a bytes object.

    Args:
        data (bytes): The SSE data as bytes.

    Returns:
        List[Dict[str, Any]]: A list of events, each represented as a dictionary with possible keys:
            - 'event': The event type.
            - 'data': The event data.
            - 'id': The event ID.
            - 'retry': The reconnection time in milliseconds.
    """
    # Decode bytes to string using utf-8
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError as e:
        raise InvalidFormatError('Invalid UTF-8 encoding') from e

    events = []
    event = {}
    data_buffer = []

    # Split the text into lines
    lines = text.splitlines()

    for line in lines:
        # Ignore comments
        if line.startswith(':'):
            continue

        if not line.strip():
            # Dispatch the event if any data is present
            if data_buffer or event:
                if data_buffer:
                    event['data'] = '\n'.join(data_buffer)
                    data_buffer = []
                events.append(event)
                event = {}
            continue

        # Split the line into field and value
        if ':' in line:
            field, value = line.split(':', 1)
            value = value.lstrip()  # Remove leading space if any
        else:
            field, value = line, ''

        # Handle different fields
        if field == 'event':
            event['event'] = value
        elif field == 'data':
            data_buffer.append(value)
        elif field == 'id':
            event['id'] = value
        elif field == 'retry':
            # Attempt to convert retry to integer
            try:
                event['retry'] = int(value)
            except ValueError:
                # Invalid retry value; ignore or handle as needed
                pass
        # You can handle other fields here as needed

    # After processing all lines, check if there's an uncommitted event
    if data_buffer or event:
        if data_buffer:
            event['data'] = '\n'.join(data_buffer)
        events.append(event)

    return events
