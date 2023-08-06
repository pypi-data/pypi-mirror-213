import json
import logging
import os
from datetime import datetime, timedelta

import requests
from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from ...db.utils import add_ws_use_rates, get_all_editors, get_ws_use_rates
from ...services.data_validator import is_valid_search_criteria
from ...services.search_time_slots import search_slots

logging.getLogger("uvicorn.error").setLevel(logging.ERROR)

router = APIRouter()


@router.websocket("/SlotsFromPositionStreaming")
async def slots_from_position_streaming(websocket: WebSocket):
    _logger = logging.getLogger("root")
    try:
        await websocket.accept()
        while True:
            raw_data = await websocket.receive_text()
            # Check use rate per minute
            if get_ws_use_rates(websocket.client.host) > 30:
                await websocket.send_text("end_of_search")
                raise Exception("Websocket rate limit exceeded")
            else:
                add_ws_use_rates(websocket.client.host)
            start_time = datetime.now()
            data = json.loads(raw_data)

            if "reCAPTCHA_token" in data:
                PARAMS = {
                    "secret": os.environ.get("GOOGLE_SITE_VERIFICATION"),
                    "response": data["reCAPTCHA_token"],
                    "remoteip": websocket.client.host,
                }
                r = requests.get(
                    url="https://www.google.com/recaptcha/api/siteverify", params=PARAMS
                )
                d = r.json()

                if d["score"] < 0.5:
                    await websocket.send_text('{"Erreur":"Captcha invalide"}')
                    raise HTTPException(
                        status_code=400, detail="Low score for recaptcha token"
                    )

            else:
                raise HTTPException(status_code=400)

            if "department_code" in data:
                data["radius_km"] = 100
                if not is_valid_search_criteria(
                    search_criteria=data, search_by_department=True
                ):
                    raise HTTPException(
                        status_code=400, detail="Invalid search criteria"
                    )
            else:
                if not is_valid_search_criteria(data):
                    raise HTTPException(
                        status_code=400, detail="Invalid search criteria"
                    )
            latitude = float(data["latitude"])
            longitude = float(data["longitude"])
            start_date = None
            try:
                if "start_date" in data:
                    start_date = datetime.strptime(
                        data["start_date"], "%Y-%m-%d"
                    ).date()
            except ValueError:
                pass
            end_date = None
            try:
                if "end_date" in data:
                    end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date()
            except ValueError:
                pass
            radius_km = int(data["radius_km"])
            reason = None
            if "reason" in data:
                reason = data["reason"]
            documents_number = None
            if "documents_number" in data:
                documents_number = int(data["documents_number"])

            settings = {}
            result = []

            if "smart_search" in data and data["smart_search"]:
                months = 1
                valide_slots = False
                while radius_km <= 60 and not valide_slots:
                    result, errors = await search_slots(
                        longitude,
                        latitude,
                        start_date,
                        start_date + relativedelta(months=months),
                        radius_km,
                        reason,
                        documents_number,
                        websocket=websocket,
                        department_code=(
                            "department_code" in data and data["department_code"]
                        ),
                    )
                    if result:
                        for meeting_point in result:
                            valide_slots = is_valide_slots(meeting_point)
                            if valide_slots:
                                break

                    months += 1
                    radius_km += 20
                settings["radius"] = radius_km - 20
                settings["end_date"] = start_date + relativedelta(months=months - 1)

            else:
                result, errors = await search_slots(
                    longitude,
                    latitude,
                    start_date,
                    end_date,
                    radius_km,
                    reason,
                    documents_number,
                    websocket=websocket,
                    department_code=(
                        "department_code" in data and data["department_code"]
                    ),
                )

            json_text = json.dumps(
                {
                    "step": "end_of_search",
                    "editors_number": len(get_all_editors()),
                    "editor_errors_number": len(errors),
                    "settings": settings,
                },
                default=str,
            )
            await websocket.send_text(json_text)
            _logger.info(
                "End of websocket search",
                extra={
                    "extra_info": {
                        "type": "access",
                        "searchCriteria": data,
                        "searchLocation": {"lat": latitude, "lon": longitude},
                        "response_time": (datetime.now() - start_time).microseconds
                        / 1000,
                        "protocol": "websocket",
                        "realip": websocket.client.host,
                    }
                },
            )
    except WebSocketDisconnect:
        _logger.debug("Client disconnected.")
    except HTTPException as websocket_e:
        _logger.error("Error during websocket connexion : %s", websocket_e.detail)
    except Exception as websocket_e:
        _logger.error("Error during websocket connexion : %s", websocket_e)


def is_valide_slots(meeting_point):
    for slot in meeting_point["available_slots"]:
        if datetime_from_str(slot["datetime"]) >= datetime.now():
            return True
    return False


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
