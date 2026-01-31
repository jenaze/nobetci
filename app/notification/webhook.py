import logging

import httpx

from app.config import WEBHOOK_ADDRESS, WEBHOOK_SECRET, WEBHOOK_TIMEOUT

logger = logging.getLogger(__name__)


async def send_webhook(payload: dict) -> None:
    if not WEBHOOK_ADDRESS:
        return

    headers = {}
    if WEBHOOK_SECRET:
        headers["X-Webhook-Secret"] = WEBHOOK_SECRET

    try:
        async with httpx.AsyncClient(timeout=WEBHOOK_TIMEOUT) as client:
            response = await client.post(
                WEBHOOK_ADDRESS,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
    except httpx.HTTPError as exc:
        logger.error("Webhook request failed: %s", exc)
