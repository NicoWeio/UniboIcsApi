import base64

from main import get_cal


def lambda_handler(event, context):
    # Create the ICS file content
    ics_content = get_cal().serialize()

    # Base64 encode the ICS content
    encoded_ics_content = base64.b64encode(ics_content.encode('utf-8')).decode('utf-8')

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/calendar',
            'Content-Disposition': 'attachment; filename="timetable.ics"',
            'Access-Control-Allow-Origin': '*',
        },
        'body': encoded_ics_content,
        'isBase64Encoded': True
    }
