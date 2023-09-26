from typing import Dict
from typing import List
from typing import Optional
from urllib.parse import urljoin
import json
import aiohttp
import jwt
from langchain.schema import Document

BASE_URL: str = "https://lightyear.com"


async def execute(token: str, instruments: List[Dict]) -> List[Document]:
    try:
        account_id = _get_account_id(token)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                urljoin(BASE_URL, f"/api/v1/account/{account_id}/balance"),
                headers={
                    "Authorization": f"Bearer {token}"
                }
            ) as response:
                response.raise_for_status()
                response_json = await response.json()
                return _format_response(response_json, instruments)
    except Exception as e:
        return []


def _get_account_id(token: str) -> str:
    decoded = jwt.decode(token, options={"verify_signature": False})
    return decoded["accountIds"]


def _format_response(response_json, instruments: List[Dict]) -> List[Document]:
    docs = []
    summary = response_json["summary"]
    docs.append(Document(
        page_content=f"User total balance: {summary['balance']} {summary['currency']}. Portfolio change: {summary['portfolioPnl']['change']} {summary['currency']}"
    ))
    docs.append(Document(
        page_content=f"Cash balance: {response_json['balances']['cash'][0]['balance']} {response_json['balances']['cash'][0]['currency']}"
    ))

    for b in response_json["balances"]["instruments"]:
        instrument = _get_instrument(instruments, b["instrumentId"])
        if instrument:
            formatted = {
                "type": b["type"],
                "quantity": b["quantity"],
                "currency": b["currency"],
                "average_entry_price": b["details"]["avgEntryPrice"],
                "market_value": b["details"]["marketValue"],
                "symbol": instrument.get("symbol", ""),
                "name": instrument.get("name", ""),
            }
            docs.append(
                Document(
                    page_content=f"User has: {json.dumps(formatted).replace('{', '').replace('}', '')}"
                )
            )
    return docs


def _get_instrument(instruments: List[Dict], instrument_id: str) -> Optional[Dict]:
    filtered = [i for i in instruments if i["id"] == instrument_id]
    if len(filtered):
        return filtered[0]
    return None
