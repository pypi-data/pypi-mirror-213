import logging
import os
from datetime import datetime, timedelta

import httpx

from ..logging.app_logger import write_external_service_data


async def search_appointments_in_optimisation_api(application_ids):
    _logger = logging.getLogger("root")
    optimisation_api_url = os.environ.get("OPTIMISATION_API_URL")
    optimisation_api_token = os.environ.get("OPTIMISATION_API_TOKEN")

    result = {}
    try:
        headers = {"x-rdv-opt-auth-token": optimisation_api_token}
        parameters = {"application_ids": application_ids}
        async with httpx.AsyncClient(verify=False) as async_client:
            response = await async_client.get(
                f"{optimisation_api_url}/api/status",
                headers=headers,
                params=parameters,
                timeout=15,
                follow_redirects=True,
            )
            write_external_service_data(_logger, response)
            if response.status_code in [200]:
                json_response = response.json()
                for key in json_response:
                    if json_response[key] and json_response[key]["appointments"]:
                        result[key] = []
                        for appointment in json_response[key]["appointments"]:
                            result[key].append(
                                {
                                    "meeting_point": appointment["meeting_point"],
                                    "datetime": appointment["appointment_date"],
                                    "management_url": appointment["management_url"],
                                }
                            )
            else:
                raise Exception(
                    f"Status code not handled : {response.status_code} : {response.reason_phrase}"
                )
    except Exception as search_appointments_e:
        _logger.error(
            "Error while seachring appointments in the optimisation api : %s",
            str(search_appointments_e),
            extra={"extra_info": {"type": "app"}},
        )
    return result


async def update_appointment_in_optimisation_api(application_id, appointment):
    _logger = logging.getLogger("root")
    optimisation_api_url = os.environ.get("OPTIMISATION_API_URL")
    optimisation_api_token = os.environ.get("OPTIMISATION_API_TOKEN")

    try:
        headers = {"x-rdv-opt-auth-token": optimisation_api_token}
        parameters = {
            "application_id": application_id,
            "meeting_point": appointment["meeting_point"],
            "appointment_date": appointment["datetime"],
            "management_url": appointment["management_url"],
        }
        async with httpx.AsyncClient(verify=False) as async_client:
            response = await async_client.post(
                f"{optimisation_api_url}/api/appointments",
                headers=headers,
                params=parameters,
                timeout=15,
                follow_redirects=True,
            )
            write_external_service_data(_logger, response)
            if response.status_code in [200]:
                _logger.info(
                    "Appointment successfully created in optimisation api : %s",
                    str(appointment),
                )
            else:
                raise Exception(
                    f"Status code not handled : {response.status_code} : {response.reason_phrase}"
                )
    except Exception as create_appointment_e:
        _logger.error(
            "Error while creating appointment in the optimisation api : %s",
            str(create_appointment_e),
            extra={"extra_info": {"type": "app"}},
        )


def is_same_appointment(appointment_1, appointment_2):
    datetime_1 = datetime_from_str(appointment_1["datetime"])
    datetime_2 = datetime_from_str(appointment_2["datetime"])

    return (
        (appointment_1["meeting_point"] == appointment_2["meeting_point"])
        and (datetime_1 == datetime_2)
        and (appointment_1["management_url"] == appointment_2["management_url"])
    )


def datetime_from_str(datetime_str):
    datetime_datetime = None
    for datetime_format in [
        "%Y-%m-%dT%H:%MZ",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S",
    ]:
        try:
            datetime_datetime = datetime.strptime(datetime_str, datetime_format)
            if datetime_datetime.tzinfo:
                utcoffset = datetime_datetime.utcoffset().total_seconds() / 60 / 60
                datetime_datetime = datetime_datetime.replace(tzinfo=None) + timedelta(
                    hours=utcoffset
                )
            break
        except ValueError:
            pass

    return datetime_datetime
