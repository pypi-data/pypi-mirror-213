import pandas

from synmax.hyperion import HyperionApiClient, ApiPayload

api_key = 'eyJwcm9qZWN0X2lkIjogIlN5bm1heCBjb21tZXJjaWFsIEFQSSIsICJwcml2YXRlX2tleSI6ICJiTGtkUDZhal9Gd1c3X3dTZjhydWxmUmJfV25iOUVSUm5MS0piVUhVRGx3IiwgImNsaWVudF9pZCI6ICJXYWxsRXllIiwgInR5cGUiOiAib25lX3llYXJfbGljZW5zZWRfY3VzdG9tZXIiLCAic3RhcnRfZGF0ZSI6ICIwMy8xMi8yMDIzIiwgImVuZF9kYXRlIjogIjAzLzEyLzIwMjQiLCAidHJpYWxfbGljZW5zZSI6IGZhbHNlLCAiaXNzdWVfZGF0ZXRpbWUiOiAiMTItMDMtMjAyMyAyMTo1MjoxNyIsICJhZG1pbl91c2VyIjogZmFsc2UsICJ1c2VyX3JvbGVzIjogWyJoeXBlcmlvbiJdfQ=='
client = HyperionApiClient(access_token=api_key, async_client=False)


def fetch_frac_crews():
    payload = ApiPayload(start_date='2021-10-01', end_date='2021-12-31', state_code='CO')
    df: pandas.DataFrame = client.frac_crews(payload)

    print(df.count())


def main():
    fetch_frac_crews()


if __name__ == '__main__':
    main()
