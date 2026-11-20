MAX_SAFE_AMOUNT = 50000
HIGH_RISK_COUNTRIES = ["XX", "YY", "ZZ"]


def filter_suspicious_transfers(transfers, vip_bypass=False):
    suspicious = []

    for tx in transfers:
        if tx.get("is_verified") and vip_bypass:
            continue

        if tx.get("sender") is None or tx.get("amount") is None:
            continue

        try:
            fee_ratio = tx["fee"] / tx["amount"]
        except ZeroDivisionError:
            fee_ratio = 0.0

        is_high_amount = tx["amount"] > MAX_SAFE_AMOUNT
        is_risk_country = tx.get("country") in HIGH_RISK_COUNTRIES
        is_high_fee = fee_ratio > 0.25

        if is_high_amount or is_risk_country or is_high_fee:
            suspicious.append(
                {
                    "tx_id": tx["id"],
                    "sender": tx["sender"],
                    "risk_fee": round(fee_ratio, 2),
                }
            )

    return suspicious