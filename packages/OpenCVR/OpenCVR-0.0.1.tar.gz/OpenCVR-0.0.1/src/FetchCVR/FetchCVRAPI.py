from FetchCVR.Labels \
    import denmark


class FetchCVRAPI:
    def __init__(
            self,
            country: None | str = denmark()
    ):
        self.country: str = country

    def get_country(self) -> None | str:
        return self.country

    def set_country(
            self,
            value: str
    ) -> None:
        self.country = value
